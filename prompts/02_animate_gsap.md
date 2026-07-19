<!-- FASE 2 — /animate + regia GSAP + GSAP master + manifesto. Testo reale dal tuo materiale. -->

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

---

# 📦 BUNDLE GSAP PLUGINS

> **Istruzioni per l'IA (Stitch):** Questo file contiene il codice sorgente completo dei plugin GSAP estratti.

---

## 📄 File: `ScrollTrigger.js`
```javascript
/*!
 * ScrollTrigger 3.15.0
 * https://gsap.com
 *
 * @license Copyright 2008-2026, GreenSock. All rights reserved.
 * Subject to the terms at https://gsap.com/standard-license
 * @author: Jack Doyle, jack@greensock.com
*/
/* eslint-disable */

import { Observer, _getTarget, _vertical, _horizontal, _scrollers, _proxies, _getScrollFunc, _getProxyProp, _getVelocityProp } from "./Observer.js";

let gsap, _coreInitted, _win, _doc, _docEl, _body, _root, _resizeDelay, _toArray, _clamp, _time2, _syncInterval, _refreshing, _pointerIsDown, _transformProp, _i, _prevWidth, _prevHeight, _autoRefresh, _sort, _suppressOverwrites, _ignoreResize, _normalizer, _ignoreMobileResize, _baseScreenHeight, _baseScreenWidth, _fixIOSBug, _context, _scrollRestoration, _div100vh, _100vh, _isReverted, _clampingMax,
	_limitCallbacks, // if true, we'll only trigger callbacks if the active state toggles, so if you scroll immediately past both the start and end positions of a ScrollTrigger (thus inactive to inactive), neither its onEnter nor onLeave will be called. This is useful during startup.
	_startup = 1,
	_getTime = Date.now,
	_time1 = _getTime(),
	_lastScrollTime = 0,
	_enabled = 0,
	_parseClamp = (value, type, self) => {
		let clamp = (_isString(value) && (value.substr(0, 6) === "clamp(" || value.indexOf("max") > -1));
		self["_" + type + "Clamp"] = clamp;
		return clamp ? value.substr(6, value.length - 7) : value;
	},
	_keepClamp = (value, clamp) => clamp && (!_isString(value) || value.substr(0, 6) !== "clamp(") ? "clamp(" + value + ")" : value,
	_rafBugFix = () => _enabled && requestAnimationFrame(_rafBugFix), // in some browsers (like Firefox), screen repaints weren't consistent unless we had SOMETHING queued up in requestAnimationFrame()! So this just creates a super simple loop to keep it alive and smooth out repaints.
	_pointerDownHandler = () => _pointerIsDown = 1,
	_pointerUpHandler = () => _pointerIsDown = 0,
	_passThrough = v => v,
	_round = value => Math.round(value * 100000) / 100000 || 0,
	_windowExists = () => typeof(window) !== "undefined",
	_getGSAP = () => gsap || (_windowExists() && (gsap = window.gsap) && gsap.registerPlugin && gsap),
	_isViewport = e => !!~_root.indexOf(e),
	_getViewportDimension = dimensionProperty => (dimensionProperty === "Height" ? _100vh : _win["inner" + dimensionProperty]) || _docEl["client" + dimensionProperty] || _body["client" + dimensionProperty],
	_getBoundsFunc = element => _getProxyProp(element, "getBoundingClientRect") || (_isViewport(element) ? () => {_winOffsets.width = _win.innerWidth; _winOffsets.height = _100vh; return _winOffsets;} : () => _getBounds(element)),
	_getSizeFunc = (scroller, isViewport, {d, d2, a}) => (a = _getProxyProp(scroller, "getBoundingClientRect")) ? () => a()[d] : () => (isViewport ? _getViewportDimension(d2) : scroller["client" + d2]) || 0,
	_getOffsetsFunc = (element, isViewport) => !isViewport || ~_proxies.indexOf(element) ? _getBoundsFunc(element) : () => _winOffsets,
	_maxScroll = (element, {s, d2, d, a}) => Math.max(0, (s = "scroll" + d2) && (a = _getProxyProp(element, s)) ? a() - _getBoundsFunc(element)()[d] : _isViewport(element) ? (_docEl[s] || _body[s]) - _getViewportDimension(d2) : element[s] - element["offset" + d2]),
	_iterateAutoRefresh = (func, events) => {
		for (let i = 0; i < _autoRefresh.length; i += 3) {
			(!events || ~events.indexOf(_autoRefresh[i+1])) && func(_autoRefresh[i], _autoRefresh[i+1], _autoRefresh[i+2]);
		}
	},
	_isString = value => typeof(value) === "string",
	_isFunction = value => typeof(value) === "function",
	_isNumber = value => typeof(value) === "number",
	_isObject = value => typeof(value) === "object",
	_endAnimation = (animation, reversed, pause) => animation && animation.progress(reversed ? 0 : 1) && pause && animation.pause(),
	_callback = (self, func, extraParam) => {
		if (self.enabled) {
			let result = self._ctx ? self._ctx.add(() => func(self, extraParam)) : func(self, extraParam);
			result && result.totalTime && (self.callbackAnimation = result);
		}
	},
	_abs = Math.abs,
	_left = "left",
	_top = "top",
	_right = "right",
	_bottom = "bottom",
	_width = "width",
	_height = "height",
	_Right = "Right",
	_Left = "Left",
	_Top = "Top",
	_Bottom = "Bottom",
	_padding = "padding",
	_margin = "margin",
	_Width = "Width",
	_Height = "Height",
	_px = "px",
	_getComputedStyle = element => _win.getComputedStyle(element.nodeType === Node.DOCUMENT_NODE ? element.scrollingElement : element),
	_makePositionable = element => { // if the element already has position: absolute or fixed, leave that, otherwise make it position: relative
		let position = _getComputedStyle(element).position;
		element.style.position = (position === "absolute" || position === "fixed") ? position : "relative";
	},
	_setDefaults = (obj, defaults) => {
		for (let p in defaults) {
			(p in obj) || (obj[p] = defaults[p]);
		}
		return obj;
	},
	_getBounds = (element, withoutTransforms) => {
		let tween = withoutTransforms && _getComputedStyle(element)[_transformProp] !== "matrix(1, 0, 0, 1, 0, 0)" && gsap.to(element, {x: 0, y: 0, xPercent: 0, yPercent: 0, rotation: 0, rotationX: 0, rotationY: 0, scale: 1, skewX: 0, skewY: 0}).progress(1),
			bounds = element.getBoundingClientRect ? element.getBoundingClientRect() : element.scrollingElement.getBoundingClientRect();
		tween && tween.progress(0).kill();
		return bounds;
	},
	_getSize = (element, {d2}) => element["offset" + d2] || element["client" + d2] || 0,
	_getLabelRatioArray = timeline => {
		let a = [],
			labels = timeline.labels,
			duration = timeline.duration(),
			p;
		for (p in labels) {
			a.push(labels[p] / duration);
		}
		return a;
	},
	_getClosestLabel = animation => value => gsap.utils.snap(_getLabelRatioArray(animation), value),
	_snapDirectional = snapIncrementOrArray => {
		let snap = gsap.utils.snap(snapIncrementOrArray),
			a = Array.isArray(snapIncrementOrArray) && snapIncrementOrArray.slice(0).sort((a, b) => a - b);
		return a ? (value, direction, threshold= 1e-3) => {
			let i;
			if (!direction) {
				return snap(value);
			}
			if (direction > 0) {
				value -= threshold; // to avoid rounding errors. If we're too strict, it might snap forward, then immediately again, and again.
				for (i = 0; i < a.length; i++) {
					if (a[i] >= value) {
						return a[i];
					}
				}
				return a[i-1];
			} else {
				i = a.length;
				value += threshold;
				while (i--) {
					if (a[i] <= value) {
						return a[i];
					}
				}
			}
			return a[0];
		} : (value, direction, threshold= 1e-3) => {
			let snapped = snap(value);
			return !direction || Math.abs(snapped - value) < threshold || ((snapped - value < 0) === direction < 0) ? snapped : snap(direction < 0 ? value - snapIncrementOrArray : value + snapIncrementOrArray);
		};
	},
	_getLabelAtDirection = timeline => (value, st) => _snapDirectional(_getLabelRatioArray(timeline))(value, st.direction),
	_multiListener = (func, element, types, callback) => types.split(",").forEach(type => func(element, type, callback)),
	_addListener = (element, type, func, nonPassive, capture) => element.addEventListener(type, func, {passive: !nonPassive, capture: !!capture}),
	_removeListener = (element, type, func, capture) => element.removeEventListener(type, func, !!capture),
	_wheelListener = (func, el, scrollFunc) => {
		scrollFunc = scrollFunc && scrollFunc.wheelHandler
		if (scrollFunc) {
			func(el, "wheel", scrollFunc);
			func(el, "touchmove", scrollFunc);
		}
	},
	_markerDefaults = {startColor: "green", endColor: "red", indent: 0, fontSize: "16px", fontWeight:"normal"},
	_defaults = {toggleActions: "play", anticipatePin: 0},
	_keywords = {top: 0, left: 0, center: 0.5, bottom: 1, right: 1},
	_offsetToPx = (value, size) => {
		if (_isString(value)) {
			let eqIndex = value.indexOf("="),
				relative = ~eqIndex ? +(value.charAt(eqIndex-1) + 1) * parseFloat(value.substr(eqIndex + 1)) : 0;
			if (~eqIndex) {
				(value.indexOf("%") > eqIndex) && (relative *= size / 100);
				value = value.substr(0, eqIndex-1);
			}
			value = relative + ((value in _keywords) ? _keywords[value] * size : ~value.indexOf("%") ? parseFloat(value) * size / 100 : parseFloat(value) || 0);
		}
		return value;
	},
	_createMarker = (type, name, container, direction, {startColor, endColor, fontSize, indent, fontWeight}, offset, matchWidthEl, containerAnimation) => {
		let e = _doc.createElement("div"),
			useFixedPosition = _isViewport(container) || _getProxyProp(container, "pinType") === "fixed",
			isScroller = type.indexOf("scroller") !== -1,
			parent = useFixedPosition ? _body : container.tagName === "IFRAME" ? container.contentDocument.body : container,
			isStart = type.indexOf("start") !== -1,
			color = isStart ? startColor : endColor,
			css = "border-color:" + color + ";font-size:" + fontSize + ";color:" + color + ";font-weight:" + fontWeight + ";pointer-events:none;white-space:nowrap;font-family:sans-serif,Arial;z-index:1000;padding:4px 8px;border-width:0;border-style:solid;";
		css += "position:" + ((isScroller || containerAnimation) && useFixedPosition ? "fixed;" : "absolute;");
		(isScroller || containerAnimation || !useFixedPosition) && (css += (direction === _vertical ? _right : _bottom) + ":" + (offset + parseFloat(indent)) + "px;");
		matchWidthEl && (css += "box-sizing:border-box;text-align:left;width:" + matchWidthEl.offsetWidth + "px;");
		e._isStart = isStart;
		e.setAttribute("class", "gsap-marker-" + type + (name ? " marker-" + name : ""));
		e.style.cssText = css;
		e.innerText = name || name === 0 ? type + "-" + name : type;
		parent.children[0] ? parent.insertBefore(e, parent.children[0]) : parent.appendChild(e);
		e._offset = e["offset" + direction.op.d2];
		_positionMarker(e, 0, direction, isStart);
		return e;
	},
	_positionMarker = (marker, start, direction, flipped) => {
		let vars = {display: "block"},
			side = direction[flipped ? "os2" : "p2"],
			oppositeSide = direction[flipped ? "p2" : "os2"];
		marker._isFlipped = flipped;
		vars[direction.a + "Percent"] = flipped ? -100 : 0;
		vars[direction.a] = flipped ? "1px" : 0;
		vars["border" + side + _Width] = 1;
		vars["border" + oppositeSide + _Width] = 0;
		vars[direction.p] = start + "px";
		gsap.set(marker, vars);
	},
	_triggers = [],
	_ids = {},
	_rafID,
	_sync = () => _getTime() - _lastScrollTime > 34 && (_rafID || (_rafID = requestAnimationFrame(_updateAll))),
	_onScroll = () => { // previously, we tried to optimize performance by batching/deferring to the next requestAnimationFrame(), but discovered that Safari has a few bugs that make this unworkable (especially on iOS). See https://codepen.io/GreenSock/pen/16c435b12ef09c38125204818e7b45fc?editors=0010 and https://codepen.io/GreenSock/pen/JjOxYpQ/3dd65ccec5a60f1d862c355d84d14562?editors=0010 and https://codepen.io/GreenSock/pen/ExbrPNa/087cef197dc35445a0951e8935c41503?editors=0010
		if (!_normalizer || !_normalizer.isPressed || _normalizer.startX > _body.clientWidth) { // if the user is dragging the scrollbar, allow it.
			_scrollers.cache++;
			if (_normalizer) {
				_rafID || (_rafID = requestAnimationFrame(_updateAll));
			} else {
				_updateAll(); // Safari in particular (on desktop) NEEDS the immediate update rather than waiting for a requestAnimationFrame() whereas iOS seems to benefit from waiting for the requestAnimationFrame() tick, at least when normalizing. See https://codepen.io/GreenSock/pen/qBYozqO?editors=0110
			}
			_lastScrollTime || _dispatch("scrollStart");
			_lastScrollTime = _getTime();
		}
	},
	_setBaseDimensions = () => {
		_baseScreenWidth = _win.innerWidth;
		_baseScreenHeight = _win.innerHeight;
	},
	_onResize = (force) => {
		_scrollers.cache++;
		(force === true || (!_refreshing && !_ignoreResize && !_doc.fullscreenElement && !_doc.webkitFullscreenElement && (!_ignoreMobileResize || _baseScreenWidth !== _win.innerWidth || Math.abs(_win.innerHeight - _baseScreenHeight) > _win.innerHeight * 0.25))) && _resizeDelay.restart(true);
	}, // ignore resizes triggered by refresh()
	_listeners = {},
	_emptyArray = [],
	_softRefresh = () => _removeListener(ScrollTrigger, "scrollEnd", _softRefresh) || _refreshAll(true),
	_dispatch = type => (_listeners[type] && _listeners[type].map(f => f())) || _emptyArray,
	_savedStyles = [], // when ScrollTrigger.saveStyles() is called, the inline styles are recorded in this Array in a sequential format like [element, cssText, gsCache, media]. This keeps it very memory-efficient and fast to iterate through.
	_revertRecorded = media => {
		for (let i = 0; i < _savedStyles.length; i+=5) {
			if (!media || _savedStyles[i+4] && _savedStyles[i+4].query === media) {
				_savedStyles[i].style.cssText = _savedStyles[i+1];
				_savedStyles[i].getBBox && _savedStyles[i].setAttribute("transform", _savedStyles[i+2] || "");
				_savedStyles[i+3].uncache = 1;
			}
		}
	},
	_recordScrollPositions = () => _scrollers.forEach(obj => _isFunction(obj) && ++obj.cacheID && (obj.rec = obj())), // record the current scroll position. Also force the clearing of the cache because some browsers take a little while to dispatch the "scroll" event and the user may have changed the scroll position and then called ScrollTrigger.refresh() right away
	_revertAll = (kill, media) => {
		let trigger;
		for (_i = 0; _i < _triggers.length; _i++) {
			trigger = _triggers[_i];
			if (trigger && (!media || trigger._ctx === media)) {
				if (kill) {
					trigger.kill(1);
				} else {
					trigger.revert(true, true);
				}
			}
		}
		_isReverted = true;
		media && _revertRecorded(media);
		media || _dispatch("revert");
	},
	_clearScrollMemory = (scrollRestoration, force) => { // zero-out all the recorded scroll positions. Don't use _triggers because if, for example, .matchMedia() is used to create some ScrollTriggers and then the user resizes and it removes ALL ScrollTriggers, and then go back to a size where there are ScrollTriggers, it would have kept the position(s) saved from the initial state.
		_scrollers.cache++;
		(force || !_refreshingAll) && _scrollers.forEach(obj => _isFunction(obj) && obj.cacheID++ && (obj.rec = 0));
		_isString(scrollRestoration) && (_win.history.scrollRestoration = _scrollRestoration = scrollRestoration);
	},
	_refreshingAll,
	_refreshID = 0,
	_queueRefreshID,
	_queueRefreshAll = () => { // we don't want to call _refreshAll() every time we create a new ScrollTrigger (for performance reasons) - it's better to batch them. Some frameworks dynamically load content and we can't rely on the window's "load" or "DOMContentLoaded" events to trigger it.
		if (_queueRefreshID !== _refreshID) {
			let id = _queueRefreshID = _refreshID;
			requestAnimationFrame(() => id === _refreshID && _refreshAll(true));
		}
	},
	_refresh100vh = () => {
		_body.appendChild(_div100vh);
		_100vh = (!_normalizer && _div100vh.offsetHeight) || _win.innerHeight;
		_body.removeChild(_div100vh);
	},
	_hideAllMarkers = hide => _toArray(".gsap-marker-start, .gsap-marker-end, .gsap-marker-scroller-start, .gsap-marker-scroller-end").forEach(el => el.style.display = hide ? "none" : "block"),
	_refreshAll = (force, skipRevert) => {
		_docEl = _doc.documentElement; // some frameworks like Astro may cache the <body> and replace it during routing, so we'll just re-record the _docEl and _body for safety (otherwise, the markers may not get added properly).
		_body = _doc.body;
		_root = [_win, _doc, _docEl, _body];
		if (_lastScrollTime && !force && !_isReverted) {
			_addListener(ScrollTrigger, "scrollEnd", _softRefresh);
			return;
		}
		_refresh100vh();
		_refreshingAll = ScrollTrigger.isRefreshing = true;
		_isReverted || _recordScrollPositions();
		let refreshInits = _dispatch("refreshInit");
		_sort && ScrollTrigger.sort();
		skipRevert || _revertAll();
		_scrollers.forEach(obj => {
			if (_isFunction(obj)) {
				obj.smooth && (obj.target.style.scrollBehavior = "auto"); // smooth scrolling interferes
				obj(0);
			}
		});
		_triggers.slice(0).forEach(t => t.refresh()) // don't loop with _i because during a refresh() someone could call ScrollTrigger.update() which would iterate through _i resulting in a skip.
		_isReverted = false;
		_triggers.forEach((t) => { // nested pins (pinnedContainer) with pinSpacing may expand the container, so we must accommodate that here.
			if (t._subPinOffset && t.pin) {
				let prop = t.vars.horizontal ? "offsetWidth" : "offsetHeight",
					original = t.pin[prop];
				t.revert(true, 1);
				t.adjustPinSpacing(t.pin[prop] - original);
				t.refresh();
			}
		});
		_clampingMax = 1; // pinSpacing might be propping a page open, thus when we .setPositions() to clamp a ScrollTrigger's end we should leave the pinSpacing alone. That's what this flag is for.
		_hideAllMarkers(true);
		_triggers.forEach(t => { // the scroller's max scroll position may change after all the ScrollTriggers refreshed (like pinning could push it down), so we need to loop back and correct any with end: "max". Same for anything with a clamped end
			let max = _maxScroll(t.scroller, t._dir),
				endClamp = t.vars.end === "max" || (t._endClamp && t.end > max),
				startClamp = t._startClamp && t.start >= max;
			(endClamp || startClamp) && t.setPositions(startClamp ? max - 1 : t.start, endClamp ? Math.max(startClamp ? max : t.start + 1, max) : t.end, true);
		});
		_hideAllMarkers(false);
		_clampingMax = 0;
		refreshInits.forEach(result => result && result.render && result.render(-1)); // if the onRefreshInit() returns an animation (typically a gsap.set()), revert it. This makes it easy to put things in a certain spot before refreshing for measurement purposes, and then put things back.
		_scrollers.forEach(obj => {
			if (_isFunction(obj)) {
				obj.smooth && requestAnimationFrame(() => obj.target.style.scrollBehavior = "smooth");
				obj.rec && obj(obj.rec);
			}
		});
		_clearScrollMemory(_scrollRestoration, 1);
		_resizeDelay.pause();
		_refreshID++;
		_refreshingAll = 2;
		_updateAll(2);
		_triggers.forEach(t => _isFunction(t.vars.onRefresh) && t.vars.onRefresh(t));
		_refreshingAll = ScrollTrigger.isRefreshing = false;
		_dispatch("refresh");
	},
	_lastScroll = 0,
	_direction = 1,
	_primary,
	_updateAll = (force) => {
		if (force === 2 || (!_refreshingAll && !_isReverted)) { // _isReverted could be true if, for example, a matchMedia() is in the process of executing. We don't want to update during the time everything is reverted.
			ScrollTrigger.isUpdating = true;
			_primary && _primary.update(0); // ScrollSmoother uses refreshPriority -9999 to become the primary that gets updated before all others because it affects the scroll position.
			let l = _triggers.length,
				time = _getTime(),
				recordVelocity = time - _time1 >= 50,
				scroll = l && _triggers[0].scroll();
			_direction = _lastScroll > scroll ? -1 : 1;
			_refreshingAll || (_lastScroll = scroll);
			if (recordVelocity) {
				if (_lastScrollTime && !_pointerIsDown && time - _lastScrollTime > 200) {
					_lastScrollTime = 0;
					_dispatch("scrollEnd");
				}
				_time2 = _time1;
				_time1 = time;
			}
			if (_direction < 0) {
				_i = l;
				while (_i-- > 0) {
					_triggers[_i] && _triggers[_i].update(0, recordVelocity);
				}
				_direction = 1;
			} else {
				for (_i = 0; _i < l; _i++) {
					_triggers[_i] && _triggers[_i].update(0, recordVelocity);
				}
			}
			ScrollTrigger.isUpdating = false;
		}
		_rafID = 0;
	},
	_propNamesToCopy = [_left, _top, _bottom, _right, _margin + _Bottom, _margin + _Right, _margin + _Top, _margin + _Left, "display", "flexShrink", "float", "zIndex", "gridColumnStart", "gridColumnEnd", "gridRowStart", "gridRowEnd", "gridArea", "justifySelf", "alignSelf", "placeSelf", "order"],
	_stateProps = _propNamesToCopy.concat([_width, _height, "boxSizing", "max" + _Width, "max" + _Height, "position", _margin, _padding, _padding + _Top, _padding + _Right, _padding + _Bottom, _padding + _Left]),
	_swapPinOut = (pin, spacer, state) => {
		_setState(state);
		let cache = pin._gsap;
		if (cache.spacerIsNative) {
			_setState(cache.spacerState);
		} else if (pin._gsap.swappedIn) {
			let parent = spacer.parentNode;
			if (parent) {
				parent.insertBefore(pin, spacer);
				parent.removeChild(spacer);
			}
		}
		pin._gsap.swappedIn = false;
	},
	_swapPinIn = (pin, spacer, cs, spacerState) => {
		if (!pin._gsap.swappedIn) {
			let i = _propNamesToCopy.length,
				spacerStyle = spacer.style,
				pinStyle = pin.style,
				p;
			while (i--) {
				p = _propNamesToCopy[i];
				spacerStyle[p] = cs[p];
			}
			spacerStyle.position = cs.position === "absolute" ? "absolute" : "relative";
			(cs.display === "inline") && (spacerStyle.display = "inline-block");
			pinStyle[_bottom] = pinStyle[_right] = "auto";
			spacerStyle.flexBasis = cs.flexBasis || "auto";
			spacerStyle.overflow = "visible";
			spacerStyle.boxSizing = "border-box";
			spacerStyle[_width] = _getSize(pin, _horizontal) + _px;
			spacerStyle[_height] = _getSize(pin, _vertical) + _px;
			spacerStyle[_padding] = pinStyle[_margin] = pinStyle[_top] = pinStyle[_left] = "0";
			_setState(spacerState);
			pinStyle[_width] = pinStyle["max" + _Width] = cs[_width];
			pinStyle[_height] = pinStyle["max" + _Height] = cs[_height];
			pinStyle[_padding] = cs[_padding];
			if (pin.parentNode !== spacer) {
				pin.parentNode.insertBefore(spacer, pin);
				spacer.appendChild(pin);
			}
			pin._gsap.swappedIn = true;
		}
	},
	_capsExp = /([A-Z])/g,
	_setState = state => {
		if (state) {
			let style = state.t.style,
				l = state.length,
				i = 0,
				p, value;
			(state.t._gsap || gsap.core.getCache(state.t)).uncache = 1; // otherwise transforms may be off
			for (; i < l; i +=2) {
				value = state[i+1];
				p = state[i];
				if (value) {
					style[p] = value;
				} else if (style[p]) {
					style.removeProperty(p.replace(_capsExp, "-$1").toLowerCase());
				}
			}
		}
	},
	_getState = element => { // returns an Array with alternating values like [property, value, property, value] and a "t" property pointing to the target (element). Makes it fast and cheap.
		let l = _stateProps.length,
			style = element.style,
			state = [],
			i = 0;
		for (; i < l; i++) {
			state.push(_stateProps[i], style[_stateProps[i]]);
		}
		state.t = element;
		return state;
	},
	_copyState = (state, override, omitOffsets) => {
		let result = [],
			l = state.length,
			i = omitOffsets ? 8 : 0, // skip top, left, right, bottom if omitOffsets is true
			p;
		for (; i < l; i += 2) {
			p = state[i];
			result.push(p, (p in override) ? override[p] : state[i+1]);
		}
		result.t = state.t;
		return result;
	},
	_winOffsets = {left:0, top:0},
	// // potential future feature (?) Allow users to calculate where a trigger hits (scroll position) like getScrollPosition("#id", "top bottom")
	// _getScrollPosition = (trigger, position, {scroller, containerAnimation, horizontal}) => {
	// 	scroller = _getTarget(scroller || _win);
	// 	let direction = horizontal ? _horizontal : _vertical,
	// 		isViewport = _isViewport(scroller);
	// 	_getSizeFunc(scroller, isViewport, direction);
	// 	return _parsePosition(position, _getTarget(trigger), _getSizeFunc(scroller, isViewport, direction)(), direction, _getScrollFunc(scroller, direction)(), 0, 0, 0, _getOffsetsFunc(scroller, isViewport)(), isViewport ? 0 : parseFloat(_getComputedStyle(scroller)["border" + direction.p2 + _Width]) || 0, 0, containerAnimation ? containerAnimation.duration() : _maxScroll(scroller), containerAnimation);
	// },
	_parsePosition = (value, trigger, scrollerSize, direction, scroll, marker, markerScroller, self, scrollerBounds, borderWidth, useFixedPosition, scrollerMax, containerAnimation, clampZeroProp) => {
		_isFunction(value) && (value = value(self));
		if (_isString(value) && value.substr(0,3) === "max") {
			value = scrollerMax + (value.charAt(4) === "=" ? _offsetToPx("0" + value.substr(3), scrollerSize) : 0);
		}
		let time = containerAnimation ? containerAnimation.time() : 0,
			p1, p2, element;
		containerAnimation && containerAnimation.seek(0);
		isNaN(value) || (value = +value); // convert a string number like "45" to an actual number
		if (!_isNumber(value)) {
			_isFunction(trigger) && (trigger = trigger(self));
			let offsets = (value || "0").split(" "),
				bounds, localOffset, globalOffset, display;
			element = _getTarget(trigger, self) || _body;
			bounds = _getBounds(element) || {};
			if ((!bounds || (!bounds.left && !bounds.top)) && _getComputedStyle(element).display === "none") { // if display is "none", it won't report getBoundingClientRect() properly
				display = element.style.display;
				element.style.display = "block";
				bounds = _getBounds(element);
				display ? (element.style.display = display) : element.style.removeProperty("display");
			}
			localOffset = _offsetToPx(offsets[0], bounds[direction.d]);
			globalOffset = _offsetToPx(offsets[1] || "0", scrollerSize);
			value = bounds[direction.p] - scrollerBounds[direction.p] - borderWidth + localOffset + scroll - globalOffset;
			markerScroller && _positionMarker(markerScroller, globalOffset, direction, (scrollerSize - globalOffset < 20 || (markerScroller._isStart && globalOffset > 20)));
			scrollerSize -= scrollerSize - globalOffset; // adjust for the marker
		} else {
			containerAnimation && (value = gsap.utils.mapRange(containerAnimation.scrollTrigger.start, containerAnimation.scrollTrigger.end, 0, scrollerMax, value));
			markerScroller && _positionMarker(markerScroller, scrollerSize, direction, true);
		}
		if (clampZeroProp) {
			self[clampZeroProp] = value || -0.001;
			value < 0 && (value = 0);
		}
		if (marker) {
			let position = value + scrollerSize,
				isStart = marker._isStart;
			p1 = "scroll" + direction.d2;
			_positionMarker(marker, position, direction, (isStart && position > 20) || (!isStart && (useFixedPosition ? Math.max(_body[p1], _docEl[p1]) : marker.parentNode[p1]) <= position + 1));
			if (useFixedPosition) {
				scrollerBounds = _getBounds(markerScroller);
				useFixedPosition && (marker.style[direction.op.p] = (scrollerBounds[direction.op.p] - direction.op.m - marker._offset) + _px);
			}
		}
		if (containerAnimation && element) {
			p1 = _getBounds(element);
			containerAnimation.seek(scrollerMax);
			p2 = _getBounds(element);
			containerAnimation._caScrollDist = p1[direction.p] - p2[direction.p];
			value = value / (containerAnimation._caScrollDist) * scrollerMax;
		}
		containerAnimation && containerAnimation.seek(time);
		return containerAnimation ? value : Math.round(value);
	},
	_prefixExp = /(webkit|moz|length|cssText|inset)/i,
	_reparent = (element, parent, top, left) => {
		if (element.parentNode !== parent) {
			let style = element.style,
				p, cs;
			if (parent === _body) {
				element._stOrig = style.cssText; // record original inline styles so we can revert them later
				cs = _getComputedStyle(element);
				for (p in cs) { // must copy all relevant styles to ensure that nothing changes visually when we reparent to the <body>. Skip the vendor prefixed ones.
					if (!+p && !_prefixExp.test(p) && cs[p] && typeof style[p] === "string" && p !== "0") {
						style[p] = cs[p];
					}
				}
				style.top = top;
				style.left = left;
			} else {
				style.cssText = element._stOrig;
			}
			gsap.core.getCache(element).uncache = 1;
			parent.appendChild(element);
		}
	},
	_interruptionTracker = (getValueFunc, initialValue, onInterrupt) => {
		let last1 = initialValue,
			last2 = last1;
		return value => {
			let current = Math.round(getValueFunc()); // round because in some [very uncommon] Windows environments, scroll can get reported with decimals even though it was set without.
			if (current !== last1 && current !== last2 && Math.abs(current - last1) > 3 && Math.abs(current - last2) > 3) { // if the user scrolls, kill the tween. iOS Safari intermittently misreports the scroll position, it may be the most recently-set one or the one before that! When Safari is zoomed (CMD-+), it often misreports as 1 pixel off too! So if we set the scroll position to 125, for example, it'll actually report it as 124.
				value = current;
				onInterrupt && onInterrupt();
			}
			last2 = last1;
			last1 = Math.round(value);
			return last1;
		};
	},
	_shiftMarker = (marker, direction, value) => {
		let vars = {};
		vars[direction.p] = "+=" + value;
		gsap.set(marker, vars);
	},
	// _mergeAnimations = animations => {
	// 	let tl = gsap.timeline({smoothChildTiming: true}).startTime(Math.min(...animations.map(a => a.globalTime(0))));
	// 	animations.forEach(a => {let time = a.totalTime(); tl.add(a); a.totalTime(time); });
	// 	tl.smoothChildTiming = false;
	// 	return tl;
	// },

	// returns a function that can be used to tween the scroll position in the direction provided, and when doing so it'll add a .tween property to the FUNCTION itself, and remove it when the tween completes or gets killed. This gives us a way to have multiple ScrollTriggers use a central function for any given scroller and see if there's a scroll tween running (which would affect if/how things get updated)
	_getTweenCreator = (scroller, direction) => {
		let getScroll = _getScrollFunc(scroller, direction),
			prop = "_scroll" + direction.p2, // add a tweenable property to the scroller that's a getter/setter function, like _scrollTop or _scrollLeft. This way, if someone does gsap.killTweensOf(scroller) it'll kill the scroll tween.
			getTween = (scrollTo, vars, initialValue, change1, change2) => {
				let tween = getTween.tween,
					onComplete = vars.onComplete,
					modifiers = {};
				initialValue = initialValue || getScroll();
				let checkForInterruption = _interruptionTracker(getScroll, initialValue, () => {
					tween.kill();
					getTween.tween = 0;
				});
				change2 = (change1 && change2) || 0; // if change1 is 0, we set that to the difference and ignore change2. Otherwise, there would be a compound effect.
				change1 = change1 || (scrollTo - initialValue);
				tween && tween.kill();
				vars[prop] = scrollTo;
				vars.inherit = false;
				vars.modifiers = modifiers;
				modifiers[prop] = () => checkForInterruption(initialValue + change1 * tween.ratio + change2 * tween.ratio * tween.ratio);
				vars.onUpdate = () => {
					_scrollers.cache++;
					getTween.tween && _updateAll(); // if it was interrupted/killed, like in a context.revert(), don't force an updateAll()
				};
				vars.onComplete = () => {
					getTween.tween = 0;
					onComplete && onComplete.call(tween);
				};
				tween = getTween.tween = gsap.to(scroller, vars);
				return tween;
			};
		scroller[prop] = getScroll;
		getScroll.wheelHandler = () => getTween.tween && getTween.tween.kill() && (getTween.tween = 0);
		_addListener(scroller, "wheel", getScroll.wheelHandler); // Windows machines handle mousewheel scrolling in chunks (like "3 lines per scroll") meaning the typical strategy for cancelling the scroll isn't as sensitive. It's much more likely to match one of the previous 2 scroll event positions. So we kill any snapping as soon as there's a wheel event.
		ScrollTrigger.isTouch && _addListener(scroller, "touchmove", getScroll.wheelHandler);
		return getTween;
	};




export class ScrollTrigger {

	constructor(vars, animation) {
		_coreInitted || ScrollTrigger.register(gsap) || console.warn("Please gsap.registerPlugin(ScrollTrigger)");
		_context(this);
		this.init(vars, animation);
	}

	init(vars, animation) {
		this.progress = this.start = 0;
		this.vars && this.kill(true, true); // in case it's being initted again
		if (!_enabled) {
			this.update = this.refresh = this.kill = _passThrough;
			return;
		}
		vars = _setDefaults((_isString(vars) || _isNumber(vars) || vars.nodeType) ? {trigger: vars} : vars, _defaults);
		let {onUpdate, toggleClass, id, onToggle, onRefresh, scrub, trigger, pin, pinSpacing, invalidateOnRefresh, anticipatePin, onScrubComplete, onSnapComplete, once, snap, pinReparent, pinSpacer, containerAnimation, fastScrollEnd, preventOverlaps} = vars,
			direction = vars.horizontal || (vars.containerAnimation && vars.horizontal !== false) ? _horizontal : _vertical,
			isToggle = !scrub && scrub !== 0,
			scroller = _getTarget(vars.scroller || _win),
			scrollerCache = gsap.core.getCache(scroller),
			isViewport = _isViewport(scroller),
			useFixedPosition = ("pinType" in vars ? vars.pinType : _getProxyProp(scroller, "pinType") || (isViewport && "fixed")) === "fixed",
			callbacks = [vars.onEnter, vars.onLeave, vars.onEnterBack, vars.onLeaveBack],
			toggleActions = isToggle && vars.toggleActions.split(" "),
			markers = "markers" in vars ? vars.markers : _defaults.markers,
			borderWidth = isViewport ? 0 : parseFloat(_getComputedStyle(scroller)["border" + direction.p2 + _Width]) || 0,
			self = this,
			onRefreshInit = vars.onRefreshInit && (() => vars.onRefreshInit(self)),
			getScrollerSize = _getSizeFunc(scroller, isViewport, direction),
			getScrollerOffsets = _getOffsetsFunc(scroller, isViewport),
			lastSnap = 0,
			lastRefresh = 0,
			prevProgress = 0,
			scrollFunc = _getScrollFunc(scroller, direction),
			tweenTo, pinCache, snapFunc, scroll1, scroll2, start, end, markerStart, markerEnd, markerStartTrigger, markerEndTrigger, markerVars, executingOnRefresh,
			change, pinOriginalState, pinActiveState, pinState, spacer, offset, pinGetter, pinSetter, pinStart, pinChange, spacingStart, spacerState, markerStartSetter, pinMoves,
			markerEndSetter, cs, snap1, snap2, scrubTween, scrubSmooth, snapDurClamp, snapDelayedCall, prevScroll, prevAnimProgress, caMarkerSetter, customRevertReturn;

		// for the sake of efficiency, _startClamp/_endClamp serve like a truthy value indicating that clamping was enabled on the start/end, and ALSO store the actual pre-clamped numeric value. We tap into that in ScrollSmoother for speed effects. So for example, if start="clamp(top bottom)" results in a start of -100 naturally, it would get clamped to 0 but -100 would be stored in _startClamp.
		self._startClamp = self._endClamp = false;
		self._dir = direction;
		anticipatePin *= 45;
		self.scroller = scroller;
		self.scroll = containerAnimation ? containerAnimation.time.bind(containerAnimation) : scrollFunc;
		scroll1 = scrollFunc();
		self.vars = vars;
		animation = animation || vars.animation;
		if ("refreshPriority" in vars) {
			_sort = 1;
			vars.refreshPriority === -9999 && (_primary = self); // used by ScrollSmoother
		}
		scrollerCache.tweenScroll = scrollerCache.tweenScroll || {
			top: _getTweenCreator(scroller, _vertical),
			left: _getTweenCreator(scroller, _horizontal)
		};
		self.tweenTo = tweenTo = scrollerCache.tweenScroll[direction.p];
		self.scrubDuration = value => {
			scrubSmooth = _isNumber(value) && value;
			if (!scrubSmooth) {
				scrubTween && scrubTween.progress(1).kill();
				scrubTween = 0;
			} else {
				scrubTween ? scrubTween.duration(value) : (scrubTween = gsap.to(animation, {ease: "expo", totalProgress: "+=0", inherit: false, duration: scrubSmooth, paused: true, onComplete: () => onScrubComplete && onScrubComplete(self)}));
			}
		};
		if (animation) {
			animation.vars.lazy = false;
			(animation._initted && !self.isReverted) || (animation.vars.immediateRender !== false && vars.immediateRender !== false && animation.duration() && animation.render(0, true, true)); // special case: if this ScrollTrigger gets re-initted, a from() tween with a stagger could get initted initially and then reverted on the re-init which means it'll need to get rendered again here to properly display things. Otherwise, See https://gsap.com/forums/topic/36777-scrollsmoother-splittext-nextjs/ and https://codepen.io/GreenSock/pen/eYPyPpd?editors=0010
			self.animation = animation.pause();
			animation.scrollTrigger = self;
			self.scrubDuration(scrub);
			snap1 = 0;
			id || (id = animation.vars.id);
		}

		if (snap) {
			// TODO: potential idea: use legitimate CSS scroll snapping by pushing invisible elements into the DOM that serve as snap positions, and toggle the document.scrollingElement.style.scrollSnapType onToggle. See https://codepen.io/GreenSock/pen/JjLrgWM for a quick proof of concept.
			if (!_isObject(snap) || snap.push) {
				snap = {snapTo: snap};
			}
			("scrollBehavior" in _body.style) && gsap.set(isViewport ? [_body, _docEl] : scroller, {scrollBehavior: "auto"}); // smooth scrolling doesn't work with snap.
			_scrollers.forEach(o => _isFunction(o) && o.target === (isViewport ? _doc.scrollingElement || _docEl : scroller) && (o.smooth = false)); // note: set smooth to false on both the vertical and horizontal scroll getters/setters
			snapFunc = _isFunction(snap.snapTo) ? snap.snapTo : snap.snapTo === "labels" ? _getClosestLabel(animation) : snap.snapTo === "labelsDirectional" ? _getLabelAtDirection(animation) : snap.directional !== false ? (value, st) => _snapDirectional(snap.snapTo)(value, _getTime() - lastRefresh < 500 ? 0 : st.direction) : gsap.utils.snap(snap.snapTo);
			snapDurClamp = snap.duration || {min: 0.1, max: 2};
			snapDurClamp = _isObject(snapDurClamp) ? _clamp(snapDurClamp.min, snapDurClamp.max) : _clamp(snapDurClamp, snapDurClamp);
			snapDelayedCall = gsap.delayedCall(snap.delay || (scrubSmooth / 2) || 0.1, () => {
				let scroll = scrollFunc(),
					refreshedRecently = _getTime() - lastRefresh < 500,
					tween = tweenTo.tween;
				if ((refreshedRecently || Math.abs(self.getVelocity()) < 10) && !tween && !_pointerIsDown && lastSnap !== scroll) {
					let progress = (scroll - start) / change, // don't use self.progress because this might run between the refresh() and when the scroll position updates and self.progress is set properly in the update() method.
						totalProgress = animation && !isToggle ? animation.totalProgress() : progress,
						velocity = refreshedRecently ? 0 : ((totalProgress - snap2) / (_getTime() - _time2) * 1000) || 0,
						change1 = gsap.utils.clamp(-progress, 1 - progress, _abs(velocity / 2) * velocity / 0.185),
						naturalEnd = progress + (snap.inertia === false ? 0 : change1),
						endValue, endScroll,
						{ onStart, onInterrupt, onComplete } = snap;
					endValue = snapFunc(naturalEnd, self);
					_isNumber(endValue) || (endValue = naturalEnd); // in case the function didn't return a number, fall back to using the naturalEnd
					endScroll = Math.max(0, Math.round(start + endValue * change));
					if (scroll <= end && scroll >= start && endScroll !== scroll) {
						if (tween && !tween._initted && tween.data <= _abs(endScroll - scroll)) { // there's an overlapping snap! So we must figure out which one is closer and let that tween live.
							return;
						}
						if (snap.inertia === false) {
							change1 = endValue - progress;
						}
						tweenTo(endScroll, {
							duration: snapDurClamp(_abs( (Math.max(_abs(naturalEnd - totalProgress), _abs(endValue - totalProgress)) * 0.185 / velocity / 0.05) || 0)),
							ease: snap.ease || "power3",
							data: _abs(endScroll - scroll), // record the distance so that if another snap tween occurs (conflict) we can prioritize the closest snap.
							onInterrupt: () => snapDelayedCall.restart(true) && onInterrupt && _callback(self, onInterrupt),
							onComplete() {
								self.update();
								lastSnap = scrollFunc();
								if (animation && !isToggle) { // the resolution of the scrollbar is limited, so we should correct the scrubbed animation's playhead at the end to match EXACTLY where it was supposed to snap
									scrubTween ? scrubTween.resetTo("totalProgress", endValue, animation._tTime / animation._tDur) : animation.progress(endValue);
								}
								snap1 = snap2 = animation && !isToggle ? animation.totalProgress() : self.progress;
								onSnapComplete && onSnapComplete(self);
								onComplete && _callback(self, onComplete);
							}
						}, scroll, change1 * change, endScroll - scroll - change1 * change);
						onStart && _callback(self, onStart, tweenTo.tween);
					}
				} else if (self.isActive && lastSnap !== scroll) {
					snapDelayedCall.restart(true);
				}
			}).pause();
		}
		id && (_ids[id] = self);
		trigger = self.trigger = _getTarget(trigger || (pin !== true && pin));

		// if a trigger has some kind of scroll-related effect applied that could contaminate the "y" or "x" position (like a ScrollSmoother effect), we needed a way to temporarily revert it, so we use the stRevert property of the gsCache. It can return another function that we'll call at the end so it can return to its normal state.
		customRevertReturn = trigger && trigger._gsap && trigger._gsap.stRevert;
		customRevertReturn && (customRevertReturn = customRevertReturn(self));

		pin = pin === true ? trigger : _getTarget(pin);
		_isString(toggleClass) && (toggleClass = {targets: trigger, className: toggleClass});
		if (pin) {
			(pinSpacing === false || pinSpacing === _margin) || (pinSpacing = !pinSpacing && pin.parentNode && pin.parentNode.style && _getComputedStyle(pin.parentNode).display === "flex" ? false : _padding); // if the parent is display: flex, don't apply pinSpacing by default. We should check that pin.parentNode is an element (not shadow dom window)
			self.pin = pin;
			pinCache = gsap.core.getCache(pin);
			if (!pinCache.spacer) { // record the spacer and pinOriginalState on the cache in case someone tries pinning the same element with MULTIPLE ScrollTriggers - we don't want to have multiple spacers or record the "original" pin state after it has already been affected by another ScrollTrigger.
				if (pinSpacer) {
					pinSpacer = _getTarget(pinSpacer);
					pinSpacer && !pinSpacer.nodeType && (pinSpacer = pinSpacer.current || pinSpacer.nativeElement); // for React & Angular
					pinCache.spacerIsNative = !!pinSpacer;
					pinSpacer && (pinCache.spacerState = _getState(pinSpacer));
				}
				pinCache.spacer = spacer = pinSpacer || _doc.createElement("div");
				spacer.classList.add("pin-spacer");
				id && spacer.classList.add("pin-spacer-" + id);
				pinCache.pinState = pinOriginalState = _getState(pin);
			} else {
				pinOriginalState = pinCache.pinState;
			}
			vars.force3D !== false && gsap.set(pin, {force3D: true});
			self.spacer = spacer = pinCache.spacer;
			cs = _getComputedStyle(pin);
			spacingStart = cs[pinSpacing + direction.os2];
			pinGetter = gsap.getProperty(pin);
			pinSetter = gsap.quickSetter(pin, direction.a, _px);
			// pin.firstChild && !_maxScroll(pin, direction) && (pin.style.overflow = "hidden"); // protects from collapsing margins, but can have unintended consequences as demonstrated here: https://codepen.io/GreenSock/pen/1e42c7a73bfa409d2cf1e184e7a4248d so it was removed in favor of just telling people to set up their CSS to avoid the collapsing margins (overflow: hidden | auto is just one option. Another is border-top: 1px solid transparent).
			_swapPinIn(pin, spacer, cs);
			pinState = _getState(pin);
		}
		if (markers) {
			markerVars = _isObject(markers) ? _setDefaults(markers, _markerDefaults) : _markerDefaults;
			markerStartTrigger = _createMarker("scroller-start", id, scroller, direction, markerVars, 0);
			markerEndTrigger = _createMarker("scroller-end", id, scroller, direction, markerVars, 0, markerStartTrigger);
			offset = markerStartTrigger["offset" + direction.op.d2];
			let content = _getTarget(_getProxyProp(scroller, "content") || scroller);
			markerStart = this.markerStart = _createMarker("start", id, content, direction, markerVars, offset, 0, containerAnimation);
			markerEnd = this.markerEnd = _createMarker("end", id, content, direction, markerVars, offset, 0, containerAnimation);
			containerAnimation && (caMarkerSetter = gsap.quickSetter([markerStart, markerEnd], direction.a, _px));
			if ((!useFixedPosition && !(_proxies.length && _getProxyProp(scroller, "fixedMarkers") === true))) {
				_makePositionable(isViewport ? _body : scroller);
				gsap.set([markerStartTrigger, markerEndTrigger], {force3D: true});
				markerStartSetter = gsap.quickSetter(markerStartTrigger, direction.a, _px);
				markerEndSetter = gsap.quickSetter(markerEndTrigger, direction.a, _px);
			}
		}

		if (containerAnimation) {
			let oldOnUpdate = containerAnimation.vars.onUpdate,
				oldParams = containerAnimation.vars.onUpdateParams;
			containerAnimation.eventCallback("onUpdate", () => {
				self.update(0, 0, 1);
				oldOnUpdate && oldOnUpdate.apply(containerAnimation, oldParams || []);
			});
		}

		self.previous = () => _triggers[_triggers.indexOf(self) - 1];
		self.next = () => _triggers[_triggers.indexOf(self) + 1];

		self.revert = (revert, temp) => {
			if (!temp) { return self.kill(true); } // for compatibility with gsap.context() and gsap.matchMedia() which call revert()
			let r = revert !== false || !self.enabled,
				prevRefreshing = _refreshing;
			if (r !== self.isReverted) {
				if (r) {
					prevScroll = Math.max(scrollFunc(), self.scroll.rec || 0); // record the scroll so we can revert later (repositioning/pinning things can affect scroll position). In the static refresh() method, we first record all the scroll positions as a reference.
					prevProgress = self.progress;
					prevAnimProgress = animation && animation.progress();
				}
				markerStart && [markerStart, markerEnd, markerStartTrigger, markerEndTrigger].forEach(m => m.style.display = r ? "none" : "block");
				if (r) {
					_refreshing = self;
					self.update(r); // make sure the pin is back in its original position so that all the measurements are correct. do this BEFORE swapping the pin out
				}
				if (pin && (!pinReparent || !self.isActive)) {
					if (r) {
						_swapPinOut(pin, spacer, pinOriginalState);
					} else {
						_swapPinIn(pin, spacer, _getComputedStyle(pin), spacerState);
					}
				}
				r || self.update(r); // when we're restoring, the update should run AFTER swapping the pin into its pin-spacer.
				_refreshing = prevRefreshing; // restore. We set it to true during the update() so that things fire properly in there.
				self.isReverted = r;
			}
		}

		self.refresh = (soft, force, position, pinOffset) => { // position is typically only defined if it's coming from setPositions() - it's a way to skip the normal parsing. pinOffset is also only from setPositions() and is mostly related to fancy stuff we need to do in ScrollSmoother with effects
			if ((_refreshing || !self.enabled) && !force) {
				return;
			}
			if (pin && soft && _lastScrollTime) {
				_addListener(ScrollTrigger, "scrollEnd", _softRefresh);
				return;
			}
			!_refreshingAll && onRefreshInit && onRefreshInit(self);
			_refreshing = self;
			if (tweenTo.tween && !position) { // we skip this if a position is passed in because typically that's from .setPositions() and it's best to allow in-progress snapping to continue.
				tweenTo.tween.kill();
				tweenTo.tween = 0;
			}
			scrubTween && scrubTween.pause();

			if (invalidateOnRefresh && animation) {
				animation.revert({kill: false}).invalidate();
				animation.getChildren ? animation.getChildren(true, true, false).forEach(t => t.vars.immediateRender && t.render(0, true, true)) : animation.vars.immediateRender && animation.render(0, true, true); // any from() or fromTo() tweens should render immediately (well, unless they have immediateRender: false)
			}

			self.isReverted || self.revert(true, true);
			self._subPinOffset = false; // we'll set this to true in the sub-pins if we find any
			let size = getScrollerSize(),
				scrollerBounds = getScrollerOffsets(),
				max = containerAnimation ? containerAnimation.duration() : _maxScroll(scroller, direction),
				isFirstRefresh = change <= 0.01 || !change,
				offset = 0,
				otherPinOffset = pinOffset || 0,
				parsedEnd = _isObject(position) ? position.end : vars.end,
				parsedEndTrigger = vars.endTrigger || trigger,
				parsedStart = _isObject(position) ? position.start : (vars.start || (vars.start === 0 || !trigger ? 0 : (pin ? "0 0" : "0 100%"))),
				pinnedContainer = self.pinnedContainer = vars.pinnedContainer && _getTarget(vars.pinnedContainer, self),
				triggerIndex = (trigger && Math.max(0, _triggers.indexOf(self))) || 0,
				i = triggerIndex,
				cs, bounds, scroll, isVertical, override, curTrigger, curPin, oppositeScroll, initted, revertedPins, forcedOverflow, markerStartOffset, markerEndOffset;
			if (markers && _isObject(position)) { // if we alter the start/end positions with .setPositions(), it generally feeds in absolute NUMBERS which don't convey information about where to line up the markers, so to keep it intuitive, we record how far the trigger positions shift after applying the new numbers and then offset by that much in the opposite direction. We do the same to the associated trigger markers too of course.
				markerStartOffset = gsap.getProperty(markerStartTrigger, direction.p);
				markerEndOffset = gsap.getProperty(markerEndTrigger, direction.p);
			}
			while (i-- > 0) { // user might try to pin the same element more than once, so we must find any prior triggers with the same pin, revert them, and determine how long they're pinning so that we can offset things appropriately. Make sure we revert from last to first so that things "rewind" properly.
				curTrigger = _triggers[i];
				curTrigger.end || curTrigger.refresh(0, 1) || (_refreshing = self); // if it's a timeline-based trigger that hasn't been fully initialized yet because it's waiting for 1 tick, just force the refresh() here, otherwise if it contains a pin that's supposed to affect other ScrollTriggers further down the page, they won't be adjusted properly.
				curPin = curTrigger.pin;
				if (curPin && (curPin === trigger || curPin === pin || curPin === pinnedContainer) && !curTrigger.isReverted) {
					revertedPins || (revertedPins = []);
					revertedPins.unshift(curTrigger); // we'll revert from first to last to make sure things reach their end state properly
					curTrigger.revert(true, true);
				}
				if (curTrigger !== _triggers[i]) { // in case it got removed.
					triggerIndex--;
					i--;
				}
			}
			_isFunction(parsedStart) && (parsedStart = parsedStart(self));
			parsedStart = _parseClamp(parsedStart, "start", self);
			start = _parsePosition(parsedStart, trigger, size, direction, scrollFunc(), markerStart, markerStartTrigger, self, scrollerBounds, borderWidth, useFixedPosition, max, containerAnimation, self._startClamp && "_startClamp") || (pin ? -0.001 : 0);
			_isFunction(parsedEnd) && (parsedEnd = parsedEnd(self));
			if (_isString(parsedEnd) && !parsedEnd.indexOf("+=")) {
				if (~parsedEnd.indexOf(" ")) {
					parsedEnd = (_isString(parsedStart) ? parsedStart.split(" ")[0] : "") + parsedEnd;
				} else {
					offset = _offsetToPx(parsedEnd.substr(2), size);
					parsedEnd = _isString(parsedStart) ? parsedStart : (containerAnimation ? gsap.utils.mapRange(0, containerAnimation.duration(), containerAnimation.scrollTrigger.start, containerAnimation.scrollTrigger.end, start) : start) + offset; // _parsePosition won't factor in the offset if the start is a number, so do it here.
					parsedEndTrigger = trigger;
				}
			}
			parsedEnd = _parseClamp(parsedEnd, "end", self);
			end = Math.max(start, _parsePosition(parsedEnd || (parsedEndTrigger ? "100% 0" : max), parsedEndTrigger, size, direction, scrollFunc() + offset, markerEnd, markerEndTrigger, self, scrollerBounds, borderWidth, useFixedPosition, max, containerAnimation, self._endClamp && "_endClamp")) || -0.001;

			offset = 0;
			i = triggerIndex;
			while (i--) {
				curTrigger = _triggers[i] || {};
				curPin = curTrigger.pin;
				if (curPin && curTrigger.start - curTrigger._pinPush <= start && !containerAnimation && curTrigger.end > 0) {
					cs = curTrigger.end - (self._startClamp ? Math.max(0, curTrigger.start) : curTrigger.start);
					if (((curPin === trigger && curTrigger.start - curTrigger._pinPush < start) || curPin === pinnedContainer) && isNaN(parsedStart)) { // numeric start values shouldn't be offset at all - treat them as absolute
						offset += cs * (1 - curTrigger.progress);
					}
					curPin === pin && (otherPinOffset += cs);
				}
			}
			start += offset;
			end += offset;
			self._startClamp && (self._startClamp += offset);

			if (self._endClamp && !_refreshingAll) {
				self._endClamp = end || -0.001;
				end = Math.min(end, _maxScroll(scroller, direction));
			}
			change = (end - start) || ((start -= 0.01) && 0.001);

			if (isFirstRefresh) { // on the very first refresh(), the prevProgress couldn't have been accurate yet because the start/end were never calculated, so we set it here. Before 3.11.5, it could lead to an inaccurate scroll position restoration with snapping.
				prevProgress = gsap.utils.clamp(0, 1, gsap.utils.normalize(start, end, prevScroll));
			}
			self._pinPush = otherPinOffset;
			if (markerStart && offset) { // offset the markers if necessary
				cs = {};
				cs[direction.a] = "+=" + offset;
				pinnedContainer && (cs[direction.p] = "-=" + scrollFunc());
				gsap.set([markerStart, markerEnd], cs);
			}

			if (pin && !(_clampingMax && self.end >= _maxScroll(scroller, direction))) {
				cs = _getComputedStyle(pin);
				isVertical = direction === _vertical;
				scroll = scrollFunc(); // recalculate because the triggers can affect the scroll
				pinStart = parseFloat(pinGetter(direction.a)) + otherPinOffset;
				if (!max && end > 1) { // makes sure the scroller has a scrollbar, otherwise if something has width: 100%, for example, it would be too big (exclude the scrollbar). See https://gsap.com/forums/topic/25182-scrolltrigger-width-of-page-increase-where-markers-are-set-to-false/
					forcedOverflow = (isViewport ? (_doc.scrollingElement || _docEl) : scroller).style;
					forcedOverflow = {style: forcedOverflow, value: forcedOverflow["overflow" + direction.a.toUpperCase()]};
					if (isViewport && _getComputedStyle(_body)["overflow" + direction.a.toUpperCase()] !== "scroll") { // avoid an extra scrollbar if BOTH <html> and <body> have overflow set to "scroll"
						forcedOverflow.style["overflow" + direction.a.toUpperCase()] = "scroll";
					}
				}
				_swapPinIn(pin, spacer, cs);
				pinState = _getState(pin);
				// transforms will interfere with the top/left/right/bottom placement, so remove them temporarily. getBoundingClientRect() factors in transforms.
				bounds = _getBounds(pin, true);
				oppositeScroll = useFixedPosition && _getScrollFunc(scroller, isVertical ? _horizontal : _vertical)();
				if (pinSpacing) {
					spacerState = [pinSpacing + direction.os2, change + otherPinOffset + _px];
					spacerState.t = spacer;
					i = (pinSpacing === _padding) ? _getSize(pin, direction) + change + otherPinOffset : 0;
					if (i) {
						spacerState.push(direction.d, i + _px); // for box-sizing: border-box (must include padding).
						spacer.style.flexBasis !== "auto" && (spacer.style.flexBasis = i + _px);
					}
					_setState(spacerState);
					if (pinnedContainer) { // in ScrollTrigger.refresh(), we need to re-evaluate the pinContainer's size because this pinSpacing may stretch it out, but we can't just add the exact distance because depending on layout, it may not push things down or it may only do so partially.
						_triggers.forEach(t => {
							if (t.pin === pinnedContainer && t.vars.pinSpacing !== false) {
								t._subPinOffset = true;
							}
						});
					}
					useFixedPosition && scrollFunc(prevScroll);
				} else {
					i = _getSize(pin, direction);
					i && spacer.style.flexBasis !== "auto" && (spacer.style.flexBasis = i + _px);
				}
				if (useFixedPosition) {
					override = {
						top: (bounds.top + (isVertical ? scroll - start : oppositeScroll)) + _px,
						left: (bounds.left + (isVertical ? oppositeScroll : scroll - start)) + _px,
						boxSizing: "border-box",
						position: "fixed"
					};
					override[_width] = override["max" + _Width] = Math.ceil(bounds.width) + _px;
					override[_height] = override["max" + _Height] = Math.ceil(bounds.height) + _px;
					override[_margin] = override[_margin + _Top] = override[_margin + _Right] = override[_margin + _Bottom] = override[_margin + _Left] = "0";
					override[_padding] = cs[_padding];
					override[_padding + _Top] = cs[_padding + _Top];
					override[_padding + _Right] = cs[_padding + _Right];
					override[_padding + _Bottom] = cs[_padding + _Bottom];
					override[_padding + _Left] = cs[_padding + _Left];
					pinActiveState = _copyState(pinOriginalState, override, pinReparent);
					_refreshingAll && scrollFunc(0);
				}
				if (animation) { // the animation might be affecting the transform, so we must jump to the end, check the value, and compensate accordingly. Otherwise, when it becomes unpinned, the pinSetter() will get set to a value that doesn't include whatever the animation did.
					initted = animation._initted; // if not, we must invalidate() after this step, otherwise it could lock in starting values prematurely.
					_suppressOverwrites(1);
					animation.render(animation.duration(), true, true);
					pinChange = pinGetter(direction.a) - pinStart + change + otherPinOffset;
					pinMoves = Math.abs(change - pinChange) > 1;
					useFixedPosition && pinMoves && pinActiveState.splice(pinActiveState.length - 2, 2); // transform is the last property/value set in the state Array. Since the animation is controlling that, we should omit it.
					animation.render(0, true, true);
					initted || animation.invalidate(true);
					animation.parent || animation.totalTime(animation.totalTime()); // if, for example, a toggleAction called play() and then refresh() happens and when we render(1) above, it would cause the animation to complete and get removed from its parent, so this makes sure it gets put back in.
					_suppressOverwrites(0);
				} else {
					pinChange = change
				}
				forcedOverflow && (forcedOverflow.value ? (forcedOverflow.style["overflow" + direction.a.toUpperCase()] = forcedOverflow.value) : forcedOverflow.style.removeProperty("overflow-" + direction.a));
			} else if (trigger && scrollFunc() && !containerAnimation) { // it may be INSIDE a pinned element, so walk up the tree and look for any elements with _pinOffset to compensate because anything with pinSpacing that's already scrolled would throw off the measurements in getBoundingClientRect()
				bounds = trigger.parentNode;
				while (bounds && bounds !== _body) {
					if (bounds._pinOffset) {
						start -= bounds._pinOffset;
						end -= bounds._pinOffset;
					}
					bounds = bounds.parentNode;
				}
			}
			revertedPins && revertedPins.forEach(t => t.revert(false, true));
			self.start = start;
			self.end = end;
			scroll1 = scroll2 = _refreshingAll ? prevScroll : scrollFunc(); // reset velocity
			if (!containerAnimation && !_refreshingAll) {
				scroll1 < prevScroll && scrollFunc(prevScroll);
				self.scroll.rec = 0;
			}
			self.revert(false, true);
			lastRefresh = _getTime();
			if (snapDelayedCall) {
				lastSnap = -1; // just so snapping gets re-enabled, clear out any recorded last value
				// self.isActive && scrollFunc(start + change * prevProgress); // previously this line was here to ensure that when snapping kicks in, it's from the previous progress but in some cases that's not desirable, like an all-page ScrollTrigger when new content gets added to the page, that'd totally change the progress.
				snapDelayedCall.restart(true);
			}
			_refreshing = 0;
			animation && isToggle && (animation._initted || prevAnimProgress) && animation.progress() !== prevAnimProgress && animation.progress(prevAnimProgress || 0, true).render(animation.time(), true, true); // must force a re-render because if saveStyles() was used on the target(s), the styles could have been wiped out during the refresh().
			if (isFirstRefresh || prevProgress !== self.progress || containerAnimation || invalidateOnRefresh || (animation && !animation._initted)) { // ensures that the direction is set properly (when refreshing, progress is set back to 0 initially, then back again to wherever it needs to be) and that callbacks are triggered.
				animation && !isToggle && (animation._initted || prevProgress || animation.vars.immediateRender !== false) && animation.totalProgress(containerAnimation && start < -0.001 && !prevProgress ? gsap.utils.normalize(start, end, 0) : prevProgress, true); // to avoid issues where animation callbacks like onStart aren't triggered.
				self.progress = isFirstRefresh || ((scroll1 - start) / change === prevProgress) ? 0 : prevProgress;
			}
			pin && pinSpacing && (spacer._pinOffset = Math.round(self.progress * pinChange));
			scrubTween && scrubTween.invalidate();

			if (!isNaN(markerStartOffset)) { // numbers were passed in for the position which are absolute, so instead of just putting the markers at the very bottom of the viewport, we figure out how far they shifted down (it's safe to assume they were originally positioned in closer relation to the trigger element with values like "top", "center", a percentage or whatever, so we offset that much in the opposite direction to basically revert them to the relative position thy were at previously.
				markerStartOffset -= gsap.getProperty(markerStartTrigger, direction.p);
				markerEndOffset -= gsap.getProperty(markerEndTrigger, direction.p);
				_shiftMarker(markerStartTrigger, direction, markerStartOffset);
				_shiftMarker(markerStart, direction, markerStartOffset - (pinOffset || 0));
				_shiftMarker(markerEndTrigger, direction, markerEndOffset);
				_shiftMarker(markerEnd, direction, markerEndOffset - (pinOffset || 0));
			}

			isFirstRefresh && !_refreshingAll && self.update(); // edge case - when you reload a page when it's already scrolled down, some browsers fire a "scroll" event before DOMContentLoaded, triggering an updateAll(). If we don't update the self.progress as part of refresh(), then when it happens next, it may record prevProgress as 0 when it really shouldn't, potentially causing a callback in an animation to fire again.

			if (onRefresh && !_refreshingAll && !executingOnRefresh) { // when refreshing all, we do extra work to correct pinnedContainer sizes and ensure things don't exceed the maxScroll, so we should do all the refreshes at the end after all that work so that the start/end values are corrected.
				executingOnRefresh = true;
				onRefresh(self);
				executingOnRefresh = false;
			}
		};

		self.getVelocity = () => ((scrollFunc() - scroll2) / (_getTime() - _time2) * 1000) || 0;

		self.endAnimation = () => {
			_endAnimation(self.callbackAnimation);
			if (animation) {
				scrubTween ? scrubTween.progress(1) : (!animation.paused() ? _endAnimation(animation, animation.reversed()) : isToggle || _endAnimation(animation, self.direction < 0, 1));
			}
		};

		self.labelToScroll = label => animation && animation.labels && ((start || self.refresh() || start) + (animation.labels[label] / animation.duration()) * change) || 0;

		self.getTrailing = name => {
			let i = _triggers.indexOf(self),
				a = self.direction > 0 ? _triggers.slice(0, i).reverse() : _triggers.slice(i+1);
			return (_isString(name) ? a.filter(t => t.vars.preventOverlaps === name) : a).filter(t => self.direction > 0 ? t.end <= start : t.start >= end);
		};


		self.update = (reset, recordVelocity, forceFake) => {
			if (containerAnimation && !forceFake && !reset) {
				return;
			}
			let scroll = _refreshingAll === true ? prevScroll : self.scroll(),
				p = reset ? 0 : (scroll - start) / change,
				clipped = p < 0 ? 0 : p > 1 ? 1 : p || 0,
				prevProgress = self.progress,
				isActive, wasActive, toggleState, action, stateChanged, toggled, isAtMax, isTakingAction;
			if (recordVelocity) {
				scroll2 = scroll1;
				scroll1 = containerAnimation ? scrollFunc() : scroll;
				if (snap) {
					snap2 = snap1;
					snap1 = animation && !isToggle ? animation.totalProgress() : clipped;
				}
			}
			// anticipate the pinning a few ticks ahead of time based on velocity to avoid a visual glitch due to the fact that most browsers do scrolling on a separate thread (not synced with requestAnimationFrame).
			if (anticipatePin && pin && !_refreshing && !_startup && _lastScrollTime) {
				if (!clipped && start < scroll + ((scroll - scroll2) / (_getTime() - _time2)) * anticipatePin) {
					clipped = 0.0001;
				} else if (clipped === 1 && end > scroll + ((scroll - scroll2) / (_getTime() - _time2)) * anticipatePin) {
					clipped = 0.9999;
				}
			}
			if (clipped !== prevProgress && self.enabled) {
				isActive = self.isActive = !!clipped && clipped < 1;
				wasActive = !!prevProgress && prevProgress < 1;
				toggled = isActive !== wasActive;
				stateChanged = toggled || !!clipped !== !!prevProgress; // could go from start all the way to end, thus it didn't toggle but it did change state in a sense (may need to fire a callback)
				self.direction = clipped > prevProgress ? 1 : -1;
				self.progress = clipped;

				if (stateChanged && !_refreshing) {
					toggleState = clipped && !prevProgress ? 0 : clipped === 1 ? 1 : prevProgress === 1 ? 2 : 3; // 0 = enter, 1 = leave, 2 = enterBack, 3 = leaveBack (we prioritize the FIRST encounter, thus if you scroll really fast past the onEnter and onLeave in one tick, it'd prioritize onEnter.
					if (isToggle) {
						action = (!toggled && toggleActions[toggleState + 1] !== "none" && toggleActions[toggleState + 1]) || toggleActions[toggleState]; // if it didn't toggle, that means it shot right past and since we prioritize the "enter" action, we should switch to the "leave" in this case (but only if one is defined)
						isTakingAction = animation && (action === "complete" || action === "reset" || action in animation);
					}
				}

				preventOverlaps && (toggled || isTakingAction) && (isTakingAction || scrub || !animation) && (_isFunction(preventOverlaps) ? preventOverlaps(self) : self.getTrailing(preventOverlaps).forEach(t => t.endAnimation()));

				if (!isToggle) {
					if (scrubTween && !_refreshing && !_startup) {
						(scrubTween._dp._time - scrubTween._start !== scrubTween._time) && scrubTween.render(scrubTween._dp._time - scrubTween._start); // if there's a scrub on both the container animation and this one (or a ScrollSmoother), the update order would cause this one not to have rendered yet, so it wouldn't make any progress before we .restart() it heading toward the new progress so it'd appear stuck thus we force a render here.
						if (scrubTween.resetTo) {
							scrubTween.resetTo("totalProgress", clipped, animation._tTime / animation._tDur);
						} else { // legacy support (courtesy), before 3.10.0
							scrubTween.vars.totalProgress = clipped;
							scrubTween.invalidate().restart();
						}
					} else if (animation) {
						animation.totalProgress(clipped, !!(_refreshing && (lastRefresh || reset)));
					}
				}
				if (pin) {
					reset && pinSpacing && (spacer.style[pinSpacing + direction.os2] = spacingStart);
					if (!useFixedPosition) {
						pinSetter(_round(pinStart + pinChange * clipped));
					} else if (stateChanged) {
						isAtMax = !reset && clipped > prevProgress && end + 1 > scroll && scroll + 1 >= _maxScroll(scroller, direction); // if it's at the VERY end of the page, don't switch away from position: fixed because it's pointless and it could cause a brief flash when the user scrolls back up (when it gets pinned again)
						if (pinReparent) {
							if (!reset && (isActive || isAtMax)) {
								let bounds = _getBounds(pin, true),
									offset = scroll - start;
								_reparent(pin, _body, (bounds.top + (direction === _vertical ? offset : 0)) + _px, (bounds.left + (direction === _vertical ? 0 : offset)) + _px);
							} else {
								_reparent(pin, spacer);
							}
						}
						_setState(isActive || isAtMax ? pinActiveState : pinState);
						(pinMoves && clipped < 1 && isActive) || pinSetter(pinStart + (clipped === 1 && !isAtMax ? pinChange : 0));
					}
				}
				snap && !tweenTo.tween && !_refreshing && !_startup && snapDelayedCall.restart(true);
				toggleClass && (toggled || (once && clipped && (clipped < 1 || !_limitCallbacks))) && _toArray(toggleClass.targets).forEach(el => el.classList[isActive || once ? "add" : "remove"](toggleClass.className)); // classes could affect positioning, so do it even if reset or refreshing is true.
				onUpdate && !isToggle && !reset && onUpdate(self);
				if (stateChanged && !_refreshing) {
					if (isToggle) {
						if (isTakingAction) {
							if (action === "complete") {
								animation.pause().totalProgress(1);
							} else if (action === "reset") {
								animation.restart(true).pause();
							} else if (action === "restart") {
								animation.restart(true);
							} else {
								animation[action]();
							}
						}
						onUpdate && onUpdate(self);
					}
					if (toggled || !_limitCallbacks) { // on startup, the page could be scrolled and we don't want to fire callbacks that didn't toggle. For example onEnter shouldn't fire if the ScrollTrigger isn't actually entered.
						onToggle && toggled && _callback(self, onToggle);
						callbacks[toggleState] && _callback(self, callbacks[toggleState]);
						once && (clipped === 1 ? self.kill(false, 1) : (callbacks[toggleState] = 0)); // a callback shouldn't be called again if once is true.
						if (!toggled) { // it's possible to go completely past, like from before the start to after the end (or vice-versa) in which case BOTH callbacks should be fired in that order
							toggleState = clipped === 1 ? 1 : 3;
							callbacks[toggleState] && _callback(self, callbacks[toggleState]);
						}
					}
					if (fastScrollEnd && !isActive && Math.abs(self.getVelocity()) > (_isNumber(fastScrollEnd) ? fastScrollEnd : 2500)) {
						_endAnimation(self.callbackAnimation);
						scrubTween ? scrubTween.progress(1) : _endAnimation(animation, action === "reverse" ? 1 : !clipped, 1);
					}
				} else if (isToggle && onUpdate && !_refreshing) {
					onUpdate(self);
				}
			}
			// update absolutely-positioned markers (only if the scroller isn't the viewport)
			if (markerEndSetter) {
				let n = containerAnimation ? scroll / containerAnimation.duration() * (containerAnimation._caScrollDist || 0) : scroll;
				markerStartSetter(n + (markerStartTrigger._isFlipped ? 1 : 0));
				markerEndSetter(n);
			}
			caMarkerSetter && caMarkerSetter(-scroll / containerAnimation.duration() * (containerAnimation._caScrollDist || 0));
		};

		self.enable = (reset, refresh) => {
			if (!self.enabled) {
				self.enabled = true;
				_addListener(scroller, "resize", _onResize);
				isViewport || _addListener(scroller, "scroll", _onScroll);
				onRefreshInit && _addListener(ScrollTrigger, "refreshInit", onRefreshInit);
				if (reset !== false) {
					self.progress = prevProgress = 0;
					scroll1 = scroll2 = lastSnap = scrollFunc();
				}
				refresh !== false && self.refresh();
			}
		};

		self.getTween = snap => snap && tweenTo ? tweenTo.tween : scrubTween;

		self.setPositions = (newStart, newEnd, keepClamp, pinOffset) => { // doesn't persist after refresh()! Intended to be a way to override values that were set during refresh(), like you could set it in onRefresh()
			if (containerAnimation) { // convert ratios into scroll positions. Remember, start/end values on ScrollTriggers that have a containerAnimation refer to the time (in seconds), NOT scroll positions.
				let st = containerAnimation.scrollTrigger,
					duration = containerAnimation.duration(),
					change = st.end - st.start;
				newStart = st.start + change * newStart / duration;
				newEnd = st.start + change * newEnd / duration;
			}
			self.refresh(false, false, {start: _keepClamp(newStart, keepClamp && !!self._startClamp), end: _keepClamp(newEnd, keepClamp && !!self._endClamp)}, pinOffset);
			self.update();
		};

		self.adjustPinSpacing = amount => {
			if (spacerState && amount) {
				let i = spacerState.indexOf(direction.d) + 1;
				spacerState[i] = (parseFloat(spacerState[i]) + amount) + _px;
				spacerState[1] = (parseFloat(spacerState[1]) + amount) + _px;
				_setState(spacerState);
			}
		};

		self.disable = (reset, allowAnimation) => {
			reset !== false && self.revert(true, true);
			if (self.enabled) {
				self.enabled = self.isActive = false;
				allowAnimation || (scrubTween && scrubTween.pause());
				prevScroll = 0;
				pinCache && (pinCache.uncache = 1);
				onRefreshInit && _removeListener(ScrollTrigger, "refreshInit", onRefreshInit);
				if (snapDelayedCall) {
					snapDelayedCall.pause();
					tweenTo.tween && tweenTo.tween.kill() && (tweenTo.tween = 0);
				}
				if (!isViewport) {
					let i = _triggers.length;
					while (i--) {
						if (_triggers[i].scroller === scroller && _triggers[i] !== self) {
							return; //don't remove the listeners if there are still other triggers referencing it.
						}
					}
					_removeListener(scroller, "resize", _onResize);
					isViewport || _removeListener(scroller, "scroll", _onScroll);
				}
			}
		};

		self.kill = (revert, allowAnimation) => {
			self.disable(revert, allowAnimation);
			scrubTween && !allowAnimation && scrubTween.kill();
			id && (delete _ids[id]);
			let i = _triggers.indexOf(self);
			i >= 0 && _triggers.splice(i, 1);
			i === _i && _direction > 0 && _i--; // if we're in the middle of a refresh() or update(), splicing would cause skips in the index, so adjust...

			// if no other ScrollTrigger instances of the same scroller are found, wipe out any recorded scroll position. Otherwise, in a single page application, for example, it could maintain scroll position when it really shouldn't.
			i = 0;
			_triggers.forEach(t => t.scroller === self.scroller && (i = 1));
			i || _refreshingAll || (self.scroll.rec = 0);

			if (animation) {
				animation.scrollTrigger = null;
				revert && animation.revert({kill: false});
				allowAnimation || animation.kill();
			}
			markerStart && [markerStart, markerEnd, markerStartTrigger, markerEndTrigger].forEach(m => m.parentNode && m.parentNode.removeChild(m));
			_primary === self && (_primary = 0);
			if (pin) {
				pinCache && (pinCache.uncache = 1);
				i = 0;
				_triggers.forEach(t => t.pin === pin && i++);
				i || (pinCache.spacer = 0); // if there aren't any more ScrollTriggers with the same pin, remove the spacer, otherwise it could be contaminated with old/stale values if the user re-creates a ScrollTrigger for the same element.
			}
			vars.onKill && vars.onKill(self);
		};

		_triggers.push(self);
		self.enable(false, false);
		customRevertReturn && customRevertReturn(self);

		if (animation && animation.add && !change) { // if the animation is a timeline, it may not have been populated yet, so it wouldn't render at the proper place on the first refresh(), thus we should schedule one for the next tick. If "change" is defined, we know it must be re-enabling, thus we can refresh() right away.
			let updateFunc = self.update; // some browsers may fire a scroll event BEFORE a tick elapses and/or the DOMContentLoaded fires. So there's a chance update() will be called BEFORE a refresh() has happened on a Timeline-attached ScrollTrigger which means the start/end won't be calculated yet. We don't want to add conditional logic inside the update() method (like check to see if end is defined and if not, force a refresh()) because that's a function that gets hit a LOT (performance). So we swap out the real update() method for this one that'll re-attach it the first time it gets called and of course forces a refresh().
			self.update = () => {
				self.update = updateFunc;
				_scrollers.cache++; // otherwise a cached scroll position may get used in the refresh() in a very rare scenario, like if ScrollTriggers are created inside a DOMContentLoaded event and the queued requestAnimationFrame() fires beforehand. See https://gsap.com/community/forums/topic/41267-scrolltrigger-breaks-on-refresh-when-using-domcontentloaded/
				start || end || self.refresh();
			};
			gsap.delayedCall(0.01, self.update);
			change = 0.01;
			start = end = 0;
		} else {
			self.refresh();
		}
		pin && _queueRefreshAll(); // pinning could affect the positions of other things, so make sure we queue a full refresh()
	}


	static register(core) {
		if (!_coreInitted) {
			gsap = core || _getGSAP();
			_windowExists() && window.document && ScrollTrigger.enable();
			_coreInitted = _enabled;
		}
		return _coreInitted;
	}

	static defaults(config) {
		if (config) {
			for (let p in config) {
				_defaults[p] = config[p];
			}
		}
		return _defaults;
	}

	static disable(reset, kill) {
		_enabled = 0;
		_triggers.forEach(trigger => trigger[kill ? "kill" : "disable"](reset));
		_removeListener(_win, "wheel", _onScroll);
		_removeListener(_doc, "scroll", _onScroll);
		clearInterval(_syncInterval);
		_removeListener(_doc, "touchcancel", _passThrough);
		_removeListener(_body, "touchstart", _passThrough);
		_multiListener(_removeListener, _doc, "pointerdown,touchstart,mousedown", _pointerDownHandler);
		_multiListener(_removeListener, _doc, "pointerup,touchend,mouseup", _pointerUpHandler);
		_resizeDelay.kill();
		_iterateAutoRefresh(_removeListener);
		for (let i = 0; i < _scrollers.length; i+=3) {
			_wheelListener(_removeListener, _scrollers[i], _scrollers[i+1]);
			_wheelListener(_removeListener, _scrollers[i], _scrollers[i+2]);
		}
	}

	static enable() {
		_win = window;
		_doc = document;
		_docEl = _doc.documentElement;
		_body = _doc.body;
		if (gsap) {
			_toArray = gsap.utils.toArray;
			_clamp = gsap.utils.clamp;
			_context = gsap.core.context || _passThrough;
			_suppressOverwrites = gsap.core.suppressOverwrites || _passThrough;
			_scrollRestoration = _win.history.scrollRestoration || "auto";
			_lastScroll = _win.pageYOffset || 0;
			gsap.core.globals("ScrollTrigger", ScrollTrigger); // must register the global manually because in Internet Explorer, functions (classes) don't have a "name" property.
			if (_body) {
				_enabled = 1;
				_div100vh = document.createElement("div"); // to solve mobile browser address bar show/hide resizing, we shouldn't rely on window.innerHeight. Instead, use a <div> with its height set to 100vh and measure that since that's what the scrolling is based on anyway and it's not affected by address bar showing/hiding.
				_div100vh.style.height = "100vh";
				_div100vh.style.position = "absolute";
				_refresh100vh();
				_rafBugFix();
				Observer.register(gsap);
				// isTouch is 0 if no touch, 1 if ONLY touch, and 2 if it can accommodate touch but also other types like mouse/pointer.
				ScrollTrigger.isTouch = Observer.isTouch;
				_fixIOSBug = Observer.isTouch && /(iPad|iPhone|iPod|Mac)/g.test(navigator.userAgent); // since 2017, iOS has had a bug that causes event.clientX/Y to be inaccurate when a scroll occurs, thus we must alternate ignoring every other touchmove event to work around it. See https://bugs.webkit.org/show_bug.cgi?id=181954 and https://codepen.io/GreenSock/pen/ExbrPNa/087cef197dc35445a0951e8935c41503
				_ignoreMobileResize = Observer.isTouch === 1;
				_addListener(_win, "wheel", _onScroll); // mostly for 3rd party smooth scrolling libraries.
				_root = [_win, _doc, _docEl, _body];
				if (gsap.matchMedia) {
					ScrollTrigger.matchMedia = vars => {
						let mm = gsap.matchMedia(),
							p;
						for (p in vars) {
							mm.add(p, vars[p]);
						}
						return mm;
					};
					gsap.addEventListener("matchMediaInit", () => { _recordScrollPositions(); _revertAll(); });
					gsap.addEventListener("matchMediaRevert", () => _revertRecorded());
					gsap.addEventListener("matchMedia", () => {
						_refreshAll(0, 1);
						_dispatch("matchMedia");
					});
					gsap.matchMedia().add("(orientation: portrait)", () => { // when orientation changes, we should take new base measurements for the ignoreMobileResize feature.
						_setBaseDimensions();
						return _setBaseDimensions;
					});
				} else {
					console.warn("Requires GSAP 3.11.0 or later");
				}
				_setBaseDimensions();
				_addListener(_doc, "scroll", _onScroll); // some browsers (like Chrome), the window stops dispatching scroll events on the window if you scroll really fast, but it's consistent on the document!
				let bodyHasStyle = _body.hasAttribute("style"),
					bodyStyle = _body.style,
					border = bodyStyle.borderTopStyle,
					AnimationProto = gsap.core.Animation.prototype,
					bounds, i;
				AnimationProto.revert || Object.defineProperty(AnimationProto, "revert", { value: function() { return this.time(-0.01, true); }}); // only for backwards compatibility (Animation.revert() was added after 3.10.4)
				bodyStyle.borderTopStyle = "solid"; // works around an issue where a margin of a child element could throw off the bounds of the _body, making it seem like there's a margin when there actually isn't. The border ensures that the bounds are accurate.
				bounds = _getBounds(_body);
				_vertical.m = Math.round(bounds.top + _vertical.sc()) || 0; // accommodate the offset of the <body> caused by margins and/or padding
				_horizontal.m = Math.round(bounds.left + _horizontal.sc()) || 0;
				border ? (bodyStyle.borderTopStyle = border) : bodyStyle.removeProperty("border-top-style");
				if (!bodyHasStyle) { // SSR frameworks like Next.js complain if this attribute gets added.
					_body.setAttribute("style", ""); // it's not enough to just removeAttribute() - we must first set it to empty, otherwise Next.js complains.
					_body.removeAttribute("style");
				}
				// TODO: (?) maybe move to leveraging the velocity mechanism in Observer and skip intervals.
				_syncInterval = setInterval(_sync, 250);
				gsap.delayedCall(0.5, () => _startup = 0);
				_addListener(_doc, "touchcancel", _passThrough); // some older Android devices intermittently stop dispatching "touchmove" events if we don't listen for "touchcancel" on the document.
				_addListener(_body, "touchstart", _passThrough); //works around Safari bug: https://gsap.com/forums/topic/21450-draggable-in-iframe-on-mobile-is-buggy/
				_multiListener(_addListener, _doc, "pointerdown,touchstart,mousedown", _pointerDownHandler);
				_multiListener(_addListener, _doc, "pointerup,touchend,mouseup", _pointerUpHandler);
				_transformProp = gsap.utils.checkPrefix("transform");
				_stateProps.push(_transformProp);
				_coreInitted = _getTime();
				_resizeDelay = gsap.delayedCall(0.2, _refreshAll).pause();
				_autoRefresh = [_doc, "visibilitychange", () => {
					let w = _win.innerWidth,
						h = _win.innerHeight;
					if (_doc.hidden) {
						_prevWidth = w;
						_prevHeight = h;
					} else if (_prevWidth !== w || _prevHeight !== h) {
						_onResize();
					}
				}, _doc, "DOMContentLoaded", _refreshAll, _win, "load", _refreshAll, _win, "resize", _onResize];
				_iterateAutoRefresh(_addListener);
				_triggers.forEach(trigger => trigger.enable(0, 1));
				for (i = 0; i < _scrollers.length; i+=3) {
					_wheelListener(_removeListener, _scrollers[i], _scrollers[i+1]);
					_wheelListener(_removeListener, _scrollers[i], _scrollers[i+2]);
				}
			} else if (_doc) {
				let onLoad = () => { ScrollTrigger.enable(); _doc.removeEventListener("DOMContentLoaded", onLoad); };
				_doc.addEventListener("DOMContentLoaded", onLoad);
			}
		}
	}

	static config(vars) {
		("limitCallbacks" in vars) && (_limitCallbacks = !!vars.limitCallbacks);
		let ms = vars.syncInterval;
		ms && clearInterval(_syncInterval) || ((_syncInterval = ms) && setInterval(_sync, ms));
		("ignoreMobileResize" in vars) && (_ignoreMobileResize = ScrollTrigger.isTouch === 1 && vars.ignoreMobileResize);
		if ("autoRefreshEvents" in vars) {
			_iterateAutoRefresh(_removeListener) || _iterateAutoRefresh(_addListener, vars.autoRefreshEvents || "none");
			_ignoreResize = (vars.autoRefreshEvents + "").indexOf("resize") === -1;
		}
	}

	static scrollerProxy(target, vars) {
		let t = _getTarget(target),
			i = _scrollers.indexOf(t),
			isViewport = _isViewport(t);
		if (~i) {
			_scrollers.splice(i, isViewport ? 6 : 2);
		}
		if (vars) {
			isViewport ? _proxies.unshift(_win, vars, _body, vars, _docEl, vars) : _proxies.unshift(t, vars);
		}
	}

	static clearMatchMedia(query) {
		_triggers.forEach(t => t._ctx && t._ctx.query === query && t._ctx.kill(true, true));
	}

	static isInViewport(element, ratio, horizontal) {
		let bounds = (_isString(element) ? _getTarget(element) : element).getBoundingClientRect(),
			offset = bounds[horizontal ? _width : _height] * ratio || 0;
		return horizontal ? bounds.right - offset > 0 && bounds.left + offset < _win.innerWidth : bounds.bottom - offset > 0 && bounds.top + offset < _win.innerHeight;
	}

	static positionInViewport(element, referencePoint, horizontal) {
		_isString(element) && (element = _getTarget(element));
		let bounds = element.getBoundingClientRect(),
			size = bounds[horizontal ? _width : _height],
			offset = referencePoint == null ? size / 2 : ((referencePoint in _keywords) ? _keywords[referencePoint] * size : ~referencePoint.indexOf("%") ? parseFloat(referencePoint) * size / 100 : parseFloat(referencePoint) || 0);
		return horizontal ? (bounds.left + offset) / _win.innerWidth : (bounds.top + offset) / _win.innerHeight;
	}

	static killAll(allowListeners) {
		_triggers.slice(0).forEach(t => t.vars.id !== "ScrollSmoother" && t.kill());
		if (allowListeners !== true) {
			let listeners = _listeners.killAll || [];
			_listeners = {};
			listeners.forEach(f => f());
		}
	}

}

ScrollTrigger.version = "3.15.0";
ScrollTrigger.saveStyles = targets => targets ? _toArray(targets).forEach(target => { // saved styles are recorded in a consecutive alternating Array, like [element, cssText, transform attribute, cache, matchMedia, ...]
	if (target && target.style) {
		let i = _savedStyles.indexOf(target);
		i >= 0 && _savedStyles.splice(i, 5);
		_savedStyles.push(target, target.style.cssText, target.getBBox && target.getAttribute("transform"), gsap.core.getCache(target), _context());
	}
}) : _savedStyles;
ScrollTrigger.revert = (soft, media) => _revertAll(!soft, media);
ScrollTrigger.create = (vars, animation) => new ScrollTrigger(vars, animation);
ScrollTrigger.refresh = safe => safe ? _onResize(true) : (_coreInitted || ScrollTrigger.register()) && _refreshAll(true);
ScrollTrigger.update = force => ++_scrollers.cache && _updateAll(force === true ? 2 : 0);
ScrollTrigger.clearScrollMemory = _clearScrollMemory;
ScrollTrigger.maxScroll = (element, horizontal) => _maxScroll(element, horizontal ? _horizontal : _vertical);
ScrollTrigger.getScrollFunc = (element, horizontal) => _getScrollFunc(_getTarget(element), horizontal ? _horizontal : _vertical);
ScrollTrigger.getById = id => _ids[id];
ScrollTrigger.getAll = () => _triggers.filter(t => t.vars.id !== "ScrollSmoother"); // it's common for people to ScrollTrigger.getAll(t => t.kill()) on page routes, for example, and we don't want it to ruin smooth scrolling by killing the main ScrollSmoother one.
ScrollTrigger.isScrolling = () => !!_lastScrollTime;
ScrollTrigger.snapDirectional = _snapDirectional;
ScrollTrigger.addEventListener = (type, callback) => {
	let a = _listeners[type] || (_listeners[type] = []);
	~a.indexOf(callback) || a.push(callback);
};
ScrollTrigger.removeEventListener = (type, callback) => {
	let a = _listeners[type],
		i = a && a.indexOf(callback);
	i >= 0 && a.splice(i, 1);
};
ScrollTrigger.batch = (targets, vars) => {
	let result = [],
		varsCopy = {},
		interval = vars.interval || 0.016,
		batchMax = vars.batchMax || 1e9,
		proxyCallback = (type, callback) => {
			let elements = [],
				triggers = [],
				delay = gsap.delayedCall(interval, () => {callback(elements, triggers); elements = []; triggers = [];}).pause();
			return self => {
				elements.length || delay.restart(true);
				elements.push(self.trigger);
				triggers.push(self);
				batchMax <= elements.length && delay.progress(1);
			};
		},
		p;
	for (p in vars) {
		varsCopy[p] = (p.substr(0, 2) === "on" && _isFunction(vars[p]) && p !== "onRefreshInit") ? proxyCallback(p, vars[p]) : vars[p];
	}
	if (_isFunction(batchMax)) {
		batchMax = batchMax();
		_addListener(ScrollTrigger, "refresh", () => batchMax = vars.batchMax());
	}
	_toArray(targets).forEach(target => {
		let config = {};
		for (p in varsCopy) {
			config[p] = varsCopy[p];
		}
		config.trigger = target;
		result.push(ScrollTrigger.create(config));
	});
	return result;
}


// to reduce file size. clamps the scroll and also returns a duration multiplier so that if the scroll gets chopped shorter, the duration gets curtailed as well (otherwise if you're very close to the top of the page, for example, and swipe up really fast, it'll suddenly slow down and take a long time to reach the top).
let _clampScrollAndGetDurationMultiplier = (scrollFunc, current, end, max) => {
		current > max ? scrollFunc(max) : current < 0 && scrollFunc(0);
		return end > max ? (max - current) / (end - current) : end < 0 ? current / (current - end) : 1;
	},
	_allowNativePanning = (target, direction) => {
		if (direction === true) {
			target.style.removeProperty("touch-action");
		} else {
			target.style.touchAction = direction === true ? "auto" : direction ? "pan-" + direction + (Observer.isTouch ? " pinch-zoom" : "") : "none"; // note: Firefox doesn't support it pinch-zoom properly, at least in addition to a pan-x or pan-y.
		}
		target === _docEl && _allowNativePanning(_body, direction);
	},
	_overflow = {auto: 1, scroll: 1},
	_nestedScroll = ({event, target, axis}) => {
		let node = (event.changedTouches ? event.changedTouches[0] : event).target,
			cache = node._gsap || gsap.core.getCache(node),
			time = _getTime(), cs;
		if (!cache._isScrollT || time - cache._isScrollT > 2000) { // cache for 2 seconds to improve performance.
			while (node && node !== _body && ((node.scrollHeight <= node.clientHeight && node.scrollWidth <= node.clientWidth) || !(_overflow[(cs = _getComputedStyle(node)).overflowY] || _overflow[cs.overflowX]))) node = node.parentNode;
			cache._isScroll = node && node !== target && !_isViewport(node) && (_overflow[(cs = _getComputedStyle(node)).overflowY] || _overflow[cs.overflowX]);
			cache._isScrollT = time;
		}
		if (cache._isScroll || axis === "x") {
			event.stopPropagation();
			event._gsapAllow = true;
		}
	},
	// capture events on scrollable elements INSIDE the <body> and allow those by calling stopPropagation() when we find a scrollable ancestor
	_inputObserver = (target, type, inputs, nested) => Observer.create({
		target: target,
		capture: true,
		debounce: false,
		lockAxis: true,
		type: type,
		onWheel: (nested = nested && _nestedScroll),
		onPress: nested,
		onDrag: nested,
		onScroll: nested,
		onEnable: () => inputs && _addListener(_doc, Observer.eventTypes[0], _captureInputs, false, true),
		onDisable: () => _removeListener(_doc, Observer.eventTypes[0], _captureInputs, true)
	}),
	_inputExp = /(input|label|select|textarea)/i,
	_inputIsFocused,
	_captureInputs = e => {
		let isInput = _inputExp.test(e.target.tagName);
		if (isInput || _inputIsFocused) {
			e._gsapAllow = true;
			_inputIsFocused = isInput;
		}
	},
	_getScrollNormalizer = vars => {
		_isObject(vars) || (vars = {});
		vars.preventDefault = vars.isNormalizer = vars.allowClicks = true;
		vars.type || (vars.type = "wheel,touch");
		vars.debounce = !!vars.debounce;
		vars.id = vars.id || "normalizer";
		let {normalizeScrollX, momentum, allowNestedScroll, onRelease} = vars,
			self, maxY,
			target = _getTarget(vars.target) || _docEl,
			smoother = gsap.core.globals().ScrollSmoother,
			smootherInstance = smoother && smoother.get(),
			content = _fixIOSBug && ((vars.content && _getTarget(vars.content)) || (smootherInstance && vars.content !== false && !smootherInstance.smooth() && smootherInstance.content())),
			scrollFuncY = _getScrollFunc(target, _vertical),
			scrollFuncX = _getScrollFunc(target, _horizontal),
			scale = 1,
			initialScale = (Observer.isTouch && _win.visualViewport ? _win.visualViewport.scale * _win.visualViewport.width : _win.outerWidth) / _win.innerWidth,
			wheelRefresh = 0,
			resolveMomentumDuration = _isFunction(momentum) ? () => momentum(self) : () => momentum || 2.8,
			lastRefreshID, skipTouchMove,
			inputObserver = _inputObserver(target, vars.type, true, allowNestedScroll),
			resumeTouchMove = () => skipTouchMove = false,
			scrollClampX = _passThrough,
			scrollClampY = _passThrough,
			updateClamps = () => {
				maxY = _maxScroll(target, _vertical);
				scrollClampY = _clamp(_fixIOSBug ? 1 : 0, maxY);
				normalizeScrollX && (scrollClampX = _clamp(0, _maxScroll(target, _horizontal)));
				lastRefreshID = _refreshID;
			},
			removeContentOffset = () => {
				content._gsap.y = _round(parseFloat(content._gsap.y) + scrollFuncY.offset) + "px";
				content.style.transform = "matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, " + parseFloat(content._gsap.y) + ", 0, 1)";
				scrollFuncY.offset = scrollFuncY.cacheID = 0;
			},
			ignoreDrag = () => {
				if (skipTouchMove) {
					requestAnimationFrame(resumeTouchMove);
					let offset = _round(self.deltaY / 2),
						scroll = scrollClampY(scrollFuncY.v - offset);
					if (content && scroll !== scrollFuncY.v + scrollFuncY.offset) {
						scrollFuncY.offset = scroll - scrollFuncY.v;
						let y = _round((parseFloat(content && content._gsap.y) || 0) - scrollFuncY.offset);
						content.style.transform = "matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, " + y + ", 0, 1)";
						content._gsap.y = y + "px";
						scrollFuncY.cacheID = _scrollers.cache;
						_updateAll();
					}
					return true;
				}
				scrollFuncY.offset && removeContentOffset();
				skipTouchMove = true;
			},
			tween, startScrollX, startScrollY, onStopDelayedCall,
			onResize = () => { // if the window resizes, like on an iPhone which Apple FORCES the address bar to show/hide even if we event.preventDefault(), it may be scrolling too far now that the address bar is showing, so we must dynamically adjust the momentum tween.
				updateClamps();
				if (tween.isActive() && tween.vars.scrollY > maxY) {
					scrollFuncY() > maxY ? tween.progress(1) && scrollFuncY(maxY) : tween.resetTo("scrollY", maxY);
				}
			};
		content && gsap.set(content, {y: "+=0"}); // to ensure there's a cache (element._gsap)
		vars.ignoreCheck = e => (_fixIOSBug && e.type === "touchmove" && ignoreDrag(e)) || (scale > 1.05 && e.type !== "touchstart") || self.isGesturing || (e.touches && e.touches.length > 1);
		vars.onPress = () => {
			skipTouchMove = false;
			let prevScale = scale;
			scale = _round(((_win.visualViewport && _win.visualViewport.scale) || 1) / initialScale);
			tween.pause();
			prevScale !== scale && _allowNativePanning(target, scale > 1.01 ? true : normalizeScrollX ? false : "x");
			startScrollX = scrollFuncX();
			startScrollY = scrollFuncY();
			updateClamps();
			lastRefreshID = _refreshID;
		}
		vars.onRelease = vars.onGestureStart = (self, wasDragging) => {
			scrollFuncY.offset && removeContentOffset();
			if (!wasDragging) {
				onStopDelayedCall.restart(true);
			} else {
				_scrollers.cache++; // make sure we're pulling the non-cached value
				// alternate algorithm: durX = Math.min(6, Math.abs(self.velocityX / 800)),	dur = Math.max(durX, Math.min(6, Math.abs(self.velocityY / 800))); dur = dur * (0.4 + (1 - _power4In(dur / 6)) * 0.6)) * (momentumSpeed || 1)
				let dur = resolveMomentumDuration(),
					currentScroll, endScroll;
				if (normalizeScrollX) {
					currentScroll = scrollFuncX();
					endScroll = currentScroll + (dur * 0.05 * -self.velocityX) / 0.227; // the constant .227 is from power4(0.05). velocity is inverted because scrolling goes in the opposite direction.
					dur *= _clampScrollAndGetDurationMultiplier(scrollFuncX, currentScroll, endScroll, _maxScroll(target, _horizontal));
					tween.vars.scrollX = scrollClampX(endScroll);
				}
				currentScroll = scrollFuncY();
				endScroll = currentScroll + (dur * 0.05 * -self.velocityY) / 0.227; // the constant .227 is from power4(0.05)
				dur *= _clampScrollAndGetDurationMultiplier(scrollFuncY, currentScroll, endScroll, _maxScroll(target, _vertical));
				tween.vars.scrollY = scrollClampY(endScroll);
				tween.invalidate().duration(dur).play(0.01);
				if (_fixIOSBug && tween.vars.scrollY >= maxY || currentScroll >= maxY-1) { // iOS bug: it'll show the address bar but NOT fire the window "resize" event until the animation is done but we must protect against overshoot so we leverage an onUpdate to do so.
					gsap.to({}, {onUpdate: onResize, duration: dur});
				}
			}
			onRelease && onRelease(self);
		};
		vars.onWheel = () => {
			tween._ts && tween.pause();
			if (_getTime() - wheelRefresh > 1000) { // after 1 second, refresh the clamps otherwise that'll only happen when ScrollTrigger.refresh() is called or for touch-scrolling.
				lastRefreshID = 0;
				wheelRefresh = _getTime();
			}
		};
		vars.onChange = (self, dx, dy, xArray, yArray) => {
			_refreshID !== lastRefreshID && updateClamps();
			dx && normalizeScrollX && scrollFuncX(scrollClampX(xArray[2] === dx ? startScrollX + (self.startX - self.x) : scrollFuncX() + dx - xArray[1])); // for more precision, we track pointer/touch movement from the start, otherwise it'll drift.
			if (dy) {
				scrollFuncY.offset && removeContentOffset();
				let isTouch = yArray[2] === dy,
					y = isTouch ? startScrollY + self.startY - self.y : scrollFuncY() + dy - yArray[1],
					yClamped = scrollClampY(y);
				isTouch && y !== yClamped && (startScrollY += yClamped - y);
				scrollFuncY(yClamped);
			}
			(dy || dx) && _updateAll();
		};
		vars.onEnable = () => {
			_allowNativePanning(target, normalizeScrollX ? false : "x");
			ScrollTrigger.addEventListener("refresh", onResize);
			_addListener(_win, "resize", onResize);
			if (scrollFuncY.smooth) {
				scrollFuncY.target.style.scrollBehavior = "auto";
				scrollFuncY.smooth = scrollFuncX.smooth = false;
			}
			inputObserver.enable();
		};
		vars.onDisable = () => {
			_allowNativePanning(target, true);
			_removeListener(_win, "resize", onResize);
			ScrollTrigger.removeEventListener("refresh", onResize);
			inputObserver.kill();
		};
		vars.lockAxis = vars.lockAxis !== false;
		self = new Observer(vars);
		self.iOS = _fixIOSBug; // used in the Observer getCachedScroll() function to work around an iOS bug that wreaks havoc with TouchEvent.clientY if we allow scroll to go all the way back to 0.
		_fixIOSBug && !scrollFuncY() && scrollFuncY(1); // iOS bug causes event.clientY values to freak out (wildly inaccurate) if the scroll position is exactly 0.
		_fixIOSBug && gsap.ticker.add(_passThrough); // prevent the ticker from sleeping
		onStopDelayedCall = self._dc;
		tween = gsap.to(self, {ease: "power4", paused: true, inherit: false, scrollX: normalizeScrollX ? "+=0.1" : "+=0", scrollY: "+=0.1", modifiers: {scrollY: _interruptionTracker(scrollFuncY, scrollFuncY(), () => tween.pause())	}, onUpdate: _updateAll, onComplete: onStopDelayedCall.vars.onComplete}); // we need the modifier to sense if the scroll position is altered outside of the momentum tween (like with a scrollTo tween) so we can pause() it to prevent conflicts.
		return self;
	};

ScrollTrigger.sort = func => {
	if (_isFunction(func)) {
		return _triggers.sort(func);
	}
	let scroll = _win.pageYOffset || 0;
	ScrollTrigger.getAll().forEach(t => t._sortY = t.trigger ? scroll + t.trigger.getBoundingClientRect().top : t.start + _win.innerHeight);
	return _triggers.sort(func || ((a, b) => (a.vars.refreshPriority || 0) * -1e6 + (a.vars.containerAnimation ? 1e6 : a._sortY) - ((b.vars.containerAnimation ? 1e6 : b._sortY) + (b.vars.refreshPriority || 0) * -1e6))); // anything with a containerAnimation should refresh last.
}
ScrollTrigger.observe = vars => new Observer(vars);
ScrollTrigger.normalizeScroll = vars => {
	if (typeof(vars) === "undefined") {
		return _normalizer;
	}
	if (vars === true && _normalizer) {
		return _normalizer.enable();
	}
	if (vars === false) {
		_normalizer && _normalizer.kill();
		_normalizer = vars;
		return;
	}
	let normalizer = vars instanceof Observer ? vars : _getScrollNormalizer(vars);
	_normalizer && _normalizer.target === normalizer.target && _normalizer.kill();
	_isViewport(normalizer.target) && (_normalizer = normalizer);
	return normalizer;
};


ScrollTrigger.core = { // smaller file size way to leverage in ScrollSmoother and Observer
	_getVelocityProp,
	_inputObserver,
	_scrollers,
	_proxies,
	bridge: {
		// when normalizeScroll sets the scroll position (ss = setScroll)
		ss: () => {
			_lastScrollTime || _dispatch("scrollStart");
			_lastScrollTime = _getTime();
		},
		// a way to get the _refreshing value in Observer
		ref: () => _refreshing
	}
};

_getGSAP() && gsap.registerPlugin(ScrollTrigger);

export { ScrollTrigger as default };
```

