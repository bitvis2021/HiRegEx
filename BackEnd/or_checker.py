import copy
from node_checker import NodeChecker


class OrChecker:
    Node = NodeChecker()

    def find(self, tree, regex):
        """
        找到整个tree中所有满足regex的部分
        :param tree:
        :param regex:
        :return:
        """
        res = []
        for item in regex['composition']:
            if item['type'] == 'node':
                tmp_res = self.Node.find(tree=tree, regex=item)
                if tmp_res:
                    res.extend(tmp_res)
            elif item['type'] == 'path':
                tmp_res = self.path_find(tree=tree, regex=item)
                if tmp_res:
                    res.extend(tmp_res)
            elif item['type'] == 'or':
                tmp_res = self.find(tree=tree, regex=item)
                if tmp_res:
                    res.extend(tmp_res)
        return res

    def judge(self, tree, regex):
        res = []
        for item in regex['composition']:
            if item['type'] == 'node':
                tmp_res = self.Node.judge(node=tree, regex=item)
            elif item['type'] == 'path':
                tmp_res = self.path_judge(tree=tree, regex=item, curRegex=0, repeatNum=0)
            if tmp_res:
                res.extend(tmp_res)
        return res

    def path_find(self, tree, regex):
        res = []
        res.extend(self.path_judge(tree=tree, regex=regex, curRegex=0, repeatNum=0))
        for child in tree['children']:
            res.extend(self.path_find(tree=child, regex=regex))
        return res

    def path_judge(self, tree, regex, curRegex, repeatNum=0):

        res = []

        repeat_min = regex["composition"][curRegex]["repeat"][0]
        repeat_max = regex["composition"][curRegex]["repeat"][1]

        if repeatNum < repeat_min:
            if regex['composition'][curRegex]['type'] == 'node':
                tmp_res = self.Node.judge(node=tree, regex=regex['composition'][curRegex])
            elif regex['composition'][curRegex]['type'] == 'path':
                tmp_res = self.path_judge(tree=tree, regex=regex['composition'][curRegex], curRegex=0, repeatNum=0)
            elif regex['composition'][curRegex]['type'] == 'or':
                tmp_res = self.judge(tree=tree, regex=regex['composition'][curRegex])

            if tmp_res:
                for item in tmp_res:
                    tmp_node = item[len(item) - 1]
                    if not tmp_node['children']:  
                        if curRegex + 1 == len(regex['composition']):  
                            if repeatNum + 1 >= repeat_min and (repeat_max == '*' or repeatNum + 1 <= repeat_max):
                                res.append(item)
                    for child in tmp_node['children']:
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
                tmp_res = self.judge(tree=tree, regex=regex['composition'][curRegex + 1])

            if tmp_res: 
                res = self.path_judge(tree=tree, regex=regex['composition'], curRegex=curRegex + 1, repeatNum=0)
            else:
                if regex['composition'][curRegex]['type'] == 'node':
                    tmp_res = self.Node.judge(node=tree, regex=regex['composition'][curRegex])
                elif regex['composition'][curRegex]['type'] == 'path':
                    tmp_res = self.path_judge(tree=tree, regex=regex['composition'][curRegex], curRegex=0, repeatNum=0)
                elif regex['composition'][curRegex]['type'] == 'or':
                    tmp_res = self.judge(tree=tree, regex=regex['composition'][curRegex])

                if tmp_res:
                    for item in tmp_res:
                        tmp_node = item[len(item) - 1]
                        if not tmp_node['children']:  
                            if curRegex + 1 == len(regex['composition']):  
                                res.append(item)
                        else:
                            for child in tmp_node['children']:
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
