import streamlit as st

from stats_engine.models.regression import run_ols, run_logit
from stats_engine.interpret import attach_coach_to_model


def _binary_numeric_columns(df):
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    binary_cols = []
    for col in numeric_cols:
        vals = set(df[col].dropna().unique().tolist())
        if vals and vals <= {0, 1}:
            binary_cols.append(col)
    return numeric_cols, binary_cols


st.title("Models")

if "df" not in st.session_state:
    st.session_state["df"] = None
if "models" not in st.session_state:
    st.session_state["models"] = []

if st.session_state["df"] is None:
    st.warning("Load data in the Data page first.")
    st.stop()

df = st.session_state["df"]

numeric_cols, binary_cols = _binary_numeric_columns(df)
all_cols = df.columns.tolist()

st.subheader("OLS Regression")
st.caption("OLS accepts numeric and categorical predictors. Identifier-style fields are usually poor analytic predictors even if the model can fit them.")
y = st.selectbox("Outcome (numeric)", numeric_cols, key="ols_y")
xs = st.multiselect(
    "Predictors",
    [c for c in all_cols if c != y],
    key="ols_xs",
    help="Numeric and categorical predictors are supported. Avoid identifier columns like student_id.",
)
if st.button("Run OLS"):
    if xs:
        try:
            result = run_ols(df, y, xs)
            result = attach_coach_to_model(result)
            st.session_state["models"].append(result)
            st.success("OLS model added")
        except Exception as exc:
            st.error(f"OLS failed: {exc}")
    else:
        st.error("Select at least one predictor.")

st.subheader("Logistic Regression")
st.caption("Logistic regression requires a binary numeric outcome coded as 0/1.")
if binary_cols:
    y2 = st.selectbox("Outcome (binary 0/1)", binary_cols, key="logit_y")
    xs2 = st.multiselect(
        "Predictors",
        [c for c in all_cols if c != y2],
        key="logit_xs",
        help="Numeric and categorical predictors are supported. Avoid identifier columns like student_id.",
    )
    if st.button("Run Logistic"):
        if xs2:
            try:
                result = run_logit(df, y2, xs2)
                result = attach_coach_to_model(result)
                st.session_state["models"].append(result)
                st.success("Logistic model added")
            except Exception as exc:
                st.error(f"Logistic regression failed: {exc}")
        else:
            st.error("Select at least one predictor.")
else:
    st.info("No binary 0/1 numeric columns are available yet for logistic regression.")

st.subheader("Model Results")
for m in st.session_state["models"]:
    st.json(m)
    coach = m.get("coach", {})
    if coach:
        st.markdown("**Model Spec**")
        st.write(coach.get("model_spec"))
        st.markdown("**Effect Sizes**")
        st.write(coach.get("effect_size_summary"))
        st.markdown("**Diagnostics**")
        st.write(coach.get("diagnostics_summary"))
        st.markdown("**Interpretation**")
        st.write(coach.get("interpretation_text"))
        st.markdown("**Limitations**")
        st.write(coach.get("limitations"))
        st.markdown("**Next Steps**")
        st.write(coach.get("next_steps"))
