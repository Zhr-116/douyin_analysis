import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="抖音数据分析中心",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义 CSS（增强对比度，修复卡片溢出） ====================
st.markdown("""
<style>
    .stApp { background-color: #0a0e17; }
    /* 卡片容器 */
    .css-1r6slb0, div[data-testid="stMetric"], div[data-testid="stPlotlyChart"] {
        background-color: #1e2438 !important;
        border-radius: 20px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #2d3450;
        box-shadow: 0 6px 14px rgba(0,0,0,0.4);
        overflow: hidden;
        width: 100%;
    }
    .css-1d391kg { background-color: #0a0e17; border-right: 1px solid #2d3450; }
    h1, h2, h3, p, .stMarkdown, label { color: #eef2ff !important; }
    .stMetric .stMetricValue { font-size: 2.2rem !important; font-weight: 600; color: #ffb347 !important; }
    .stMetric .stMetricLabel { color: #a0aec0 !important; font-size: 0.9rem; }
    .stRadio label, .stSelectbox label { color: #eef2ff !important; }
    .stButton button { background-color: #2d3450; color: white; border-radius: 12px; }
    .stButton button:hover { background-color: #4a5a8c; }
</style>
""", unsafe_allow_html=True)

# ==================== 辅助函数：统一中文标签 ====================
def apply_chinese_labels(fig, x_title=None, y_title=None, title=None):
    """为 plotly 图表添加中文轴标题和字体"""
    if title:
        fig.update_layout(title=title)
    fig.update_layout(
        xaxis_title=x_title if x_title else fig.layout.xaxis.title.text,
        yaxis_title=y_title if y_title else fig.layout.yaxis.title.text,
        font=dict(family="Microsoft YaHei, SimHei, sans-serif", size=12)
    )
    return fig

# ==================== 加载数据 ====================
@st.cache_data
def load_all_data():
    base_dir = Path(__file__).parent
    user_path = base_dir / "src/core/processed/user_analysis.csv"
    author_path = base_dir / "src/core/processed/author_analysis.csv"
    video_path = base_dir / "src/core/processed/video_analysis.csv"
    user_df = pd.read_csv(user_path)
    author_df = pd.read_csv(author_path)
    video_df = pd.read_csv(video_path)
    return user_df, author_df, video_df

try:
    user_df, author_df, video_df = load_all_data()
except Exception as e:
    st.error(f"数据加载失败：{e}\n请先运行 python main.py 生成分析结果。")
    st.stop()

# 平均点赞率显示（避免显示0.00%）
avg_like_rate = video_df["点赞播放比"].mean()
if avg_like_rate < 0.0001:
    avg_like_rate_display = f"{avg_like_rate:.6f} (比率)"
else:
    avg_like_rate_display = f"{avg_like_rate:.4%}"

@st.cache_data
def compute_global_correlation(video_df, numeric_cols_tuple):
    """计算并缓存全局相关性矩阵，numeric_cols_tuple 用于 hash"""
    return video_df[list(numeric_cols_tuple)].corr()

# ==================== 侧边栏 ====================
st.sidebar.title("📌 导航菜单")
menu = st.sidebar.radio(
    "",
    ["🏠 核心指标", "👥 用户洞察", "✍️ 作者洞察", "🎬 作品洞察", "🔥 高级分析"]
)
st.sidebar.markdown("---")
st.sidebar.caption("数据更新：2025-06-02 | 基于170万条记录")

# ==================== 首页：核心指标 ====================
if menu == "🏠 核心指标":
    st.title("抖音创作者数据中心")
    st.caption("实时分析用户、作者、作品三维度核心指标")

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("总用户数", f"{len(user_df):,}")
    with col2: st.metric("总作者数", f"{len(author_df):,}")
    with col3: st.metric("总作品数", f"{len(video_df):,}")
    with col4: st.metric("平均点赞率", avg_like_rate_display)

    col5, col6, col7, col8 = st.columns(4)
    with col5: st.metric("总播放量", f"{video_df['播放量'].sum():,.0f}")
    with col6: st.metric("总点赞量", f"{video_df['点赞量'].sum():,.0f}")
    with col7: st.metric("平均完播率", f"{user_df['完播率'].mean():.2%}")
    with col8: st.metric("热门发布城市", video_df["发布城市"].value_counts().index[0])

    st.subheader("数据速览")
    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.bar(user_df.nlargest(10, "总浏览量"), x="uid", y="总浏览量",
                     color="总浏览量", color_continuous_scale="Blues")
        fig = apply_chinese_labels(fig, x_title="用户ID", y_title="总浏览量", title="用户浏览量 TOP10")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        fig = px.histogram(user_df, x="完播率", nbins=20, color_discrete_sequence=["#4CAF50"])
        fig = apply_chinese_labels(fig, x_title="完播率", y_title="用户数", title="完播率分布")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
        st.plotly_chart(fig, use_container_width=True)

