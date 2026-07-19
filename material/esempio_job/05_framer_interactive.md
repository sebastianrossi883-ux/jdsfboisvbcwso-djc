# VERIFIED ORIGINAL FRAMER INTERACTIVE

**REGOLA D'ORO ZERO-DISTRUZIONE: APPLICA QUESTA INTERAZIONE DENTRO UNA SEZIONE ESISTENTE COMPATIBILE. NON CREARE, CANCELLARE, SOSTITUIRE, FONDERE O RIORDINARE SEZIONI. NON TOCCARE IL GUEST COMPONENT GIA INSERITO.**

Selected: `Framer Stryds Interactive` (`framer-stryds`)
Original interaction archive: `/Users/utente/Desktop/arsenal_v7/cartella senza nome 6final/ANIMAZIONI/Framer_Interactions/stryds.learnframer.site`
Selected source: `/Users/utente/Downloads/stitch_downloads/_ONE_SITE_JOBS/227b1915-f932-4744-bd06-e691c2285669-e23558e915/STITCH_AMMO_BOX/REACT_FRAMER_INTERACTIVE_STITCH_BUNDLE.md`
Source mode: `portable_react`
SHA256: `4773531927ac5c6aed0cc46fb9799a7f1493ed8a169ce2daaa4bd273243219a9`

Questo e il componente React/TSX portabile verificato. Montalo realmente con script type=module/React, senza riscriverne fisica o struttura.

```tsx
import React, { useRef } from 'react';
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

interface StrydsProps {
  imageSrc: string;
  title: string;
  subtitle?: string;
}

export const StrydsInteractiveReact: React.FC<StrydsProps> = ({ imageSrc, title, subtitle }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cardRef = useRef<HTMLDivElement>(null);
  const imgRef = useRef<HTMLImageElement>(null);

  useGSAP(() => {
    if (!cardRef.current || !imgRef.current) return;

    gsap.set(cardRef.current, { clipPath: 'polygon(0% 100%, 100% 100%, 100% 100%, 0% 100%)' });
    gsap.set(imgRef.current, { scale: 1.25, yPercent: 12 });

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: containerRef.current,
        start: 'top 80%',
        end: 'bottom 40%',
        scrub: 1
      }
    });

    tl.to(cardRef.current, {
      clipPath: 'polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)',
      ease: 'none'
    });

    tl.to(imgRef.current, {
      scale: 1,
      yPercent: 0,
      ease: 'none'
    }, 0);
  }, { scope: containerRef });

  return (
    <div ref={containerRef} className="relative w-full py-20 px-6">
      <div ref={cardRef} className="relative overflow-hidden rounded-2xl shadow-2xl max-w-5xl mx-auto">
        <img ref={imgRef} src={imageSrc} alt={title} className="w-full h-[65vh] object-cover" />
        <div className="absolute inset-0 bg-black/30 flex flex-col justify-end p-10 text-white">
          <h3 className="text-4xl font-serif">{title}</h3>
          {subtitle && <p className="text-lg opacity-80 mt-2">{subtitle}</p>}
        </div>
      </div>
    </div>
  );
};
```
