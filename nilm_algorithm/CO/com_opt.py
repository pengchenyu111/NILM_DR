from nilmtk.api import API
from nilmtk.disaggregate import CO
from util.draw_util import draw_main_with_sub_appliance_power, draw_appliance_disaggregate_result, draw_metrics

CO_experiment_REDD = {
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

CO_experiment_Dataport = {
    'power': {'mains': ['apparent', 'active'], 'appliance': ['apparent', 'active']},
    'sample_rate': 1,
    'appliances': ['freezer', 'electric vehicle', 'sockets', 'electric water heating appliance', 'air conditioner'],
    'methods': {"CO": CO({})},
    'train': {
        'datasets': {
            'dataport': {
                'path': '../../data/DATAPORT/newyork/dataport_newyork_1s.h5',
                'buildings': {
                    1: {
                        'start_time': '2019-05-18',
                        'end_time': '2019-06-01'
                    }
                }
            }
        }
    },
    'test': {
        'datasets': {
            'dataport': {
                'path': '../../data/DATAPORT/newyork/dataport_newyork_1s.h5',
                'buildings': {
                    1: {
                        'start_time': '2019-06-01',
                        'end_time': '2019-06-02'
                    }
                }
            }
        },
        'metrics': ['rmse', 'mae', 'sae', 'mr']
    }
}

# ??????
api_res = API(CO_experiment_Dataport)
appliances = api_res.gt_overall.columns.values  # ???????????????
methods = [i for i in api_res.methods]  # ??????????????????
metrics = api_res.metrics  # ??????????????????
main_power = api_res.test_mains[0]  # ????????????
sub_true_power = api_res.gt_overall  # ?????????????????????
sub_pre_power = api_res.pred_overall  # ?????????????????????
errors = api_res.errors  # ??????????????????

# ????????????????????????????????????
# draw_main_with_sub_appliance_power(methods, appliances, main_power, sub_pre_power)

# ?????????????????????????????????
draw_appliance_disaggregate_result(methods, appliances, sub_true_power, sub_pre_power)

# ???????????????????????????
draw_metrics(methods, appliances, metrics, errors)
