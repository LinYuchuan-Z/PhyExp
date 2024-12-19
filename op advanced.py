import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import subprocess

# 输入：传感器记录文件，xxx.txt
# 输出：该文件记录的周期，运动图像处于y>0的包络线

# 定义m和n的值

def rdfile(filename):
    # 勿动m n
    m = 1  # 第m个元素的索引（从0开始）
    n = 8  # 第n个元素的索引（从0开始）

    # 检查文件是否以.txt结尾
    if not filename.endswith('.txt'):
        filename += '.txt'

    # 构造完整的文件路径
    file_path = os.path.join('.', filename)
    
    # 初始化一个空列表来存储当前文件的二元组
    file_tuples = []
    
    # 打开文件并按行读取内容
    # print(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 移除行尾的换行符并分割行
            elements = line.strip().split()
            
            # 提取第m个和第n个元素，并创建二元组
            if ':' in elements[m][-6:]:
                ind = elements[m][-6:].index(':')
                tmp = (elements[m] + (ind + 1) * '0')[-6:]
            else:
                tmp = elements[m][-6:]
            tuple_ = (tmp, elements[n])
            file_tuples.append(tuple_)
    
    # 将当前文件的二元组列表追加到总列表中
    file_tuples.pop(0)
    file_tuples = list(map(lambda x: (float(x[0]), abs(float(x[1]))), file_tuples))
    print(file_tuples)
    return file_tuples

# 求极值列表
def getT(a: list):
    # 极大值列表
    filtered_elements = [
        a[i] for i in range(1, len(a) - 1)  # 排除列表头尾的元素
        if a[i][1] > a[i - 1][1] and a[i][1] > a[i + 1][1]
    ]

    # 求周期，周期为两个极大值之间的距离乘以2
    Ts = []
    for i in range(1, len(filtered_elements)):
        Ts.append(filtered_elements[i][0] - filtered_elements[i - 1][0])

    # 周期
    return 2 * np.mean(Ts), Ts, filtered_elements

# 绘制包络线并拟合其方程
def draw(max_tuple_list: list):
    x = np.array([point[0] for point in max_tuple_list])
    y = np.array([point[1] for point in max_tuple_list])

    # 定义指数衰减的包络线拟合函数
    def envelope_func(t, omega_0, beta):
        return omega_0 * np.exp(-beta * t)

    # 曲线拟合
    popt, _ = curve_fit(envelope_func, x, y, p0=(max(y), 0.1))  # 初值假设
    omega_0_optimized, beta_optimized = popt

    # 使用拟合参数生成拟合曲线
    y_fit = envelope_func(x, *popt)

    # 绘图
    plt.scatter(x, y, label='Envelope Data', color='blue', alpha=0.6)
    plt.plot(x, y_fit, label=f'Fitted Curve: $\\omega_0={omega_0_optimized:.3f}, \\beta={beta_optimized:.3f}$', color='red', linewidth=2)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Damped Oscillation Envelope and Fitting')
    plt.legend()
    plt.grid()
    plt.show()

    # 输出优化参数
    print(f"Optimized Parameters: \u03c9_0={omega_0_optimized:.3f}, \u03b2={beta_optimized:.3f}")

# main
if __name__ == "__main__":
    filename = input("Enter the filename (without .txt): ")
    data = rdfile(filename)
    period, periods, max_points = getT(data)
    print(f"Detected period: {period}")
    draw(max_points)
