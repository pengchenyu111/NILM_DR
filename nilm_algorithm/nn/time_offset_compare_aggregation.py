from tensorflow.keras.callbacks import ModelCheckpoint

from nilmtk import DataSet
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from nilm_algorithm.nn.s2p import Seq2Point
from nilmtk.losses import rmse, mae, sae, mr
from tqdm import tqdm
import random
import util.convert_util as cu
import util.draw_util as du

"""
    时间步长内多种实践偏差造成的预测精度结果比较
    模拟采集操作的时间不同步性
"""

# building_no = 1  # 家庭编号
# train_start_time = '2019-05-18'  # 训练集开始时间，包含
# train_end_time = '2019-06-01'  # 训练集结束时间，不包含
# test_start_time = '2019-06-01'  # 训练集开始时间，包含
# test_end_time = '2019-06-02'  # 训练集结束时间，不包含
# target_appliances = ['freezer', 'electric vehicle', 'sockets', 'electric water heating appliance', 'air conditioner']

building_no = 4  # 家庭编号
train_start_time = '2019-05-18'  # 训练集开始时间，包含
train_end_time = '2019-05-25'  # 训练集结束时间，不包含
test_start_time = '2019-05-30'  # 训练集开始时间，包含
test_end_time = '2019-05-31'  # 训练集结束时间，不包含
target_appliances = ['electric vehicle', 'electric water heating appliance', 'electric space heater', 'spin dryer', 'stove']

sample_period = 60  # 采样频率，几秒一次
abnormal_rate = 0.3
offset_width = 10

# 加载训练用数据集
train_data = DataSet('../../data/DATAPORT/newyork/dataport_newyork_1s.h5')
train_data.set_window(start=train_start_time, end=train_end_time)

scaler = StandardScaler()


# 各设备分功率
appliances_train_df_list = []
appliances_train_scaler_list = []
for ta in target_appliances:
    appliance_train_df = next(
        train_data.buildings[building_no].elec[ta].load(physical_quantity='power', ac_type='active',
                                                        sample_period=sample_period))
    appliance_train_df.columns = ['active_power']
    appliance_train_df.index.name = 'datetime'
    appliance_train_df['active_power'] = appliance_train_df['active_power'].apply(lambda x: x if x >= 0 else 0)
    appliances_train_df_list.append(appliance_train_df.values)



# 使用所有设备的总功率
origin_main_df = next(train_data.buildings[building_no].elec.mains().load(physical_quantity='power', ac_type='active',
                                                                          sample_period=sample_period))
offset_aggregate_main_df = cu.time_offset_converter_2(origin_main_df, abnormal_rate, offset_width)

# s2q特殊处理
sequence_length = 61
units_to_pad = sequence_length // 2  # 用前后30s的数据来预测中点
padded_val = 0  # 填充值默认为0
new_mains_df = pd.DataFrame(
    np.pad(array=offset_aggregate_main_df.values.flatten(),
           pad_width=(units_to_pad, units_to_pad),
           mode='constant',
           constant_values=(padded_val, padded_val)))
# 对数据标准化处理
new_mains_df = scaler.fit_transform(new_mains_df)
# (len,sequence_length,1)
new_mains_df = np.array([new_mains_df[i:i + sequence_length] for i in range(len(new_mains_df) - sequence_length + 1)])

model = Seq2Point(sequence_length)

# 开始训练各个分设备的模型
for idx, app in enumerate(appliances_train_df_list):
    print('*******start training: building_no==>{}, ab_rate==>{}, offset==>{},app==>{}************'.format(building_no,
                                                                                                           abnormal_rate,
                                                                                                           offset_width,
                                                                                                           target_appliances[idx]))
    model.compile(loss='mse', optimizer='adam')

    checkpoint = ModelCheckpoint(
        './model_trained/time_offset/building_{}/aggregate/{}_{}_{}.tf'.format(building_no, target_appliances[idx],
                                                                               abnormal_rate, offset_width),
        save_format='tf', monitor='val_loss',
        verbose=1, save_best_only=True,
        mode='min')
    model.fit(
        x=new_mains_df,
        y=appliances_train_df_list[idx],
        validation_split=0.15,
        epochs=10,
        batch_size=512,
        callbacks=[checkpoint])

    model.summary()
    model.save_weights(
        './model_trained/time_offset/building_{}/aggregate/{}_{}_{}.h5'.format(building_no, target_appliances[idx],
                                                                               abnormal_rate, offset_width))

print('************start test**************')
# 处理测试集的总功率
test_data = DataSet('../../data/DATAPORT/newyork/dataport_newyork_1s.h5')
test_data.set_window(start=test_start_time, end=test_end_time)

test_origin_main_df = next(test_data.buildings[building_no].elec.mains().load(physical_quantity='power', ac_type='active',
                                                                          sample_period=sample_period))
test_offset_aggregate_main_df = cu.time_offset_converter_2(test_origin_main_df,abnormal_rate, offset_width)

new_test_df = pd.DataFrame(
    np.pad(array=test_offset_aggregate_main_df.values.flatten(),
           pad_width=(units_to_pad, units_to_pad),
           mode='constant',
           constant_values=(padded_val, padded_val)))
new_test_df = scaler.fit_transform(new_test_df)
new_test_df = np.array([new_test_df[i:i + sequence_length] for i in range(len(new_test_df) - sequence_length + 1)])

for idx_t, app in enumerate(target_appliances):
    model.load_weights('./model_trained/time_offset/building_{}/aggregate/{}_{}_{}.tf'.format(building_no, app, abnormal_rate, offset_width))
    test_app_df = next(test_data.buildings[building_no].elec[app].load(physical_quantity='power', ac_type='active', sample_period=sample_period))
    test_app_df.columns = ['active_power']
    # 去除预测结果中可能结果为负数的情况
    test_app_df['active_power'] = test_app_df['active_power'].apply(lambda x: x if x >= 0 else 0)
    print('*******start predict: building_no==>{}, ab_rate==>{}, offset==>{},app==>{}************'.format(building_no, abnormal_rate, offset_width,app))
    test_res_pre = model.predict(new_test_df, batch_size=1)
    # 去除预测结果中可能结果为负数的情况
    test_res_pre = np.maximum(test_res_pre, 0)
    # 打印评价指标结果
    print('RMSE===>{}'.format(rmse(test_app_df.values, test_res_pre)))
    print('MAE===>{}'.format(mae(test_app_df.values, test_res_pre)))
    print('SAE===>{}'.format(sae(test_app_df.values, test_res_pre)))
    print('MR===>{}'.format(mr(test_app_df.values, test_res_pre)))
    # 绘制预测结果
    du.draw_true_pre_compare(app, test_app_df.values, test_res_pre)
