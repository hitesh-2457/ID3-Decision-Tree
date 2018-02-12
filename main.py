import random
import sys

from node import Tree
from readData import ParseData


class Id3:

    def __init__(self):
        try:
            self.dataParser = ParseData()

            self.L = int(sys.argv[1])
            self.K = int(sys.argv[2])
            self.trainFile = sys.argv[3]
            self.valFile = sys.argv[4]
            self.testFile = sys.argv[5]
            self.printFlag = (sys.argv[6].upper() == "YES")
            self.data_set = self.dataParser.parse_file(self.trainFile)
        except Exception as e:
            sys.exit("Insufficient argument set provided: %s " % (str(e)))

    def prune(self, d):
        d_best = Tree(self.data_set)
        d_best.copy(d)

        val_data_set = self.dataParser.parse_file(self.valFile)
        d_best_acc = d_best.validate(val_data_set)

        non_leaves = [x for x in range(1, d_best.root.assigned_num + 1)]

        for i in range(self.L):
            d_dash = Tree(self.data_set)
            d_dash.copy(d_best)

            M = random.randint(1, self.K)
            for j in range(M):
                if len(non_leaves) > 1:
                    ran = random.randint(1, len(non_leaves) - 1)
                    P = non_leaves[ran]
                    d_dash.replace_with_leaf(P)
                    non_leaves.pop(ran)
                    if x in non_leaves:
                        non_leaves.pop(non_leaves.index(x))

            d_dash_acc = d_dash.validate(val_data_set)
            if d_dash_acc >= d_best_acc:
                d_best = d_dash
                d_best_acc = d_dash_acc

        return d_best


def main():
    id3 = Id3()
    tree = Tree(id3.data_set)
    print "Information gain heuristic: "
    tree.train_id3()

    id3.test_data_set = id3.dataParser.parse_file(id3.testFile)
    print "Accuracy on test data before pruning: ", tree.validate(id3.test_data_set)

    tree = id3.prune(tree)

    print "Accuracy on test data after pruning: ", tree.validate(id3.test_data_set)

    if id3.printFlag:
        tree.print_tree()

    print "\n\nVariance impurity heuristic: "
    tree.train_id3(1)

    print "Accuracy on test data before pruning: ", tree.validate(id3.test_data_set)

    tree = id3.prune(tree)

    print "Accuracy on test data after pruning: ", tree.validate(id3.test_data_set)

    if id3.printFlag:
        tree.print_tree()


if __name__ == "__main__":
    main()
