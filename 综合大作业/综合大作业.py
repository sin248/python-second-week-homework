# -*- coding: utf-8 -*-
"""
第2周 数据分析综合大作业
功能：数据集自动生成 → 异常值处理 → 数据清洗 → 数据统计 → 可视化绘图
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ========== 全局设置 ==========
# 设置中文字体，防止乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置随机种子，保证结果可复现
np.random.seed(42)

# 输出目录
OUTPUT_DIR = r"C:\Users\86159\Desktop\赵佳瑞week2\综合大作业"


# =====================================================
# 一、数据集自动生成
# =====================================================
def generate_dataset(n_students=200):
    """
    自动生成模拟成绩数据集
    包含：学号、姓名、语文、数学、英语、物理、化学、生物
    """
    print("=" * 60)
    print("【第一步】数据集自动生成")
    print("=" * 60)

    # 生成学号
    student_ids = [f"S{i:04d}" for i in range(1, n_students + 1)]

    # 生成姓名（随机组合）
    surnames = ['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴',
                '徐', '孙', '马', '朱', '胡', '郭', '何', '高', '林', '罗']
    given_names = ['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '军', '洋',
                   '勇', '艳', '杰', '娟', '涛', '明', '超', '秀英', '霞', '平',
                   '刚', '桂英', '文', '辉', '玲', '鑫', '斌', '波', '宇', '浩']
    names = [np.random.choice(surnames) + np.random.choice(given_names)
             for _ in range(n_students)]

    # 生成各科成绩（正态分布，均值75，标准差12，范围0-100）
    # 不同科目设置不同的均值和标准差，模拟真实情况
    subjects = {
        '语文': np.random.normal(loc=78, scale=10, size=n_students),
        '数学': np.random.normal(loc=72, scale=15, size=n_students),
        '英语': np.random.normal(loc=75, scale=12, size=n_students),
        '物理': np.random.normal(loc=70, scale=14, size=n_students),
        '化学': np.random.normal(loc=73, scale=13, size=n_students),
        '生物': np.random.normal(loc=76, scale=11, size=n_students),
    }

    # 限制成绩在 0-100 范围内
    for subject in subjects:
        subjects[subject] = np.clip(subjects[subject], 0, 100).round(1)

    # 构建 DataFrame
    df = pd.DataFrame({
        '学号': student_ids,
        '姓名': names,
        **subjects
    })

    print(f"✓ 成功生成 {n_students} 名学生的成绩数据")
    print(f"✓ 包含科目：{'、'.join(subjects.keys())}")
    print(f"✓ 数据集形状：{df.shape}")
    print("\n前5行数据预览：")
    print(df.head())

    # 保存原始数据
    df.to_csv(os.path.join(OUTPUT_DIR, '原始成绩数据.csv'),
              index=False, encoding='utf-8-sig')
    print("\n✓ 原始数据已保存为：原始成绩数据.csv")

    return df


# =====================================================
# 二、人为制造缺失值与异常值
# =====================================================
def introduce_anomalies(df, missing_rate=0.05, anomaly_rate=0.03):
    """
    人为制造缺失值和异常值
    - missing_rate: 缺失值比例
    - anomaly_rate: 异常值比例
    """
    print("\n" + "=" * 60)
    print("【第二步】人为制造缺失值与异常值")
    print("=" * 60)

    df_dirty = df.copy()
    subject_cols = ['语文', '数学', '英语', '物理', '化学', '生物']

    # --- 制造缺失值 ---
    n_missing = int(len(df) * len(subject_cols) * missing_rate)
    missing_count = 0
    for _ in range(n_missing):
        row_idx = np.random.randint(0, len(df))
        col_idx = np.random.randint(0, len(subject_cols))
        df_dirty.iloc[row_idx, df_dirty.columns.get_loc(subject_cols[col_idx])] = np.nan
        missing_count += 1

    print(f"✓ 已注入缺失值：{missing_count} 个（约 {missing_rate*100:.1f}%）")

    # --- 制造异常值 ---
    # 类型1：超出正常范围的极端值（如负分、超100分）
    n_anomaly_extreme = int(len(df) * len(subject_cols) * anomaly_rate * 0.5)
    for _ in range(n_anomaly_extreme):
        row_idx = np.random.randint(0, len(df))
        col = np.random.choice(subject_cols)
        # 随机生成极端值：要么特别低（负数），要么特别高（>100）
        if np.random.random() > 0.5:
            df_dirty.iloc[row_idx, df_dirty.columns.get_loc(col)] = np.random.uniform(-20, 0)
        else:
            df_dirty.iloc[row_idx, df_dirty.columns.get_loc(col)] = np.random.uniform(101, 150)

    # 类型2：录入错误型异常值（明显不合理的整数，如 999、-1 等）
    n_anomaly_error = int(len(df) * len(subject_cols) * anomaly_rate * 0.5)
    error_values = [999, -1, 0, 1000, -99, 250]
    for _ in range(n_anomaly_error):
        row_idx = np.random.randint(0, len(df))
        col = np.random.choice(subject_cols)
        df_dirty.iloc[row_idx, df_dirty.columns.get_loc(col)] = np.random.choice(error_values)

    total_anomalies = n_anomaly_extreme + n_anomaly_error
    print(f"✓ 已注入异常值：{total_anomalies} 个（约 {anomaly_rate*100:.1f}%）")
    print(f"  - 极端值（超0-100范围）：{n_anomaly_extreme} 个")
    print(f"  - 录入错误型异常值：{n_anomaly_error} 个")

    # 保存脏数据
    df_dirty.to_csv(os.path.join(OUTPUT_DIR, '含异常成绩数据.csv'),
                    index=False, encoding='utf-8-sig')
    print("\n✓ 含异常数据已保存为：含异常成绩数据.csv")

    return df_dirty


# =====================================================
# 三、数据清洗
# =====================================================
def clean_data(df_dirty):
    """
    数据清洗：缺失值检测与填充 + 异常值剔除
    """
    print("\n" + "=" * 60)
    print("【第三步】数据清洗")
    print("=" * 60)

    df_clean = df_dirty.copy()
    subject_cols = ['语文', '数学', '英语', '物理', '化学', '生物']

    # ---- 3.1 缺失值检测 ----
    print("\n--- 3.1 缺失值检测 ---")
    missing_stats = df_clean[subject_cols].isnull().sum()
    missing_total = missing_stats.sum()
    print(f"缺失值总数：{missing_total} 个")
    print("各科缺失值分布：")
    for col in subject_cols:
        print(f"  {col}：{missing_stats[col]} 个")

    # ---- 3.2 缺失值填充（用各科均值填充） ----
    print("\n--- 3.2 缺失值填充（均值填充法）---")
    for col in subject_cols:
        mean_val = df_clean[col].mean()
        n_fill = df_clean[col].isnull().sum()
        df_clean[col] = df_clean[col].fillna(round(mean_val, 1))
        print(f"  {col}：填充 {n_fill} 个缺失值，填充值 = {mean_val:.2f}")

    # ---- 3.3 异常值检测 ----
    print("\n--- 3.3 异常值检测（IQR 方法 + 范围校验）---")

    anomaly_records = []  # 记录异常值信息

    # 方法1：范围校验（成绩必须在 0-100 之间）
    print("\n【范围校验】成绩超出 0-100 范围：")
    for col in subject_cols:
        out_of_range = df_clean[(df_clean[col] < 0) | (df_clean[col] > 100)]
        if len(out_of_range) > 0:
            print(f"  {col}：{len(out_of_range)} 个异常值")
            for idx, row in out_of_range.iterrows():
                anomaly_records.append({
                    '学号': row['学号'],
                    '科目': col,
                    '异常值': row[col],
                    '类型': '超出范围'
                })

    # 方法2：IQR 方法（四分位距法）
    print("\n【IQR 方法】统计学异常值：")
    iqr_anomaly_count = 0
    for col in subject_cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df_clean[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)]
        # 排除已经被范围校验标记的
        iqr_outliers = outliers[
            (outliers[col] >= 0) & (outliers[col] <= 100)
        ]
        if len(iqr_outliers) > 0:
            iqr_anomaly_count += len(iqr_outliers)
            print(f"  {col}：{len(iqr_outliers)} 个 IQR 异常值 "
                  f"（下界={lower_bound:.1f}, 上界={upper_bound:.1f}）")
            for idx, row in iqr_outliers.iterrows():
                anomaly_records.append({
                    '学号': row['学号'],
                    '科目': col,
                    '异常值': row[col],
                    '类型': 'IQR异常'
                })

    print(f"\nIQR 异常值总数：{iqr_anomaly_count} 个")

    # 保存异常值记录
    anomaly_df = pd.DataFrame(anomaly_records)
    if len(anomaly_df) > 0:
        anomaly_df.to_csv(os.path.join(OUTPUT_DIR, '异常值记录.csv'),
                          index=False, encoding='utf-8-sig')
        print(f"\n✓ 异常值记录已保存：异常值记录.csv（共 {len(anomaly_df)} 条）")

    # ---- 3.4 异常值处理（剔除/修正） ----
    print("\n--- 3.4 异常值处理 ---")

    # 策略：超出 0-100 范围的 → 用该科均值替换
    #       IQR 异常但在范围内的 → 保留（可能是真实的极端高分/低分）
    replaced_count = 0
    for col in subject_cols:
        # 找出超出范围的值
        mask = (df_clean[col] < 0) | (df_clean[col] > 100)
        n_replace = mask.sum()
        if n_replace > 0:
            # 用该科中位数替换（中位数比均值更稳健，不受异常值影响）
            median_val = df_clean.loc[~mask, col].median()
            df_clean.loc[mask, col] = round(median_val, 1)
            replaced_count += n_replace
            print(f"  {col}：用中位数 {median_val:.1f} 替换了 {n_replace} 个超范围异常值")

    print(f"\n✓ 共修正 {replaced_count} 个超范围异常值")
    print("✓ IQR 范围内的统计异常值予以保留（可能是真实极端成绩）")

    # 保存清洗后数据
    df_clean.to_csv(os.path.join(OUTPUT_DIR, '清洗后成绩数据.csv'),
                    index=False, encoding='utf-8-sig')
    print(f"\n✓ 清洗后数据已保存：清洗后成绩数据.csv")
    print(f"✓ 清洗后数据形状：{df_clean.shape}")

    return df_clean


# =====================================================
# 四、数据统计
# =====================================================
def analyze_data(df_clean):
    """
    统计各科成绩指标
    """
    print("\n" + "=" * 60)
    print("【第四步】数据统计分析")
    print("=" * 60)

    subject_cols = ['语文', '数学', '英语', '物理', '化学', '生物']

    # ---- 4.1 描述性统计 ----
    print("\n--- 4.1 各科成绩描述性统计 ---")
    stats = df_clean[subject_cols].describe().round(2)
    print(stats)

    # 计算额外统计指标
    print("\n--- 4.2 补充统计指标 ---")
    extra_stats = pd.DataFrame({
        '中位数': df_clean[subject_cols].median().round(2),
        '极差': (df_clean[subject_cols].max() - df_clean[subject_cols].min()).round(2),
        '变异系数': (df_clean[subject_cols].std() / df_clean[subject_cols].mean() * 100).round(2),
        '及格率(≥60)': (df_clean[subject_cols] >= 60).mean().round(4) * 100,
        '优秀率(≥85)': (df_clean[subject_cols] >= 85).mean().round(4) * 100,
        '不及格率(<60)': (df_clean[subject_cols] < 60).mean().round(4) * 100,
    })
    print(extra_stats)

    # ---- 4.3 总分统计 ----
    print("\n--- 4.3 总分统计 ---")
    df_clean['总分'] = df_clean[subject_cols].sum(axis=1).round(1)
    print(f"总分均值：{df_clean['总分'].mean():.2f}")
    print(f"总分中位数：{df_clean['总分'].median():.2f}")
    print(f"总分标准差：{df_clean['总分'].std():.2f}")
    print(f"总分最高分：{df_clean['总分'].max():.1f}")
    print(f"总分最低分：{df_clean['总分'].min():.1f}")

    # ---- 4.4 成绩等级分布 ----
    print("\n--- 4.4 成绩等级分布（按总分）---")

    def get_grade(total):
        if total >= 510:  # 85*6
            return '优秀'
        elif total >= 420:  # 70*6
            return '良好'
        elif total >= 360:  # 60*6
            return '及格'
        else:
            return '不及格'

    df_clean['等级'] = df_clean['总分'].apply(get_grade)
    grade_dist = df_clean['等级'].value_counts().reindex(['优秀', '良好', '及格', '不及格']).fillna(0).astype(int)
    print(grade_dist)

    # ---- 4.5 相关性分析 ----
    print("\n--- 4.5 各科成绩相关性矩阵 ---")
    corr_matrix = df_clean[subject_cols].corr().round(3)
    print(corr_matrix)

    # 保存统计结果
    stats.to_csv(os.path.join(OUTPUT_DIR, '统计结果_描述性统计.csv'),
                 encoding='utf-8-sig')
    extra_stats.to_csv(os.path.join(OUTPUT_DIR, '统计结果_补充指标.csv'),
                       encoding='utf-8-sig')
    corr_matrix.to_csv(os.path.join(OUTPUT_DIR, '统计结果_相关性矩阵.csv'),
                       encoding='utf-8-sig')
    df_clean.to_csv(os.path.join(OUTPUT_DIR, '最终分析数据.csv'),
                    index=False, encoding='utf-8-sig')

    print("\n✓ 统计结果已保存为多个 CSV 文件")

    return df_clean, stats, extra_stats, corr_matrix, grade_dist


# =====================================================
# 五、可视化绘图
# =====================================================
def visualize_data(df_clean, stats, extra_stats, corr_matrix, grade_dist):
    """
    绘制柱状图与相关性热力图
    """
    print("\n" + "=" * 60)
    print("【第五步】可视化绘图")
    print("=" * 60)

    subject_cols = ['语文', '数学', '英语', '物理', '化学', '生物']

    # ---- 图1：各科平均分柱状图 ----
    print("\n--- 绘制图1：各科平均分柱状图 ---")
    fig, ax = plt.subplots(figsize=(10, 6))

    means = df_clean[subject_cols].mean().sort_values(ascending=False)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']

    bars = ax.bar(means.index, means.values, color=colors, edgecolor='white', linewidth=1.5)

    # 在柱子上标注数值
    for bar, val in zip(bars, means.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f'{val:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_title('各科平均成绩对比', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('科目', fontsize=12)
    ax.set_ylabel('平均分', fontsize=12)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    path1 = os.path.join(OUTPUT_DIR, '图1_各科平均分柱状图.png')
    plt.savefig(path1, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已保存：图1_各科平均分柱状图.png")

    # ---- 图2：各科成绩分布柱状图（分组柱状图：均值+中位数）----
    print("\n--- 绘制图2：各科均值与中位数对比柱状图 ---")
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(subject_cols))
    width = 0.35

    means_all = df_clean[subject_cols].mean()
    medians_all = df_clean[subject_cols].median()

    bars1 = ax.bar(x - width / 2, means_all, width, label='平均分',
                   color='#4ECDC4', edgecolor='white', linewidth=1)
    bars2 = ax.bar(x + width / 2, medians_all, width, label='中位数',
                   color='#FF6B6B', edgecolor='white', linewidth=1)

    ax.set_title('各科平均分与中位数对比', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('科目', fontsize=12)
    ax.set_ylabel('分数', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(subject_cols)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    path2 = os.path.join(OUTPUT_DIR, '图2_均值中位数对比柱状图.png')
    plt.savefig(path2, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已保存：图2_均值中位数对比柱状图.png")

    # ---- 图3：相关性热力图 ----
    print("\n--- 绘制图3：成绩相关性热力图 ---")
    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(corr_matrix,
                annot=True,        # 显示数值
                fmt='.3f',         # 数值格式
                cmap='RdBu_r',     # 颜色方案（红蓝渐变）
                center=0,          # 中心值为0
                square=True,       # 正方形格子
                linewidths=1,      # 格子边框宽度
                linecolor='white', # 边框颜色
                cbar_kws={'label': '相关系数', 'shrink': 0.8},
                annot_kws={'size': 12, 'fontweight': 'bold'},
                ax=ax)

    ax.set_title('各科成绩相关性热力图', fontsize=16, fontweight='bold', pad=20)
    ax.tick_params(axis='both', labelsize=11)

    plt.tight_layout()
    path3 = os.path.join(OUTPUT_DIR, '图3_相关性热力图.png')
    plt.savefig(path3, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已保存：图3_相关性热力图.png")

    # ---- 图4：成绩等级分布柱状图 ----
    print("\n--- 绘制图4：成绩等级分布柱状图 ---")
    fig, ax = plt.subplots(figsize=(8, 6))

    grade_colors = ['#2ECC71', '#3498DB', '#F39C12', '#E74C3C']
    bars = ax.bar(grade_dist.index, grade_dist.values,
                  color=grade_colors, edgecolor='white', linewidth=1.5)

    for bar, val in zip(bars, grade_dist.values):
        pct = val / len(df_clean) * 100
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f'{val}人\n({pct:.1f}%)', ha='center', va='bottom',
                fontsize=11, fontweight='bold')

    ax.set_title('学生成绩等级分布', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('等级', fontsize=12)
    ax.set_ylabel('人数', fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    path4 = os.path.join(OUTPUT_DIR, '图4_成绩等级分布柱状图.png')
    plt.savefig(path4, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已保存：图4_成绩等级分布柱状图.png")

    # ---- 图5：各科及格率与优秀率对比 ----
    print("\n--- 绘制图5：各科及格率与优秀率柱状图 ---")
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(subject_cols))
    width = 0.35

    pass_rates = extra_stats['及格率(≥60)']
    excel_rates = extra_stats['优秀率(≥85)']

    bars1 = ax.bar(x - width / 2, pass_rates, width, label='及格率(≥60)',
                   color='#2ECC71', edgecolor='white', linewidth=1)
    bars2 = ax.bar(x + width / 2, excel_rates, width, label='优秀率(≥85)',
                   color='#E74C3C', edgecolor='white', linewidth=1)

    # 标注数值
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=10)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=10)

    ax.set_title('各科及格率与优秀率对比', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('科目', fontsize=12)
    ax.set_ylabel('百分比 (%)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(subject_cols)
    ax.set_ylim(0, 110)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    path5 = os.path.join(OUTPUT_DIR, '图5_及格率优秀率柱状图.png')
    plt.savefig(path5, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已保存：图5_及格率优秀率柱状图.png")

    print("\n✓ 所有图表绘制完成！")
    return [path1, path2, path3, path4, path5]


# =====================================================
# 主函数
# =====================================================
def main():
    print("\n" + "=" * 60)
    print("  第2周 数据分析综合大作业")
    print("  数据集生成 → 异常注入 → 数据清洗 → 统计分析 → 可视化")
    print("=" * 60)

    # 第一步：生成数据集
    df_raw = generate_dataset(n_students=200)

    # 第二步：人为制造缺失值与异常值
    df_dirty = introduce_anomalies(df_raw, missing_rate=0.05, anomaly_rate=0.03)

    # 第三步：数据清洗
    df_clean = clean_data(df_dirty)

    # 第四步：数据统计
    df_final, stats, extra_stats, corr_matrix, grade_dist = analyze_data(df_clean)

    # 第五步：可视化
    image_paths = visualize_data(df_final, stats, extra_stats, corr_matrix, grade_dist)

    # ---- 总结 ----
    print("\n" + "=" * 60)
    print("【作业完成总结】")
    print("=" * 60)
    print(f"""
✅ 已完成全部任务：

1. 数据集自动生成
   - 生成 200 名学生、6 门科目成绩数据
   - 保存文件：原始成绩数据.csv

2. 异常值处理
   - 注入约 5% 缺失值、3% 异常值
   - 保存文件：含异常成绩数据.csv

3. 数据清洗
   - 缺失值检测 + 均值填充
   - 异常值检测（范围校验 + IQR 方法）
   - 超范围异常值用中位数修正
   - 保存文件：清洗后成绩数据.csv、异常值记录.csv

4. 数据统计
   - 描述性统计（均值、标准差、最值等）
   - 补充指标（中位数、变异系数、及格率、优秀率）
   - 相关性分析
   - 保存文件：统计结果_*.csv、最终分析数据.csv

5. 可视化绘图
   - 图1：各科平均分柱状图
   - 图2：均值中位数对比柱状图
   - 图3：相关性热力图
   - 图4：成绩等级分布柱状图
   - 图5：及格率优秀率柱状图

输出目录：{OUTPUT_DIR}
    """)


if __name__ == '__main__':
    main()
