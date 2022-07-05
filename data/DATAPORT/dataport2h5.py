from nilmtk.dataset_converters.dataport import csv_converter as dataport_cv


def convert_1min_data():
    csvs = [
        './newyork/1minute_data_newyork.csv'
    ]
    dataport_cv.convert_dataport(csvs, "metadata.csv", "./newyork/dataport_newyork_1min.h5", 3e6)


def convert_1s_data():
    csvs = [
        "./newyork/1s_data_newyork_file1.csv",
        "./newyork/1s_data_newyork_file2.csv",
        "./newyork/1s_data_newyork_file3.csv",
        "./newyork/1s_data_newyork_file4.csv",
    ]
    dataport_cv.convert_dataport(csvs, "metadata.csv", "./newyork/dataport_newyork_1s.h5", 3e6)


def convert_15min_data():
    csvs = [
        './newyork/15minute_data_newyork.csv'
    ]
    dataport_cv.convert_dataport(csvs, "metadata.csv", "./newyork/dataport_newyork_1s.h5", 3e6)


convert_1s_data()
