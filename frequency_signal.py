
import re, sys, os
import matplotlib.pyplot as plt
reg = re.compile('(.*)  (.*)')
totalf, totals= [], []
if len(sys.argv) >= 2 :
    for file in sys.argv:
        if file == sys.argv[0]:
            continue
        try:
            frequency = []
            signal = []
            with open(file) as f:
                for line in f:
                    result = reg.match(line)
                    if result:
                        f, s = result.groups()
                        frequency.append(float(f))
                        signal.append(float(s))
            totalf += frequency
            totals += signal
        except:
            print('无法打开文件：',file)
            sys.exit()
        label = os.path.basename(file).split('.')[0]
        plt.plot(frequency, signal, label=label)
    xmin, xmax = min(totalf), max(totalf)
    ymin, ymax = min(totals), max(totals)
    axis_density = 10 #坐标轴密度
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
    python frequency_signal.py xxx.txt [yyy.txt ...]
    python 版本>=3.6
    运行后弹出绘图窗口，关闭该窗口后程序自动退出
    ''')