import matplotlib.pyplot as plt
from pathlib import Path

# 解决中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def generate_all_charts(user_df, author_df, video_df, output_dir="images"):
    """
    生成所有可视化图表（满足作业全部指标）
    """
    images_dir = Path(output_dir)
    images_dir.mkdir(exist_ok=True)

    # ==================== 1. 用户维度 ====================
    # 1.1 用户总浏览量 TOP10
    plt.figure(figsize=(10, 6))
    top10_user = user_df.sort_values("总浏览量", ascending=False).head(10)
    plt.bar(top10_user["uid"].astype(str), top10_user["总浏览量"], color="#4CAF50")
    plt.title("用户总浏览量 TOP10", fontsize=16)
    plt.xlabel("用户ID")
    plt.ylabel("总浏览量")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(images_dir / "user_top10_views.png", dpi=300)
    plt.close()

    # 1.2 用户点赞量分布
    plt.figure(figsize=(10, 6))
    plt.hist(user_df["总点赞数"], bins=30, color="#FF5722", edgecolor="black")
    plt.title("用户点赞量分布", fontsize=16)
    plt.xlabel("点赞量")
    plt.ylabel("用户数")
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig(images_dir / "user_likes_distribution.png", dpi=300)
    plt.close()

    # 1.3 用户完播率分布
    plt.figure(figsize=(10, 6))
    plt.hist(user_df["完播率"], bins=20, color="#2196F3", edgecolor="black")
    plt.title("用户完播率分布", fontsize=16)
    plt.xlabel("完播率")
    plt.ylabel("用户数")
    plt.tight_layout()
    plt.savefig(images_dir / "user_completion_rate.png", dpi=300)
    plt.close()

    # 1.4 用户观看城市数分布
    plt.figure(figsize=(10, 6))
    plt.hist(user_df["观看城市数"], bins=20, color="#00BCD4", edgecolor="black")
    plt.title("用户观看城市数分布", fontsize=16)
    plt.xlabel("观看过的城市数量")
    plt.ylabel("用户数")
    plt.tight_layout()
    plt.savefig(images_dir / "user_cities_distribution.png", dpi=300)
    plt.close()

    # ==================== 2. 作者维度 ====================
    # 2.1 作者发布作品数 TOP10
    plt.figure(figsize=(10, 6))
    top10_author = author_df.sort_values("发布作品数", ascending=False).head(10)
    plt.bar(top10_author["author_id"].astype(str), top10_author["发布作品数"], color="#FF9800")
    plt.title("作者发布作品数 TOP10", fontsize=16)
    plt.xlabel("作者ID")
    plt.ylabel("发布作品数")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(images_dir / "author_top10_posts.png", dpi=300)
    plt.close()

    # 2.2 作者作品平均时长分布
    plt.figure(figsize=(10, 6))
    plt.hist(author_df["作品平均时长"], bins=30, color="#795548", edgecolor="black")
    plt.title("作者作品平均时长分布", fontsize=16)
    plt.xlabel("平均时长（秒）")
    plt.ylabel("作者数")
    plt.tight_layout()
    plt.savefig(images_dir / "author_avg_duration.png", dpi=300)
    plt.close()

    # 2.3 作者创作活跃度（日均发布作品数）分布
    plt.figure(figsize=(10, 6))
    plt.hist(author_df["创作活跃度(日均发布)"], bins=30, color="#9E9E9E", edgecolor="black")
    plt.title("作者创作活跃度分布", fontsize=16)
    plt.xlabel("日均发布作品数")
    plt.ylabel("作者数")
    plt.tight_layout()
    plt.savefig(images_dir / "author_activity_daily.png", dpi=300)
    plt.close()

    # 2.4 作者去过城市数分布
    plt.figure(figsize=(10, 6))
    plt.hist(author_df["去过城市数"], bins=20, color="#FFC107", edgecolor="black")
    plt.title("作者去过城市数分布", fontsize=16)
    plt.xlabel("去过城市数量")
    plt.ylabel("作者数")
    plt.tight_layout()
    plt.savefig(images_dir / "author_cities_count.png", dpi=300)
    plt.close()

    # 2.5 作者活跃度散点图（发布数 vs 总获赞）
    plt.figure(figsize=(10, 6))
    plt.scatter(author_df["发布作品数"], author_df["总获赞"], color="#E91E63", alpha=0.6)
    plt.title("作者活跃度：发布数 vs 总获赞", fontsize=16)
    plt.xlabel("发布作品数")
    plt.ylabel("总获赞数")
    plt.tight_layout()
    plt.savefig(images_dir / "author_activity_scatter.png", dpi=300)
    plt.close()

    # ==================== 3. 作品维度 ====================
    # 3.1 作品点赞播放比 TOP10
    plt.figure(figsize=(10, 6))
    top10_video = video_df.sort_values("点赞播放比", ascending=False).head(10)
    plt.bar(top10_video["item_id"].astype(str), top10_video["点赞播放比"], color="#9C27B0")
    plt.title("作品点赞播放比 TOP10", fontsize=16)
    plt.xlabel("作品ID")
    plt.ylabel("点赞播放比")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(images_dir / "video_top10_like_ratio.png", dpi=300)
    plt.close()

    # 3.2 作品播放量分布（直方图展示浏览量）
    plt.figure(figsize=(10, 6))
    plt.hist(video_df["播放量"], bins=50, color="#3F51B5", edgecolor="black")
    plt.title("作品播放量分布", fontsize=16)
    plt.xlabel("播放量")
    plt.ylabel("作品数")
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig(images_dir / "video_views_distribution.png", dpi=300)
    plt.close()

    # 3.3 作品点赞量分布
    plt.figure(figsize=(10, 6))
    plt.hist(video_df["点赞量"], bins=50, color="#E91E63", edgecolor="black")
    plt.title("作品点赞量分布", fontsize=16)
    plt.xlabel("点赞量")
    plt.ylabel("作品数")
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig(images_dir / "video_likes_distribution.png", dpi=300)
    plt.close()

    # 3.4 发布城市饼图 TOP8
    plt.figure(figsize=(10, 8))
    city_counts = video_df["发布城市"].value_counts().head(8)
    plt.pie(city_counts.values, labels=city_counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("作品发布城市分布（TOP8）", fontsize=16)
    plt.tight_layout()
    plt.savefig(images_dir / "video_city_distribution.png", dpi=300)
    plt.close()

    # 3.5 背景音乐 TOP10（柱状图）
    bgm_counts = video_df["背景音乐ID"].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    plt.bar(bgm_counts.index.astype(str), bgm_counts.values, color="#00BCD4")
    plt.title("作品使用背景音乐 TOP10", fontsize=16)
    plt.xlabel("背景音乐ID")
    plt.ylabel("作品数量")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(images_dir / "top_bgm.png", dpi=300)
    plt.close()

    print(f"✅ 所有图表已保存到 {images_dir}/ 文件夹，共生成 14 张图表")