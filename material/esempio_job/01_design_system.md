---
name: Artisan Heritage System
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1c1b1b'
  on-surface-variant: '#4d4635'
  inverse-surface: '#313030'
  inverse-on-surface: '#f3f0ef'
  outline: '#7f7663'
  outline-variant: '#d0c5af'
  surface-tint: '#735c00'
  primary: '#735c00'
  on-primary: '#ffffff'
  primary-container: '#d4af37'
  on-primary-container: '#554300'
  inverse-primary: '#e9c349'
  secondary: '#77574d'
  on-secondary: '#ffffff'
  secondary-container: '#fed3c7'
  on-secondary-container: '#795950'
  tertiary: '#5e604d'
  on-tertiary: '#ffffff'
  tertiary-container: '#b4b49d'
  on-tertiary-container: '#454634'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffe088'
  primary-fixed-dim: '#e9c349'
  on-primary-fixed: '#241a00'
  on-primary-fixed-variant: '#574500'
  secondary-fixed: '#ffdbd0'
  secondary-fixed-dim: '#e7bdb1'
  on-secondary-fixed: '#2c160e'
  on-secondary-fixed-variant: '#5d4037'
  tertiary-fixed: '#e4e4cc'
  tertiary-fixed-dim: '#c8c8b0'
  on-tertiary-fixed: '#1b1d0e'
  on-tertiary-fixed-variant: '#474836'
  background: '#fcf9f8'
  on-background: '#1c1b1b'
  surface-variant: '#e5e2e1'
typography:
  display-lg:
    fontFamily: Libre Caslon Text
    fontSize: 48px
    fontWeight: '400'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Libre Caslon Text
    fontSize: 32px
    fontWeight: '400'
    lineHeight: '1.3'
  headline-lg-mobile:
    fontFamily: Libre Caslon Text
    fontSize: 28px
    fontWeight: '400'
    lineHeight: '1.3'
  subheading:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.5'
    letterSpacing: 0.15em
  body-lg:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '300'
    lineHeight: '1.7'
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
spacing:
  container-max: 1280px
  gutter: 24px
  margin-mobile: 20px
  section-gap: 80px
  element-gap: 16px
---

## Brand & Style

The brand identity is rooted in the concepts of "Timeless Heritage" and "Agricultural Elegance." It targets a sophisticated audience that appreciates the slow-living philosophy, artisanal winemaking, and authentic hospitality. The UI should evoke a sense of warmth, historical depth, and premium quality through a blend of classical editorial layouts and modern transparency.

The design style is **Corporate Modern with a Minimalist/Tactile edge**. It utilizes heavy whitespace to allow high-quality photography to breathe, paired with structured, linear dividers that reference the rows of a vineyard. The atmosphere is established through a mix of warm wood tones and professional gold accents, creating a bridge between traditional craftsmanship and contemporary digital clarity.

## Colors

The palette is a strict extraction from the heritage of Italian viticulture and masonry:

- **Primary Gold (#D4AF37):** Used for primary CTAs, active states, and decorative flourishes. It represents excellence and the sun-drenched hills.
- **Warm Wood / Earth (#5D4037):** A deep brown used for secondary elements, footers, and text on light backgrounds to soften the contrast compared to pure black.
- **Crema & Bone (#FAF9F6, #F5F5DC):** The foundation of the UI. This provides a softer, more organic feel than clinical white, mimicking aged parchment or limestone.
- **Translucent White:** Utilized for "Glassmorphism" overlays on top of rich photography, ensuring text legibility without obscuring the visual context of the estates.

## Typography

The typographic system relies on the contrast between an authoritative Serif and a functional Sans-Serif.

- **Headlines:** Uses `Libre Caslon Text`. This serif is chosen for its literary and historical character. Headlines should often be paired with a gold `subheading` in all-caps Manrope to create a structured information hierarchy.
- **Body & Interface:** Uses `Manrope`. This font provides high legibility for long-form descriptions of wines or rooms. The lighter weight (300) should be used for larger body text to maintain a "high-fashion" editorial feel.
- **Scale:** On mobile, display sizes should scale down by 20% to ensure readability and prevent excessive line-breaking in Italian, which often uses longer words.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy for desktop to maintain the "book-like" alignment seen in the references. 

- **Grid:** A 12-column grid with a wide 24px gutter to emphasize whitespace.
- **Sectioning:** Sections are separated by significant vertical padding (80px+) and thin, 1px linear dividers in Primary Gold or Light Grey.
- **Alignment:** Content is often asymmetrical, with text blocks offset against large-scale imagery to create a dynamic, premium flow.
- **Mobile:** Transition to a single-column fluid layout with 20px side margins. Vertical gaps between elements are reduced to 48px to maintain momentum.

## Elevation & Depth

Depth is achieved through **Tonal Layers and Glassmorphism** rather than traditional shadows.

- **Overlays:** Content cards placed over images use a white-transparent background (85-90% opacity) with a subtle backdrop blur. This mimics frosted glass or light filtering through a window.
- **Outlines:** Instead of shadows, use 1px borders in gold or cream to define container boundaries.
- **Photography:** Images are the primary source of "depth." Use high-contrast, warm-toned photography (woods, vineyards, cellar interiors) to provide a rich backdrop for the flat UI elements.

## Shapes

The shape language is strictly **Sharp (0px)**. 

To reflect the architectural lines of the estates and the precision of the wine labels, all buttons, input fields, and image containers must have square corners. This reinforces the "Classic" and "Traditional" brand personality. The only exception is the use of circular icons for social media or specific "scroll down" indicators.

## Components

- **Buttons (CTA):** These are rectangular, with a 1px border. The text is always in all-caps `label-md`. Every primary button must include a right-pointing arrow (`→`) following the text. Use a ghost style (transparent background, gold border) for a lighter touch, or solid gold for high-priority actions.
- **Dividers:** Horizontal lines are 1px thick. Use Gold (#D4AF37) for separating major thematic sections and a light neutral for secondary separation.
- **Input Fields:** Minimalist design with only a bottom border (1px) or a full rectangular stroke. No rounded corners. Use `Manrope` for placeholder text.
- **Cards:** Product or Experience cards should feature a subtle "lift" on hover, or a simple gold border highlight. 
- **Navigation:** Top-tier navigation uses vertical bars (`|`) as dividers between menu items to mirror the linear language used throughout the system.