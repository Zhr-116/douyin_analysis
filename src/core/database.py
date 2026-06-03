import sqlite3
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    """SQLite数据库存储，适配分析结果"""
    def __init__(self, db_path: str = "./douyin_analysis.db"):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self._init_tables()

    def _init_tables(self):
        """初始化数据表"""
        cursor = self.conn.cursor()
        # 用户分析表
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_analysis (
                            uid TEXT PRIMARY KEY,
                            总浏览量 REAL,
                            总点赞数 REAL,
                            观看作品数 INTEGER,
                            观看城市数 INTEGER,
                            完播率 REAL,
                            平均点赞率 REAL
                        )''')
        # 作者分析表
        cursor.execute('''CREATE TABLE IF NOT EXISTS author_analysis (
                            author_id TEXT PRIMARY KEY,
                            发布作品数 INTEGER,
                            总获赞 REAL,
                            作品平均时长 REAL,
                            去过城市数 INTEGER,
                            创作活跃度 REAL
                        )''')
        # 作品分析表
        cursor.execute('''CREATE TABLE IF NOT EXISTS video_analysis (
                            item_id TEXT PRIMARY KEY,
                            播放量 REAL,
                            点赞量 REAL,
                            发布城市 TEXT,
                            背景音乐ID TEXT,
                            点赞播放比 REAL
                        )''')
        self.conn.commit()
        logger.info("数据库表初始化完成")

    def save_analysis(self, df: pd.DataFrame, table_name: str):
        """保存分析结果到数据库"""
        df.to_sql(table_name, self.conn, if_exists="replace", index=False)
        logger.info(f"{table_name} 数据已保存")

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

if __name__ == "__main__":
    # 读取分析结果
    user_df = pd.read_csv("./processed/user_analysis.csv")
    author_df = pd.read_csv("./processed/author_analysis.csv")
    video_df = pd.read_csv("./processed/video_analysis.csv")

    # 保存到数据库
    db = Database()
    db.save_analysis(user_df, "user_analysis")
    db.save_analysis(author_df, "author_analysis")
    db.save_analysis(video_df, "video_analysis")
    db.close()
    print("✅ 所有分析结果已保存到数据库")