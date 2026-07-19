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
  document.querySelectorAll('button, [role="button"], [role="option"], [role="tab"], a').forEach(e => {
    const t = (e.innerText || e.getAttribute('aria-label') || '').trim();
    if (/pro|flash|web|app|send|invia|download|scarica|model|3\.1|export/i.test(t)) push('ACTION', e);
  });
  return out;
}
"""


def _report(sender: StitchSender) -> None:
    seen = 0
    for i, ctx in enumerate(sender._frames()):  # noqa: SLF001 - script interno
        try:
            items = ctx.evaluate(_COLLECT_JS)
        except Exception:
            continue
        if not items:
            continue
        print(f"\n=== FRAME {i} ({getattr(ctx, 'url', '')}) ===")
        for it in items:
            seen += 1
            attrs = " ".join(
                f"{k}={it[k]!r}" for k in ("testid", "aria", "role", "type", "id", "ph")
                if it[k]
            )
            print(f"  [{it['kind']}] <{it['tag']}> text={it['text']!r}  {attrs}")
    if not seen:
        print("\n(nessun elemento riconosciuto: forse la pagina non è ancora caricata,"
              " o il login non è completo)")


def main() -> None:
    from ..config import Config, load_config

    try:
        cfg = load_config()
    except FileNotFoundError:
        cfg = load_config("config.example.yaml")

    # forza il browser VISIBILE per la calibrazione
    if isinstance(cfg, Config):
        cfg.data.setdefault("stitch", {})["headless"] = False

    print("Apro Stitch in un browser visibile...")
    with StitchSender(cfg) as sender:
        sender.open()
        input(
            "\n>> Fai il login e vai alla schermata dove si SCRIVE il prompt "
            "(con il menu del modello visibile).\n"
            ">> Poi torna qui e premi INVIO per fotografare la pagina... "
        )
        print("\nElementi trovati nella pagina di Stitch:")
        _report(sender)
        sender.save_debug("calibrazione")
    print("\nFatto. Ho salvato screenshot + DOM in ./debug/")
    print("Copia-incolla l'elenco qui sopra (o mandami i file di debug).")


if __name__ == "__main__":
    main()
