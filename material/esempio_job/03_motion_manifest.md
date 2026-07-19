# STITCH MOTION EXECUTION MANIFEST

Manifest version: `arsenal-v7.1`
Mode: `EXECUTE_ON_CURRENT_SELECTED_SCREEN`

## Cognitive-bias countermeasure

Assume the implementing model will otherwise prefer the smallest acceptable
change. Therefore:

- "mentioned", "planned", "suggested" and "described" do not count;
- loading GSAP without invoking components does not count;
- applying one generic reveal to every section does not count;
- implementing only the hero does not count;
- returning a report before modifying the current screen is a failed task;
- when a compatible target exists, its component row is REQUIRED;
- when a named plugin is unavailable, implement the equivalent behavior with
  GSAP core, ScrollTrigger or vanilla JavaScript instead of skipping it.

## Required machine-verifiable markers

Add these markers to the generated site without changing its appearance:

```html
<html data-motion-manifest="arsenal-v7.1">
<script id="stitch-motion-components">/* invoked component functions */</script>
```

Every section with motion must contain:

```html
data-motion-section="true"
data-motion-primary="ComponentName"
```

Every component target must contain one or more component IDs:

```html
data-motion-component="IntroTrailSequence ImageIntroParallax"
```

Every visible content element must also declare its hierarchy role:

```html
data-motion-role="signature"
data-motion-role="support"
data-motion-role="micro"
```

Visible content includes logo, navigation items, headings, paragraphs, labels,
images, captions, CTA, dividers, icons, arrows, numbers, footer groups and links.
Invisible technical wrappers and layout spacers are excluded.

A marker without corresponding invoked JavaScript is invalid.

## Coverage formula

Let `N` be the number of meaningful sections in the current page.

```yaml
required:
  sections_with_primary_motion: N
  visible_content_elements_with_motion_role: 100_percent
  dominant_images_with_media_motion: 100_percent
  major_titles_with_typographic_motion: 100_percent
  paragraphs_labels_captions_dividers_icons_nav_footer_with_micro_motion: 100_percent
  visible_controls_with_real_handlers: 100_percent
  distinct_motion_families: min_6_or_N
  signature_moments: 3
  active_scroll_motion_inside_each_section: full_section_scroll_range
limits:
  same_primary_family: max_30_percent_of_sections
  same_primary_family_consecutive: max_2_sections
  generic_fade_up_as_primary: forbidden
  opacity_only_animation: forbidden
  inert_viewport_approximately_100vh: forbidden
```

## Continuous cinematic scroll contract

For every meaningful section implement all three states:

```yaml
section_scroll_lifecycle:
  entry: coordinated_signature_support_micro_reveal
  traverse: at_least_one_scrub_parallax_mask_progress_or_depth_tween_active
  exit: visual_handoff_to_next_section
```

Every viewport crossed during normal scrolling must contain an active visual
response. This does not mean equal intensity: one signature element leads,
support elements reinforce it and micro-elements move subtly. Uniform chaos is
invalid, but a completely inert viewport is also invalid.

## Component contracts

