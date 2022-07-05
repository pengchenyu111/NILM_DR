from nilmtk import DataSet
from matplotlib import pyplot as plt
import util.draw_util as du

data = DataSet('./newyork/dataport_newyork_1s.h5')
elec = data.buildings[1].elec
freezer = elec['freezer']
# print(next(freezer.load(physical_quantity='power'))) # 数据是从2019-05-01到2019-10-31
print('*******************************')
print(next(elec.load()))
print('*******************************')
print(elec.mains())



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

# du.show_pie_appliance_enery_consumption(data=data, building_no=2)
