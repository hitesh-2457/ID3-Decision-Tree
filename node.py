import math
from copy import deepcopy

from readData import Model


class Node:

    def __init__(self, attr=None, attr_values=None, child_nodes=None, target_count=None, num=0):
        if child_nodes is None:
            child_nodes = {}
        if target_count is None:
            target_count = []
        self.attr = attr
        self.attr_values = attr_values
        self.child_nodes = child_nodes
        self.target_count = target_count
        self.assigned_num = num

    def is_leaf(self):
        return len(self.child_nodes.keys()) == 0


class Tree:

    def __init__(self, data_set=None):
        self.root = None
        self.trainSet = data_set

    def print_tree(self):
        self.__print_node(self.root)

    def __print_node(self, node, depth=0):
        for ch in node.attr_values:
            for i in range(0, depth, 1):
                print "| ",
            if node.child_nodes[ch].is_leaf():
                print node.attr, " = ", ch, " : ", node.child_nodes[ch].attr
            else:
                print node.attr, " = ", ch, " : "
                self.__print_node(node.child_nodes[ch], depth=depth + 1)

    def train_id3(self, method=0):
        num, root = self.__build_tree(self.trainSet, method)
        self.root = root

    def __build_tree(self, data_set, method, num=0):
        grouped = data_set.dataFrame.groupby(data_set.targetName).groups
        tar_val_count = [grouped[x].values.size for x in grouped]

        if data_set.dataFrame['class'].size == max(tar_val_count):
            node = Node(attr=data_set.dataFrame['class'].head(1).values[0], target_count=[max(tar_val_count)])
        elif len(data_set.features) == 1:
            poss_values = list(data_set.dataFrame[data_set.features[0]].unique())
            child_nodes = {}
            for pV in poss_values:
                child_groups = data_set.dataFrame[data_set.dataFrame[data_set.features[0]] == pV].groupby(
                    data_set.targetName).groups
                child_tar_val = [child_groups[x].values.size for x in child_groups]
                child_nodes[pV] = Node(attr=child_groups.keys()[child_tar_val.index(max(child_tar_val))],
                                       target_count=[max(child_tar_val)])
            num += 1
            node = Node(attr=data_set.features[0], attr_values=poss_values, child_nodes=child_nodes,
                        target_count=tar_val_count, num=num)
        else:
            best_feature, gain = self.__best_gain(data_set, method, tar_val_count)
            poss_values = list(data_set.dataFrame[best_feature].unique())
            child_nodes = {}
            for va in poss_values:
                new_data_set = data_set.dataFrame[data_set.dataFrame[best_feature] == va]
                new_data_set.pop(best_feature)
                num, child_nodes[va] = self.__build_tree(Model(new_data_set), method, num=num)
            num += 1
            node = Node(attr=best_feature, attr_values=poss_values, target_count=tar_val_count, child_nodes=child_nodes,
                        num=num)
        return num, node

    def __best_gain(self, data_set, method, tar_val_count):
        attributes = data_set.features

        tot_count = sum(tar_val_count)
        tot_entropy = self.__entropy(tar_val_count) if method == 0 else self.__variance(tar_val_count)
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
                pre = (float(sum(count_tuple)) / tot_count)
                ent = self.__entropy(count_tuple) if method == 0 else self.__variance(count_tuple)
                attr_gain -= (pre * ent)

            if best_gain <= attr_gain:
                best_gain, best_attr = attr_gain, attr

        return best_attr, best_gain

    @staticmethod
    def __entropy(count_list):
        tot = float(sum(count_list))
        neg_prob = count_list[1] / tot
        pos_prob = count_list[0] / tot
        if min(neg_prob, pos_prob) == 0.0:
            return 0

        return -(pos_prob * math.log(pos_prob, 2) + neg_prob * math.log(neg_prob, 2))

    @staticmethod
    def __variance(count_tuple):
        tot = float(sum(count_tuple))
        return (count_tuple[0] * count_tuple[1]) / (tot * tot)

    def validate(self, data_set):
        hits = 0;
        for index, row in data_set.dataFrame.iterrows():
            exp_val = row[data_set.targetName]
            pred_val = self.__predict(row, self.root)
            if exp_val == pred_val:
                hits += 1
        return 100 * float(hits) / data_set.dataFrame.shape[0]

    def __predict(self, data_entry, node):
        if node.is_leaf():
            return node.attr
        attr_val = data_entry[node.attr]
        return self.__predict(data_entry, node.child_nodes[attr_val]) if attr_val in node.attr_values else -1

    def copy(self, tree):
        self.root = deepcopy(tree.root)

    def replace_with_leaf(self, n):
        self.root = self.__replace_non_leaf(self.root, self.trainSet, n)

    def __replace_non_leaf(self, node, data_set, n):
        if node.is_leaf():
            return node
        elif node.assigned_num == n:
            groups = data_set.dataFrame.groupby(data_set.targetName).groups
            tar_val_count = [groups[x].values.size for x in groups]
            return Node(attr=groups.keys()[tar_val_count.index(max(tar_val_count))], target_count=[max(tar_val_count)],
                        num=node.assigned_num)
        else:
            child_node_nums = {}
            for ch in node.child_nodes:
                child_node_nums[node.child_nodes[ch].assigned_num] = ch
            child_nums = child_node_nums.keys()
            child_nums.sort()
            path = 0
            for num in child_nums:
                if num >= n:
                    path = num
                    break
            new_data_set = data_set.dataFrame[data_set.dataFrame[node.attr] == child_node_nums[path]]
            new_data_set.pop(node.attr)
            node.child_nodes[child_node_nums[path]] = self.__replace_non_leaf(node.child_nodes[child_node_nums[path]],
                                                                              Model(new_data_set), n)
            return node
