from nilmtk.api import API
from nilmtk.disaggregate import CO
from matplotlib import pyplot as plt

CO_experiment = {
    'power': {'mains': ['apparent', 'active'], 'appliance': ['apparent', 'active']},
    'sample_rate': 6,
    'appliances': ['microwave', 'fridge', 'dish washer', 'washer dryer'],
    'methods': {"CO": CO({})},
    'train': {
        'datasets': {
            'REDD': {
                'path': '../../data/REDD/redd_low.h5',
                'buildings': {
                    1: {
                        'start_time': '2011-04-18',
                        'end_time': '2011-04-30'
                    }
                }
            }
        }
    },
    'test': {
        'datasets': {
            'REDD': {
                'path': '../../data/REDD/redd_low.h5',
                'buildings': {
                    1: {
                        'start_time': '2011-05-01 08:00:00',
                        'end_time': '2011-05-01 09:00:00'
                    }
                }
            }
        },
        'metrics': ['rmse', 'mae', 'nep', 'mr']
    }
}

# 实验
api_res = API(CO_experiment)
appliances = api_res.gt_overall.columns.values
methods = [i for i in api_res.methods]

# 绘制总表和分设备的对比图
colors_picker = ["#377eb8", "#ff7f00", "#4daf4a", "#f781bf", "#a65628", "#984ea3", "#999999", "#e41a1c", "#dede00"]
for method in methods:
    plt.figure(figsize=(15, 10))
    plt.plot(api_res.test_mains[0], color='indianred', linestyle='-', alpha=0.5, label='True value')
    for idx, appliance in enumerate(appliances):
        pre_val = api_res.pred_overall.get(method)[appliance]
        plt.plot(pre_val, color=colors_picker[idx % len(colors_picker)], linestyle='-.', alpha=0.5, label=appliance)
    plt.style.use('ggplot')
    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel("Power(W)")
    plt.title('{} disaggregate result'.format(method))
    plt.legend(loc='upper left')
    plt.show()

# 绘制各个分设备的结果图
for col in appliances:
    true_val = api_res.gt_overall[col]
    plt.figure(figsize=(15, 10))
    plt.plot(true_val, color='indianred', linestyle='-', alpha=0.5, label='True value')
    # 如果有多种方法这里一起可以画出来
    for method in methods:
        pre_val = api_res.pred_overall.get(method)[col]
        plt.plot(pre_val, color='steelblue', linestyle='-.', alpha=0.5, label=method)
    plt.style.use('ggplot')
    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel("Power(W)")
    plt.title('{} disaggregate result'.format(col))
    plt.legend(loc='upper left')
    plt.show()
