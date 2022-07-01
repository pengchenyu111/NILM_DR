from nilmtk.api import API
from nilmtk.disaggregate import CO
from util.draw_util import draw_main_with_sub_appliance_power, draw_appliance_disaggregate_result, draw_metrics

CO_experiment = {
    'power': {'mains': ['apparent', 'active'], 'appliance': ['apparent', 'active']},
    'sample_rate': 6,
    'appliances': ['microwave', 'fridge', 'dish washer', 'washer dryer', 'sockets', 'light'],
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
                        'end_time': '2011-05-01 11:30:00'
                    }
                }
            }
        },
        'metrics': ['rmse', 'mae', 'sae', 'mr']
    }
}

# 实验
api_res = API(CO_experiment)
appliances = api_res.gt_overall.columns.values  # 分设备列表
methods = [i for i in api_res.methods]  # 分解算法列表
metrics = api_res.metrics  # 评价指标列表
main_power = api_res.test_mains[0]  # 总表读数
sub_true_power = api_res.gt_overall  # 分设备原始读数
sub_pre_power = api_res.pred_overall  # 分设备分解结果
errors = api_res.errors  # 评价指标结果

# 绘制总表和分设备的对比图
# draw_main_with_sub_appliance_power(methods, appliances, main_power, sub_pre_power)

# 绘制各个分设备的结果图
# draw_appliance_disaggregate_result(methods, appliances, sub_true_power, sub_pre_power)

# 绘制各个指标结果图
draw_metrics(methods, appliances, metrics, errors)
