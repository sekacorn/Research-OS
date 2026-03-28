# Usage Guide

This system is designed to reduce cognitive overload during research work.
The goal is to spend less time wrestling with tool mechanics and more time thinking clearly about what the data means.
Think of it as a structured research copilot: it handles repetitive flow so your attention stays on judgment.

## Main Goal
- Offload repetitive statistical and literature workflow steps.
- Keep interpretation cautious and structured.
- Create space for higher-value reasoning, not manual pipeline assembly.
- Maintain momentum without losing methodological discipline.

## Before You Start
If you are on Linux or macOS, you can prepare the environment with:

```bash
bash setup.sh
```

Use one command to start everything:

### Windows
```bat
run.bat
```

### Linux/macOS
```bash
bash run.sh
```

When startup succeeds:
- API docs: use the endpoint printed by `run.bat` / `run.sh` (default starts near `http://127.0.0.1:8000/docs`)
- Streamlit app: use the UI endpoint printed by `run.bat` / `run.sh` (default starts near `http://127.0.0.1:8501`)

If both URLs open, the full stack is up and ready to use.

To stop:

### Windows
```bat
stop.bat
```

### Linux/macOS
```bash
bash stop.sh
```

## How To Work In The App

### 1) Data Tab
Use this to load and inspect your dataset.

What to do:
- Load your file.
- Or click `Load sample dataset` to explore the full workflow quickly.
- Review column types and missingness.
- Confirm variable names before analysis.
- Edit rows directly in the table if you need a quick cleanup pass.
- Save or download the current snapshot after edits.

Why this matters:
- Fast schema checks prevent avoidable mistakes later.
- You catch structural issues before they contaminate tests or models.
- This is the best place to pause and sanity-check before pressing into inference.

### 2) Analysis Tab
Use this for exploratory analysis and hypothesis tests.

What to do:
- Run summary statistics and EDA outputs.
- Review the correlation matrix and generated plots.
- Select group comparisons or association tests.
- Review assumptions, p-values, effect sizes, and warnings together.

Why this matters:
- You get a compact evidence snapshot without juggling multiple tools.
- Interpretation is framed as association, not causation, by default.
- This is where you can test ideas quickly without turning every run into a deep manual audit.
- Plots are paired with textual summaries so you are not relying on color alone to understand the results.

### 3) Models Tab
Use this for OLS/logit modeling and diagnostics.

What to do:
- Define outcome and predictors.
- Run the model.
- Read coefficients with diagnostics and warnings side by side.
- For logistic regression, use a binary numeric outcome column coded as `0/1`.
- Avoid identifier-style predictors such as `student_id` unless they are analytically meaningful.

Why this matters:
- Model quality signals (VIF, residual warnings, etc.) stay attached to results.
- You think in terms of robustness, not just significance.
- When diagnostics push back, treat that as useful signal, not friction.
- Categorical predictors are supported in OLS and logistic models, while standardized-beta summaries are limited to numeric predictors.

### 4) Report Tab
Use this to assemble research-grade output.

What to do:
- Open the page after you have run tests or models.
- Preview the generated HTML report in-app.
- Download the HTML report when it looks right.
- Verify sections are present:
  - methods
  - interpretation
  - diagnostics
  - limitations
  - next steps
  - citations (if attached)

Why this matters:
- You move from results to defensible writing faster.
- The structure reduces blank-page drag when drafting.
- This gives you a clean first-draft skeleton so your edits can focus on argument quality.

### 5) Literature Tab
Use this for open-access paper workflow support.

What to do:
- Optionally upload a PDF and search within its extracted text.
- Search for relevant literature metadata.
- Resolve open-access availability.
- Download OA PDFs only.
- Add notes and attach citations to the report.

Why this matters:
- You avoid scattered reference workflows.
- You link sources directly into analysis/report context.
- This keeps evidence collection close to your analysis loop instead of in separate tabs all day.

## Recommended Workflow (Practical Loop)
1. Load data and validate structure.
2. Run EDA and one focused hypothesis test.
3. Fit one baseline model.
4. Review diagnostics and coach warnings.
5. Pull 3-5 relevant papers from the Literature tab.
6. Export a report and iterate.

This loop is intentionally tight. Speed is useful, but clean reasoning is the real win.
Short loops beat marathon sessions when you need consistent quality decisions.

## Reading Outputs Correctly
- Treat p-values as one signal, not the decision engine.
- Keep effect sizes and diagnostics in the same frame.
- If assumptions or warnings appear, branch into sensitivity checks.
- Avoid causal language unless your design justifies it.

## Typical Session Outcomes
By the end of a normal run, you should have:
- a tested analysis path,
- model diagnostics with explicit caveats,
- linked citations and notes,
- and a report draft ready for revision.

That is the point: less cognitive overhead on mechanics, more bandwidth for judgment.
