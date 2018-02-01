import sys

from readData import parseData


class Id3:
    """
    Id3 Algorithm
    """

    def __init__(self):
        """
        Initialize the Id3 class by Parsing all the incoming arguments.
        main.py <L> <K> <training_set.csv> <validation_set.csv> <test_set.csv> <flag_to_print>
        """
        try:
            self.trainData = None
            self.valData = None
            self.testData = None

            self.L = sys.argv[1]
            self.K = sys.argv[2]
            self.trainFile = sys.argv[3]
            self.valFile = sys.argv[4]
            self.testFile = sys.argv[5]
            self.printFlag = sys.argv[6]
        except Exception as e:
            sys.exit("Insufficient argument set provided: %s " % (str(e)))

    def main(self):
        """
        The Main function on the program
        """
        self.fetchData()

    def fetchData(self):
        """
        Fetches all the data from the training, validation and test data sets.
        """
        dataParser = parseData()
        self.trainData = dataParser.parseFile(self.trainFile)
        self.valData = dataParser.parseFile(self.valFile)
        self.testData = dataParser.parseFile(self.testFile)


if __name__ == "__main__":
    id3 = Id3()
    id3.main()
