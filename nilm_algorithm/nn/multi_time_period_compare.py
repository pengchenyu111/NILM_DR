from tensorflow.keras.callbacks import ModelCheckpoint

from nilmtk import DataSet
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from nilm_algorithm.nn.s2p import Seq2Point
from nilmtk.losses import rmse, mae, sae, mr

"""
    多种时间步长预测精度结果比较
"""

building_no = 1  # 家庭编号
train_start_time = '2019-05-18'  # 训练集开始时间，包含
train_end_time = '2019-06-01'  # 训练集结束时间，不包含
test_start_time = '2019-06-01'  # 训练集开始时间，包含
test_end_time = '2019-06-02'  # 训练集结束时间，不包含
sample_period = 10  # 采样频率，几秒一次
target_appliances = ['freezer', 'electric vehicle', 'sockets', 'electric water heating appliance', 'air conditioner']

# 加载训练用数据集
train_data = DataSet('../../data/DATAPORT/newyork/dataport_newyork_1s.h5')
train_data.set_window(start=train_start_time, end=train_end_time)

scaler = StandardScaler()

# 总功率
train_main_df = next(train_data.buildings[building_no].elec.mains().load(physical_quantity='power', ac_type='active',
                                                                         sample_period=sample_period))
train_main_df.columns = ['active_power']

# 各设备分功率
appliances_train_df_list = []
appliances_train_scaler_list = []
for ta in target_appliances:
    appliance_df = next(train_data.buildings[building_no].elec[ta].load(physical_quantity='power', ac_type='active',
                                                                        sample_period=sample_period))
    appliance_df.columns = ['active_power']
    appliances_train_df_list.append(appliance_df.values)
    appliances_train_scaler_list.append(scaler.fit_transform(appliance_df))

# s2q特殊处理
sequence_length = 61
units_to_pad = sequence_length // 2  # 用前后30s的数据来预测中点
padded_val = 0  # 填充值默认为0
new_mains_df = pd.DataFrame(
    np.pad(array=train_main_df.values.flatten(),
           pad_width=(units_to_pad, units_to_pad),
           mode='constant',
           constant_values=(padded_val, padded_val)))
# 对数据标准化处理
new_mains_df = scaler.fit_transform(new_mains_df)
# (len,sequence_length,1)
new_mains_df = np.array([new_mains_df[i:i + sequence_length] for i in range(len(new_mains_df) - sequence_length + 1)])

model = Seq2Point(sequence_length)

for idx, app in enumerate(appliances_train_df_list):
    print('*******start training {}************'.format(target_appliances[idx]))
    model.compile(loss='mse', optimizer='adam')

    checkpoint = ModelCheckpoint('./model_trained/s2q/{}_{}s.tf'.format(target_appliances[idx], sample_period),
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
    model.save_weights('./model_trained/s2q_{}_{}s.h5'.format(target_appliances[idx], sample_period))

print('************start test**************')
test_data = DataSet('../../data/DATAPORT/newyork/dataport_newyork_1s.h5')
test_data.set_window(start=test_start_time, end=test_end_time)
test_main_df = next(test_data.buildings[building_no].elec.mains().load(physical_quantity='power', ac_type='active',
                                                                       sample_period=sample_period))
test_main_df.columns = ['active_power']
new_test_df = pd.DataFrame(
    np.pad(array=test_main_df.values.flatten(),
           pad_width=(units_to_pad, units_to_pad),
           mode='constant',
           constant_values=(padded_val, padded_val)))
new_test_df = scaler.fit_transform(new_test_df)
new_test_df = np.array([new_test_df[i:i + sequence_length] for i in range(len(new_test_df) - sequence_length + 1)])

for idx_t, app in enumerate(target_appliances):
    model.load_weights('./model_trained/s2q/{}_{}s.tf'.format(app, sample_period))
    test_app_df = next(test_data.buildings[building_no].elec[app].load(physical_quantity='power', ac_type='active',
                                                                       sample_period=sample_period))
    test_app_df.columns = ['active_power']
    print('************start predict {}---{} **************'.format(app,sample_period))
    test_res_pre = model.predict(new_test_df, batch_size=1)
    print('RMSE===>{}'.format(rmse(test_app_df.values, test_res_pre)))
    print('MAE===>{}'.format(mae(test_app_df.values, test_res_pre)))
    print('SAE===>{}'.format(sae(test_app_df.values, test_res_pre)))
    print('MR===>{}'.format(mr(test_app_df.values, test_res_pre)))
