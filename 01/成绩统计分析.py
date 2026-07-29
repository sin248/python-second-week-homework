#班级 5 名学生，3 门科目成绩矩阵，计算每科平均分、最高分、每位学生总分、筛选总分高于 240 的学生
import numpy as np

# 5学生3科目成绩
scores = np.array([
    [85, 92, 78],
    [90, 88, 95],
    [76, 80, 82],
    [93, 89, 91],
    [88, 79, 85]
])

# 1. 每门科目平均分（按列）
avg_subject = np.mean(scores, axis=0)
print("各科平均分：", avg_subject)

# 2. 每科最高分
max_subject = np.max(scores, axis=0)
print("各科最高分：", max_subject)

# 3. 每位学生总分（按行）
student_sum = np.sum(scores, axis=1)
print("学生总分：", student_sum)

# 4. 筛选总分>240的学生成绩
high = scores[student_sum > 240]
print("总分240以上学生成绩：\n", high)