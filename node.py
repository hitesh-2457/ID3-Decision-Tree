import math

from readData import Model


class Node:
    """
    This is the class that defines the structure of each node in the tree
    """

    def __init__(self, attr=None, attrValues=None, childNodes={}, targetCount=[]):
        """
        The constructor that initializes the node.
        Args:
            val: str :type: str
        """
        self.attr = attr
        self.attrValues = attrValues
        self.childNodes = childNodes
        self.targetCount = targetCount

    def is_leaf(self):
        return len(self.childNodes.keys()) == 0


class Tree:
    """
    The Class that is used to maintain the tree.
    """

    def __init__(self, data_set):
        """
        The constructor that initializes the tree.
        """
        self.root = None
        self.trainSet = data_set

    def print_tree(self):
        self.print_node(self.root)

    def print_node(self, node, depth=0):
        for ch in node.attrValues:
            for i in range(0, depth, 1):
                print "| ",
            if node.childNodes[ch].is_leaf():
                print node.attr, " = ", ch, " : ", node.childNodes[ch].attr
            else:
                print node.attr, " = ", ch, " : "
                self.print_node(node.childNodes[ch], depth=depth + 1)

    def train_id3(self, method):
        """

        Args:
            method:
        """
        root = self.build_tree(self.trainSet, method)
        self.root = root

    def build_tree(self, data_set, method):
        """

        Args:
            data_set:
            method:

        Returns:

        """
        grouped = data_set.dataFrame.groupby(data_set.targetName).groups
        tar_val_count = [grouped[x].values.size for x in grouped]
        node = None

        if data_set.dataFrame['class'].size == max(tar_val_count):
            node = Node(attr=data_set.dataFrame['class'].head(1).values[0], targetCount=[max(tar_val_count)])
        elif len(data_set.features) == 1:
            poss_values = list(data_set.dataFrame[data_set.features[0]].unique())
            childNodes = {}
            for pV in poss_values:
                child_groups = data_set.dataFrame[data_set.dataFrame[data_set.features[0]] == pV].groupby(
                    data_set.targetName).groups
                child_tar_val = [child_groups[x].values.size for x in child_groups]
                childNodes[pV] = Node(attr=child_groups.keys()[child_tar_val.index(max(child_tar_val))],
                                      targetCount=[max(child_tar_val)])
            node = Node(attr=data_set.features[0], attrValues=poss_values, childNodes=childNodes,
                        targetCount=tar_val_count)
        else:
            best_feature, gain = self.best_gain(data_set, method, tar_val_count)
            poss_values = list(data_set.dataFrame[best_feature].unique())
            childNodes = {}
            for va in poss_values:
                new_data_set = data_set.dataFrame[data_set.dataFrame[best_feature] == va]
                new_data_set.pop(best_feature)
                childNodes[va] = self.build_tree(Model(new_data_set), method)
            node = Node(attr=best_feature, attrValues=poss_values, targetCount=tar_val_count, childNodes=childNodes)
        return node

    def best_gain(self, data_set, method, tar_val_count):
        """

        Args:
            data_set:
            method:
            tar_val_count:

        """
        attributes = data_set.features

        tot_count = sum(tar_val_count)
        tot_entropy = self.entropy(tar_val_count) if method == 1 else self.variance(tar_val_count)
        best_gain = 0
        best_attr = ''
        for attr in attributes:
            poss_values = list(data_set.dataFrame[attr].unique())
            attr_gain = tot_entropy
            for pV in poss_values:
                count_tuple = (data_set.dataFrame[
                                   (data_set.dataFrame[data_set.targetName] == data_set.targetPosVal[0]) &
                                   (data_set.dataFrame[attr] == pV)
                                   ].shape[0],
                               data_set.dataFrame[
                                   (data_set.dataFrame[data_set.targetName] == data_set.targetPosVal[1]) &
                                   (data_set.dataFrame[attr] == pV)
                                   ].shape[0])
                attr_gain -= sum(count_tuple) / tot_count * (
                    self.entropy(count_tuple) if method == 1 else self.variance(count_tuple))

            if best_gain <= attr_gain:
                best_gain, best_attr = attr_gain, attr

        return best_attr, best_gain

    def entropy(self, count_list):
        """

        Args:
            count_list:

        Returns:

        """
        tot = float(sum(count_list))
        neg_prob = count_list[1] / tot
        pos_prob = count_list[0] / tot
        if min(neg_prob, pos_prob) == 0.0:
            return 1

        return -(pos_prob * math.log(pos_prob, 2) + neg_prob * math.log(neg_prob, 2))

    def variance(self, count_tuple):
        """

        Args:
            count_tuple:

        Returns:

        """
        tot = float(sum(count_tuple))
        return (count_tuple[0] * count_tuple[1]) / (tot * tot)
        # attributes = dataSet.features[:]
        # attributes.remove('xb')
        # attributes.append(dataSet.targetName)
        # newSet = model(
        #     dataSet.dataFrame[(dataSet.dataFrame['xb'] == dataSet.targetPosVal[0])].filter(items=attributes))
