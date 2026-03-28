# METHODS & LIMITATIONS

This document describes how analysis outputs should be interpreted within Research OS.

The goal is to support careful social-science research thinking, not automated decision-making.

---

## Intended use

This system supports:

- exploratory data analysis
- hypothesis testing
- regression modeling
- interpretation with assumptions and limitations

It is NOT intended for:

- operational decision systems
- scoring individuals
- automated interventions
- predictive policing or surveillance use cases

All results are research-oriented.

---

## Interpretation framework

All statistical outputs pass through the **Methods + Assumptions Coach**.

This ensures each analysis includes:

- methods explanation
- assumption checks
- diagnostics summary
- effect sizes
- limitations
- next steps

The system prioritizes transparency over certainty.

---

## Data limitations

Data issues may affect interpretation:

- missing values may bias results
- measurement quality varies across sources
- sampling may not be representative
- variable definitions may differ across datasets
- outliers may influence models

Always inspect:

- missingness patterns
- distributions
- data provenance

---

## Statistical limitations

The system supports standard statistical techniques, but:

- correlation does not imply causation
- p-values alone are not evidence of importance
- effect sizes must be interpreted in context
- assumptions may be violated
- models may be sensitive to specification choices

Diagnostics are surfaced to guide interpretation.

---

## Modeling limitations

Regression and inference depend on:

- adequate sample size
- correct model specification
- independence of observations
- stable measurement

Potential risks:

- multicollinearity
- heteroskedasticity
- non-normal residuals
- omitted variable bias

Warnings are provided where detectable.

---

## Causality statement

This system does not infer causal relationships unless:

- study design supports it
- the user explicitly documents causal assumptions

Default stance:

> results represent associations, not causal claims.

---

## Ethics and responsible use

Users must:

- avoid including personally identifiable information
- avoid using outputs to label or rank individuals
- avoid surveillance or enforcement applications
- avoid punitive decision-making

Appropriate uses include:

- research exploration
- academic study
- policy discussion
- social trend analysis

---

## Limitations of automated interpretation

The Methods Coach generates structured interpretation, but:

- it does not replace subject-matter expertise
- it cannot detect all confounding
- it cannot validate causal claims
- it cannot evaluate external validity

Human judgment remains essential.

---

## Recommended research workflow

1. Inspect dataset structure
2. Review missingness and distributions
3. Run exploratory analysis
4. Test hypotheses cautiously
5. Review diagnostics and assumptions
6. Interpret effect sizes
7. Document limitations
8. Connect findings to literature

This workflow prioritizes rigor over speed.

---

## Design philosophy

This system exists to:

- strengthen statistical reasoning
- encourage intellectual humility
- support transparent interpretation
- mirror peer-review thinking
- prevent misuse of analysis

Treat this as a research laboratory rather than a research analytics dashboard.
