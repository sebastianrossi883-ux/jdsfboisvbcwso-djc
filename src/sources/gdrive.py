"""Sorgente Google Drive.

Struttura attesa su Drive:

    <cartella_madre>/            <- source.gdrive.folder_id
        <nome_job_1>/            <- una sottocartella per ogni job
            *.jpg / *.png        (reference)
            *.md                 (prompt)
        <nome_job_2>/
            ...

Il programma scarica ogni sottocartella-job in locale (source.gdrive.download_dir)
e da lì la tratta come un LocalSource. Lo stato (done/error) viene marcato su Drive
rinominando la cartella con un prefisso, così non viene riscaricata.

Autenticazione: service account (file JSON in source.gdrive.credentials_file).
Ricordati di CONDIVIDERE la cartella Drive con l'email del service account.
"""

from __future__ import annotations

import io
import logging
from pathlib import Path

from ..config import Config
from ..job import Job, load_job
from .base import Source
from .local import DONE_MARKER, ERROR_MARKER

log = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive"]
DONE_PREFIX = "[FATTO] "
ERROR_PREFIX = "[ERRORE] "
FOLDER_MIME = "application/vnd.google-apps.folder"


class GDriveSource(Source):
    def __init__(self, cfg: Config):
        self.parent_id = cfg.get("source.gdrive.folder_id", "")
        self.credentials_file = cfg.get(
            "source.gdrive.credentials_file", "./gdrive-service-account.json"
        )
        self.download_dir = Path(cfg.get("source.gdrive.download_dir", "./material"))
        self.download_dir.mkdir(parents=True, exist_ok=True)

        if not self.parent_id:
            raise ValueError("source.gdrive.folder_id non impostato in config.yaml")

        self._service = self._build_service()
        # mappa nome_job_locale -> id cartella Drive (per marcare done/error)
        self._drive_folder_ids: dict[str, str] = {}

    def _build_service(self):
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=SCOPES
        )
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    def _list_child_folders(self, parent_id: str) -> list[dict]:
        query = f"'{parent_id}' in parents and mimeType='{FOLDER_MIME}' and trashed=false"
        folders: list[dict] = []
        page_token = None
        while True:
            resp = (
                self._service.files()
                .list(
                    q=query,
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            folders.extend(resp.get("files", []))
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        return folders

    def _list_files(self, folder_id: str) -> list[dict]:
        query = f"'{folder_id}' in parents and trashed=false and mimeType!='{FOLDER_MIME}'"
        resp = (
            self._service.files()
            .list(q=query, fields="files(id, name, mimeType)")
            .execute()
        )
        return resp.get("files", [])

    def _download_file(self, file_id: str, dest: Path) -> None:
        from googleapiclient.http import MediaIoBaseDownload

        request = self._service.files().get_media(fileId=file_id)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with io.FileIO(dest, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _status, done = downloader.next_chunk()

    def list_pending_jobs(self) -> list[Job]:
        pending: list[Job] = []
        for folder in self._list_child_folders(self.parent_id):
            name = folder["name"]
            if name.startswith(DONE_PREFIX) or name.startswith(ERROR_PREFIX):
                continue

            local_folder = self.download_dir / name
            # se già scaricato e marcato done in locale, salta
            if (local_folder / DONE_MARKER).exists():
                continue

            log.info("Scarico job da Drive: %s", name)
            local_folder.mkdir(parents=True, exist_ok=True)
            for file in self._list_files(folder["id"]):
                self._download_file(file["id"], local_folder / file["name"])

            self._drive_folder_ids[name] = folder["id"]

            job = load_job(local_folder)
            if not job.is_valid():
                log.warning("Job Drive '%s' ignorato: nessun prompt trovato.", name)
                continue
            pending.append(job)
        return pending

    def _rename_drive_folder(self, job: Job, prefix: str) -> None:
        folder_id = self._drive_folder_ids.get(job.name)
        if not folder_id:
            return
        try:
            self._service.files().update(
                fileId=folder_id, body={"name": prefix + job.name}
            ).execute()
        except Exception as exc:  # noqa: BLE001
            log.warning("Impossibile rinominare la cartella Drive '%s': %s", job.name, exc)

    def mark_done(self, job: Job) -> None:
        (job.path / DONE_MARKER).write_text("ok\n", encoding="utf-8")
        self._rename_drive_folder(job, DONE_PREFIX)

    def mark_error(self, job: Job, error: str) -> None:
        (job.path / ERROR_MARKER).write_text(error + "\n", encoding="utf-8")
        self._rename_drive_folder(job, ERROR_PREFIX)
