import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """适配你路径的抖音数据加载与清洗模块"""

    def __init__(self, raw_path: str = "./douyin_dataset.csv"):
        self.raw_path = Path(raw_path)
        self.processed_dir = Path("./processed")
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def load_large_csv(self) -> pd.DataFrame:
        logger.info("开始加载170万条数据...")
        if not self.raw_path.exists():
            raise FileNotFoundError(f"找不到数据文件，请检查路径：{self.raw_path.resolve()}")

        chunk_list = []
        for chunk in pd.read_csv(self.raw_path, chunksize=100000):
            chunk_list.append(chunk)
        df = pd.concat(chunk_list, ignore_index=True)
        logger.info(f"加载完成，数据量：{len(df):,}行")
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("开始数据清洗...")
        # 先复制一份数据，避免 SettingWithCopyWarning
        df = df.copy()

        # 去重
        df = df.drop_duplicates(subset=["item_id", "uid", "date"])
        # 缺失值填充（现在不会有警告了）
        df["user_city"] = df["user_city"].fillna("未知")
        df["item_city"] = df["item_city"].fillna("未知")
        df["music_id"] = df["music_id"].fillna("无背景音乐")
        # 删除关键列缺失的行
        df = df.dropna(subset=["uid", "item_id", "author_id", "like", "duration_time"])
        # 时间格式转换
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        logger.info("清洗完成")
        return df

    def save_processed(self, df: pd.DataFrame, filename: str = "cleaned_data.csv"):
        """改成保存为CSV格式，不用依赖pyarrow"""
        save_path = self.processed_dir / filename
        df.to_csv(save_path, index=False)
        logger.info(f"清洗后数据已保存：{save_path.resolve()}")
        return str(save_path)

def run_data_loader():
    """供外部调用的数据清洗入口，生成 cleaned_data.csv"""
    print("未找到清洗后的数据文件，正在运行数据清洗...")
    loader = DataLoader()
    raw_df = loader.load_large_csv()
    clean_df = loader.clean_data(raw_df)
    loader.save_processed(clean_df)
    print("数据清洗完成，已保存 cleaned_data.csv。")

    # ==================== 保留独立运行入口 ====================
if __name__ == "__main__":
    run_data_loader()
