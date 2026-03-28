# SPEC - Research OS (Research-Grade Edition with Methods Coach)

This version replaces the MVP-only framing with a research-grade system architecture.

The Methods + Assumptions Coach is now a required component of the pipeline.

---

## 1) Product intent

A local-first research environment designed to support rigorous social-scientific and social-data analysis.

The system must:

- accelerate dataset exploration
- support transparent hypothesis testing
- generate defensible interpretations
- surface assumptions and limitations clearly
- integrate literature context into analysis
- produce academically appropriate reports

This is not a dashboard.

This is a research environment.

---

## 2) Target user

Primary user:

- quantitative social-science researcher
- data-driven thinker
- strong statistical interest
- computer science familiarity
- prefers analysis and theory building over frontline intervention

Secondary users (future):

- policy researchers
- academic labs
- civic tech analysts

---

## 3) Non-goals (explicit)

Version 1 must NOT include:

- user accounts / authentication
- cloud hosting dependency
- real-time collaboration
- surveillance tools
- individual risk scoring
- predictive policing use cases
- paywalled article scraping

OA PDFs only.

---

## 4) Core user stories

### Data -> Analysis

1. Upload a dataset (CSV).
2. Auto-detect variable types.
3. Surface missingness patterns.
4. Suggest basic cleaning steps.
5. Run EDA (distributions, correlations).
6. Run hypothesis tests.
7. Run regression models.
8. View effect sizes and diagnostics.
9. Receive structured interpretation.

All outputs must pass through the Methods Coach.

---

### Analysis -> Interpretation

10. System surfaces:

- methods explanation
- assumption checks
- diagnostics summary
- interpretation text
- limitations
- next research steps

Generated via Methods + Assumptions Coach.

---

### Analysis -> Report

11. Generate research-grade HTML report including:

- dataset description
- methods section
- test/model outputs
- interpretation
- diagnostics
- limitations
- next steps
- citations

---

### Literature

12. Search research papers (metadata).
13. Detect OA availability.
14. Download OA PDFs locally.
15. View PDFs in UI.
16. Add notes linked to page/section.
17. Attach citations to analysis/report.

---

## 5) Statistics coverage

### Core analytics

- missingness analysis
- outlier detection
- correlations
- descriptive statistics

### Hypothesis tests

- t-test
- Mann-Whitney U
- chi-square
- ANOVA
- Kruskal-Wallis

### Models

- OLS regression
- logistic regression

### Diagnostics

- VIF (multicollinearity)
- residual checks
- heteroskedasticity flag

### Effect sizes

- Cohen's d
- Cramer's V
- standardized betas
- odds ratios with CI

---

## 6) Methods + Assumptions Coach (mandatory layer)

All statistical outputs MUST pass through:

`stats_engine/methods_coach.py`

This layer:

- converts outputs into research language
- surfaces assumption failures
- highlights diagnostics
- generates limitations
- recommends next steps
- enforces cautious interpretation
- prevents causal overreach

Pipeline:

raw stats -> interpret layer -> methods coach -> UI/report

---

## 7) Interpretation output standard

Every analysis result must include:

- method description
- test/model parameters
- p-values
- confidence intervals (if applicable)
- effect sizes
- diagnostics summary
- assumptions checked
- warnings
- limitations
- next steps

No output may skip this structure.

---

## 8) Data privacy & ethics

System must:

- warn if columns resemble PII
- default to local storage
- allow clearing stored data
- state clearly:

  "Results represent associations, not causal claims."

Must include:

- ethics notice in report
- limitations notice in METHODS.md

---

## 9) Architecture requirement

System must follow multi-agent structure:

- stats_engine
- literature
- methods_coach
- interpret layer
- report layer
- UI
- API
- QA
- docs

Agents must not cross boundaries.

---

## 10) Acceptance criteria (definition of done)

System is complete when:

- `make test` passes
- Streamlit app runs end-to-end
- FastAPI app runs
- OA-only PDF download enforced
- at least:
  - one hypothesis test
  - one regression
  produce coach outputs

Exported report must include:

- Methods section
- Interpretation
- Diagnostics
- Limitations
- Next steps
- Citations (if attached)

Outputs must be:

- deterministic
- cautious
- academically appropriate
- transparent
- assumption-aware

---

## 11) Design philosophy

This system exists to:

- strengthen statistical reasoning
- support intellectual rigor
- encourage humility in interpretation
- mirror peer-review thinking
- build trust through transparency

It must feel like:

a research lab environment,
not an analytics dashboard.
