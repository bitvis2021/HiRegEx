import copy
from node_checker import NodeChecker
from or_checker import OrChecker


class PathChecker:
    Node = NodeChecker()
    Or = OrChecker()

    def judge(self, tree, regex, curRegex, repeatNum=0):

        res = []
        repeat_min = regex[curRegex]["repeat"][0]
        repeat_max = regex[curRegex]["repeat"][1]

        if repeatNum < int(repeat_min):
            if regex[curRegex]['type'] == 'node':
                tmp_res = self.Node.judge(node=tree, regex=regex[curRegex])
            elif regex[curRegex]['type'] == 'or':
                tmp_res = self.Or.judge(tree=tree, regex=regex[curRegex])

            if tmp_res:
                if 'children' not in tree or not tree['children']:  
                    if curRegex + 1 == len(regex):  
                        if repeatNum + 1 >= int(repeat_min) and (repeat_max == '*' or repeatNum + 1 <= int(repeat_max)):
                            res.append([tree['index']])
                else:
                    for child in tree['children']:
                        tmp_list = self.judge(tree=child, regex=regex, curRegex=curRegex, repeatNum=repeatNum + 1)
                        if tmp_list:
                            if tmp_list[0] == 'end':
                                res.append([tree['index']])
                                break
                            for element in tmp_list:
                                tmp_item = [tree['index']]
                                tmp_item.extend(element)
                                res.append(tmp_item)

        elif repeat_max == '*' or repeatNum < int(repeat_max):
            if curRegex + 1 == len(regex): 
                tmp_res = []
            else:
                tmp_res = self.judge(tree=tree, regex=regex, curRegex=curRegex+1, repeatNum=0)

            if tmp_res:  
                res = tmp_res
            else:
                if regex[curRegex]['type'] == 'node':
                    tmp_res = self.Node.judge(node=tree, regex=regex[curRegex])
                elif regex[curRegex]['type'] == 'or':
                    tmp_res = self.Or.judge(tree=tree, regex=regex[curRegex])

                if tmp_res:
                    if 'children' not in tree or not tree['children']: 
                        if curRegex + 1 == len(regex): 
                            res.append([tree['index']])
                    else:
                        for child in tree['children']:
                            tmp_list = self.judge(tree=child, regex=regex, curRegex=curRegex,
                                                  repeatNum=repeatNum + 1)
                            if tmp_list:
                                if tmp_list[0] == 'end':
                                    res.append([tree['index']])
                                    break
                                for element in tmp_list:
                                    tmp_item = [tree['index']]
                                    tmp_item.extend(element)
                                    res.append(tmp_item)
                elif curRegex + 1 == len(regex):  
                    return ['end']

        elif repeatNum == int(repeat_max):
            if curRegex + 1 == len(regex):  
                res = ['end']
            else:
                res = self.judge(tree=tree, regex=regex, curRegex=curRegex + 1, repeatNum=0)

        return res

