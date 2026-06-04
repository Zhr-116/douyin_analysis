import sys
from pathlib import Path
import pandas as pd

# 检查 cleaned_data.csv 是否存在，如果不存在则运行数据清洗
from core.data_loader import run_data_loader
cleaned_path = Path("src/core/processed/cleaned_data.csv")
if not cleaned_path.exists():
    run_data_loader()

# 添加 src 到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "src"))
from visualization.charts import generate_all_charts
from core.analysis_functions import AnalysisFunctions
from advanced.correlation import correlation_analysis

def main():
    print("=" * 60)
    print("抖音数据分析系统启动")
    print("=" * 60)

    # 1. 加载数据（自动读取 src/core/processed/cleaned_data.csv）
    try:
        analyzer = AnalysisFunctions()
        print("✅ 数据加载成功")
    except FileNotFoundError as e:
        print(f"❌ 数据加载失败：{e}")
        print("请确认 src/core/processed/cleaned_data.csv 存在")
        return

    # 2. 用户维度分析
    print("\n--- 用户行为分析 ---")
    user_df = analyzer.analyze_user_behavior()
    print(f"用户数：{len(user_df)}")

    # 3. 作者维度分析
    print("\n--- 作者特征分析 ---")
    author_df = analyzer.analyze_author_characteristics()
    print(f"作者数：{len(author_df)}")

    # 4. 作品维度分析
    print("\n--- 作品表现分析 ---")
    video_df = analyzer.analyze_video_performance()
    print(f"作品数：{len(video_df)}")

    # 5. 保存结果（类内部也会保存，这里再存一次确保）
    analyzer.save_result(user_df, "user_analysis.csv")
    analyzer.save_result(author_df, "author_analysis.csv")
    analyzer.save_result(video_df, "video_analysis.csv")

    # 生成所有可视化图表
    print("\n--- 生成可视化图表 ---")
    generate_all_charts(user_df, author_df, video_df, output_dir="images")

    # 6. 高级分析：相关性热力图
    print("\n--- 高级分析：相关性热力图 ---")
    correlation_analysis(analyzer.df)

    # ========== 预计算高级分析结果 ==========
    print("\n--- 预计算时间活跃度分析 ---")
    # 时间分析：需要原始 cleaned_data.csv（包含 real_time 和浏览行为）
    try:
        # 注意：cleaned_data.csv 的路径可能需要调整，这里假设在 src/core/processed/ 下
        raw_df = pd.read_csv("src/core/processed/cleaned_data.csv")
        # 提取小时和星期
        raw_df['real_time'] = pd.to_datetime(raw_df['real_time'], errors='coerce')
        raw_df['hour'] = raw_df['real_time'].dt.hour
        raw_df['weekday'] = raw_df['real_time'].dt.dayofweek  # 0=周一
        # 按小时统计浏览量（Unnamed: 0 代表浏览量）
        hourly = raw_df.groupby('hour')['Unnamed: 0'].sum().reset_index()
        hourly.columns = ['hour', 'total_views']
        # 按星期统计
        weekly = raw_df.groupby('weekday')['Unnamed: 0'].sum().reset_index()
        weekly.columns = ['weekday', 'total_views']
        # 保存结果
        hourly.to_csv("src/core/processed/hourly_activity.csv", index=False)
        weekly.to_csv("src/core/processed/weekly_activity.csv", index=False)
        print("✅ 时间活跃度分析完成，已保存 hourly_activity.csv 和 weekly_activity.csv")
    except Exception as e:
        print(f"⚠️ 时间活跃度分析失败：{e}")


    print("\n" + "=" * 60)
    print("全部完成！结果保存在 src/core/processed/ 目录下")
    print("相关性热力图已保存为 correlation_heatmap.png")
    print("=" * 60)

if __name__ == "__main__":
    main()