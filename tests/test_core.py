import pytest
import pandas as pd
from src.core.data_loader import DataLoader
from src.core.analysis_functions import AnalysisFunctions
from src.core.database import Database

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "user_id": ["u1","u2","u1"],
        "author_id": ["a1","a2","a1"],
        "video_id": ["v1","v2","v3"],
        "view": [100,200,300],
        "like": [10,20,30],
        "user_city": ["北京","上海","北京"],
        "author_city": ["深圳","广州","深圳"],
        "bgm": ["bgm1","bgm2","bgm1"],
        "publish_time": pd.date_range("2024-01-01", periods=3),
        "watch_time": pd.date_range("2024-01-01", periods=3)
    })

def test_user_analysis(sample_df):
    res = AnalysisFunctions.analyze_user_behavior(sample_df)
    assert list(res.columns)[:5] == ["user_id","总浏览量","总点赞数","观看作品数","活跃天数"]

def test_author_analysis(sample_df):
    res = AnalysisFunctions.analyze_author_characteristics(sample_df)
    assert "均赞" in res.columns

def test_video_analysis(sample_df):
    res = AnalysisFunctions.analyze_video_performance(sample_df)
    assert "点赞播放比" in res.columns

def test_db_save_read(sample_df):
    db = Database(":memory:")
    db.save_to_db(sample_df, "test")
    df_back = db.read_from_db("test")
    assert len(df_back) == len(sample_df)