## 📄 File: `CustomWiggle.js`
```javascript
/*!
 * CustomWiggle 3.15.0
 * https://gsap.com
 *
 * @license Copyright 2008-2026, GreenSock. All rights reserved.
 * Subject to the terms at https://gsap.com/standard-license
 * @author: Jack Doyle, jack@greensock.com
*/
/* eslint-disable */

let gsap, _coreInitted, createCustomEase,
	_getGSAP = () => gsap || (typeof(window) !== "undefined" && (gsap = window.gsap) && gsap.registerPlugin && gsap),
	_eases = {
		easeOut: "M0,1,C0.7,1,0.6,0,1,0",
		easeInOut: "M0,0,C0.1,0,0.24,1,0.444,1,0.644,1,0.6,0,1,0",
		anticipate: "M0,0,C0,0.222,0.024,0.386,0,0.4,0.18,0.455,0.65,0.646,0.7,0.67,0.9,0.76,1,0.846,1,1",
		uniform: "M0,0,C0,0.95,0,1,0,1,0,1,1,1,1,1,1,1,1,0,1,0"
	},
	_linearEase = p => p,
	_initCore = required => {
		if (!_coreInitted) {
			gsap = _getGSAP();
			createCustomEase = gsap && gsap.parseEase("_CE");
			if (createCustomEase) {
				for (let p in _eases) {
					_eases[p] = createCustomEase("", _eases[p]);
				}
				_coreInitted = 1;
				_create("wiggle").config = vars => typeof(vars) === "object" ? _create("", vars) : _create("wiggle(" + vars + ")", {wiggles:+vars});
			} else {
				required && console.warn("Please gsap.registerPlugin(CustomEase, CustomWiggle)");
			}
		}
	},
	_parseEase = (ease, invertNonCustomEases) => {
		if (typeof(ease) !== "function") {
			ease = gsap.parseEase(ease) || createCustomEase("", ease);
		}
		return (ease.custom || !invertNonCustomEases) ? ease : p => 1 - ease(p);
	},
	_bonusValidated = 1, //<name>CustomWiggle</name>
	_create = (id, vars) => {
		if (!_coreInitted) {
			_initCore(1);
		}
		vars = vars || {};
		let wiggles = (vars.wiggles || 10) | 0,
			inc = 1 / wiggles,
			x = inc / 2,
			anticipate = (vars.type === "anticipate"),
			yEase = _eases[vars.type] || _eases.easeOut,
			xEase = _linearEase,
			rnd = 1000,
			nextX, nextY, angle, handleX, handleY, easedX, y, path, i;
		if (_bonusValidated) {
			if (anticipate) { //the anticipate ease is actually applied on the x-axis (timing) and uses easeOut for amplitude.
				xEase = yEase;
				yEase = _eases.easeOut;
			}
			if (vars.timingEase) {
				xEase = _parseEase(vars.timingEase);
			}
			if (vars.amplitudeEase) {
				yEase = _parseEase(vars.amplitudeEase, true);
			}
			easedX = xEase(x);
			y = anticipate ? -yEase(x) : yEase(x);
			path = [0, 0, easedX / 4, 0, easedX / 2, y, easedX, y];

			if (vars.type === "random") { //if we just select random values on the y-axis and plug them into the "normal" algorithm, since the control points are always straight horizontal, it creates a bit of a slowdown at each anchor which just didn't seem as desirable, so we switched to an algorithm that bends the control points to be more in line with their context.
				path.length = 4;
				nextX = xEase(inc);
				nextY = Math.random() * 2 - 1;
				for (i = 2; i < wiggles; i++) {
					x = nextX;
					y = nextY;
					nextX = xEase(inc * i);
					nextY = Math.random() * 2 - 1;
					angle = Math.atan2(nextY - path[path.length - 3], nextX - path[path.length - 4]);
					handleX = Math.cos(angle) * inc;
					handleY = Math.sin(angle) * inc;
					path.push(x - handleX, y - handleY, x, y, x + handleX, y + handleY);
				}
				path.push(nextX, 0, 1, 0);
			} else {
				for (i = 1; i < wiggles; i++) {
					path.push(xEase(x + inc / 2), y);
					x += inc;
					y = ((y > 0) ? -1 : 1) * (yEase(i * inc));
					easedX = xEase(x);
					path.push(xEase(x - inc / 2), y, easedX, y);
				}
				path.push(xEase(x + inc / 4), y, xEase(x + inc / 4), 0, 1, 0);
			}
			i = path.length;
			while (--i > -1) {
				path[i] = ~~(path[i] * rnd) / rnd; //round values to avoid odd strings for super tiny values
			}
			path[2] = "C" + path[2];
			return createCustomEase(id, "M" + path.join(","));
		}
	};

export class CustomWiggle {

	constructor(id, vars) {
		this.ease = _create(id, vars);
	}

	static create(id, vars) {
		return _create(id, vars);
	}

	static register(core) {
		gsap = core;
		_initCore();
	}

}

_getGSAP() && gsap.registerPlugin(CustomWiggle);

CustomWiggle.version = "3.15.0";

export { CustomWiggle as default };
```

