import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisFunctions:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.processed_dir = self.script_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        self.data_path = self.processed_dir / "cleaned_data.csv"
        if not self.data_path.exists():
            raise FileNotFoundError(f"找不到数据文件：{self.data_path.resolve()}\n请先运行 data_loader.py 生成数据")

        self.df = pd.read_csv(self.data_path, encoding="utf-8")
        logger.info(f"✅ 加载数据：{len(self.df):,}行")
        logger.info(f"📋 数据列名：{list(self.df.columns)}")

    def analyze_user_behavior(self):
        """用户维度：浏览量、点赞数、观看城市数、完播率"""
        logger.info("开始用户行为分析...")
        user_df = self.df.groupby("uid").agg(
            总浏览量=("Unnamed: 0", "sum"),
            总点赞数=("like", "sum"),
            观看作品数=("item_id", "nunique"),
            观看城市数=("user_city", "nunique"),
            完播作品数=("finish", "sum"),
            常看背景音乐=("music_id", lambda x: x.mode()[0] if not x.mode().empty else "无")
        ).reset_index()

        user_df["完播率"] = (user_df["完播作品数"] / user_df["观看作品数"]).fillna(0)
        user_df["平均点赞率"] = (user_df["总点赞数"] / user_df["总浏览量"]).fillna(0)
        logger.info("✅ 用户行为分析完成")
        return user_df

    def analyze_author_characteristics(self):
        """作者维度：作品时长、发布数、活跃度、去过城市数"""
        logger.info("开始作者特征分析...")
        author_df = self.df.groupby("author_id").agg(
            发布作品数=("item_id", "nunique"),
            总获赞=("like", "sum"),
            总播放=("Unnamed: 0", "sum"),
            作品平均时长=("duration_time", "mean"),
            去过城市数=("item_city", "nunique"),
            首发日期=("date", "min"),
            末次发布=("date", "max")
        ).reset_index()

        author_df["创作天数"] = (pd.to_datetime(author_df["末次发布"]) - pd.to_datetime(author_df["首发日期"])).dt.days + 1
        author_df["创作活跃度(日均发布)"] = (author_df["发布作品数"] / author_df["创作天数"]).fillna(0)
        logger.info("✅ 作者特征分析完成")
        return author_df

    def analyze_video_performance(self):
        """作品维度：点赞量、浏览量、背景音乐、发布城市"""
        logger.info("开始作品表现分析...")
        video_df = self.df.groupby("item_id").agg(
            播放量=("Unnamed: 0", "first"),
            点赞量=("like", "first"),
            发布城市=("item_city", "first"),
            背景音乐ID=("music_id", "first"),
            发布日期=("date", "first"),
            观看人数=("uid", "nunique")
        ).reset_index()

        video_df["点赞播放比"] = (video_df["点赞量"] / video_df["播放量"]).fillna(0)
        logger.info("✅ 作品表现分析完成")
        return video_df

    def save_result(self, df: pd.DataFrame, filename: str):
        save_path = self.processed_dir / filename
        df.to_csv(save_path, index=False, encoding="utf-8-sig")
        logger.info(f"📁 文件已保存：{save_path.resolve()}")

if __name__ == "__main__":
    print("=" * 50)
    print("          抖音数据分析程序开始运行")
    print("=" * 50)

    try:
        analyzer = AnalysisFunctions()

        user_analysis = analyzer.analyze_user_behavior()
        author_analysis = analyzer.analyze_author_characteristics()
        video_analysis = analyzer.analyze_video_performance()

        analyzer.save_result(user_analysis, "user_analysis.csv")
        analyzer.save_result(author_analysis, "author_analysis.csv")
        analyzer.save_result(video_analysis, "video_analysis.csv")

        print("\n" + "=" * 50)
        print("✅ 三大维度分析全部完成！")
        print("=" * 50)

    except Exception as e:
        logger.error(f"程序运行失败：{str(e)}", exc_info=True)
        print(f"\n❌ 程序出错：{str(e)}")