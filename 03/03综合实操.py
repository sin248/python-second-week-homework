# 1. 正确导入pandas库
import pandas as pd

# 2. 读取Excel文件（路径r原始字符串保留不变）
df = pd.read_excel(r"C:/Users/86159/Desktop/赵佳瑞week1/工作表.xlsx")

# 3. 去重
df = df.drop_duplicates()

# 4. 缺失值填充：年龄列用均值填充空值
df["年龄"] = df["年龄"].fillna(df["年龄"].mean())

# 5. 四分位数剔除学号异常值（IQR箱线法）
Q1, Q3 = df["学号"].quantile([0.25, 0.75])
IQR = Q3 - Q1
df = df[(df["学号"] >= Q1 - 1.5*IQR) & (df["学号"] <= Q3 + 1.5*IQR)]

# 6. 分组统计（兼容所有pandas版本写法）
stat = df.groupby("年龄").agg(
    人数=("姓名", "count"),
    平均学号=("学号", "mean")
)

print("清洗后分组统计结果：")
print(stat)