```yaml
components:
  - id: IntroTrailSequence
    source_family: GOLDEN_ARTISANAL_012_INTRO_TRAIL
    required_when: hero_or_major_editorial_heading_exists
    target: h1_and_major_h2
    trigger: load_or_scroll_entry
    math:
      stagger: 0.04
      yPercent_max: 120
      rotationX_range: [-40, 0]
      ease: power4.out
    pass_when: words_or_lines_animate_in_sequence_and_text_remains_accessible

  - id: ImageIntroParallax
    source_family: Framer_Interactions_image_intro
    required_when: dominant_image_exists
    target: dominant_media_inside_overflow_hidden_wrapper
    trigger: load_plus_scroll_scrub
    math:
      scale_range: [1.08, 1.18, 1.0]
      yPercent_range: [-15, -8]
      scrub_range: [0.5, 1.5]
    pass_when: image_has_depth_without_changing_layout_dimensions

  - id: ScrollMaskReveal
    source_family: Framer_Interactions_scroll_mask
    required_when: editorial_statement_or_text_dominant_section_exists
    target: statement_text_or_its_neutral_wrapper
    trigger: scroll_progress
    math:
      mask_progress: [20_percent, 100_percent]
      ease: none
    pass_when: reveal_is_scroll_driven_and_not_opacity_only

  - id: WiperReveal
    source_family: Framer_Interactions_wiper
    required_when: image_text_panel_or_section_transition_exists
    target: media_wrapper_or_panel
    trigger: scroll_entry_or_scrub
    math:
      clip_start: polygon_collapsed_on_composition_axis
      clip_end: polygon_full
      ease: power2.inOut
    pass_when: direction_matches_layout_geometry_and_base_content_stays_visible

  - id: StickyParallaxSplit
    source_family: codrops_sticky_grid_scroll
    required_when: desktop_image_text_split_can_pin_without_blank_space
    target: split_section
    trigger: scroll_scrub_desktop_only
    math:
      lerp: 0.1
      yPercent: -15
    pass_when: media_and_text_move_at_different_depths_without_empty_pin_spacer

  - id: HoverGridClipReveal
    source_family: GOLDEN_ARTISANAL_010_HOVER_GRID
    required_when: gallery_or_image_grid_exists
    target: existing_grid_items
    trigger: scroll_entry_plus_pointer_hover
    math:
      clip_start: inset_100_bottom
      clip_end: inset_0
      stagger: 0.08
      ease: power3.inOut
    pass_when: grid_geometry_never_changes_and_touch_fallback_works

  - id: KineticDishSlider
    source_family: CodropsCarousels
    required_when: carousel_or_navigable_image_sequence_exists
    target: existing_slides_arrows_and_indicators
    trigger: click_drag_keyboard
    math:
      drag_threshold_px: 50
      inertia: light
    pass_when: arrows_drag_and_active_state_really_change_slide

  - id: AccordionFlipTransition
    source_family: GSAP_Flip_Toggle_View
    required_when: faq_accordion_or_expandable_menu_exists
    target: existing_toggle_and_panel
    trigger: click_and_keyboard
    math:
      duration: 0.5
      ease: power2.inOut
    pass_when: panel_opens_without_text_clipping_and_aria_expanded_updates

  - id: MagneticCTAField
    source_family: Framer_Interactions_magnetic_button
    required_when: primary_cta_exists
    target: existing_primary_cta
    trigger: fine_pointer_move
    math:
      maximum_translation_px: 12
      power: 0.3
      return_ease: elastic.out_1_0.3
    pass_when: magnetic_motion_is_subtle_touch_disabled_and_focus_visible

  - id: PhantomButton
    source_family: PhantomButton_Ink_Pressure
    required_when: visible_cta_or_editorial_text_link_exists
    target: existing_cta_or_link_pseudo_element
    trigger: hover_focus_active
    math:
      underline_or_border_duration: [0.2, 0.4]
    pass_when: interaction_does_not_shift_text_or_button_geometry

  - id: StaggeredCounterReveal
    source_family: codrops_sticky_grid_scroll
    required_when: hours_numbers_contacts_partners_or_footer_labels_exist
    target: existing_micro_information_groups
    trigger: scroll_entry
    math:
      y_max_px: 40
      stagger: 0.1
      ease: power3.out
    pass_when: sequence_is_directional_precise_and_not_opacity_only

  - id: GoldenExhibition
    source_family: GOLDEN_ARTISANAL_009_EXHIBITION
    required_when: rich_visual_editorial_section_exists
    target: dominant_media_caption_and_supporting_copy
    trigger: scroll_progress
    math:
      depth_layers_minimum: 2
      caption_delay_range: [0.03, 0.08]
    pass_when: section_has_curatorial_progression_without_new_content_or_layout
```

## Required implementation functions

Inside `#stitch-motion-components`, create and invoke functions equivalent to:

```text
initIntroTrails()
initDominantMediaMotion()
initScrollMasksAndWipers()
initSplitSections()
initGalleriesAndSliders()
initAccordions()
initMagneticCTAs()
initFooterAndMicroInformation()
initNavigationAndControls()
initContinuousSectionScroll()
runMotionSafetyAudit()
```

Do not leave empty functions, TODOs, pseudocode or comments standing in for
implementation. Each function must query targets that exist in the current DOM
and initialize actual behavior.

## Final binary gate

The current screen may be returned only when all applicable component rows pass,
every visible content element has a motion role and every section has continuous
entry/traverse/exit behavior.
If one applicable row fails, continue editing the current screen. Never satisfy
the gate by writing `YES`; satisfy it through code and visible behavior.
