import json
from wholeTree_checker import WholeTreeChecker
import os


def read_files():
    data = []
    path = "./data/graph_list2"
    files = os.listdir(path) 
    for index in range(len(files)):
        filepath = path + '/' + str(index + 1) + '.json'
        print(filepath)
        if os.path.isfile(filepath):  
            filepath = path + '/' + str(index + 1) + '.json'
            with open(filepath, 'r', encoding='UTF-8') as js_file:
                js = json.load(js_file)
                data.append(js)
    return data


def node_judge(node, regex):
    for item in regex['data']:
        attribute = item['queryAttribute']
        op = item['queryOperation']
        value = item['queryValue']
        if attribute not in node.keys():
            return False
        elif op == '=':
            if float(value) != float(node[attribute]):
                return False
        elif op == '>':
            if float(value) >= float(node[attribute]):
                return False
        elif op == '>=':
            if float(value) > float(node[attribute]):
                return False
        elif op == '<':
            if float(value) <= float(node[attribute]):
                return False
        elif op == '<=':
            if float(value) < float(node[attribute]):
                return False
        elif op == '⊂':
            tmp1 = str.lower(value)
            tmp2 = str.lower(node[attribute])
            if tmp1 not in tmp2:
                return False
    return True


def tree_dfs(root, index):
    global index_data
    index_data.append(root)
    root['index'] = index
    if 'children' in root:
        for child in root['children']:
            tree_dfs(child, index + 1)


def exist_dfs(root, node_regex, num):
    if node_judge(root, node_regex):
        num += 1
    if 'children' in root:
        for child in root['children']:
            exist_dfs(child, node_regex, num)


def all_dfs(root, node_regex):
    if node_judge(root, node_regex):
        return False
    if 'children' in root:
        for child in root['children']:
            if not exist_dfs(child, node_regex):
                return False
    return True


def check_condition(tree, node_list, condition):
    if not (int(condition['Size'][0]) <= tree['size'] <= int(condition['Size'][1])):
        print("int: ", int(condition['Size'][0]))
        print("size: ", tree['size'])
        print("type: ", type(tree['size']))
        return False
    if not (int(condition['Height'][0]) <= tree['height'] <= int(condition['Height'][1])):
        return False
    if not (int(condition['Width'][0]) <= tree['width'] <= int(condition['Width'][1])):
        return False
    for comp_condition in condition['ElementComposition']:
        if comp_condition['type'] == 'exist':
            if comp_condition['repeat'][0] != '' and comp_condition['repeat'][1] != '':
                num = 0
                for tmp in node_list:
                    if node_judge(tmp, comp_condition['node']):
                        num += 1
                print(int(comp_condition['repeat'][0]))
                print(comp_condition['repeat'][1])
                if int(comp_condition['repeat'][0]) > num or comp_condition['repeat'][1] != "*" and num > int(comp_condition['repeat'][1]):
                    return False
        if comp_condition['type'] == 'all':
            for tmp in node_list:
                if not node_judge(tmp, comp_condition['node']):
                    return False
    if condition['Aggregation']['op'] == 'mean':
        Sum = 0
        attribute = condition['Aggregation']['attribute']
        for tmp in node_list:
            Sum += int(tmp[attribute])
        if not (int(condition['Aggregation']['value'][0]) <= Sum / len(node_list) <= int(
                condition['Aggregation']['value'][1])):
            return False
    elif condition['Aggregation']['op'] == 'sum':
        Sum = 0
        attribute = condition['Aggregation']['attribute']
        for tmp in node_list:
            Sum += int(tmp[attribute])
        if not (int(condition['Aggregation']['value'][0]) <= Sum <= int(condition['Aggregation']['value'][1])):
            return False
    elif condition['Aggregation']['op'] == 'min':
        attribute = condition['Aggregation']['attribute']
        Min = int(node_list[0][attribute])
        for tmp in node_list:
            if int(tmp[attribute]) < Min:
                Min = int(tmp[attribute])
        if not (int(condition['Aggregation']['value'][0]) <= Min <= int(condition['Aggregation']['value'][1])):
            return False
    elif condition['Aggregation']['op'] == 'max':
        attribute = condition['Aggregation']['attribute']
        Max = int(node_list[0][attribute])
        for tmp in node_list:
            if int(tmp[attribute]) > Max:
                Max = int(tmp[attribute])
        if not (int(condition['Aggregation']['value'][0]) <= Max <= int(condition['Aggregation']['value'][1])):
            return False

    return True


def tree_color_dfs(root):
    root['color_flag'] = False
    root['color'] = []
    for tmp_root in root['children']:
        tree_color_dfs(tmp_root)


