import random
import numpy as np
import pandas as pd

from tqdm import tqdm

'''
    时间偏差聚合工具
'''


def get_offset_index(cur_idx, data_length, target_time_period, offset_lower_bound, offset_upper_bound):
    """
    获取窗口的起止index
    :param cur_idx: 当前index
    :param data_length: 原数据长度
    :param target_time_period: 要聚合的窗口长度
    :param offset_lower_bound: 偏移下限
    :param offset_upper_bound: 偏移上限
    :return:
    """
    # 生成往前或往后的随机offset
    front_offset = random.randint(offset_lower_bound, offset_upper_bound)
    behind_offset = random.randint(offset_lower_bound, offset_upper_bound)
    # 是往前偏移还是往后偏移
    front_flag = random.randint(0, 1)  # 0往前 1往后
    behind_flag = random.randint(0, 1)
    # 计算最终窗口的起止index
    front_idx = cur_idx + front_offset if front_flag else cur_idx - front_offset
    front_idx = 0 if front_idx < 0 else front_idx
    front_idx = cur_idx if front_idx >= data_length else front_idx
    behind_idx = cur_idx + target_time_period - 1 + behind_offset if behind_flag else cur_idx + target_time_period - 1 - behind_offset
    behind_idx = data_length - 1 if behind_idx >= data_length else behind_idx
    return front_idx, behind_idx


def time_offset_converter(df, target_time_period=60, abnormal_rate=0.3, offset_lower_bound=3, offset_upper_bound=15):
    """
    返回偏移转换后的df
    :param df: 要聚合的dataframe
    :param target_time_period: 要聚合的窗口长度
    :param abnormal_rate: 发生偏移的比例，0-1
    :param offset_lower_bound: 偏移下限
    :param offset_upper_bound: 偏移上限
    :return:
    """
    res_list = []
    df.reset_index(inplace=True)
    data_length = len(df)
    idx_list = [idx for idx in range(0, data_length, 60)]
    abnormal_idx = random.sample(idx_list, int(len(idx_list) * abnormal_rate))
    for cur_idx in tqdm(range(0, data_length, 60)):
        if cur_idx in abnormal_idx:
            front_idx, behind_idx = get_offset_index(cur_idx, data_length, target_time_period, offset_lower_bound,
                                                     offset_upper_bound)
        else:
            front_idx = cur_idx
            behind_idx = cur_idx + target_time_period - 1
        res_list.append([df.iloc[cur_idx, 0:1][0], np.mean(df.iloc[front_idx: behind_idx + 1]).values[0]])
    res_df = pd.DataFrame(res_list)
    res_df.columns = ['datetime', 'active_power']
    res_df.set_index('datetime', inplace=True)
    return res_df


def time_offset_converter_2(df, abnormal_rate, offset_width):
    res_df = df.copy()
    data_length = len(df)
    idx_list = [idx for idx in range(0, data_length)]
    abnormal_idx = random.sample(idx_list, int(len(idx_list) * abnormal_rate))
    for cur_idx in tqdm(abnormal_idx):
        # 是往前偏移还是往后偏移
        offset_direction_flag = random.randint(0, 1)  # 0往前 1往后
        # 偏移幅度
        offset_num = random.randint(1, offset_width)
        if offset_direction_flag:
            replace_idx = cur_idx + offset_num
            if replace_idx >= data_length:
                replace_idx = data_length - 1
            res_df.iloc[cur_idx:cur_idx + 1] = df.iloc[replace_idx:replace_idx + 1].values[0][0]
        else:
            replace_idx = cur_idx - offset_num
            if replace_idx < 0:
                replace_idx = 0
            res_df.iloc[cur_idx:cur_idx + 1] = df.iloc[replace_idx:replace_idx + 1].values[0][0]
    return res_df
