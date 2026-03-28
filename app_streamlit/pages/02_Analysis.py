import streamlit as st
import pandas as pd

from stats_engine import describe_dataframe, correlation_matrix, generate_basic_plots
from stats_engine.tests.group_tests import t_test, chi_square
from stats_engine.interpret import attach_coach_to_test


@st.cache_data(show_spinner=False)
def _cached_summary(df):
    return describe_dataframe(df)


@st.cache_data(show_spinner=False)
def _cached_correlation(df):
    return correlation_matrix(df)


@st.cache_data(show_spinner=False)
def _cached_plots(df):
    return generate_basic_plots(df)


st.title("Analysis")

if "df" not in st.session_state:
    st.session_state["df"] = None
if "tests" not in st.session_state:
    st.session_state["tests"] = []

if st.session_state["df"] is None:
    st.warning("Load data in the Data page first.")
    st.stop()

df = st.session_state["df"]

st.subheader("EDA Summary")
summary = _cached_summary(df)
numeric_summary = summary.get("numeric", {})
categorical_summary = summary.get("categorical_top_counts", {})
if numeric_summary:
    st.markdown("**Numeric Summary**")
    st.dataframe(
        st.session_state["df"].select_dtypes(include=["number"]).describe().transpose(),
        use_container_width=True,
    )
if categorical_summary:
    st.markdown("**Categorical Top Counts**")
    cat_frames = []
    for col, counts in categorical_summary.items():
        for value, count in counts.items():
            cat_frames.append({"column": col, "value": value, "count": count})
    st.dataframe(cat_frames, use_container_width=True)

st.subheader("Correlation Matrix")
corr = _cached_correlation(df)
if corr.get("columns"):
    corr_df = pd.DataFrame(corr["matrix"], columns=corr["columns"], index=corr["columns"])
    st.dataframe(corr_df, use_container_width=True)
else:
    st.info("At least two numeric columns are needed to display a correlation matrix.")

st.subheader("Plots")
st.caption("Use the EDA summary and correlation matrix above alongside these charts so interpretation does not depend on color or visuals alone.")
plots = _cached_plots(df)
plot_columns = st.columns(2)
for idx, p in enumerate(plots):
    with plot_columns[idx % 2]:
        st.markdown(f"**{p['title']}**")
        st.plotly_chart(p["fig"], use_container_width=True)

st.subheader("Run Hypothesis Tests")

numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
cat_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

with st.expander("t-test (numeric by 2 groups)"):
    y = st.selectbox("Value column", numeric_cols, key="ttest_y")
    g = st.selectbox("Group column", cat_cols, key="ttest_g")
    if st.button("Run t-test"):
        result = t_test(df, y, g)
        result = attach_coach_to_test(result)
        st.session_state["tests"].append(result)
        st.success("t-test added")

with st.expander("Chi-square (categorical x categorical)"):
    x = st.selectbox("Column X", cat_cols, key="chisq_x")
    y2 = st.selectbox("Column Y", cat_cols, key="chisq_y")
    if st.button("Run chi-square"):
        result = chi_square(df, x, y2)
        result = attach_coach_to_test(result)
        st.session_state["tests"].append(result)
        st.success("chi-square added")

st.subheader("Test Results")
for t in st.session_state["tests"]:
    st.expander(f"Raw result: {t.get('test_name', 'test')}").json(t)
    coach = t.get("coach", {})
    if coach:
        st.markdown("**Methods**")
        st.write(coach.get("methods_text"))
        st.markdown("**Interpretation**")
        st.write(coach.get("interpretation_text"))
        st.markdown("**Limitations**")
        st.write(coach.get("limitations"))
        st.markdown("**Next Steps**")
        st.write(coach.get("next_steps"))
