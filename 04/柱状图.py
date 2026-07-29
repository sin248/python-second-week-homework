# 导入绘图库
import matplotlib.pyplot as plt
# 导入数值库（本文件少量使用，统一规范导入）
import numpy as np
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 12
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.bbox"] = "tight"

# 创建画布，尺寸宽7高5
fig, ax = plt.subplots(figsize=(7, 5))

# X轴类别：4个不同模型名称
models = ["CNN", "LSTM", "Transformer", "GNN"]
# 对应每个模型的测试准确率数值
acc = [0.82, 0.85, 0.91, 0.89]

# 绘制柱状图，width柱子宽度0.6，返回柱子对象bars用于后续加数字
bars = ax.bar(models, acc, width=0.6)

# 循环遍历每一根柱子，在柱子顶部标注具体数值（科研图加分项）
for bar in bars:
    # 获取当前柱子的高度（也就是准确率数值）
    height = bar.get_height()
    # 在柱子水平居中位置，高度+0.005防止贴住柱子，写入保留两位小数的数字
    # ha="center" 水平居中对齐
    ax.text(bar.get_x()+bar.get_width()/2, height+0.005, f"{height:.2f}", ha="center")

# 设置Y轴显示范围，下限0.75，上限0.95，避免柱子顶到边框
ax.set_ylim(0.75, 0.95)
# Y轴名称
ax.set_ylabel("Test Accuracy")
# 图表标题
ax.set_title("Accuracy of Different Models")
import os
save_path = r"C:\Users\86159\Desktop\04"
# 保存矢量图
plt.savefig(os.path.join(save_path, "柱状图.pdf"))
# 保存图片
plt.savefig(os.path.join(save_path, "柱状图.png"))
# 弹窗看图
plt.show()