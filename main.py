import sys
from pathlib import Path
from visualization.charts import generate_all_charts

# 检查 cleaned_data.csv 是否存在，如果不存在则运行数据清洗
from core.data_loader import run_data_loader
cleaned_path = Path("src/core/processed/cleaned_data.csv")
if not cleaned_path.exists():
    run_data_loader()

# 添加 src 到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

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

    # 6. 高级分析：相关性热力图（使用原始数据）
    print("\n--- 高级分析：相关性热力图 ---")
    correlation_analysis(analyzer.df)

    print("\n" + "=" * 60)
    print("全部完成！结果保存在 src/core/processed/ 目录下")
    print("相关性热力图已保存为 correlation_heatmap.png")
    print("=" * 60)

if __name__ == "__main__":
    main()