# ==================== 用户洞察 ====================
elif menu == "👥 用户洞察":
    st.header("👥 用户行为分析")
    st.caption("浏览量、点赞量、完播率及城市覆盖")
    min_views = st.sidebar.slider("筛选最小浏览量", int(user_df["总浏览量"].min()), int(user_df["总浏览量"].max()), 0)
    filtered_user = user_df[user_df["总浏览量"] >= min_views]

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(filtered_user.nlargest(10, "总浏览量"), x="uid", y="总浏览量", color="总浏览量", color_continuous_scale="Blues")
        fig = apply_chinese_labels(fig, x_title="用户ID", y_title="总浏览量", title="用户总浏览量 TOP10")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
        st.plotly_chart(fig, use_container_width=True)

        fig = px.histogram(filtered_user, x="完播率", nbins=20, color_discrete_sequence=["#4CAF50"])
        fig = apply_chinese_labels(fig, x_title="完播率", y_title="用户数", title="完播率分布")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(filtered_user, x="总点赞数", nbins=30, color_discrete_sequence=["#FF5722"])
        fig = apply_chinese_labels(fig, x_title="点赞量", y_title="用户数（对数坐标）", title="点赞量分布")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438", yaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)

        if "观看城市数" in filtered_user.columns:
            fig = px.histogram(filtered_user, x="观看城市数", nbins=15, color_discrete_sequence=["#00BCD4"])
            fig = apply_chinese_labels(fig, x_title="观看过的城市数量", y_title="用户数", title="观看城市数分布")
            fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("观看城市数数据暂缺")

# ==================== 作者洞察 ====================
elif menu == "✍️ 作者洞察":
    st.header("✍️ 作者特征分析")
    st.caption("发布作品数、创作活跃度、作品时长及地理跨度")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(author_df.nlargest(10, "发布作品数"), x="author_id", y="发布作品数", color="发布作品数", color_continuous_scale="Oranges")
        fig = apply_chinese_labels(fig, x_title="作者ID", y_title="发布作品数", title="作者发布作品数 TOP10")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
        st.plotly_chart(fig, use_container_width=True)

        fig = px.histogram(author_df, x="作品平均时长", nbins=30, color_discrete_sequence=["#795548"])
        fig = apply_chinese_labels(fig, x_title="作品平均时长（秒）", y_title="作者数", title="作品平均时长分布")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(author_df, x="创作活跃度(日均发布)", nbins=30, color_discrete_sequence=["#9E9E9E"])
        fig = apply_chinese_labels(fig, x_title="日均发布作品数", y_title="作者数", title="创作活跃度分布")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
        st.plotly_chart(fig, use_container_width=True)

        if "去过城市数" in author_df.columns:
            fig = px.histogram(author_df, x="去过城市数", nbins=20, color_discrete_sequence=["#FFC107"])
            fig = apply_chinese_labels(fig, x_title="去过城市数", y_title="作者数", title="去过城市数分布")
            fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("活跃度散点图：发布作品数 vs 总获赞")
    fig = px.scatter(author_df, x="发布作品数", y="总获赞", color="发布作品数", size="总获赞", hover_data=["author_id"])
    fig = apply_chinese_labels(fig, x_title="发布作品数", y_title="总获赞数", title="作者活跃度分析")
    fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
    st.plotly_chart(fig, use_container_width=True)

