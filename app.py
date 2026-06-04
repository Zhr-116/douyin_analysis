import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="抖音数据分析中心", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# 自定义 CSS（保持不变，略写核心）
st.markdown("""
<style>
    .stApp { background-color: #0a0e17; }
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

# ==================== 核心样式函数 ====================
def set_style(fig, x_title=None, y_title=None, title=None, log_y=False, x_tickformat=None, y_tickformat=None):
    """统一设置图表样式，支持分别指定 X/Y 轴的刻度格式"""
    if title:
        fig.update_layout(title=title)
    if x_title:
        fig.update_xaxes(title_text=x_title)
    if y_title:
        fig.update_yaxes(title_text=y_title)

    # 如果未指定特定格式，则使用默认的千位分隔整数格式（适合大数值）
    default_tick = ',.0f'
    x_tick = x_tickformat if x_tickformat is not None else default_tick
    y_tick = y_tickformat if y_tickformat is not None else default_tick

    fig.update_xaxes(tickformat=x_tick, showgrid=True, gridwidth=0.5, gridcolor='gray')
    fig.update_yaxes(tickformat=y_tick, showgrid=True, gridwidth=0.5, gridcolor='gray')

    if log_y:
        fig.update_yaxes(type='log')

    fig.update_layout(
        paper_bgcolor='#1e2438',
        plot_bgcolor='#1e2438',
        font={'family': 'Arial, SimHei', 'size': 12}
    )
    return fig

# ==================== 加载数据 ====================
@st.cache_data
def load_all_data():
    base_dir = Path(__file__).parent
    user_df = pd.read_csv(base_dir / "src/core/processed/user_analysis.csv")
    author_df = pd.read_csv(base_dir / "src/core/processed/author_analysis.csv")
    video_df = pd.read_csv(base_dir / "src/core/processed/video_analysis.csv")
    return user_df, author_df, video_df

user_df, author_df, video_df = load_all_data()

# 平均点赞率（排除播放量为0的视频）
valid_ratio = video_df[video_df['播放量'] > 0]['点赞播放比']
avg_like_rate = valid_ratio.mean() if not valid_ratio.empty else 0.0
avg_like_rate_display = f"{avg_like_rate:.4%}" if avg_like_rate >= 0.0001 else f"{avg_like_rate:.6f} (比率)"

# ==================== 侧边栏 ====================
st.sidebar.title("📌 导航菜单")
menu = st.sidebar.radio("", ["🏠 核心指标", "👥 用户洞察", "✍️ 作者洞察", "🎬 作品洞察", "🔥 高级分析"])
st.sidebar.markdown("---")
current_date = datetime.now().strftime("%Y-%m-%d")
st.sidebar.caption(f"数据更新：{current_date} | 基于170万条记录")

# ==================== 核心指标页 ====================
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
        fig = px.bar(user_df.nlargest(10, "总浏览量"), x="uid", y="总浏览量", color="总浏览量")
        fig = set_style(fig, x_title="用户ID", y_title="总浏览量", title="用户浏览量 TOP10")
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        fig = px.histogram(user_df, x="完播率", nbins=20)
        fig = set_style(fig, x_title="完播率", y_title="用户数", title="完播率分布", x_tickformat='.0%')
        st.plotly_chart(fig, use_container_width=True)

# ==================== 用户洞察 ====================
elif menu == "👥 用户洞察":
    st.header("👥 用户行为分析")
    st.caption("浏览量、点赞量、完播率及城市覆盖")
    min_views = st.sidebar.slider("筛选最小浏览量", 0, int(user_df["总浏览量"].max()), 0)
    filtered = user_df[user_df["总浏览量"] >= min_views]

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(filtered.nlargest(10, "总浏览量"), x="uid", y="总浏览量", color="总浏览量")
        fig = set_style(fig, x_title="用户ID", y_title="总浏览量", title="用户总浏览量 TOP10")
        st.plotly_chart(fig, use_container_width=True)

        fig = px.histogram(filtered, x="完播率", nbins=20)
        fig = set_style(fig, x_title="完播率", y_title="用户数", title="完播率分布", x_tickformat='.0%')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(filtered, x="总点赞数", nbins=30)
        fig = set_style(fig, x_title="点赞量", y_title="用户数", title="点赞量分布", log_y=True)
        st.plotly_chart(fig, use_container_width=True)

        if "观看城市数" in filtered.columns:
            fig = px.histogram(filtered, x="观看城市数", nbins=15)
            fig = set_style(fig, x_title="观看过的城市数量", y_title="用户数", title="观看城市数分布")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("观看城市数数据暂缺")

# ==================== 作者洞察 ====================
elif menu == "✍️ 作者洞察":
    st.header("✍️ 作者特征分析")
    st.caption("发布作品数、创作活跃度、作品时长及地理跨度")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(author_df.nlargest(10, "发布作品数"), x="author_id", y="发布作品数", color="发布作品数")
        fig = set_style(fig, x_title="作者ID", y_title="发布作品数", title="作者发布作品数 TOP10")
        st.plotly_chart(fig, use_container_width=True)

        fig = px.histogram(author_df, x="作品平均时长", nbins=30)
        fig = set_style(fig, x_title="作品平均时长（秒）", y_title="作者数", title="作品平均时长分布")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(author_df, x="创作活跃度(日均发布)", nbins=30)
        fig = set_style(fig, x_title="日均发布作品数", y_title="作者数", title="创作活跃度分布")
        st.plotly_chart(fig, use_container_width=True)

        if "去过城市数" in author_df.columns:
            fig = px.histogram(author_df, x="去过城市数", nbins=20)
            fig = set_style(fig, x_title="去过城市数", y_title="作者数", title="去过城市数分布")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("活跃度散点图：发布作品数 vs 总获赞")
    fig = px.scatter(author_df, x="发布作品数", y="总获赞", hover_data=["author_id"])
    fig = set_style(fig, x_title="发布作品数", y_title="总获赞数", title="作者活跃度分析")
    st.plotly_chart(fig, use_container_width=True)

# ==================== 作品洞察 ====================
elif menu == "🎬 作品洞察":
    st.header("🎬 作品表现分析")
    st.caption("点赞率、播放量分布、热门城市及背景音乐")

    city_list = ["全部"] + list(video_df["发布城市"].value_counts().head(10).index)
    selected_city = st.sidebar.selectbox("筛选发布城市（仅作用于本页）", city_list)
    filtered = video_df if selected_city == "全部" else video_df[video_df["发布城市"] == selected_city]

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(filtered.nlargest(10, "点赞播放比"), x="item_id", y="点赞播放比", color="点赞播放比")
        fig = set_style(fig, x_title="作品ID", y_title="点赞播放比", title="作品点赞播放比 TOP10")
        st.plotly_chart(fig, use_container_width=True)

        fig = px.histogram(filtered, x="播放量", nbins=50)
        fig = set_style(fig, x_title="播放量", y_title="作品数", title="播放量分布", log_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(filtered, x="点赞量", nbins=50)
        fig = set_style(fig, x_title="点赞量", y_title="作品数", title="点赞量分布", log_y=True)
        st.plotly_chart(fig, use_container_width=True)

        city_counts = filtered["发布城市"].value_counts().head(8)
        fig = px.pie(values=city_counts.values, names=city_counts.index, title="发布城市 TOP8")
        fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438", font=dict(family="Arial, SimHei", size=12))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("热门背景音乐 TOP10")
    bgm_counts = filtered["背景音乐ID"].value_counts().head(10)
    fig = px.bar(x=bgm_counts.index.astype(str), y=bgm_counts.values, color=bgm_counts.values)
    fig = set_style(fig, x_title="音乐ID", y_title="使用次数", title="背景音乐使用次数 TOP10")
    st.plotly_chart(fig, use_container_width=True)

# ==================== 高级分析 ====================
elif menu == "🔥 高级分析":
    st.header("高级分析")
    st.caption("多维度数据探索：相关性、时间活跃度")

    tab1, tab2 = st.tabs(["📈 相关性分析", "⏰ 时间活跃度"])

    with tab1:
        numeric_cols = video_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        exclude = ['item_id', 'Unnamed: 0', 'uid', 'author_id', 'music_id']
        numeric_cols = [c for c in numeric_cols if c not in exclude]

        if len(numeric_cols) < 2:
            st.warning("数值列不足，无法进行相关性分析。")
        else:
            st.subheader("📈 全局相关性热力图")
            corr_all = video_df[numeric_cols].corr()
            fig = px.imshow(corr_all, text_auto='.2f', aspect='auto', title="所有指标相关性矩阵",
                            color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
            fig.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438", height=600,
                              font=dict(family="Arial, SimHei"))
            st.plotly_chart(fig, use_container_width=True)

            # 最强相关性对表格
            corr_tri = corr_all.where(np.triu(np.ones(corr_all.shape), k=1).astype(bool))
            pairs = corr_tri.unstack().dropna().sort_values(key=abs, ascending=False).head(5).reset_index()
            pairs.columns = ["指标1", "指标2", "相关系数"]
            st.subheader("🌟 全局最强相关性对")
            st.dataframe(pairs.style.format({'相关系数': '{:.3f}'}), use_container_width=True)

            st.markdown("---")
            st.subheader("🔍 自定义指标分析")
            selected = st.multiselect("选择特定指标（至少2个）", numeric_cols, default=numeric_cols[:4])
            if len(selected) >= 2:
                corr_sub = video_df[selected].corr()
                fig2 = px.imshow(corr_sub, text_auto='.2f', aspect='auto', title="自定义指标热力图",
                                 color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
                fig2.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438", height=500,
                                   font=dict(family="Arial, SimHei"))
                st.plotly_chart(fig2, use_container_width=True)

                if len(selected) <= 5:
                    st.subheader("散点图矩阵")
                    fig3 = px.scatter_matrix(video_df[selected], dimensions=selected, opacity=0.3)
                    fig3.update_layout(paper_bgcolor="#1e2438", plot_bgcolor="#1e2438",
                                       font=dict(family="Arial, SimHei", size=10))
                    st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.subheader("用户活跃时段分析")
        st.caption("基于170万条浏览记录，分析用户观看行为的时间分布")
        hourly_path = Path("src/core/processed/hourly_activity.csv")
        weekly_path = Path("src/core/processed/weekly_activity.csv")
        if hourly_path.exists() and weekly_path.exists():
            hourly = pd.read_csv(hourly_path)
            weekly = pd.read_csv(weekly_path)

            col1, col2 = st.columns(2)
            with col1:
                fig = px.line(hourly, x='hour', y='total_views', markers=True)
                fig = set_style(fig, x_title="小时", y_title="总浏览量", title="每小时浏览量分布")
                st.plotly_chart(fig, use_container_width=True)
                peak_hour = hourly.loc[hourly['total_views'].idxmax(), 'hour']
                st.caption(f"💡 浏览高峰出现在 **{peak_hour}:00**，建议创作者此时段前后发布内容。")
            with col2:
                weekday_names = {0:'周一',1:'周二',2:'周三',3:'周四',4:'周五',5:'周六',6:'周日'}
                weekly['weekday_name'] = weekly['weekday'].map(weekday_names)
                fig = px.bar(weekly, x='weekday_name', y='total_views', color='total_views')
                fig = set_style(fig, x_title="星期", y_title="总浏览量", title="按星期浏览量分布")
                st.plotly_chart(fig, use_container_width=True)
                peak_weekday = weekly.loc[weekly['total_views'].idxmax(), 'weekday_name']
                st.caption(f"💡 一周中 **{peak_weekday}** 浏览量最高，可加大运营投入。")
        else:
            st.warning("未找到时间分析数据，请先运行 python main.py 生成预计算结果。")