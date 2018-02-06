import numpy as np
import pandas as pd


class Model:
    """
    The model that wraps the DataFrame along with the list of features and the target.
    """

    def __init__(self, d_frame):
        """
        The constructor that initializes the model.
        Args:
            dFrame: DataFrame from pandas
            :type d_frame: DataFrame
        """
        self.features = list(d_frame.columns.values)
        self.targetName = self.features.pop(-1)
        self.dataFrame = d_frame
        self.targetPosVal = list(d_frame[self.targetName].unique())


class ParseData:
    """
    The class responsible to parse the data from the CSV file.
    """

    def __init__(self):
        """
        The constructor for initializing.
        """
        self.headerList = []

    def parse_file(self, file_name):
        """
        Reads all the data from the "fileName" :argument and parses it to the model
        Args:
            file_name (str): string, the file name along with path to the file.

        Returns: an instance of the model class.
        """
        ar = np.recfromcsv(file_name)
        data = pd.DataFrame(data=ar)

        return Model(data)
