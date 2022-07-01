from sklearn.metrics import mean_squared_error, mean_absolute_error, f1_score, r2_score, mean_absolute_percentage_error
import numpy as np
import pandas as pd

pd.set_option('display.float_format',lambda x : '%.4f' % x)


def mae(app_gt, app_pred):
    # 代表不同时刻实际值和预测值的平均差值
    return mean_absolute_error(app_gt, app_pred)


def rmse(app_gt, app_pred):
    return mean_squared_error(app_gt, app_pred) ** (.5)


def mse(app_gt, app_pred):
    return mean_squared_error(app_gt, app_pred)


def mape(app_gt, app_pred):
    return mean_absolute_percentage_error(app_gt, app_pred)


def f1score(app_gt, app_pred):
    threshold = 10
    gt_temp = np.array(app_gt)
    gt_temp = np.where(gt_temp < threshold, 0, 1)
    pred_temp = np.array(app_pred)
    pred_temp = np.where(pred_temp < threshold, 0, 1)

    return f1_score(gt_temp, pred_temp)


def relative_error(app_gt, app_pred):
    constant = 1
    numerator = np.abs(app_gt - app_pred)
    denominator = constant + app_pred
    return np.mean(numerator / denominator)


def r2score(app_gt, app_pred):
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html#sklearn.metrics.r2_score
    return r2_score(app_gt, app_pred)


def nde(app_gt, app_pred):
    # Normalized Disaggregation Error (NDE)
    # Inspired by http://proceedings.mlr.press/v22/zico12/zico12.pdf
    numerator = np.sum((app_gt - app_pred) ** 2)
    denominator = np.sum(app_gt ** 2)

    return np.sqrt(numerator / denominator)


def nep(app_gt, app_pred):
    # Normalized Error in Assigned Power (NEP)
    # Inspired by https://www.springer.com/gp/book/9783030307813
    numerator = np.sum(np.abs(app_gt - app_pred))
    denominator = np.sum(app_gt)
    return numerator / denominator


def sae(app_gt, app_pred):
    # signal aggregate error  代表实际功率和预测功率之间差值的相对值
    numerator = np.abs(np.sum(app_gt) - np.sum(app_pred))
    denominator = np.sum(app_gt)
    return numerator / denominator

def mr(app_gt, app_pred):
    # match rate
    # FROM: Load disaggregation technologies: real world and laboratory performance
    numerator = np.sum(np.min([app_gt, app_pred], axis=0))
    denominator = np.sum(np.max([app_gt, app_pred], axis=0))
    return numerator / denominator
