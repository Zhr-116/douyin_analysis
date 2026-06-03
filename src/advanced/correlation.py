import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False   # 用来正常显示负号


def correlation_analysis(df):
    """
    计算数值列之间的相关性并绘制热力图
    """
    # 如果数据太大，抽样10%
    if len(df) > 100000:
        df = df.sample(frac=0.1, random_state=42)
        print(f"数据量较大，已抽样 {len(df)} 行进行计算")

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) < 2:
        print("数值列不足，无法进行相关性分析")
        return

    corr_matrix = df[numeric_cols].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f',
                square=True, linewidths=0.5)
    plt.title('抖音数据各指标相关性分析热力图')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=150)
    plt.show()
    print("相关性热力图已保存为 correlation_heatmap.png")

    # 输出最强相关性
    corr_pairs = corr_matrix.unstack().sort_values(key=abs, ascending=False)
    corr_pairs = corr_pairs[corr_pairs != 1].drop_duplicates()
    print("\n最强的几组相关性：")
    for (var1, var2), corr_val in corr_pairs.head(5).items():
        print(f"  {var1} 与 {var2}: {corr_val:.3f}")