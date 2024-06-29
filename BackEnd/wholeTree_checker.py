import copy
from node_checker import NodeChecker
from branch_checker import BranchChecker
from path_checker import PathChecker
from or_checker import OrChecker
from queue import Queue


class WholeTreeChecker:
    Node = NodeChecker()
    Path = PathChecker()
    Branch = BranchChecker()
    Or = OrChecker()

    def __init__(self, reg_list):
        self.reg_list = reg_list

    def path_find(self, tree, regex):
        res = []
        res.extend(self.path_judge(tree=tree, regex=regex, curRegex=0, repeatNum=0))
        for child in tree['tmp_children']:
            res.extend(self.path_find(tree=child, regex=regex))
        return res

    def path_judge(self, tree, regex, curRegex, repeatNum=0):
        res = []
        repeat_min = regex[curRegex]["repeat"][0]
        repeat_max = regex[curRegex]["repeat"][1]


        if repeatNum < repeat_min:
            if regex[curRegex]['type'] == 'node':
                tmp_res = self.Node.judge(node=tree, regex=regex[curRegex])
            elif regex[curRegex]['type'] == 'or':
                tmp_res = self.or_judge(tree=tree, regex=regex[curRegex])

            if tmp_res:
                for item in tmp_res:
                    tmp_node = item[len(item) - 1]
                    if not tmp_node['tmp_children']: 
                        if curRegex + 1 == len(regex):  
                            if repeatNum + 1 >= repeat_min and (repeat_max == '*' or repeatNum + 1 <= repeat_max):
                                res.append(item)
                    for child in tmp_node['tmp_children']:
                        tmp_list = self.path_judge(tree=child, regex=regex, curRegex=curRegex, repeatNum=repeatNum + 1)
                        if tmp_list:
                            if tmp_list[0] == 'end':
                                res.append(item)
                                break
                            for element in tmp_list:
                                tmp_item = copy.copy(item)
                                tmp_item.extend(element)
                                res.append(tmp_item)

        elif repeat_max == '*' or repeatNum < repeat_max:
            if curRegex + 1 == len(regex['composition']):  
                tmp_res = []
            elif regex['composition'][curRegex + 1]['type'] == 'node':
                tmp_res = self.Node.judge(node=tree, regex=regex['composition'][curRegex + 1])
            elif regex['composition'][curRegex + 1]['type'] == 'path':
                tmp_res = self.path_judge(tree=tree, regex=regex['composition'][curRegex + 1], curRegex=0, repeatNum=0)
            elif regex['composition'][curRegex + 1]['type'] == 'or':
                tmp_res = self.or_judge(tree=tree, regex=regex['composition'][curRegex + 1])

            if tmp_res: 
                res = self.path_judge(tree=tree, regex=regex, curRegex=curRegex + 1, repeatNum=0)
            else:
                if regex['composition'][curRegex]['type'] == 'node':
                    tmp_res = self.Node.judge(node=tree, regex=regex['composition'][curRegex])
                elif regex['composition'][curRegex]['type'] == 'path':
                    tmp_res = self.path_judge(tree=tree, regex=regex['composition'][curRegex], curRegex=0, repeatNum=0)
                elif regex['composition'][curRegex]['type'] == 'or':
                    tmp_res = self.or_judge(tree=tree, regex=regex['composition'][curRegex])

                if tmp_res:
                    for item in tmp_res:
                        tmp_node = item[len(item) - 1]
                        if not tmp_node['tmp_children']:  
                            if curRegex + 1 == len(regex['composition']): 
                                res.append(item)
                        else:
                            for child in tmp_node['tmp_children']:
                                tmp_list = self.path_judge(tree=child, regex=regex, curRegex=curRegex,
                                                           repeatNum=repeatNum + 1)
                                if tmp_list:
                                    if tmp_list[0] == 'end':
                                        res.append(item)
                                        break
                                    for element in tmp_list:
                                        tmp_item = copy.copy(item)
                                        tmp_item.extend(element)
                                        res.append(tmp_item)
                elif curRegex + 1 == len(regex['composition']):
                    return ['end']

        elif repeatNum == repeat_max:
            if curRegex + 1 == len(regex['composition']): 
                res = ['end']
            else:
                res = self.path_judge(tree=tree, regex=regex, curRegex=curRegex + 1, repeatNum=0)

        return res

    def or_judge(self, tree, regex):
        res = []
        for item in regex['composition']:
            if item['type'] == 'node':
                tmp_res = self.Node.judge(node=tree, regex=item)
            else:
                tmp_res = self.path_judge(tree=tree, regex=item, curRegex=0, repeatNum=0)
            if tmp_res:
                res.extend(tmp_res)
        return res

    def branch_judge(self, tree, index_map, regex):
        res = []
        if 'children' in tree:
            subtrees = tree['children']
        else:
            subtrees = []

        flag = True
        for tmp_branch in regex:
            path_num = 0
            for subtree in subtrees:
                tmp_path_set = self.Path.judge(tree=subtree, regex=tmp_branch['composition'], curRegex=0, repeatNum=0)
                for item in tmp_path_set:
                    tmp_node = index_map[int(item[-1])]
                    if tmp_branch['children']:
                        next_res = self.branch_judge(tree=tmp_node, index_map=index_map, regex=tmp_branch['children'])
                        if next_res:
                            if next_res[0] == 'end':
                                path_num = path_num + 1
                                res.append(item)
                            else:
                                path_num = path_num + 1
                                for next_path in next_res:
                                    tmp_item = copy.copy(item)
                                    tmp_item.extend(next_path)
                                    res.append(tmp_item)
                    else:
                        res.append(item)
                        path_num = path_num + 1
            branch_repeat_min = tmp_branch['repeat'][0]
            branch_repeat_max = tmp_branch['repeat'][1]
            if path_num < int(branch_repeat_min):  
                flag = False
                break
            if branch_repeat_max != "*" and path_num > int(branch_repeat_max):
                flag = False
                break
        if not flag:
            res = []
        if flag and not res:
            res = ['end']
        return res

    def judge(self, tree, index_map, regex):
        res = []  
        root = self.Node.judge(tree, regex)
        if root:
            if not regex['children']:
                res.append(root[0])
            else:
                tmp_next = self.branch_judge(tree=tree, index_map=index_map, regex=regex['children'])
                tmp_subtree = []
                if tmp_next:
                    for tmp_path in tmp_next:
                        if tmp_path == 'end':
                            tmp_subtree.append(root[0])
                        else:
                            tmp_item = copy.copy(root[0])
                            tmp_item.extend(tmp_path)
                            tmp_subtree.append(tmp_item)
                if tmp_subtree:
                    res = tmp_subtree
        return res

    def judge1(self, tree, index_map, regex):
        q = Queue() 
        root = self.Node.judge(tree, regex)  
        if root:
            for child_reg in regex['children']:
                q.put(child_reg)
                child_reg['node_list'].append(tree['index'])
            while not q.empty():
                reg = q.get()
                node_num = len(reg['composition'])
                flag = True 
                path_set = []
                for i in range(node_num, -1, -1):
                    flag = True
                    path_set = []
                    if i != node_num:
                        reg['composition'][i]['coding'] = '*'
                    for node_index in reg['node_list']:
                        node = index_map[node_index]
                        res_path_set = []
                        for subtree in node['children']:
                            tmp_path_set = self.Path.judge(tree=subtree, regex=reg['composition'], curRegex=0,
                                                           repeatNum=0)
                            res_path_set.extend(tmp_path_set) 
                        path_num = len(res_path_set)
                        repeat_min = reg['repeat'][0]
                        repeat_max = reg['repeat'][1]
                        if reg['coding_1'] != '.':
                            repeat_min = reg['coding_1']
                        if reg['coding_2'] != '.':
                            repeat_max = reg['coding_2']
                        if int(repeat_min) <= path_num and (repeat_max == '*' or path_num <= int(repeat_max)):
                            if path_num > int(repeat_min):
                                node_flag = True
                                for reg_node in reg['composition']:
                                    if reg_node['coding'] == '*':
                                        node_flag = False
                                        break
                                if node_flag:
                                    reg['coding_1'] = str(path_num)
                            pass
                        elif int(repeat_min) > path_num > 0: 
                            reg['coding_1'] = str(path_num)
                        elif repeat_max != '*' and path_num > int(repeat_max): 
                            reg['coding_2'] = str(path_num)
                        else:   
                            flag = False
                            break
                        path_set.extend(res_path_set)
                    if flag:
                        break
                    else:
                        reg['coding_1'] = '.'
                        reg['coding_2'] = '.'
                        for tmp_node in reg['composition']:
                            tmp_node['coding'] = '.'
                if flag:
                    for child_reg in reg['children']:
                        for tmp_path in path_set:
                            child_reg['node_list'].append(index_map[tmp_path[-1]]['index'])
                        q.put(child_reg)
                else:
                    reg['coding_1'] = '!'
                    reg['coding_2'] = '!'
            return True
        else:
            regex['coding_1'] = '!'
            regex['coding_2'] = '!'
            return False



