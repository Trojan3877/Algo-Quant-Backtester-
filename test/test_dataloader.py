import pandas as pd
from src.data.data_loader import DataLoader


def test_load_csv(tmp_path):
    file = tmp_path / "sample.csv"
    file.write_text("Date,Close\n2020-01-01,10\n2020-01-02,11")

    loader = DataLoader()
    df = loader.load_csv(file)

    assert isinstance(df, pd.DataFrame)
    assert "Close" in df.columns
    assert len(df) == 2