## 📄 File: `Flip.js`
```javascript
/*!
 * Flip 3.15.0
 * https://gsap.com
 *
 * @license Copyright 2008-2026, GreenSock. All rights reserved.
 * Subject to the terms at https://gsap.com/standard-license
 * @author: Jack Doyle, jack@greensock.com
*/
/* eslint-disable */

import { getGlobalMatrix, _getDocScrollTop, _getDocScrollLeft, Matrix2D, _setDoc, _getCTM } from "./utils/matrix.js";

let _id = 1,
	_toArray, gsap, _batch, _batchAction, _body, _closestTenth, _getStyleSaver,
	_forEachBatch = (batch, name) => batch.actions.forEach(a => a.vars[name] && a.vars[name](a)),
	_batchLookup = {},
	_RAD2DEG = 180 / Math.PI,
	_DEG2RAD = Math.PI / 180,
	_emptyObj = {},
	_dashedNameLookup = {},
	_memoizedRemoveProps = {},
	_listToArray = list => typeof(list) === "string" ? list.split(" ").join("").split(",") : list, // removes extra spaces contaminating the names, returns an Array.
	_callbacks = _listToArray("onStart,onUpdate,onComplete,onReverseComplete,onInterrupt"),
	_removeProps = _listToArray("transform,transformOrigin,width,height,position,top,left,opacity,zIndex,maxWidth,maxHeight,minWidth,minHeight"),
	_getEl = target => _toArray(target)[0] || console.warn("Element not found:", target),
	_round = value => Math.round(value * 10000) / 10000 || 0,
	_toggleClass = (targets, className, action) => targets.forEach(el => el.classList[action](className)),
	_reserved = {zIndex:1, kill:1, simple:1, spin:1, clearProps:1, targets:1, toggleClass:1, onComplete:1, onUpdate:1, onInterrupt:1, onStart:1, delay:1, repeat:1, repeatDelay:1, yoyo:1, scale:1, fade:1, absolute:1, props:1, onEnter:1, onLeave:1, custom:1, paused:1, nested:1, prune:1, absoluteOnLeave: 1},
	_fitReserved = {zIndex:1, simple:1, clearProps:1, scale:1, absolute:1, fitChild:1, getVars:1, props:1},
	_camelToDashed = p => p.replace(/([A-Z])/g, "-$1").toLowerCase(),
	_copy = (obj, exclude) => {
		let result = {}, p;
		for (p in obj) {
			exclude[p] || (result[p] = obj[p]);
		}
		return result;
	},
	_memoizedProps = {},
	_memoizeProps = props => {
		let p = _memoizedProps[props] = _listToArray(props);
		_memoizedRemoveProps[props] = p.concat(_removeProps);
		return p;
	},
	_getInverseGlobalMatrix = el => { // integrates caching for improved performance
		let cache = el._gsap || gsap.core.getCache(el);
		if (cache.gmCache === gsap.ticker.frame) {
			return cache.gMatrix;
		}
		cache.gmCache = gsap.ticker.frame;
		return (cache.gMatrix = getGlobalMatrix(el, true, false, true));
	},
	_getDOMDepth = (el, invert, level = 0) => { // In invert is true, the sibling depth is increments of 1, and parent/nesting depth is increments of 1000. This lets us order elements in an Array to reflect document flow.
		let parent = el.parentNode,
			inc = 1000 * (10 ** level) * (invert ? -1 : 1),
			l = invert ? -inc * 900 : 0;
		while (el) {
			l += inc;
			el = el.previousSibling;
		}
		return parent ? l + _getDOMDepth(parent, invert, level + 1) : l;
	},
	_orderByDOMDepth = (comps, invert, isElStates) => {
		comps.forEach(comp => comp.d = _getDOMDepth(isElStates ? comp.element : comp.t, invert));
		comps.sort((c1, c2) => c1.d - c2.d);
		return comps;
	},
	_recordInlineStyles = (elState, props) => { // records the current inline CSS properties into an Array in alternating name/value pairs that's stored in a "css" property on the state object so that we can revert later.
		let style = elState.element.style,
			a = elState.css = elState.css || [],
			i = props.length,
			p, v;
		while (i--) {
			p = props[i];
			v = style[p] || style.getPropertyValue(p);
			a.push(v ? p : _dashedNameLookup[p] || (_dashedNameLookup[p] = _camelToDashed(p)), v);
		}
		return style;
	},
	_applyInlineStyles = state => {
		let css = state.css,
			style = state.element.style,
			i = 0;
		state.cache.uncache = 1;
		for (; i < css.length; i+=2) {
			css[i+1] ? (style[css[i]] = css[i+1]) : style.removeProperty(css[i]);
		}
		if (!css[css.indexOf("transform")+1] && style.translate) { // CSSPlugin adds scale, translate, and rotate inline CSS as "none" in order to keep CSS rules from contaminating transforms.
			style.removeProperty("translate");
			style.removeProperty("scale");
			style.removeProperty("rotate");
		}
	},
	_setFinalStates = (comps, onlyTransforms) => {
		comps.forEach(c => c.a.cache.uncache = 1);
		onlyTransforms || comps.finalStates.forEach(_applyInlineStyles);
	},
	_absoluteProps = "paddingTop,paddingRight,paddingBottom,paddingLeft,gridArea,transition".split(","), // properties that we must record just
	_makeAbsolute = (elState, fallbackNode, ignoreBatch) => {
		let { element, width, height, uncache, getProp } = elState,
			style = element.style,
			i = 4,
			result, displayIsNone, cs;
		(typeof(fallbackNode) !== "object") && (fallbackNode = elState);
		if (_batch && ignoreBatch !== 1) {
			_batch._abs.push({t: element, b: elState, a: elState, sd: 0});
			_batch._final.push(() => (elState.cache.uncache = 1) && _applyInlineStyles(elState));
			return element;
		}
		displayIsNone = getProp("display") === "none";

		if (!elState.isVisible || displayIsNone) {
			displayIsNone && (_recordInlineStyles(elState, ["display"]).display = fallbackNode.display);
			elState.matrix = fallbackNode.matrix;
			elState.width = width = elState.width || fallbackNode.width;
			elState.height = height = elState.height || fallbackNode.height;
		}

		_recordInlineStyles(elState, _absoluteProps);
		cs = window.getComputedStyle(element);
		while (i--) {
			style[_absoluteProps[i]] = cs[_absoluteProps[i]]; // record paddings as px-based because if removed from grid, percentage-based ones could be altered.
		}
		style.gridArea = "1 / 1 / 1 / 1";
		style.transition = "none";

		style.position = "absolute";
		style.width = width + "px";
		style.height = height + "px";
		style.top || (style.top = "0px");
		style.left || (style.left = "0px");
		if (uncache) {
			result = new ElementState(element);
		} else { // better performance
			result = _copy(elState, _emptyObj);
			result.position = "absolute";
			if (elState.simple) {
				let bounds = element.getBoundingClientRect();
				result.matrix = new Matrix2D(1, 0, 0, 1, bounds.left + _getDocScrollLeft(), bounds.top + _getDocScrollTop());
			} else {
				result.matrix = getGlobalMatrix(element, false, false, true);
			}
		}
		result = _fit(result, elState, true);
		elState.x = _closestTenth(result.x, 0.01);
		elState.y = _closestTenth(result.y, 0.01);
		return element;
	},
	_filterComps = (comps, targets) => {
		if (targets !== true) {
			targets = _toArray(targets);
			comps = comps.filter(c => {
				if (targets.indexOf((c.sd < 0 ? c.b : c.a).element) !== -1) {
				    return true;
				} else {
					c.t._gsap.renderTransform(1); // we must force transforms to render on anything that isn't being made position: absolute, otherwise the absolute position happens and then when animation begins it applies transforms which can create a new stacking context, throwing off positioning!
					if (c.b.isVisible) {
						c.t.style.width = c.b.width + "px"; // otherwise things can collapse when contents are made position: absolute.
						c.t.style.height = c.b.height + "px";
					}
				}
			});
		}
		return comps;
	},
	_makeCompsAbsolute = comps => _orderByDOMDepth(comps, true).forEach(c => (c.a.isVisible || c.b.isVisible) && _makeAbsolute(c.sd < 0 ? c.b : c.a, c.b, 1)),
	_findElStateInState = (state, other) => (other && state.idLookup[_parseElementState(other).id]) || state.elementStates[0],
	_parseElementState = (elOrNode, props, simple, other) => elOrNode instanceof ElementState ? elOrNode : elOrNode instanceof FlipState ? _findElStateInState(elOrNode, other) : new ElementState(typeof(elOrNode) === "string" ? _getEl(elOrNode) || console.warn(elOrNode + " not found") : elOrNode, props, simple),
	_recordProps = (elState, props) => {
		let getProp = gsap.getProperty(elState.element, null, "native"),
			obj = elState.props = {},
			i = props.length;
		while (i--) {
			obj[props[i]] = (getProp(props[i]) + "").trim();
		}
		obj.zIndex && (obj.zIndex = parseFloat(obj.zIndex) || 0);
		return elState;
	},
	_applyProps = (element, props) => {
		let style = element.style || element, // could pass in a vars object.
			p;
		for (p in props) {
			style[p] = props[p];
		}
	},
	_getID = el => {
		let id = el.getAttribute("data-flip-id");
		id || el.setAttribute("data-flip-id", (id = "auto-" + _id++));
		return id;
	},
	_elementsFromElementStates = elStates => elStates.map(elState => elState.element),
	_handleCallback = (callback, elStates, tl) => callback && elStates.length && tl.add(callback(_elementsFromElementStates(elStates), tl, new FlipState(elStates, 0, true)), 0),

	_fit = (fromState, toState, scale, applyProps, fitChild, vars) => {
		let { element, cache, parent, x, y } = fromState,
			{ width, height, scaleX, scaleY, rotation, bounds } = toState,
			styles = vars && _getStyleSaver && _getStyleSaver(element, "transform,width,height"), // requires at least 3.11.5
			dimensionState = fromState,
			{e, f} = toState.matrix,
			deep = fromState.bounds.width !== bounds.width || fromState.bounds.height !== bounds.height || fromState.scaleX !== scaleX || fromState.scaleY !== scaleY || fromState.rotation !== rotation,
			simple = !deep && fromState.simple && toState.simple && !fitChild,
			skewX, fromPoint, toPoint, getProp, parentMatrix, matrix, bbox;
		if (simple || !parent) {
			scaleX = scaleY = 1;
			rotation = skewX = 0;
		} else {
			parentMatrix = _getInverseGlobalMatrix(parent);
			matrix = parentMatrix.clone().multiply(toState.ctm ? toState.matrix.clone().multiply(toState.ctm) : toState.matrix); // root SVG elements have a ctm that we must factor out (for example, viewBox:"0 0 94 94" with a width of 200px would scale the internals by 2.127 but when we're matching the size of the root <svg> element itself, that scaling shouldn't factor in!)
			rotation = _round(Math.atan2(matrix.b, matrix.a) * _RAD2DEG);
			skewX = _round(Math.atan2(matrix.c, matrix.d) * _RAD2DEG + rotation) % 360; // in very rare cases, minor rounding might end up with 360 which should be 0.
			scaleX = Math.sqrt(matrix.a ** 2 + matrix.b ** 2);
			scaleY = Math.sqrt(matrix.c ** 2 + matrix.d ** 2) * Math.cos(skewX * _DEG2RAD);
			if (fitChild) {
				fitChild = _toArray(fitChild)[0];
				getProp = gsap.getProperty(fitChild);
				bbox = fitChild.getBBox && typeof(fitChild.getBBox) === "function" && fitChild.getBBox();
				dimensionState = {scaleX: getProp("scaleX"), scaleY: getProp("scaleY"), width: bbox ? bbox.width : Math.ceil(parseFloat(getProp("width", "px"))), height: bbox ? bbox.height : parseFloat(getProp("height", "px")) };
			}
			cache.rotation = rotation + "deg";
			cache.skewX = skewX + "deg";
		}
		if (scale) {
			scaleX *= width === dimensionState.width || !dimensionState.width ? 1 : width / dimensionState.width; // note if widths are both 0, we should make scaleX 1 - some elements have box-sizing that incorporates padding, etc. and we don't want it to collapse in that case.
			scaleY *= height === dimensionState.height || !dimensionState.height ? 1 : height / dimensionState.height;
			cache.scaleX = scaleX;
			cache.scaleY = scaleY;
		} else {
			width = _closestTenth(width * scaleX / dimensionState.scaleX, 0);
			height = _closestTenth(height * scaleY / dimensionState.scaleY, 0);
			element.style.width = width + "px";
			element.style.height = height + "px";
		}
		// if (fromState.isFixed) { // commented out because it's now taken care of in getGlobalMatrix() with a flag at the end.
		// 	e -= _getDocScrollLeft();
		// 	f -= _getDocScrollTop();
		// }
		applyProps && _applyProps(element, toState.props);
		if (simple || !parent) {
			x += e - fromState.matrix.e;
			y += f - fromState.matrix.f;
		} else if (deep || parent !== toState.parent) {
			cache.x = x + "px";
			cache.y = y + "px";
			cache.renderTransform(1, cache);
			matrix = getGlobalMatrix(fitChild || element, false, false, true);
			fromPoint = parentMatrix.apply({x: matrix.e, y: matrix.f});
			toPoint = parentMatrix.apply({x: e, y: f});
			x += toPoint.x - fromPoint.x;
			y += toPoint.y - fromPoint.y;
		} else { // use a faster/cheaper algorithm if we're just moving x/y
			parentMatrix.e = parentMatrix.f = 0;
			toPoint = parentMatrix.apply({x: e - fromState.matrix.e, y: f - fromState.matrix.f});
			x += toPoint.x;
			y += toPoint.y;
		}
		x = _closestTenth(x, 0.02);
		y = _closestTenth(y, 0.02);
		if (vars && !(vars instanceof ElementState)) { // revert
			styles && styles.revert();
		} else { // or apply the transform immediately
			cache.x = x + "px";
			cache.y = y + "px";
			cache.renderTransform(1, cache);
		}
		if (vars) {
			vars.x = x;
			vars.y = y;
			vars.rotation = rotation;
			vars.skewX = skewX;
			if (scale) {
				vars.scaleX = scaleX;
				vars.scaleY = scaleY;
			} else {
				vars.width = width;
				vars.height = height;
			}
		}
		return vars || cache;
	},

	_parseState = (targetsOrState, vars) => targetsOrState instanceof FlipState ? targetsOrState : new FlipState(targetsOrState, vars),
	_getChangingElState = (toState, fromState, id) => {
		let to1 = toState.idLookup[id],
			to2 = toState.alt[id];
		return to2.isVisible && (!(fromState.getElementState(to2.element) || to2).isVisible || !to1.isVisible) ? to2 : to1;
	},
	_bodyMetrics = [], _bodyProps = "width,height,overflowX,overflowY".split(","), _bodyLocked,
	_lockBodyScroll = lock => { // if there's no scrollbar, we should lock that so that measurements don't get affected by temporary repositioning, like if something is centered in the window.
		if (lock !== _bodyLocked) {
			let s = _body.style,
				w = _body.clientWidth === window.outerWidth,
				h = _body.clientHeight === window.outerHeight,
				i = 4;
			if (lock && (w || h)) {
				while (i--) {
					_bodyMetrics[i] = s[_bodyProps[i]];
				}
				if (w) {
					s.width = _body.clientWidth + "px";
					s.overflowY = "hidden";
				}
				if (h) {
					s.height = _body.clientHeight + "px";
					s.overflowX = "hidden";
				}
				_bodyLocked= lock;
			} else if (_bodyLocked) {
				while (i--) {
					_bodyMetrics[i] ? (s[_bodyProps[i]] = _bodyMetrics[i]) : s.removeProperty(_camelToDashed(_bodyProps[i]));
				}
				_bodyLocked = lock;
			}
		}
	},
	_revertTempStyles = (temps, stateIndex) => { // in _fromTo(), we store the inline styles temporarily when nested is true, and the Array is like [element, styles1, styles2, element, styles1, styles2, ...] where styles1 is one state and styles2 is another state (the element.getAttribute("style")).
		for (let i = 0; i < temps.length; i+=3) {
			gsap.set(temps[i], {clearProps: true}); // to clear cached transforms too
			temps[i].setAttribute("style", temps[i+stateIndex]);
			temps[i]._gsap.gmCache = -1; // bust the globalMatrix cache
		}
	},

	_fromTo = (fromState, toState, vars, relative) => { // relative is -1 if "from()", and 1 if "to()"
		(fromState instanceof FlipState && toState instanceof FlipState) || console.warn("Not a valid state object.");
		vars = vars || {};
		let { clearProps, onEnter, onLeave, absolute, absoluteOnLeave, custom, delay, paused, repeat, repeatDelay, yoyo, toggleClass, nested, zIndex, scale, fade, stagger, spin, prune } = vars,
			props = ("props" in vars ? vars : fromState).props,
			tweenVars = _copy(vars, _reserved),
			animation = gsap.timeline({ delay, paused, repeat, repeatDelay, yoyo, data: "isFlip" }),
			remainingProps = tweenVars,
			entering = [],
			leaving = [],
			comps = [],
			swapOutTargets = [],
			spinNum = spin === true ? 1 : spin || 0,
			spinFunc = typeof(spin) === "function" ? spin : () => spinNum,
			interrupted = fromState.interrupted || toState.interrupted,
			addFunc = animation[relative !== 1 ? "to" : "from"],
			v, p, endTime, i, el, comp, state, targets, finalStates, fromNode, toNode, run, a, b;
		//relative || (toState = (new FlipState(toState.targets, {props: props})).fit(toState, scale));
		for (p in toState.idLookup) {
			toNode = !toState.alt[p] ? toState.idLookup[p] : _getChangingElState(toState, fromState, p);
			el = toNode.element;
			fromNode = fromState.idLookup[p];
			fromState.alt[p] && el === fromNode.element && (fromState.alt[p].isVisible || !toNode.isVisible) && (fromNode = fromState.alt[p]);
			if (fromNode) {
				comp = {t: el, b: fromNode, a: toNode, sd: fromNode.element === el ? 0 : toNode.isVisible ? 1 : -1};
				comps.push(comp);
				if (comp.sd) { // from and to elements are different, so we need to swap them.
					if (comp.sd < 0) {
						comp.b = toNode;
						comp.a = fromNode;
					}
					// for swapping elements that got interrupted, we must re-record the inline styles to ensure they're not tainted. Remember, .batch() permits getState() not to force in-progress flips to their end state.
					interrupted && _recordInlineStyles(comp.b, props ? _memoizedRemoveProps[props] : _removeProps);
					fade && comps.push(comp.swap = {t: fromNode.element, b: comp.b, a: comp.a, sd: -comp.sd, swap: comp});
				}
				el._flip = fromNode.element._flip = _batch ? _batch.timeline : animation;
			} else if (toNode.isVisible) {
				comps.push({t: el, b: _copy(toNode, {isVisible:1}), a: toNode, sd: 0, entering: 1}); // to include it in the "entering" Array and do absolute positioning if necessary
				el._flip = _batch ? _batch.timeline : animation;
			}
		}

		props && (_memoizedProps[props] || _memoizeProps(props)).forEach(p => tweenVars[p] = i => comps[i].a.props[p]);
		comps.finalStates = finalStates = [];

		run = () => {
			_orderByDOMDepth(comps);
			_lockBodyScroll(true); // otherwise, measurements may get thrown off when things get fit.
			let recordedStyles = [];
			for (i = 0; i < comps.length; i++) {
				comp = comps[i];
				a = comp.a;
				b = comp.b;
				if (prune && !a.isDifferent(b) && !comp.entering) { // only flip if things changed! Don't omit it from comps initially because that'd prevent the element from being positioned absolutely (if necessary)
					comps.splice(i--, 1);
				} else {
					el = comp.t;
					if (nested && !(comp.sd < 0) && i) { // moving a parent affects the position of children
						a = comp.a = a.clone({matrix: getGlobalMatrix(el, false, false, true)});
					}
					if (b.isVisible && a.isVisible) {
						if (comp.sd < 0) { // swapping OUT (swap direction of -1 is out)
							nested && _revertTempStyles(recordedStyles, 1); // get the ancestor elements into the final state for proper measuring
							state = new ElementState(el, props, fromState.simple);
							_fit(state, a, scale, 0, 0, state);
							state.matrix = getGlobalMatrix(el, false, false, true);
							state.bounds = el.getBoundingClientRect();
							state.css = comp.b.css;
							comp.a = a = state;
							fade && (el.style.opacity = interrupted ? b.opacity : a.opacity);
							stagger && swapOutTargets.push(el);
							if (nested) {
								_revertTempStyles(recordedStyles, 2); // now return the ancestor elements back to the before state
								recordedStyles.push(el, el.getAttribute("style"));
							}
						} else if (comp.sd > 0 && fade) { // swapping IN (swap direction of 1 is in)
							el.style.opacity = interrupted ? a.opacity - b.opacity : "0";
						}
						_fit(a, b, scale, props);
						nested && comp.sd < 0 && recordedStyles.push(el.getAttribute("style"));

					} else if (b.isVisible !== a.isVisible) { // either entering or leaving (one side is invisible)
						if (!b.isVisible) { // entering
							a.isVisible && entering.push(a);
							comps.splice(i--, 1);
						} else if (!a.isVisible) { // leaving
							b.css = a.css;
							leaving.push(b);
							comps.splice(i--, 1);
							absolute && nested && _fit(a, b, scale, props);
						}
					}
					if (!scale) {
						el.style.maxWidth = Math.max(a.width, b.width) + "px";
						el.style.maxHeight = Math.max(a.height, b.height) + "px";
						el.style.minWidth = Math.min(a.width, b.width) + "px";
						el.style.minHeight = Math.min(a.height, b.height) + "px";
					}
					nested && toggleClass && el.classList.add(toggleClass);
				}
				finalStates.push(a);
			}
			let classTargets;
			if (toggleClass) {
				classTargets = finalStates.map(s => s.element);
				nested && classTargets.forEach(e => e.classList.remove(toggleClass)); // there could be a delay, so don't leave the classes applied (we'll do it in a timeline callback)
			}

			_lockBodyScroll(false);

			if (scale) {
				tweenVars.scaleX = i => comps[i].a.scaleX;
				tweenVars.scaleY = i => comps[i].a.scaleY;
			} else {
				tweenVars.width = i => comps[i].a.width + "px";
				tweenVars.height = i => comps[i].a.height + "px";
				tweenVars.autoRound = vars.autoRound || false;
			}
			tweenVars.x = i => comps[i].a.x + "px";
			tweenVars.y = i => comps[i].a.y + "px";
			tweenVars.rotation = i => comps[i].a.rotation + (spin ? spinFunc(i, targets[i], targets) * 360 : 0);
			tweenVars.skewX = i => comps[i].a.skewX;

			targets = comps.map(c => c.t);

			if (zIndex || zIndex === 0) {
				tweenVars.modifiers = {zIndex: () => zIndex};
				tweenVars.zIndex = zIndex;
				tweenVars.immediateRender = vars.immediateRender !== false;
			}

			fade && (tweenVars.opacity = i => comps[i].sd < 0 ? 0 : comps[i].sd > 0 ? comps[i].a.opacity : "+=0");

			if (swapOutTargets.length) {
				stagger = gsap.utils.distribute(stagger);
				let dummyArray = targets.slice(swapOutTargets.length);
				tweenVars.stagger = (i, el) => stagger(~swapOutTargets.indexOf(el) ? targets.indexOf(comps[i].swap.t) : i, el, dummyArray);
			}

			// // for testing...
			// gsap.delayedCall(vars.data ? 50 : 1, function() {
			// 	animation.eventCallback("onComplete", () => _setFinalStates(comps, !clearProps));
			// 	addFunc.call(animation, targets, tweenVars, 0).play();
			// });
			// return;

			_callbacks.forEach(name => vars[name] && animation.eventCallback(name, vars[name], vars[name + "Params"])); // apply callbacks to the timeline, not tweens (because "custom" timing can make multiple tweens)

			if (custom && targets.length) { // bust out the custom properties as their own tweens so they can use different eases, durations, etc.
				remainingProps = _copy(tweenVars, _reserved);
				if ("scale" in custom) {
					custom.scaleX = custom.scaleY = custom.scale;
					delete custom.scale;
				}
				for (p in custom) {
					v = _copy(custom[p], _fitReserved);
					v[p] = tweenVars[p];
					!("duration" in v) && ("duration" in tweenVars) && (v.duration = tweenVars.duration);
					v.stagger = tweenVars.stagger;
					addFunc.call(animation, targets, v, 0);
					delete remainingProps[p];
				}
			}
			if (targets.length || leaving.length || entering.length) {
				toggleClass && animation.add(() => _toggleClass(classTargets, toggleClass, animation._zTime < 0 ? "remove" : "add"), 0) && !paused && _toggleClass(classTargets, toggleClass, "add");
				targets.length && addFunc.call(animation, targets, remainingProps, 0);
			}

			_handleCallback(onEnter, entering, animation);
			_handleCallback(onLeave, leaving, animation);

			let batchTl = _batch && _batch.timeline;

			if (batchTl) {
				batchTl.add(animation, 0);
				_batch._final.push(() => _setFinalStates(comps, !clearProps));
			}

			endTime = animation.duration();
			animation.call(() => {
				let forward = animation.time() >= endTime;
				forward && !batchTl && _setFinalStates(comps, !clearProps);
				toggleClass && _toggleClass(classTargets, toggleClass, forward ? "remove" : "add");
			});
		};

		absoluteOnLeave && (absolute = comps.filter(comp => !comp.sd && !comp.a.isVisible && comp.b.isVisible).map(comp => comp.a.element));
		if (_batch) {
			absolute && _batch._abs.push(..._filterComps(comps, absolute));
			_batch._run.push(run);
		} else {
			absolute && _makeCompsAbsolute(_filterComps(comps, absolute)); // when making absolute, we must go in a very particular order so that document flow changes don't affect things. Don't make it visible if both the before and after states are invisible! There's no point, and it could make things appear visible during the flip that shouldn't be.
			run();
		}

		let anim = _batch ? _batch.timeline : animation;
		anim.revert = () => _killFlip(anim, 1, 1); // a Flip timeline should behave very different when reverting - it should actually jump to the end so that styles get cleared out.

		return anim;
	},
	_interrupt = tl => {
		tl.vars.onInterrupt && tl.vars.onInterrupt.apply(tl, tl.vars.onInterruptParams || []);
		tl.getChildren(true, false, true).forEach(_interrupt);
	},
	_killFlip = (tl, action, force) => { // action: 0 = nothing, 1 = complete, 2 = only kill (don't complete)
		if (tl && tl.progress() < 1 && (!tl.paused() || force)) {
			if (action) {
				_interrupt(tl);
				action < 2 && tl.progress(1); // we should also kill it in case it was added to a parent timeline.
				tl.kill();
			}
			return true;
		}
	},
	_createLookup = state => {
		let lookup = state.idLookup = {},
			alt = state.alt = {},
			elStates = state.elementStates,
			i = elStates.length,
			elState;
		while (i--) {
			elState = elStates[i];
			lookup[elState.id] ? (alt[elState.id] = elState) : (lookup[elState.id] = elState);
		}
	};






class FlipState {

	constructor(targets, vars, targetsAreElementStates) {
		this.props = vars && vars.props;
		this.simple = !!(vars && vars.simple);
		if (targetsAreElementStates) {
			this.targets = _elementsFromElementStates(targets);
			this.elementStates = targets;
			_createLookup(this);
		} else {
			this.targets = _toArray(targets);
			let soft = vars && (vars.kill === false || (vars.batch && !vars.kill));
			_batch && !soft && _batch._kill.push(this);
			this.update(soft || !!_batch); // when batching, don't force in-progress flips to their end; we need to do that AFTER all getStates() are called.
		}
	}

	update(soft) {
		this.elementStates = this.targets.map(el => new ElementState(el, this.props, this.simple));
		_createLookup(this);
		this.interrupt(soft);
		this.recordInlineStyles();
		return this;
	}

	clear() {
		this.targets.length = this.elementStates.length = 0;
		_createLookup(this);
		return this;
	}

	fit(state, scale, nested) {
		let elStatesInOrder = _orderByDOMDepth(this.elementStates.slice(0), false, true),
			toElStates = (state || this).idLookup,
			i = 0,
			fromNode, toNode;
		for (; i < elStatesInOrder.length; i++) {
			fromNode = elStatesInOrder[i];
			nested && (fromNode.matrix = getGlobalMatrix(fromNode.element, false, false, true)); // moving a parent affects the position of children
			toNode = toElStates[fromNode.id];
			toNode && _fit(fromNode, toNode, scale, true, 0, fromNode);
			fromNode.matrix = getGlobalMatrix(fromNode.element, false, false, true);
		}
		return this;
	}

	getProperty(element, property) {
		let es = this.getElementState(element) || _emptyObj;
		return (property in es ? es : es.props || _emptyObj)[property];
	}

	add(state) {
		let i = state.targets.length,
			lookup = this.idLookup,
			alt = this.alt,
			index, es, es2;
		while (i--) {
			es = state.elementStates[i];
			es2 = lookup[es.id];
			if (es2 && (es.element === es2.element || (alt[es.id] && alt[es.id].element === es.element))) { // if the flip id is already in this FlipState, replace it!
				index = this.elementStates.indexOf(es.element === es2.element ? es2 : alt[es.id]);
				this.targets.splice(index, 1, state.targets[i]);
				this.elementStates.splice(index, 1, es);
			} else {
				this.targets.push(state.targets[i]);
				this.elementStates.push(es);
			}
		}
		state.interrupted && (this.interrupted = true);
		state.simple || (this.simple = false);
		_createLookup(this);
		return this;
	}

	compare(state) {
		let l1 = state.idLookup,
			l2 = this.idLookup,
			unchanged = [],
			changed = [],
			enter = [],
			leave = [],
			targets = [],
			a1 = state.alt,
			a2 = this.alt,
			place = (s1, s2, el) => (s1.isVisible !== s2.isVisible ? (s1.isVisible ? enter : leave) : s1.isVisible ? changed : unchanged).push(el) && targets.push(el),
			placeIfDoesNotExist = (s1, s2, el) => targets.indexOf(el) < 0 && place(s1, s2, el),
			s1, s2, p, el, s1Alt, s2Alt, c1, c2;
		for (p in l1) {
			s1Alt = a1[p];
			s2Alt = a2[p];
			s1 = !s1Alt ? l1[p] : _getChangingElState(state, this, p);
			el = s1.element;
			s2 = l2[p];
			if (s2Alt) {
				c2 = s2.isVisible || (!s2Alt.isVisible && el === s2.element) ? s2 : s2Alt;
				c1 = s1Alt && !s1.isVisible && !s1Alt.isVisible && c2.element === s1Alt.element ? s1Alt : s1;
				//c1.element !== c2.element && c1.element === s2.element && (c2 = s2);
				if (c1.isVisible && c2.isVisible && c1.element !== c2.element) { // swapping, so force into "changed" array
					(c1.isDifferent(c2) ? changed : unchanged).push(c1.element, c2.element);
					targets.push(c1.element, c2.element);
				} else {
					place(c1, c2, c1.element);
				}
				s1Alt && c1.element === s1Alt.element && (s1Alt = l1[p]);
				placeIfDoesNotExist(c1.element !== s2.element && s1Alt ? s1Alt : c1, s2, s2.element);
				placeIfDoesNotExist(s1Alt && s1Alt.element === s2Alt.element ? s1Alt : c1, s2Alt, s2Alt.element);
				s1Alt && placeIfDoesNotExist(s1Alt, s2Alt.element === s1Alt.element ? s2Alt : s2, s1Alt.element);
			} else {
				!s2 ? enter.push(el) : !s2.isDifferent(s1) ? unchanged.push(el) : place(s1, s2, el);
				s1Alt && placeIfDoesNotExist(s1Alt, s2, s1Alt.element);
			}
		}
		for (p in l2) {
			if (!l1[p]) {
				leave.push(l2[p].element);
				a2[p] && leave.push(a2[p].element);
			}
		}
		return {changed, unchanged, enter, leave};
	}

	recordInlineStyles() {
		let props = _memoizedRemoveProps[this.props] || _removeProps,
			i = this.elementStates.length;
		while (i--) {
			_recordInlineStyles(this.elementStates[i], props);
		}
	}

	interrupt(soft) { // soft = DON'T force in-progress flip animations to completion (like when running a batch, we can't immediately kill flips when getting states because it could contaminate positioning and other .getState() calls that will run in the batch (we kill AFTER all the .getState() calls complete).
		let timelines = [];
		this.targets.forEach(t => {
			let tl = t._flip,
				foundInProgress = _killFlip(tl, soft ? 0 : 1);
			soft && foundInProgress && timelines.indexOf(tl) < 0 && tl.add(() => this.updateVisibility());
			foundInProgress && timelines.push(tl);
		});
		!soft && timelines.length && this.updateVisibility(); // if we found an in-progress Flip animation, we must record all the values in their current state at that point BUT we should update the isVisible value AFTER pushing that flip to completion so that elements that are entering or leaving will populate those Arrays properly.
		this.interrupted || (this.interrupted = !!timelines.length);
	}

	updateVisibility() {
		this.elementStates.forEach(es => {
			let b = es.element.getBoundingClientRect();
			es.isVisible = !!(b.width || b.height || b.top || b.left);
			es.uncache = 1;
		});
	}

	getElementState(element) {
		return this.elementStates[this.targets.indexOf(_getEl(element))];
	}

	makeAbsolute() {
		return _orderByDOMDepth(this.elementStates.slice(0), true, true).map(_makeAbsolute);
	}

}



class ElementState {

	constructor(element, props, simple) {
		if (element instanceof ElementState) { // allows us to essentially clone
			Object.assign(this, element, props || {});
		} else {
			this.element = element;
			this.update(props, simple);
		}
	}

	isDifferent(state) {
		let b1 = this.bounds,
			b2 = state.bounds;
		return b1.top !== b2.top || b1.left !== b2.left || b1.width !== b2.width || b1.height !== b2.height || !this.matrix.equals(state.matrix) || this.opacity !== state.opacity || (this.props && state.props && JSON.stringify(this.props) !== JSON.stringify(state.props));
	}

	clone(overrides) {
		return new ElementState(this, overrides);
	}

	update(props, simple) {
		let self = this,
			element = self.element,
			getProp = gsap.getProperty(element),
			cache = gsap.core.getCache(element),
			bounds = element.getBoundingClientRect(),
			bbox = element.getBBox && typeof(element.getBBox) === "function" && element.nodeName.toLowerCase() !== "svg" && element.getBBox(),
			m = simple ? new Matrix2D(1, 0, 0, 1, bounds.left + _getDocScrollLeft(), bounds.top + _getDocScrollTop()) : getGlobalMatrix(element, false, false, true);
		cache.uncache = 1; // in case there are CSS rules that affect the element. Example: https://gsap.com/community/forums/topic/44321-bug-on-fixed-position-using-flip/
		self.getProp = getProp;
		self.element = element;
		self.id = _getID(element);
		self.matrix = m;
		self.cache = cache;
		self.bounds = bounds;
		self.isVisible = !!(bounds.width || bounds.height || bounds.left || bounds.top);
		self.display = getProp("display");
		self.position = getProp("position");
		self.parent = element.parentNode;
		self.x = getProp("x", "px");
		self.y = getProp("y", "px");
		self.scaleX = cache.scaleX;
		self.scaleY = cache.scaleY;
		self.rotation = getProp("rotation");
		self.skewX = getProp("skewX");
		self.opacity = getProp("opacity");
		self.width =  bbox ? bbox.width : _closestTenth(getProp("width", "px"), 0.04); // round up to the closest 0.1 so that text doesn't wrap.
		self.height = bbox ? bbox.height : _closestTenth(getProp("height", "px"), 0.04);
		props && _recordProps(self, _memoizedProps[props] || _memoizeProps(props));
		self.ctm = element.getCTM && element.nodeName.toLowerCase() === "svg" && _getCTM(element).inverse();
		self.simple = simple || (_round(m.a) === 1 && !_round(m.b) && !_round(m.c) && _round(m.d) === 1); // allows us to speed through some other tasks if it's not scale/rotated
		self.uncache = 0;
	}

}

class FlipAction {
	constructor(vars, batch) {
		this.vars = vars;
		this.batch = batch;
		this.states = [];
		this.timeline = batch.timeline;
	}

	getStateById(id) {
		let i = this.states.length;
		while (i--) {
			if (this.states[i].idLookup[id]) {
				return this.states[i];
			}
		}
	}

	kill() {
		this.batch.remove(this);
	}
}

class FlipBatch {
	constructor(id) {
		this.id = id;
		this.actions = [];
		this._kill = [];
		this._final = [];
		this._abs = [];
		this._run = [];
		this.data = {};
		this.state = new FlipState();
		this.timeline = gsap.timeline();
	}

	add(config) {
		let result = this.actions.filter(action => action.vars === config);
		if (result.length) {
			return result[0];
		}
		result = new FlipAction(typeof(config) === "function" ? {animate: config} : config, this);
		this.actions.push(result);
		return result;
	}

	remove(action) {
		let i = this.actions.indexOf(action);
		i >= 0 && this.actions.splice(i, 1);
		return this;
	}

	getState(merge) {
		let prevBatch = _batch,
			prevAction = _batchAction;
		_batch = this;
		this.state.clear();
		this._kill.length = 0;
		this.actions.forEach(action => {
			if (action.vars.getState) {
				action.states.length = 0;
				_batchAction = action;
				action.state = action.vars.getState(action);
			}
			merge && action.states.forEach(s => this.state.add(s));
		});
		_batchAction = prevAction;
		_batch = prevBatch;
		this.killConflicts();
		return this;
	}

	animate() {
		let prevBatch = _batch,
			tl = this.timeline,
			i = this.actions.length,
			finalStates, endTime;
		_batch = this;
		tl.clear();
		this._abs.length = this._final.length = this._run.length = 0;
		this.actions.forEach(a => {
			a.vars.animate && a.vars.animate(a);
			let onEnter = a.vars.onEnter,
				onLeave = a.vars.onLeave,
				targets = a.targets, s, result;
			if (targets && targets.length && (onEnter || onLeave)) {
				s = new FlipState();
				a.states.forEach(state => s.add(state));
				result = s.compare(Flip.getState(targets));
				result.enter.length && onEnter && onEnter(result.enter);
				result.leave.length && onLeave && onLeave(result.leave);
			}
		});
		_makeCompsAbsolute(this._abs);
		this._run.forEach(f => f());
		endTime = tl.duration();
		finalStates = this._final.slice(0);
		tl.add(() => {
			if (endTime <= tl.time()) { // only call if moving forward in the timeline (in case it's nested in a timeline that gets reversed)
				finalStates.forEach(f => f());
				_forEachBatch(this, "onComplete");
			}
		});
		_batch = prevBatch;
		while (i--) {
			this.actions[i].vars.once && this.actions[i].kill();
		}
		_forEachBatch(this, "onStart");
		tl.restart();
		return this;
	}

	loadState(done) {
		done || (done = () => 0);
		let queue = [];
		this.actions.forEach(c => {
			if (c.vars.loadState) {
				let i, f = targets => {
					targets && (c.targets = targets);
					i = queue.indexOf(f);
					if (~i) {
						queue.splice(i, 1);
						queue.length || done();
					}
				};
				queue.push(f);
				c.vars.loadState(f);
			}
		});
		queue.length || done();
		return this;
	}

	setState() {
		this.actions.forEach(c => c.targets = c.vars.setState && c.vars.setState(c));
		return this;
	}

	killConflicts(soft) {
		this.state.interrupt(soft);
		this._kill.forEach(state => state.interrupt(soft));
		return this;
	}

	run(skipGetState, merge) {
		if (this !== _batch) {
			skipGetState || this.getState(merge);
			this.loadState(() => {
				if (!this._killed) {
					this.setState();
					this.animate();
				}
			});
		}
		return this;
	}

	clear(stateOnly) {
		this.state.clear();
		stateOnly || (this.actions.length = 0);
	}

	getStateById(id) {
		let i = this.actions.length,
			s;
		while (i--) {
			s = this.actions[i].getStateById(id);
			if (s) {
				return s;
			}
		}
		return this.state.idLookup[id] && this.state;
	}

	kill() {
		this._killed = 1;
		this.clear();
		delete _batchLookup[this.id];
	}
}


export class Flip {

	static getState(targets, vars) {
		let state = _parseState(targets, vars);
		_batchAction && _batchAction.states.push(state);
		vars && vars.batch && Flip.batch(vars.batch).state.add(state);
		return state;
	}

	static from(state, vars) {
		vars = vars || {};
		("clearProps" in vars) || (vars.clearProps = true);
		return _fromTo(state, _parseState(vars.targets || state.targets, {props: vars.props || state.props, simple: vars.simple, kill: !!vars.kill}), vars, -1);
	}

	static to(state, vars) {
		return _fromTo(state, _parseState(vars.targets || state.targets, {props: vars.props || state.props, simple: vars.simple, kill: !!vars.kill}), vars, 1);
	}

	static fromTo(fromState, toState, vars) {
		return _fromTo(fromState, toState, vars);
	}

	static fit(fromEl, toEl, vars) {
		let v = vars ? _copy(vars, _fitReserved) : {},
			{absolute, scale, getVars, props, runBackwards, onComplete, simple} = vars || v,
			fitChild = vars && vars.fitChild && _getEl(vars.fitChild),
			before = _parseElementState(toEl, props, simple, fromEl),
			after = _parseElementState(fromEl, 0, simple, before),
			inlineProps = props ? _memoizedRemoveProps[props] : _removeProps,
			ctx = gsap.context();
		props && _applyProps(v, before.props);
		_recordInlineStyles(after, inlineProps);
		if (runBackwards) {
			("immediateRender" in v) || (v.immediateRender = true);
			v.onComplete = function() {
				_applyInlineStyles(after);
				onComplete && onComplete.apply(this, arguments);
			};
		}
		absolute && _makeAbsolute(after, before);
		v = _fit(after, before, scale || fitChild, !v.duration && props, fitChild, v.duration || getVars ? v : 0);
		typeof(vars) === "object" && "zIndex" in vars && (v.zIndex = vars.zIndex);
		ctx && !getVars && ctx.add(() => () => _applyInlineStyles(after));
		return getVars ? v : v.duration ? gsap.to(after.element, v) : null;
	}

	static makeAbsolute(targetsOrStates, vars) {
		return (targetsOrStates instanceof FlipState ? targetsOrStates : new FlipState(targetsOrStates, vars)).makeAbsolute();
	}

	static batch(id) {
		id || (id = "default");
		return _batchLookup[id] || (_batchLookup[id] = new FlipBatch(id));
	}

	static killFlipsOf(targets, complete) {
		(targets instanceof FlipState ? targets.targets : _toArray(targets)).forEach(t => t && _killFlip(t._flip, complete !== false ? 1 : 2));
	}

	static isFlipping(target) {
		let f = Flip.getByTarget(target);
		return !!f && f.isActive();
	}

	static getByTarget(target) {
		return (_getEl(target) || _emptyObj)._flip;
	}

	static getElementState(target, props) {
		return new ElementState(_getEl(target), props);
	}

	static convertCoordinates(fromElement, toElement, point) {
		let m = getGlobalMatrix(toElement, true, true).multiply(getGlobalMatrix(fromElement));
		return point ? m.apply(point) : m;
	}


	static register(core) {
		_body = typeof(document) !== "undefined" && document.body;
		if (_body) {
			gsap = core;
			_setDoc(_body);
			_toArray = gsap.utils.toArray;
			_getStyleSaver = gsap.core.getStyleSaver;
			let snap = gsap.utils.snap(0.1);
			_closestTenth = (value, add) => snap(parseFloat(value) + add);
		}
	}
}

Flip.version = "3.15.0";

// function whenImagesLoad(el, func) {
// 	let pending = [],
// 		onLoad = e => {
// 			pending.splice(pending.indexOf(e.target), 1);
// 			e.target.removeEventListener("load", onLoad);
// 			pending.length || func();
// 		};
// 	gsap.utils.toArray(el.tagName.toLowerCase() === "img" ? el : el.querySelectorAll("img")).forEach(img => img.complete || img.addEventListener("load", onLoad) || pending.push(img));
// 	pending.length || func();
// }

typeof(window) !== "undefined" && window.gsap && window.gsap.registerPlugin(Flip);

export { Flip as default };
```

