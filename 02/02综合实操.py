import pandas as pd
import os

# 1. 创建表格
data = {
    "姓名":["张三","李四","王五","赵六","钱七"],
    "语文":[78,95,82,90,66],
    "数学":[85,72,91,88,75],
    "班级":["一班","二班","一班","二班","一班"]
}
df = pd.DataFrame(data)

# 2. 查看基础信息
print("表格形状：", df.shape)
print("数值统计：")
print(df.describe())

# 3. 取单列
print("\n全部语文成绩：")
print(df["语文"])

# 4. 条件筛选：一班，语文大于80
res = df[(df["班级"]=="一班") & (df["语文"]>80)]
print("\n一班语文80分以上学生：")
print(res)

# 5. loc筛选指定列
print("\n筛选姓名、数学两列：")
print(df.loc[:, ["姓名","数学"]])

# 6. 保存数据到csv
df.to_csv(r"C:\Users\86159\Desktop\02\学生成绩.csv", index=False, encoding="utf-8")
print(os.path.abspath(r"C:\Users\86159\Desktop\02\学生成绩.csv"))