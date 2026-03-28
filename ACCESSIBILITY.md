# Accessibility

Research OS aims to be usable by as many people as possible, but it has not been formally audited or certified for Section 508 compliance or WCAG 2.1 AA conformance.

## Current Accessibility Posture

Strengths in the current implementation:

- most interactive controls use native Streamlit widgets with visible labels
- major workflow actions include text labels rather than color-only cues
- analysis outputs are accompanied by text summaries, diagnostics, and interpretation blocks
- README screenshots include descriptive alt text

## Known Gaps

The following areas still need a formal accessibility pass:

- Plotly chart accessibility for screen readers and keyboard-only navigation
- screen-reader behavior for `st.data_editor`
- contrast and focus-state auditing across all Streamlit themes and browser zoom levels
- full keyboard-only workflow testing for upload, analysis, report, and literature actions
- accessible handling of long JSON output blocks and dense model results

## Practical Assessment

At this point, the application should be treated as:

- accessibility-aware
- partially accessible in common desktop browser workflows
- not yet formally Section 508 compliant

## Recommended Next Steps

1. Run automated accessibility checks on a deployed build where possible.
2. Test the UI with keyboard-only navigation.
3. Test the full workflow with common screen readers.
4. Add text or table alternatives for complex charts where needed.
5. Re-check color contrast after any visual design changes.
