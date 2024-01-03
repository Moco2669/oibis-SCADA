import pandas as pd
import sklearn.model_selection
import xgboost as xgb
import numpy as np
import sklearn as skl

pdDf = pd.read_csv('learningDataNew.csv')
pdDf.head()


def loadModel(data='xgb.json'):
    newModel = xgb.XGBClassifier()
    newModel.load_model(data)
    return newModel
