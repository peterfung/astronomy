
import re, sys, os
import matplotlib.pyplot as plt

reg = re.compile('(.*)  (.*)')
#处理噪音样本
raw_noise_freq, raw_noise_sign = [], []
with open(sys.argv[1]) as f:
    for line in f:
        result = reg.match(line)
        if result:
            f, s = result.groups()
            raw_noise_freq.append(float(f))
            raw_noise_sign.append(float(s))
#取最小的20%的均值作为底噪
sorted_raw_noise_sign = sorted(raw_noise_sign)
least_per_20_len = round(len(sorted_raw_noise_sign)*0.2)
least_per_20 = sorted_raw_noise_sign[:least_per_20_len]
min_noise_sign = 0 if len(least_per_20) == 0 else sum(least_per_20)/len(least_per_20)
#取频率的误差步长
index, step_list = 1, []
sorted_raw_noise_freq = sorted(raw_noise_freq)
while index < len(sorted_raw_noise_freq):
    step_list.append(sorted_raw_noise_freq[index] - sorted_raw_noise_freq[index-1])
    index += 1
freq_step = 0 if len(step_list) == 0 else sum(step_list)/len(step_list)
freq_step = 1 * freq_step


freq_xy, sign_xy = [], []
if len(sys.argv) >= 3 :
    for file in sys.argv:
        if file == sys.argv[0] or file == sys.argv[1]:
            continue
        try:
            raw_data_freq, raw_data_sign = [], []
            with open(file) as f:
                for line in f:
                    result = reg.match(line)
                    if result:
                        f, s = result.groups()
                        raw_data_freq.append(float(f))
                        raw_data_sign.append(float(s))
            freq_xy.append(max(raw_data_freq))
            freq_xy.append(min(raw_data_freq))
            sign_xy.append(max(raw_data_sign))
            sign_xy.append(min(raw_data_sign))
        except:
            print('无法打开文件：',file)
            sys.exit()
        #取最小的20%的均值作为底噪
        sorted_raw_data_sign = sorted(raw_data_sign)
        least_per_20_len = round(len(sorted_raw_data_sign)*0.2)
        least_per_20 = sorted_raw_data_sign[:least_per_20_len]
        min_data_sign = 0 if len(least_per_20) == 0 else sum(least_per_20)/len(least_per_20)
        gap = min_data_sign - min_noise_sign
        new_noise_sign = [x+gap for x in raw_noise_sign]
        new_data_sign = []
        flag_idx = 0
        for data_idx, data_val in enumerate(raw_data_freq):
            max_sign = min_data_sign
            for noise_idx, noise_val in enumerate(raw_noise_freq):
                if noise_idx < flag_idx:
                    continue
                if noise_val > data_val + freq_step:
                    break
                if noise_val < data_val - freq_step:
                    flag_idx = noise_idx
                    continue
                # print('noise---',noise_idx, noise_val,max_sign, new_noise_sign[noise_idx])
                max_sign = max(max_sign, new_noise_sign[noise_idx])
            
            new_sign = raw_data_sign[data_idx]-max_sign+0 if raw_data_sign[data_idx]-max_sign>=0 else 0
            new_data_sign.append(new_sign)
        label = os.path.basename(file).split('.')[0]
        plt.plot(raw_data_freq, new_data_sign, label=label)
    axis_density = 10 #坐标轴密度
    xmax, xmin = max(freq_xy), min(freq_xy)
    ymax, ymin = max(sign_xy), 0
    xlist = [xmin + i*(xmax-xmin)/axis_density for i in range(axis_density+1)]
    ylist = [ymin + i*(ymax-ymin)/axis_density for i in range(axis_density+1)]
    plt.legend(loc='upper left')
    plt.xlabel('frequency')
    plt.ylabel('signal')
    plt.xticks(xlist)
    plt.yticks(ylist)
    plt.show()
else:
    print('''使用方法：
    python noise_reduction.py 噪音样本.txt [数据.txt ...]
    python 版本>=3.6
    运行后弹出绘图窗口，关闭该窗口后程序自动退出
    ''')