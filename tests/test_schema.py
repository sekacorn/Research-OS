import pandas as pd

from stats_engine.schema import infer_schema


def test_infer_schema_basic():
    df = pd.read_csv("data/sample_students.csv")
    schema = infer_schema(df)
    assert "columns" in schema
    assert len(schema["columns"]) == len(df.columns)