# ==================== 作品洞察 ====================
elif menu == "🎬 作品洞察":
    st.header("🎬 作品表现分析")
    st.caption("点赞率、播放量分布、热门城市及背景音乐")

    city_list = ["全部"] + list(video_df["发布城市"].value_counts().head(10).index)
    selected_city = st.sidebar.selectbox("筛选发布城市（仅作用于本页）", city_list)
    filtered_video = video_df if selected_city == "全部" else video_df[video_df["发布城市"] == selected_city]

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(filtered_video.nlargest(10, "点赞播放比"), x="item_id", y="点赞播放比", color="点赞播放比", color_continuous_scale="Purples")
        fig = apply_chinese_labels(fig, x_title="作品ID", y_title="点赞播放比", title="作品点赞播放比 TOP10")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
        st.plotly_chart(fig, use_container_width=True)

        fig = px.histogram(filtered_video, x="播放量", nbins=50, color_discrete_sequence=["#3F51B5"])
        fig = apply_chinese_labels(fig, x_title="播放量", y_title="作品数（对数坐标）", title="播放量分布")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438", yaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(filtered_video, x="点赞量", nbins=50, color_discrete_sequence=["#E91E63"])
        fig = apply_chinese_labels(fig, x_title="点赞量", y_title="作品数（对数坐标）", title="点赞量分布")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438", yaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)

        city_counts = filtered_video["发布城市"].value_counts().head(8)
        fig = px.pie(values=city_counts.values, names=city_counts.index, title="发布城市 TOP8")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438", font=dict(family="Microsoft YaHei, SimHei", size=12))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("热门背景音乐 TOP10")
    bgm_counts = filtered_video["背景音乐ID"].value_counts().head(10)
    fig = px.bar(x=bgm_counts.index.astype(str), y=bgm_counts.values, color=bgm_counts.values, color_continuous_scale="Teal")
    fig = apply_chinese_labels(fig, x_title="音乐ID", y_title="使用次数", title="背景音乐使用次数 TOP10")
    fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438")
    st.plotly_chart(fig, use_container_width=True)

# ==================== 高级分析 ====================
elif menu == "🔥 高级分析":
    st.header("相关性分析")
    st.caption("基于作品维度的指标相关性（播放量、点赞量、完播率等）")

    numeric_cols = video_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    exclude = ['item_id', 'Unnamed: 0', 'uid', 'author_id', 'music_id']
    numeric_cols = [c for c in numeric_cols if c not in exclude]

    if len(numeric_cols) >= 2:
        # 使用缓存计算全局相关性
        with st.spinner("正在计算全局相关性矩阵..."):
            corr_all = compute_global_correlation(video_df, tuple(numeric_cols))
        st.subheader("📈 全局相关性热力图")
        fig = px.imshow(corr_all, text_auto='.2f', aspect='auto',
                        title="所有指标相关性矩阵", color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438", font_color="white", height=600)
        st.plotly_chart(fig, use_container_width=True)

        # 最强相关性对（全局）
        corr_tri_all = corr_all.where(np.triu(np.ones(corr_all.shape), k=1).astype(bool))
        corr_pairs_all = corr_tri_all.unstack().dropna()
        corr_pairs_all = corr_pairs_all.sort_values(key=abs, ascending=False)
        top_global = corr_pairs_all.head(5).reset_index()
        top_global.columns = ["指标1", "指标2", "相关系数"]
        st.subheader("🌟 全局最强相关性对")
        st.dataframe(top_global.style.format({'相关系数': '{:.3f}'}), use_container_width=True)

        st.markdown("---")
        st.subheader("🔍 自定义指标分析")
        selected_cols = st.multiselect("选择特定指标（至少2个）", numeric_cols, default=numeric_cols[:4])


        if len(selected_cols) >= 2:
            corr_sub = video_df[selected_cols].corr()
            fig2 = px.imshow(corr_sub, text_auto='.2f', aspect='auto',
                             title="自定义指标热力图", color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
            fig2.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438", font_color="white", height=500)
            st.plotly_chart(fig2, use_container_width=True)

            # 子集最强相关性对
            corr_tri_sub = corr_sub.where(np.triu(np.ones(corr_sub.shape), k=1).astype(bool))
            corr_pairs_sub = corr_tri_sub.unstack().dropna()
            corr_pairs_sub = corr_pairs_sub.sort_values(key=abs, ascending=False)
            top_sub = corr_pairs_sub.head(5).reset_index()
            top_sub.columns = ["指标1", "指标2", "相关系数"]
            st.subheader("📌 自定义指标最强相关性对")
            st.dataframe(top_sub.style.format({'相关系数': '{:.3f}'}), use_container_width=True)

            if len(selected_cols) <= 5:
                st.subheader("散点图矩阵")
                fig3 = px.scatter_matrix(video_df[selected_cols], dimensions=selected_cols, opacity=0.3)
                fig3.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438", font_color="white")
                st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("请至少选择两个指标进行自定义分析。")