class RegexMatch:
    node_index = 0
    index_list = []
    reg_index = 0
    reg_list = []  

    def reg_dfs(self, reg):
        reg['node_list'] = []
        reg['index'] = self.reg_index

        for node in reg['composition']:
            node['coding'] = '.'
        reg['coding_1'] = '.'
        reg['coding_2'] = '.'
        self.reg_index += 1
        self.reg_list.append(reg)
        if 'children' in reg:
            for child_reg in reg['children']:
                self.reg_dfs(child_reg)

    def get_reg_coding(self, reg, new_reg, flag):
        res = ''
        if reg['coding_1'] == '!':
            flag = False
        if flag:
            if reg['type'] == 'node':
                new_reg['type'] = 'node'
                new_reg['nodeColor'] = reg['nodeColor']
                new_reg['nodeName'] = reg['nodeName']
                new_reg['data'] = reg['data']
            elif reg['type'] == 'branch':
                new_reg['type'] = 'branch'
                new_reg['composition'] = []
                for node in reg['composition']:
                    if node['coding'] == '*':
                        tmp_node = {
                            'type': 'node',
                            'data': {

                            },
                            'repeat': [node['repeat'][0], node['repeat'][1]],
                            'nodeColor': '#ABABAB',
                            'nodeName': '*',
                        }
                        new_reg['composition'].append(tmp_node)
                    else:
                        tmp_node = {
                            'type': 'node',
                            'data': node['data'],
                            'repeat': [node['repeat'][0], node['repeat'][1]],
                            'nodeColor': node['nodeColor'],
                            'nodeName': node['nodeName'],
                        }
                        new_reg['composition'].append(tmp_node)
                    res += node['coding']
                    node['coding'] = '.'
            new_reg['children'] = []
            new_reg['repeat'] = [reg['repeat'][0], reg['repeat'][1]]
            if reg['coding_1'] != '.':
                new_reg['repeat'][0] = reg['coding_1']
            if reg['coding_2'] != '.':
                new_reg['repeat'][1] = reg['coding_2']
            res += reg['coding_1']
            res += reg['coding_2']
            reg['coding_1'] = '.'
            reg['coding_2'] = '.'
            reg['node_list'] = []
            for child_reg in reg['children']:
                if child_reg['coding_1'] != '!':
                    tmp_reg = {}
                    new_reg['children'].append(tmp_reg)
                    res += self.get_reg_coding(child_reg, tmp_reg, flag)
                else:
                    tmp_reg = {}
                    res += self.get_reg_coding(child_reg, tmp_reg, flag)
        else:
            for node in reg['composition']:
                res += '!'
                node['coding'] = '.'
            res += '!!'
            reg['coding_1'] = '.'
            reg['coding_2'] = '.'
            reg['node_list'] = []
            for child_reg in reg['children']:
                tmp_reg = {}
                res += self.get_reg_coding(child_reg, tmp_reg, flag)

        return res

    def tree_list_match(self, tree_list, index_data_map, hierarchicalParam, query_result, reg_dict):
        hierarchicalParam['regex']['composition'] = []
        self.reg_dfs(hierarchicalParam['regex'])
        for i in range(len(tree_list)):
            tree_color_dfs(tree_list[i]['data'])
            WholeTree = WholeTreeChecker(self.reg_list)
            tmp_res = WholeTree.judge(tree=tree_list[i]['data'], index_map=index_data_map[i],
                                      regex=hierarchicalParam['regex'])
            if tmp_res:
                if check_condition(tree=tree_list[i], node_list=index_data_map[i],
                                   condition=hierarchicalParam['condition']):
                    query_result['index_list'].append(i)
                    query_result['tree_list'].append(tmp_res)
                    for tmp_subtree in tmp_res:
                        for tmp_path in tmp_subtree:
                            index_data_map[i][tmp_path]['color_flag'] = True
            WholeTree.judge1(tree=tree_list[i]['data'], index_map=index_data_map[i],
                             regex=hierarchicalParam['regex'])
            if hierarchicalParam['regex']['coding_1'] != '!':
                reg = {}
                reg_coding = self.get_reg_coding(hierarchicalParam['regex'], reg, True)
                if reg_coding in reg_dict:
                    pass
                else:
                    reg_dict[reg_coding] = {
                        'num': 0,
                        'reg': reg,
                        'tree_index': []
                    }
            else:
                reg = {}
                reg_coding = self.get_reg_coding(hierarchicalParam['regex'], reg, True)
        for key, value in reg_dict.items():
            tmp_reg = value['reg']
            for i in range(len(tree_list)):
                WholeTree = WholeTreeChecker(self.reg_list)
                tmp_res = WholeTree.judge(tree=tree_list[i]['data'], index_map=index_data_map[i],
                                          regex=tmp_reg)
                if tmp_res:
                    value['num'] += 1
                    value['tree_index'].append(i)


if __name__ == '__main__':
    tree_data = read_files()
    index_data_map = []
    for tree in tree_data:
        index_data = []
        tree_dfs(tree['data'], 0)
        index_data_map.append(index_data)
    matcher = RegexMatch()
    query_result = {
        "index_list": [],
        "tree_list": []
    }
    regex = [
        {
            "type": "node",
            "data": {
            },
            "repeat": [2, 2]
        },
        {
            "type": "branch",
            "composition": [
                {
                    "type": "path",
                    "composition": [
                        {
                            "type": "node",
                            "data": {
                            },
                            "repeat": [1, 1]
                        }
                    ],
                    "branchRepeat": [30, '*']
                }
            ]
        },
        {
            "type": "branch",
            "composition": [
                {
                    "type": "path",
                    "composition": [
                        {
                            "type": "node",
                            "data": {
                            },
                            "repeat": [1, 1]
                        }
                    ],
                    "branchRepeat": [10, '*']
                }
            ]
        }

    ]
    matcher.tree_list_match(tree_list=tree_data, index_data_map=index_data_map, hierarchicalParam=regex,
                            query_result=query_result)
    print(len(query_result['index_list']))
