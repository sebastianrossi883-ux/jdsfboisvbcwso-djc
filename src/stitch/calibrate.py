"""Prova + calibrazione di Stitch in locale (sul tuo Mac, browser visibile).

Apre Stitch in un browser vero, ti lascia fare il login, poi "fotografa" la
pagina: stampa gli elementi interattivi (campo prompt, pulsanti, menu modello,
Web/App, Download) e salva screenshot + DOM in `debug/`. Da quell'output si
ricavano i selettori esatti da mettere in config.yaml.

Uso (sul Mac):
    python -m src.stitch.calibrate

Poi copia-incolla l'elenco che stampa (o manda i file in debug/).
"""

from __future__ import annotations

from .sender import StitchSender

# JS che raccoglie gli elementi interessanti in un frame
_COLLECT_JS = r"""
() => {
  const out = [];
  const push = (kind, el) => {
    const t = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 40);
    out.push({
      kind,
      tag: el.tagName.toLowerCase(),
      text: t,
      id: el.id || '',
      testid: el.getAttribute('data-testid') || '',
      aria: el.getAttribute('aria-label') || '',
      role: el.getAttribute('role') || '',
      type: el.getAttribute('type') || '',
      ph: el.getAttribute('placeholder') || '',
    });
  };
  document.querySelectorAll('textarea, [contenteditable="true"], [role="textbox"]').forEach(e => push('INPUT', e));
  document.querySelectorAll('input[type=file]').forEach(e => push('UPLOAD', e));
  document.querySelectorAll('button, [role="button"], [role="option"], [role="tab"], [role="menuitem"], [role="menuitemradio"], a').forEach(e => {
    const t = (e.innerText || e.getAttribute('aria-label') || '').trim();
    if (/pro|flash|web|app|send|invia|download|scarica|model|gemini|2\.5|3\.1|export/i.test(t)) push('ACTION', e);
  });
  return out;
}
"""


def _report(sender: StitchSender, out_lines: list[str]) -> None:
    """Stampa a schermo E accumula le righe in out_lines (per salvarle su file)."""
    seen = 0
    for i, ctx in enumerate(sender._frames()):  # noqa: SLF001 - script interno
        try:
            items = ctx.evaluate(_COLLECT_JS)
        except Exception:
            continue
        if not items:
            continue
        header = f"\n=== FRAME {i} ({getattr(ctx, 'url', '')}) ==="
        print(header)
        out_lines.append(header)
        for it in items:
            seen += 1
            attrs = " ".join(
                f"{k}={it[k]!r}" for k in ("testid", "aria", "role", "type", "id", "ph")
                if it[k]
            )
            line = f"  [{it['kind']}] <{it['tag']}> text={it['text']!r}  {attrs}"
            print(line)
            out_lines.append(line)
    if not seen:
        msg = ("\n(nessun elemento riconosciuto: forse la pagina non è ancora caricata,"
               " o il login non è completo)")
        print(msg)
        out_lines.append(msg)


def main() -> None:
    from ..config import Config, load_config

    try:
        cfg = load_config()
    except FileNotFoundError:
        cfg = load_config("config.example.yaml")

    # forza il browser VISIBILE + Chrome vero (il login Google funziona meglio)
    if isinstance(cfg, Config):
        st = cfg.data.setdefault("stitch", {})
        st["headless"] = False
        if not st.get("browser_channel"):
            st["browser_channel"] = "chrome"

    import time

    print("Apro Stitch con Chrome (login gia' salvato)... nessun tasto da premere.")
    with StitchSender(cfg) as sender:
        sender.open()

        # Aspetta che la pagina di Stitch sia caricata (compare il campo prompt).
        print("Aspetto che Stitch carichi...")
        ready = sender._find("prompt_input", timeout=60000)  # noqa: SLF001
        if ready is None:
            print("Non vedo ancora il campo del prompt. Se non sei loggato, "
                  "fai il login nella finestra e rilancia il comando.")
        time.sleep(3)  # lascia finire il rendering

        # Apre il menu del modello da solo (così non si richiude per il focus).
        print("Apro il menu del modello per catturarne le voci...")
        try:
            if sender._click("model_menu_button", required=False):  # noqa: SLF001
                time.sleep(1.5)
                print("Menu del modello aperto.")
        except Exception as exc:  # noqa: BLE001
            print("Non sono riuscito ad aprire il menu del modello:", exc)

        print("\n================= ELEMENTI DI STITCH =================")
        out_lines: list[str] = []
        _report(sender, out_lines)
        sender.save_debug("calibrazione")
        print("=====================================================")

        # salva tutto in un file, così basta mandare quello
        from pathlib import Path
        out_file = Path("debug") / "elementi_stitch.txt"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text("\n".join(out_lines), encoding="utf-8")
        print(f"\n>>> Ho salvato tutto nel file:  {out_file.resolve()}")
        print(">>> MANDAMI QUEL FILE (trascinalo qui nella chat).")
        time.sleep(2)
    print("\nFatto.")


if __name__ == "__main__":
    main()
