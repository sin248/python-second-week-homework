# 导入基础绘图库
import matplotlib.pyplot as plt
# 导入数值数组库，构建相关性矩阵
import numpy as np
# 导入seaborn库，对matplotlib二次封装，热力图更美观简洁
import seaborn as sns

# 全局绘图风格配置，同上统一科研规范
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 12
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.bbox"] = "tight"

# 手动构建5行5列的特征相关系数矩阵，数值范围-1~1
# 对角线全为1：自身和自己相关性为1
corr_matrix = np.array([
    [1.0, 0.82, 0.12, -0.05, 0.33],
    [0.82, 1.0, 0.21, 0.03, 0.41],
    [0.12, 0.21, 1.0, 0.75, 0.22],
    [-0.05, 0.03, 0.75, 1.0, 0.18],
    [0.33, 0.41, 0.22, 0.18, 1.0]
])
# 行列对应的特征名称
cols = ["Feature1","Feature2","Feature3","Feature4","Feature5"]

# 创建画布，宽7高6
fig, ax = plt.subplots(figsize=(7, 6))

# ====================== 绘制热力图核心函数 ======================
sns.heatmap(
    corr_matrix,        # 输入的相关系数矩阵数据
    annot=True,         # True：每个格子内显示具体数值
    fmt=".2f",          # 数值格式：保留2位小数
    cmap="RdBu_r",      # 配色方案：红蓝反向，红色正相关，蓝色负相关，科研标准配色
    vmin=-1, vmax=1,    # 颜色条数值上下限固定为-1到1，符合相关系数定义
    xticklabels=cols,   # X轴刻度文字
    yticklabels=cols,   # Y轴刻度文字
    ax=ax               # 指定画在我们提前创建好的ax坐标轴上
)

# 设置热力图标题
ax.set_title("Feature Correlation Heatmap")
import os
save_path = r"C:\Users\86159\Desktop\04"
# 保存矢量文件
plt.savefig(os.path.join(save_path, "热力图.pdf"))
# 保存图片
plt.savefig(os.path.join(save_path, "热力图.png"))
# 弹出窗口查看热力图
plt.show()