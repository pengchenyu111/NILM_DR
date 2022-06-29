from matplotlib import pyplot as plt
from nilmtk import DataSet
import pandas as  pd

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载数据集
data = DataSet('./redd_low.h5')
data.set_window(start='1-4-2011', end='5-4-2011')
elec = data.buildings[1].elec
fridge = elec['fridge']
print(fridge.available_columns())
df = next(fridge.load())
print(df.head())


def show_pie_appliance_enery_consumption():
    """
    展示每个家庭的电器耗电饼图
    :param data:
    :return:
    """
    for i in range(len(data.buildings)):
        elec = data.buildings[i + 1].elec
        fraction = elec.submeters().fraction_per_meter().dropna()
        # 画图
        labels = elec.get_labels(fraction.index)
        plt.figure(figsize=(10, 10))
        plt.title("building{}电器耗电分布图".format(i + 1))
        fraction.plot(kind='pie', labels=labels)
        plt.show()


def show_top_k_appliance_each_building():
    """
    查看每个building里的用电量排名前五的电器，便于选出公共的电器
    注意building的序号是从1开始的
    注意这里并不是按照从高到低排序的
    :return:
    """
    for i in range(len(data.buildings)):
        appliance_list = data.buildings[i + 1].elec.submeters().select_top_k(k=5).appliances
        print("************building{}*************".format(i + 1))
        for appliance in appliance_list:
            print("building[{}]----{}".format(i + 1, appliance.identifier.type))


def show_building_period_data(building_no, start, end):
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

def show_df():
    fridge_df = next(data.buildings[1].elec['washer dryer'].load())
    print(fridge_df.isna())


# show_pie_appliance_enery_consumption()
show_top_k_appliance_each_building()
#show_building_period_data(building_no=1, start='2011-04-21', end='2011-04-22')
#show_df()