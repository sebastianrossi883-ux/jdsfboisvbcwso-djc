"""Loop principale: gira in continuazione, cerca job, li invia a Stitch.

Uso:
    python -m src.main                 # gira in continuo (24/7)
    python -m src.main --once          # processa i job in coda una volta e esce
    python -m src.main --config x.yaml # usa un config specifico

Flusso per ogni job:
    1) costruisce la sequenza di prompt (reference + prompt in ordine)
    2) apre Stitch, seleziona modello/versione, invia tutto in sequenza
    3) salva il risultato in results/<nome_job>/
    4) marca il job come "fatto" (non verrà rifatto)
"""

from __future__ import annotations

import argparse
import logging
import time

from .config import load_config
from .prompt_builder import build_steps
from .results import result_dir_for
from .sources import build_source
from .stitch import StitchBrowser

log = logging.getLogger("stitch_bot")


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def process_pending(cfg, source) -> int:
    """Elabora tutti i job pendenti una volta. Restituisce quanti ne ha fatti."""
    jobs = source.list_pending_jobs()
    if not jobs:
        return 0

    result_type = cfg.get("result.type", "code")
    done = 0

    for job in jobs:
        log.info("=== JOB: %s (%d prompt, %d reference) ===",
                 job.name, len(job.prompts), len(job.references))
        try:
            steps = build_steps(job, cfg)
            dest = result_dir_for(job.name, cfg)

            with StitchBrowser(cfg) as browser:
                out = browser.run_job(
                    steps=steps,
                    result_type=result_type,
                    dest_dir=dest,
                    model=job.model,
                    version=job.version,
                )

            source.mark_done(job)
            done += 1
            log.info("Job '%s' completato. Risultato: %s", job.name, out or "(nessuno)")
        except Exception as exc:  # noqa: BLE001 - un job non deve fermare il loop
            log.exception("Job '%s' fallito: %s", job.name, exc)
            source.mark_error(job, str(exc))

    return done


def main() -> None:
    parser = argparse.ArgumentParser(description="Stitch Reference Mirroring System")
    parser.add_argument("--config", default=None, help="Percorso a config.yaml")
    parser.add_argument("--once", action="store_true",
                        help="Elabora i job in coda una volta e poi esce")
    args = parser.parse_args()

    setup_logging()
    cfg = load_config(args.config)
    source = build_source(cfg)

    once = args.once or bool(cfg.get("loop.once", False))
    interval = int(cfg.get("loop.poll_interval_sec", 60))

    log.info("Avvio. Sorgente: %s | modalità: %s",
             cfg.get("source.type"), "once" if once else "loop 24/7")

    if once:
        process_pending(cfg, source)
        return

    while True:
        try:
            n = process_pending(cfg, source)
            if n == 0:
                log.debug("Nessun job pendente. Attendo %ds...", interval)
        except Exception as exc:  # noqa: BLE001 - il loop non deve mai morire
            log.exception("Errore nel ciclo: %s", exc)
        time.sleep(interval)


if __name__ == "__main__":
    main()
