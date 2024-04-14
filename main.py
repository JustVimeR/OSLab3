import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns

filename = "result.txt"

try:
    data = pd.read_csv(filename, header=None, names=['Size'])
except FileNotFoundError:
    print(f"File {filename} not found.")
    exit()

# Підрахунок частот для шкірного унікального розміру
size_counts = data['Size'].value_counts().reset_index()
size_counts.columns = ['Size', 'Frequency']

# Логарифмічний масштаб для частот
size_counts['Log_Frequency'] = np.log10(size_counts['Frequency'])

size_counts['Size'] = size_counts['Size'].apply(lambda x: max(x, 1))

# Побудова гістограми розмірів файлів
plt.figure(figsize=(10, 6))
plt.hist(data['Size'], bins=50, color='blue', log=True)
plt.title('Розподіл розміру файлів')
plt.xlabel('Розмір файлів (байти)')
plt.ylabel('Кількість файлів (логарифмічна шкала)')
plt.grid(True)
plt.show()

# Побудова гістограми частот у логарифмічному масштабі
plt.figure(figsize=(10, 6))
plt.bar(size_counts['Size'].apply(lambda x: f"10^{int(math.log10(x))}"),
        size_counts['Log_Frequency'], color='skyblue')
plt.xlabel('Логарифм розміру файлів')
plt.ylabel('Логарифм частоти')
plt.title('Логарифмічна гістограма частот розмірів файлів')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Боксплот для логарифмічних частот
plt.figure(figsize=(10, 6))
sns.boxplot(x=size_counts['Log_Frequency'], palette="pastel")
plt.xlabel('Логарифм частоти')
plt.title('Боксплот логарифмічних частот')
plt.tight_layout()
plt.show()

# CDF розмірів файлів
cdf = np.cumsum(size_counts['Frequency'].sort_values()) / sum(size_counts['Frequency'])
sorted_sizes = np.sort(size_counts['Size'])
plt.figure(figsize=(10, 6))
plt.plot(sorted_sizes, cdf, marker='.', linestyle='none')
plt.xlabel('Розмір файла')
plt.ylabel('Кумулятивна функція розподілу (CDF)')
plt.title('CDF розмірів файлів')
plt.tight_layout()
plt.show()

# Визначення CDF
size_counts['Cumulative'] = size_counts['Frequency'].cumsum()
size_counts['CDF'] = size_counts['Cumulative'] / size_counts['Frequency'].sum()

# Визначення діапазону розмірів файлів для переважної більшості
target_CDF = 0.8
subset = size_counts[size_counts['CDF'] <= target_CDF]
min_size = subset['Size'].min()
max_size = subset['Size'].max()
percentage = target_CDF * 100

print(f"Переважна більшість файлів ({percentage}%) має розміри у діапазоні від {min_size} до {max_size} байтів.")
