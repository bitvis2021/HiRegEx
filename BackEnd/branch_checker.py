# -*- coding = utf-8 -*-
from path_checker import PathChecker
from node_checker import NodeChecker


class BranchChecker:
    Path = PathChecker()
    Node = NodeChecker()

    def judge(self, tree, branch_regex):
        res = []
        subtrees = tree['children']
        flag = True
        for path in branch_regex['composition']:
            path_set = []
            for subtree in subtrees:
                path_set.extend(self.Path.judge(tree=subtree, regex=path, curRegex=0, repeatNum=0))
            repeat_min = path['branchRepeat'][0]
            repeat_max = path['branchRepeat'][1]
            if len(path_set) < repeat_min:
                flag = False
                break
            if repeat_max != "*" and len(path_set) > repeat_max:
                flag = False
                break
            if not path_set:
                path_set.append('end')
            res.extend(path_set)

        if flag:
            return res
        return []

    def dfs(self, tree, node_index):
        if tree['index'] == node_index:
            return tree['children']
        else:
            for node in tree['children']:
                return self.dfs(node, node_index)

    def find(self, tree, regex, rootNode):
        res = []
        for node_index in rootNode:
            subtrees = self.dfs(tree, node_index)
            subtree_set = [node_index]
            flag = True
            for path in regex['compose']:
                path_set = []
                for subtree in subtrees:
                    path_set.extend(PathChecker.judge(tree=subtree, regex=path, curRegex=0, repeatNum=0))
                repeat_min = path['repeat'][0]
                repeat_max = path['repeat'][1]
                if len(path_set) < repeat_min:
                    flag = False
                    break
                if repeat_max != "*" and len(path_set) > repeat_max:
                    flag = False
                    break
                for element in path_set:
                    subtree_set.extend(element)
            if flag:
                res.append(subtree_set)
        return res
