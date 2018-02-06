import sys

from node import Tree
from readData import ParseData


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
            self.dataParser = ParseData()

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
        data_set = self.dataParser.parse_file(self.trainFile)
        tree = Tree(data_set)
        tree.train_id3(1)
        tree.print_tree()


if __name__ == "__main__":
    id3 = Id3()
    id3.main()
