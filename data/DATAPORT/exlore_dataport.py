from nilmtk import DataSet
from matplotlib import pyplot as plt
import util.draw_util as du

data = DataSet('./newyork/dataport_newyork_1s.h5')
elec = data.buildings[4].elec
# freezer = elec['freezer']
# print(next(freezer.load(physical_quantity='power'))) # building_1数据是从2019-05-01到2019-10-31
print('*******************************')
# print(next(elec.load()))
# print('*******************************')
# mains = next(elec.mains().load())
# print(mains)
# print('*******************************')
# print(next(freezer.load()))

# building[1]----freezer
# building[1]----freezer
# building[1]----electric vehicle
# building[1]----sockets
# building[1]----electric water heating appliance
# building[1]----air conditioner
# building[1]----electric vehicle
# building[1]----air conditioner
# building[1]----air conditioner
# building[1]----freezer
# building[1]----electric water heating appliance
# building[1]----electric vehicle
# building[1]----sockets
# building[1]----electric vehicle
# building[1]----freezer
# building[1]----electric water heating appliance
# building[1]----air conditioner
# building[1]----sockets
# building[1]----electric water heating appliance
# building[1]----sockets
# du.show_top_k_appliance_each_building(data=data, building_no=1, k=5)
# du.show_top_k_appliance_each_building(data=data, building_no=2, k=5)

# du.show_pie_appliance_enery_consumption(data=data, building_no=1)
# du.show_building_appliance_period_data(data=data, building_no=1, appliance='freezer', start='2019-05-18', end='2019-07-18')
du.show_building_appliance_period_data(data=data, building_no=1, appliance='electric vehicle', start='2019-05-18', end='2019-06-01')
# du.show_building_appliance_period_data(data=data, building_no=1, appliance='sockets', start='2019-05-18', end='2019-07-18')
du.show_building_appliance_period_data(data=data, building_no=1, appliance='electric water heating appliance', start='2019-05-18', end='2019-06-01')
# du.show_building_appliance_period_data(data=data, building_no=1, appliance='air conditioner', start='2019-05-18', end='2019-07-18')


# du.show_building_appliance_period_data(data=data, building_no=4, appliance='electric space heater', start='2019-05-18', end='2019-09-01')
# du.show_building_appliance_period_data(data=data, building_no=4, appliance='electric vehicle', start='2019-05-18', end='2019-09-01')
# du.show_building_appliance_period_data(data=data, building_no=4, appliance='spin dryer', start='2019-05-18', end='2019-09-01')
# du.show_building_appliance_period_data(data=data, building_no=4, appliance='stove', start='2019-05-18', end='2019-09-01')
# du.show_building_appliance_period_data(data=data, building_no=4, appliance='electric water heating appliance', start='2019-05-18', end='2019-09-01')



# 显示各家庭用电分布
# for i in range(len(data.buildings)):
#     du.show_pie_appliance_enery_consumption(data, i + 1, 'newyork_building_pie/building-{}.png'.format(i + 1))
