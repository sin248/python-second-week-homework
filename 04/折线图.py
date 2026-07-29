# ====================== 导入库部分 ======================
# 导入绘图核心库，起别名plt，后续所有绘图操作都用plt调用
import matplotlib.pyplot as plt
# 导入数值计算库，用来生成连续x坐标、数组数据
import numpy as np

# ====================== 全局科研绘图参数配置（一次性生效） ======================
# 设置全局字体为黑体SimHei，解决图表中文显示方框乱码问题
plt.rcParams["font.family"] = ["SimHei"]
# 解决坐标轴负数符号显示异常（负号变成小方块）
plt.rcParams["axes.unicode_minus"] = False
# 设置全局文字字号为12号，符合期刊论文规范
plt.rcParams["font.size"] = 12
# 隐藏图表顶部边框，科研图简约风格要求
plt.rcParams["axes.spines.top"] = False
# 隐藏图表右侧边框，只保留左下两条坐标轴
plt.rcParams["axes.spines.right"] = False
# 设置图片分辨率300dpi，期刊投稿硬性要求，清晰度最高
plt.rcParams["figure.dpi"] = 300
# 保存图片时自动裁剪四周多余空白白边，排版更整洁
plt.rcParams["savefig.bbox"] = "tight"

# ====================== 构造模拟实验数据 ======================
# 生成从1到12的整数数组，代表12个月份，作为X轴横坐标
x = np.arange(1, 13)
# 算法A每组对应的准确率Y值
y1 = np.array([2.1, 2.3, 2.8, 3.2, 3.5, 3.6, 3.9, 4.2, 4.5, 4.7, 4.9, 5.1])
# 算法B每组对应的准确率Y值
y2 = np.array([1.8, 2.0, 2.2, 2.5, 2.7, 2.9, 3.0, 3.3, 3.5, 3.6, 3.8, 4.0])

# ====================== 创建画布与绘图容器 ======================
# fig：整个画布；ax：实际画图的坐标轴区域；figsize设置画布宽8高5英寸
fig, ax = plt.subplots(figsize=(8, 5))

# ====================== 绘制第一条折线（算法A） ======================
# x,y1：横纵坐标数据
# color：线条颜色（科研经典蓝色）
# marker="o"：每个数据点画实心圆圈标记
# linewidth=2：线条粗细为2像素，更清晰
# label：图例显示名称
ax.plot(x, y1, color="#1f77b4", marker="o", linewidth=2, label="算法A")

# ====================== 绘制第二条折线（算法B） ======================
# marker="s"：数据点用正方形标记，和A做视觉区分
ax.plot(x, y2, color="#ff7f0e", marker="s", linewidth=2, label="算法B")

# ====================== 坐标轴、标题、辅助元素设置 ======================
# X轴坐标轴标签：月份
ax.set_xlabel("Month")
# Y轴坐标轴标签：准确率
ax.set_ylabel("Accuracy")
# 图表总标题
ax.set_title("Model Accuracy Trend Comparison")
# 显示图例，放在右下角lower right
ax.legend(loc="lower right")
# 绘制背景网格，alpha透明度0.3避免遮挡曲线，虚线样式
ax.grid(alpha=0.3, linestyle="--")

# ====================== 保存图片 + 弹窗展示 ======================
import os
save_path = r"C:\Users\86159\Desktop\04"
# 保存矢量PDF格式，论文插入无损放大，投稿首选
plt.savefig(os.path.join(save_path, "折线图.pdf"))
# 保存PNG高清图片，日常查看使用
plt.savefig(os.path.join(save_path, "折线图.png"))
# 弹出窗口预览绘制好的图表
plt.show()