from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

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


def show_building_period_data(data, building_no, start, end):
    """
    绘制某个家庭某个时间段的电器使用情况
    :param building_no:
    :param start:
    :param end:
    :return:
    """
    data.set_window(start=start, end=end)
    plt.figure(figsize=(30, 10))
    data.buildings[building_no].elec.plot()
    plt.xlabel("Time")
    plt.show()

def show_building_appliance_period_data(data, building_no, appliance, start, end):
    """
    绘制某个家庭某个时间段的某个电器使用情况
    :param building_no:
    :param start:
    :param end:
    :return:
    """
    data.set_window(start=start, end=end)
    plt.figure(figsize=(30, 10))
    data.buildings[building_no].elec[appliance].plot()
    plt.xlabel("Time")
    plt.show()


def show_pie_appliance_enery_consumption(data, building_no):
    """
    展示一个家庭的电器耗电饼图
    :param data:
    :return:
    """
    elec = data.buildings[building_no].elec
    fraction = elec.submeters().fraction_per_meter().dropna()
    # 画图
    labels = elec.get_labels(fraction.index)
    plt.figure(figsize=(10, 10))
    plt.title("building{}电器耗电分布图".format(building_no))
    fraction.plot(kind='pie', labels=labels)
    plt.show()


def show_top_k_appliance_each_building(data, building_no, k):
    """
    查看building里的用电量排名前五的电器，便于选出公共的电器
    注意building的序号是从1开始的
    注意这里并不是按照从高到低排序的
    :return:
    """
    appliance_list = data.buildings[building_no].elec.submeters().select_top_k(k=k).appliances
    print("************building{}*************".format(building_no))
    for appliance in appliance_list:
        print("building[{}]----{}".format(building_no, appliance.identifier.type))

