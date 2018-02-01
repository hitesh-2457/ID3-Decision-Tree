import numpy as np
import pandas as pd


class model:
    """
    The model that wraps the DataFrame along with the list of features and the target.
    """

    def __init__(self, dFrame):
        """
        The constructor that initializes the model.
        Args:
            dFrame: DataFrame from pandas
            :type dFrame: DataFrame
        """
        self.features = list(dFrame.columns.values)
        self.targetName = self.features.pop(-1)
        self.dataFrame = dFrame


class parseData:
    """
    The class responsible to parse the data from the CSV file.
    """

    def __init__(self):
        """
        The constructor for initializing.
        """
        self.headerList = [];

    def parseFile(self, fileName):
        """
        Reads all the data from the "fileName" :argument and parses it to the model
        Args:
            fileName: string, the file name along with path to the file.

        Returns: an instance of the model class.
        :type fileName: str

        """
        ar = np.recfromcsv(fileName)
        data = pd.DataFrame(data=ar, dtype=bool)

        return model(data)
        # try:
        #     tData = []
        #     header = True
        #     fp = open(fileName, 'r')
        #
        #     for line in fp:
        #         data = line.strip().split(',')
        #         if header:
        #             self.headerList = data
        #             header = not header
        #         else:
        #             tData.append(model(data))
        #
        #     fp.close()
        #     return tData
        #
        # except Exception as e:
        #     sys.exit("Failed to open file: %s\nException: %s" % (fileName) % (str(e)))
