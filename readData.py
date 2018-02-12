import numpy as np
import pandas as pd


class Model:

    def __init__(self, d_frame):
        self.features = list(d_frame.columns.values)
        self.targetName = self.features.pop(-1)
        self.dataFrame = d_frame
        self.targetPosVal = list(d_frame[self.targetName].unique())


class ParseData:

    def __init__(self):
        self.headerList = []

    def parse_file(self, file_name):
        ar = np.recfromcsv(file_name)
        data = pd.DataFrame(data=ar)

        return Model(data)
