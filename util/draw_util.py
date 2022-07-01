from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

colors_picker = ["#377eb8", "#ff7f00", "#4daf4a", "#f781bf", "#a65628", "#984ea3", "#999999", "#e41a1c", "#dede00"]


def draw_main_with_sub_appliance_power(methods, appliances, main_power, sub_pre_power):
    """
    绘制总表和分设备的对比图
    :param methods: list 所使用的分解算法
    :param appliances: ndarray 所有分设备
    :param main_power: df 实际总表读数
    :param sub_pre_power: dict[str,df] <-> dict['CO',df[fridge,light,...]] 分设备分解读数
    :return:
    """
    for method in methods:
        plt.figure(figsize=(15, 10))
        plt.plot(main_power, color='r', linestyle='-', label='True value')
        for idx, appliance in enumerate(appliances):
            pre_val = sub_pre_power.get(method)[appliance]
            plt.plot(pre_val, color=colors_picker[idx % len(colors_picker)], linestyle='-.', alpha=0.5, label=appliance)
        plt.xticks(rotation=45)
        plt.xlabel("Time")
        plt.ylabel("Power(W)")
        plt.title('{} disaggregate result'.format(method))
        plt.legend(loc='upper left')
        plt.show()


def draw_appliance_disaggregate_result(methods, appliances, sub_true_power, sub_pre_power):
    """
    绘制各个分设备的结果图
    :param methods: list 所使用的分解算法
    :param appliances: ndarray 所有分设备
    :param sub_true_power: df[fridge,light,...] 实际分设备读数
    :param sub_pre_power: dict[str,df] <-> dict['CO',df[fridge,light,...]] 分设备分解读数
    :return:
    """
    for col in appliances:
        true_val = sub_true_power[col]
        plt.figure(figsize=(15, 10))
        plt.plot(true_val, color='r', linestyle='-', label='True value')
        # 如果有多种方法这里一起可以画出来
        for method in methods:
            pre_val = sub_pre_power.get(method)[col]
            plt.plot(pre_val, color='steelblue', linestyle='-.', alpha=0.5, label=method)
        plt.xticks(rotation=45)
        plt.xlabel("Time")
        plt.ylabel("Power(W)")
        plt.title('{} disaggregate result'.format(col))
        plt.legend(loc='upper left')
        plt.show()


def draw_metrics(methods, appliances, metrics, errors):
    """
    绘制各个指标结果图
    :param methods: list 所使用的分解算法
    :param appliances: ndarray 所有分设备
    :param metrics: list 所使用的评价指标
    :param errors: list[df['CO','FHMM']] 指标计算结果
    :return:
    """
    colors_picker_2 = ['#1d87da', '#da701d', '#1ddacf', '#cf1dda']
    for idx_1, metric in enumerate(metrics):
        bar_width = 0.3
        x = np.arange(len(appliances))
        plt.figure(figsize=(8, 6))
        for idx, method in enumerate(methods):
            plt.bar(x + idx * bar_width, errors[idx_1].iloc[:, idx], bar_width,
                    color=colors_picker[idx % len(colors_picker_2)],
                    align='center', label=method)
            for a, b in zip(x + idx * bar_width, errors[idx_1].iloc[:, idx]):
                plt.text(a, b, '%.3f' % b, ha='center', va='bottom', fontsize=8)
        plt.xticks(x + bar_width / 2, appliances)
        plt.xlabel("appliance")
        plt.ylabel("score")
        plt.title(metric.upper())
        plt.legend(loc='upper right')
        plt.show()
