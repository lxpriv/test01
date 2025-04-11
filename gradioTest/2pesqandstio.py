import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 示例评分数据
data = {
    'audio_file': ['audio01.wav', 'audio02.wav', 'audio03.wav', 'audio04.wav', 'audio05.wav',
'audio06.wav', 'audio07.wav', 'audio08.wav', 'audio09.wav', 'audio10.wav',
'audio11.wav', 'audio12.wav', 'audio13.wav', 'audio14.wav', 'audio15.wav',
'audio16.wav', 'audio17.wav', 'audio18.wav', 'audio19.wav', 'audio20.wav'],
    # 'pesq_score': [3.12, 2.45, 2.98, 3.29, 2.51,
    #                3.14, 2.86, 3.47, 2.68, 3.05,
    #                3.32, 2.74, 2.97, 3.21, 2.59,
    #                3.34, 2.77, 2.91, 3.18, 2.63],
    # 'stoi_score': [0.67, 0.74, 0.66, 0.72, 0.77,
    #                0.68, 0.75, 0.71, 0.73, 0.69,
    #                0.76, 0.70, 0.78, 0.65, 0.74,
    #                0.72, 0.66, 0.77, 0.68, 0.73]
'pesq_score': [2.03, 1.82, 2.68, 3.14, 1.75, 2.94, 3.01, 1.89, 2.36, 1.94, 2.47, 3.11, 1.65, 2.58, 3.20, 1.72, 2.76, 2.04, 2.49, 1.87
],
    'stoi_score': [0.57, 0.60, 0.62, 0.59, 0.63, 0.56, 0.61, 0.64, 0.58, 0.57, 0.61, 0.62, 0.60, 0.63, 0.58, 0.56, 0.59, 0.61, 0.64, 0.60
]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 统计分析
pesq_mean = df['pesq_score'].mean()
pesq_std = df['pesq_score'].std()
stoi_mean = df['stoi_score'].mean()
stoi_std = df['stoi_score'].std()

print(f"PESQ Mean: {pesq_mean}, PESQ Std: {pesq_std}")
print(f"STOI Mean: {stoi_mean}, STOI Std: {stoi_std}")

# 可视化分析

# 设置Seaborn风格
sns.set(style="whitegrid")

# 创建一个2x1的图形区域
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# PESQ评分分布箱线图
sns.boxplot(x='pesq_score', data=df, ax=axes[0])
axes[0].set_title('PESQ Score Distribution')
axes[0].set_xlabel('PESQ Score')

# STOI评分分布箱线图
sns.boxplot(x='stoi_score', data=df, ax=axes[1])
axes[1].set_title('STOI Score Distribution')
axes[1].set_xlabel('STOI Score')

# 显示图形
plt.tight_layout()
plt.show()

# 评分比较柱状图
df_melted = df.melt(id_vars=['audio_file'], value_vars=['pesq_score', 'stoi_score'],
                    var_name='score_type', value_name='score')

plt.figure(figsize=(10, 6))
sns.barplot(x='audio_file', y='score', hue='score_type', data=df_melted)
plt.title('PESQ and STOI Scores Comparison')
plt.xlabel('Audio File')
plt.ylabel('Score')
plt.show()