## 📄 File: `SplitText.js`
```javascript
/*!
 * SplitText 3.15.0
 * https://gsap.com
 *
 * @license Copyright 2026, GreenSock. All rights reserved. Subject to the terms at https://gsap.com/standard-license.
 * @author: Jack Doyle
 */

let gsap, _fonts, _splitProp = typeof Symbol === "function" ? Symbol() : "_split", _coreInitted, _initIfNecessary = () => _coreInitted || SplitText.register(window.gsap), _charSegmenter = typeof Intl !== "undefined" && "Segmenter" in Intl ? new Intl.Segmenter() : 0, _toArray = (r) => !r ? [] : typeof r === "string" ? _toArray(document.querySelectorAll(r)) : "length" in r ? Array.from(r).reduce((acc, cur) => {
  typeof cur === "string" ? acc.push(..._toArray(cur)) : acc.push(cur);
  return acc;
}, []) : [r], _elements = (targets) => _toArray(targets).filter((e) => e && e.nodeType === 1), _emptyArray = [], _context = function() {
}, _defaultContext = { add: (f) => f() }, _spacesRegEx = /\s+/g, _emojiSafeRegEx = new RegExp("\\p{RI}\\p{RI}|\\p{Emoji}(\\p{EMod}|\\u{FE0F}\\u{20E3}?|[\\u{E0020}-\\u{E007E}]+\\u{E007F})?(\\u{200D}\\p{Emoji}(\\p{EMod}|\\u{FE0F}\\u{20E3}?|[\\u{E0020}-\\u{E007E}]+\\u{E007F})?)*|.", "gu"), _emptyBounds = { left: 0, top: 0, width: 0, height: 0 }, _findNextValidBounds = (allBounds, startIndex) => {
  while (++startIndex < allBounds.length && allBounds[startIndex] === _emptyBounds) {
  }
  return allBounds[startIndex] || _emptyBounds;
}, _revertOriginal = ({ element, html, ariaL, ariaH }) => {
  element.innerHTML = html;
  ariaL ? element.setAttribute("aria-label", ariaL) : element.removeAttribute("aria-label");
  ariaH ? element.setAttribute("aria-hidden", ariaH) : element.removeAttribute("aria-hidden");
}, _stretchToFitSpecialChars = (collection, specialCharsRegEx) => {
  if (specialCharsRegEx) {
    let charsFound = new Set(collection.join("").match(specialCharsRegEx) || _emptyArray), i = collection.length, slots, word, char, combined;
    if (charsFound.size) {
      while (--i > -1) {
        word = collection[i];
        for (char of charsFound) {
          if (char.startsWith(word) && char.length > word.length) {
            slots = 0;
            combined = word;
            while (char.startsWith(combined += collection[i + ++slots]) && combined.length < char.length) {
            }
            if (slots && combined.length === char.length) {
              collection[i] = char;
              collection.splice(i + 1, slots);
              break;
            }
          }
        }
      }
    }
  }
  return collection;
}, _disallowInline = (element) => window.getComputedStyle(element).display === "inline" && (element.style.display = "inline-block"), _insertNodeBefore = (newChild, parent, existingChild) => parent.insertBefore(typeof newChild === "string" ? document.createTextNode(newChild) : newChild, existingChild), _getWrapper = (type, config, collection) => {
  let className = config[type + "sClass"] || "", { tag = "div", aria = "auto", propIndex = false } = config, display = type === "line" ? "block" : "inline-block", incrementClass = className.indexOf("++") > -1, wrapper = (text) => {
    let el = document.createElement(tag), i = collection.length + 1;
    className && (el.className = className + (incrementClass ? " " + className + i : ""));
    propIndex && el.style.setProperty("--" + type, i + "");
    aria !== "none" && el.setAttribute("aria-hidden", "true");
    if (tag !== "span") {
      el.style.position = "relative";
      el.style.display = display;
    }
    el.textContent = text;
    collection.push(el);
    return el;
  };
  incrementClass && (className = className.replace("++", ""));
  wrapper.collection = collection;
  return wrapper;
}, _getLineWrapper = (element, nodes, config, collection) => {
  let lineWrapper = _getWrapper("line", config, collection), textAlign = window.getComputedStyle(element).textAlign || "left";
  return (startIndex, endIndex) => {
    let newLine = lineWrapper("");
    newLine.style.textAlign = textAlign;
    element.insertBefore(newLine, nodes[startIndex]);
    for (; startIndex < endIndex; startIndex++) {
      newLine.appendChild(nodes[startIndex]);
    }
    newLine.normalize();
  };
}, _splitWordsAndCharsRecursively = (element, config, wordWrapper, charWrapper, prepForCharsOnly, deepSlice, ignore, charSplitRegEx, specialCharsRegEx, isNested) => {
  var _a;
  let nodes = Array.from(element.childNodes), i = 0, { wordDelimiter, reduceWhiteSpace = true, prepareText } = config, elementBounds = element.getBoundingClientRect(), lastBounds = elementBounds, isPreformatted = !reduceWhiteSpace && window.getComputedStyle(element).whiteSpace.substring(0, 3) === "pre", ignoredPreviousSibling = 0, wordsCollection = wordWrapper.collection, wordDelimIsNotSpace, wordDelimString, wordDelimSplitter, curNode, words, curWordEl, startsWithSpace, endsWithSpace, j, bounds, curWordChars, clonedNode, curSubNode, tempSubNode, curTextContent, wordText, lastWordText, k;
  if (typeof wordDelimiter === "object") {
    wordDelimSplitter = wordDelimiter.delimiter || wordDelimiter;
    wordDelimString = wordDelimiter.replaceWith || "";
  } else {
    wordDelimString = wordDelimiter === "" ? "" : wordDelimiter || " ";
  }
  wordDelimIsNotSpace = wordDelimString !== " ";
  for (; i < nodes.length; i++) {
    curNode = nodes[i];
    if (curNode.nodeType === 3) {
      curTextContent = curNode.textContent || "";
      if (reduceWhiteSpace) {
        curTextContent = curTextContent.replace(_spacesRegEx, " ");
      } else if (isPreformatted) {
        curTextContent = curTextContent.replace(/\n/g, wordDelimString + "\n");
      }
      prepareText && (curTextContent = prepareText(curTextContent, element));
      curNode.textContent = curTextContent;
      words = wordDelimString || wordDelimSplitter ? curTextContent.split(wordDelimSplitter || wordDelimString) : curTextContent.match(charSplitRegEx) || _emptyArray;
      lastWordText = words[words.length - 1];
      endsWithSpace = wordDelimIsNotSpace ? lastWordText.slice(-1) === " " : !lastWordText;
      lastWordText || words.pop();
      lastBounds = elementBounds;
      startsWithSpace = wordDelimIsNotSpace ? words[0].charAt(0) === " " : !words[0];
      startsWithSpace && _insertNodeBefore(" ", element, curNode);
      words[0] || words.shift();
      _stretchToFitSpecialChars(words, specialCharsRegEx);
      deepSlice && isNested || (curNode.textContent = "");
      for (j = 1; j <= words.length; j++) {
        wordText = words[j - 1];
        if (!reduceWhiteSpace && isPreformatted && wordText.charAt(0) === "\n") {
          (_a = curNode.previousSibling) == null ? void 0 : _a.remove();
          _insertNodeBefore(document.createElement("br"), element, curNode);
          wordText = wordText.slice(1);
        }
        if (!reduceWhiteSpace && wordText === "") {
          _insertNodeBefore(wordDelimString, element, curNode);
        } else if (wordText === " ") {
          element.insertBefore(document.createTextNode(" "), curNode);
        } else {
          wordDelimIsNotSpace && wordText.charAt(0) === " " && _insertNodeBefore(" ", element, curNode);
          if (ignoredPreviousSibling && j === 1 && !startsWithSpace && wordsCollection.indexOf(ignoredPreviousSibling.parentNode) > -1) {
            curWordEl = wordsCollection[wordsCollection.length - 1];
            curWordEl.appendChild(document.createTextNode(charWrapper ? "" : wordText));
          } else {
            curWordEl = wordWrapper(charWrapper ? "" : wordText);
            _insertNodeBefore(curWordEl, element, curNode);
            ignoredPreviousSibling && j === 1 && !startsWithSpace && curWordEl.insertBefore(ignoredPreviousSibling, curWordEl.firstChild);
          }
          if (charWrapper) {
            curWordChars = _charSegmenter ? _stretchToFitSpecialChars([..._charSegmenter.segment(wordText)].map((s) => s.segment), specialCharsRegEx) : wordText.match(charSplitRegEx) || _emptyArray;
            for (k = 0; k < curWordChars.length; k++) {
              curWordEl.appendChild(curWordChars[k] === " " ? document.createTextNode(" ") : charWrapper(curWordChars[k]));
            }
          }
          if (deepSlice && isNested) {
            curTextContent = curNode.textContent = curTextContent.substring(wordText.length + 1, curTextContent.length);
            bounds = curWordEl.getBoundingClientRect();
            if (bounds.top > lastBounds.top && bounds.left <= lastBounds.left) {
              clonedNode = element.cloneNode();
              curSubNode = element.childNodes[0];
              while (curSubNode && curSubNode !== curWordEl) {
                tempSubNode = curSubNode;
                curSubNode = curSubNode.nextSibling;
                clonedNode.appendChild(tempSubNode);
              }
              element.parentNode.insertBefore(clonedNode, element);
              prepForCharsOnly && _disallowInline(clonedNode);
            }
            lastBounds = bounds;
          }
          if (j < words.length || endsWithSpace) {
            _insertNodeBefore(j >= words.length ? " " : wordDelimIsNotSpace && wordText.slice(-1) === " " ? " " + wordDelimString : wordDelimString, element, curNode);
          }
        }
      }
      element.removeChild(curNode);
      ignoredPreviousSibling = 0;
    } else if (curNode.nodeType === 1) {
      if (ignore && ignore.indexOf(curNode) > -1) {
        wordsCollection.indexOf(curNode.previousSibling) > -1 && wordsCollection[wordsCollection.length - 1].appendChild(curNode);
        ignoredPreviousSibling = curNode;
      } else {
        _splitWordsAndCharsRecursively(curNode, config, wordWrapper, charWrapper, prepForCharsOnly, deepSlice, ignore, charSplitRegEx, specialCharsRegEx, true);
        ignoredPreviousSibling = 0;
      }
      prepForCharsOnly && _disallowInline(curNode);
    }
  }
};
const _SplitText = class _SplitText {
  constructor(elements, config) {
    this.isSplit = false;
    _initIfNecessary();
    this.elements = _elements(elements);
    this.chars = [];
    this.words = [];
    this.lines = [];
    this.masks = [];
    this.vars = config;
    this.elements.forEach((el) => {
      var _a;
      config.overwrite !== false && ((_a = el[_splitProp]) == null ? void 0 : _a._data.orig.filter(({ element }) => element === el).forEach(_revertOriginal));
      el[_splitProp] = this;
    });
    this._split = () => this.isSplit && this.split(this.vars);
    let orig = [], timerId, checkWidths = () => {
      let i = orig.length, o;
      while (i--) {
        o = orig[i];
        let w = o.element.offsetWidth;
        if (w !== o.width) {
          o.width = w;
          this._split();
          return;
        }
      }
    };
    this._data = { orig, obs: typeof ResizeObserver !== "undefined" && new ResizeObserver(() => {
      clearTimeout(timerId);
      timerId = setTimeout(checkWidths, 200);
    }) };
    _context(this);
    this.split(config);
  }
  split(config) {
    (this._ctx || _defaultContext).add(() => {
      this.isSplit && this.revert();
      this.vars = config = config || this.vars || {};
      let { type = "chars,words,lines", aria = "auto", deepSlice = true, smartWrap, onSplit, autoSplit = false, specialChars, mask } = this.vars, splitLines = type.indexOf("lines") > -1, splitCharacters = type.indexOf("chars") > -1, splitWords = type.indexOf("words") > -1, onlySplitCharacters = splitCharacters && !splitWords && !splitLines, specialCharsRegEx = specialChars && ("push" in specialChars ? new RegExp("(?:" + specialChars.join("|") + ")", "gu") : specialChars), finalCharSplitRegEx = specialCharsRegEx ? new RegExp(specialCharsRegEx.source + "|" + _emojiSafeRegEx.source, "gu") : _emojiSafeRegEx, ignore = !!config.ignore && _elements(config.ignore), { orig, animTime, obs } = this._data, onSplitResult;
      if (splitCharacters || splitWords || splitLines) {
        this.elements.forEach((element, index) => {
          orig[index] = {
            element,
            html: element.innerHTML,
            ariaL: element.getAttribute("aria-label"),
            ariaH: element.getAttribute("aria-hidden")
          };
          aria === "auto" ? element.setAttribute("aria-label", (element.textContent || "").trim()) : aria === "hidden" && element.setAttribute("aria-hidden", "true");
          let chars = [], words = [], lines = [], charWrapper = splitCharacters ? _getWrapper("char", config, chars) : null, wordWrapper = _getWrapper("word", config, words), i, curWord, smartWrapSpan, nextSibling;
          _splitWordsAndCharsRecursively(element, config, wordWrapper, charWrapper, onlySplitCharacters, deepSlice && (splitLines || onlySplitCharacters), ignore, finalCharSplitRegEx, specialCharsRegEx, false);
          if (splitLines) {
            let nodes = _toArray(element.childNodes), wrapLine = _getLineWrapper(element, nodes, config, lines), curNode, toRemove = [], lineStartIndex = 0, allBounds = nodes.map((n) => n.nodeType === 1 ? n.getBoundingClientRect() : _emptyBounds), lastBounds = _emptyBounds, curBounds;
            for (i = 0; i < nodes.length; i++) {
              curNode = nodes[i];
              if (curNode.nodeType === 1) {
                if (curNode.nodeName === "BR") {
                  if (!i || nodes[i - 1].nodeName !== "BR") {
                    toRemove.push(curNode);
                    wrapLine(lineStartIndex, i + 1);
                  }
                  lineStartIndex = i + 1;
                  lastBounds = _findNextValidBounds(allBounds, i);
                } else {
                  curBounds = allBounds[i];
                  if (i && curBounds.top > lastBounds.top && curBounds.left < lastBounds.left + lastBounds.width - 1) {
                    wrapLine(lineStartIndex, i);
                    lineStartIndex = i;
                  }
                  lastBounds = curBounds;
                }
              }
            }
            lineStartIndex < i && wrapLine(lineStartIndex, i);
            toRemove.forEach((el) => {
              var _a;
              return (_a = el.parentNode) == null ? void 0 : _a.removeChild(el);
            });
          }
          if (!splitWords) {
            for (i = 0; i < words.length; i++) {
              curWord = words[i];
              if (splitCharacters || !curWord.nextSibling || curWord.nextSibling.nodeType !== 3) {
                if (smartWrap && !splitLines) {
                  smartWrapSpan = document.createElement("span");
                  smartWrapSpan.style.whiteSpace = "nowrap";
                  while (curWord.firstChild) {
                    smartWrapSpan.appendChild(curWord.firstChild);
                  }
                  curWord.replaceWith(smartWrapSpan);
                } else {
                  curWord.replaceWith(...curWord.childNodes);
                }
              } else {
                nextSibling = curWord.nextSibling;
                if (nextSibling && nextSibling.nodeType === 3) {
                  nextSibling.textContent = (curWord.textContent || "") + (nextSibling.textContent || "");
                  curWord.remove();
                }
              }
            }
            words.length = 0;
            element.normalize();
          }
          this.lines.push(...lines);
          this.words.push(...words);
          this.chars.push(...chars);
        });
        mask && this[mask] && this.masks.push(...this[mask].map((el) => {
          let maskEl = el.cloneNode();
          el.replaceWith(maskEl);
          maskEl.appendChild(el);
          el.className && (maskEl.className = el.className.trim().split(" ").map((s) => s + "-mask").join(" "));
          maskEl.style.overflow = "clip";
          return maskEl;
        }));
      }
      this.isSplit = true;
      _fonts && splitLines && autoSplit && _fonts.addEventListener("loadingdone", this._split);
      if ((onSplitResult = onSplit && onSplit(this)) && onSplitResult.totalTime) {
        this._data.anim = animTime ? onSplitResult.totalTime(animTime) : onSplitResult;
      }
      splitLines && autoSplit && this.elements.forEach((element, index) => {
        orig[index].width = element.offsetWidth;
        obs && obs.observe(element);
      });
    });
    return this;
  }
  kill() {
    let { obs } = this._data;
    obs && obs.disconnect();
    _fonts == null ? void 0 : _fonts.removeEventListener("loadingdone", this._split);
  }
  revert() {
    var _a, _b;
    if (this.isSplit) {
      let { orig, anim } = this._data;
      this.kill();
      orig.forEach(_revertOriginal);
      this.chars.length = this.words.length = this.lines.length = orig.length = this.masks.length = 0;
      this.isSplit = false;
      if (anim) {
        this._data.animTime = anim.totalTime();
        anim.revert();
      }
      (_b = (_a = this.vars).onRevert) == null ? void 0 : _b.call(_a, this);
    }
    return this;
  }
  static create(elements, config) {
    return new _SplitText(elements, config);
  }
  static register(core) {
    gsap = gsap || core || window.gsap;
    if (gsap) {
      _toArray = gsap.utils.toArray;
      _context = gsap.core.context || _context;
    }
    if (!_coreInitted && window.innerWidth > 0) {
      _fonts = document.fonts;
      _coreInitted = true;
    }
  }
};
_SplitText.version = "3.15.0";
let SplitText = _SplitText;

export { SplitText, SplitText as default };

```

