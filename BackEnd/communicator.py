from IPython.core.display import JSON
import os
import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from regex_match import RegexMatch
import numpy as np


def read_files():
    data = []
    path = "./data/graph_keywords1"
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


def takeSecond(elem):
    return elem[1]


def get_recommendation(tree_index):
    cosin_list = []

    for i in range(len(tree_data)):
        vec1 = np.array(tree_data[tree_index - 1]['embedding'])
        if i == tree_index - 1:
            continue
        vec2 = np.array(tree_data[i]['embedding'])
        cos_sim = vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        cosin_list.append([i, cos_sim])
    cosin_list.sort(key=takeSecond, reverse=True)
    index_list = [cosin_list[x][0] for x in range(0, 10)]
    result_list = []
    for idx in index_list:
        result_list.append(tree_data[idx])
    print("tree_index: ", tree_index)
    print("index_list: ", index_list)
    print("cosin: ", cosin_list[0: 10])
    return result_list


def tree_dfs(root, index, depth):
    global index_data
    global node_index
    index_data.append(root)
    root['index'] = node_index
    node_index += 1

    if 'children' not in root:
        root['children'] = []
    root['depth'] = depth
    root['degree'] = len(root['children'])

    max_height = 0
    for child in root['children']:
        tmp_height = tree_dfs(child, index+1, depth+1)
        if tmp_height > max_height:
            max_height = tmp_height
    root['height'] = max_height
    return max_height + 1


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'
tree_data = read_files()
index_data_map = []
query_result = {
    "index_list": [], 
    "tree_list": []   
}
page_data_index = []
reg_dict = {}
size_list = [0 for x in range(13)]
height_list = [0 for x in range(11)]
width_list = [0 for x in range(13)]

f_tree_map = open("./data/TED/new_same_tree1.json", 'r')
tree_map = json.load(f_tree_map)
f_tree_map.close()
f_same_tree = open("./data/TED/new_same_tree.json", 'r')
same_tree = json.load(f_same_tree)
f_same_tree.close()


for tree in tree_data:
    index_data = []
    node_index = 0
    tree_dfs(tree['data'], 0, 0)
    index_data_map.append(index_data)
    print(len(index_data_map))


@app.route('/hierarchydata', methods=['POST'])
@cross_origin()
def getHierarchyData():
    global page_data_index
    json_hierarchicalParam = json.loads(request.data)
    print("test", json_hierarchicalParam)
    if json_hierarchicalParam['hierarchicalParam']['type'] == 1:
        tree_index = int(json_hierarchicalParam['hierarchicalParam']['index'])
        same_tree_list = [tree_index]
        if str(tree_index) in same_tree:
            same_tree_list.extend(same_tree[str(tree_index)])
        res = []
        for index in same_tree_list:
            res.append(int(index))
        page_data_index = res
        cur_result = []
        visualization = {}
        if len(res) > 10:
            for i in range(0, 10):
                cur_result.append(tree_data[res[i]])
        else:
            for i in range(0, len(res)):
                cur_result.append(tree_data[res[i]])
        if len(res) > 0:
            visualization = tree_data[res[0]]
        result_data = {'visualization': visualization,
                       'list_num': len(res),
                       'vis_list': cur_result}

    elif json_hierarchicalParam['hierarchicalParam']['type'] == 2:
        query_result['index_list'] = []
        query_result['tree_list'] = []
        Matcher = RegexMatch()
        global reg_dict
        reg_dict = {}
        Matcher.tree_list_match(tree_list=tree_data, index_data_map=index_data_map, hierarchicalParam=
                            json_hierarchicalParam['hierarchicalParam'], query_result=query_result, reg_dict=reg_dict)
        tmp_result = []
        for tmp_index in query_result['index_list']:
            tmp_result.append([tmp_index+1, tree_data[tmp_index]['data']['doi']])
        global size_list
        global height_list
        global width_list
        size_list = [0 for x in range(13)]
        height_list = [0 for x in range(11)]
        width_list = [0 for x in range(13)]
        for tmp in query_result['index_list']:
            if 0 < tree_data[tmp]['size'] <= 5:
                size_list[0] += 1
            elif 5 < tree_data[tmp]['size'] <= 10:
                size_list[1] += 1
            elif 10 < tree_data[tmp]['size'] <= 20:
                size_list[2] += 1
            elif 20 < tree_data[tmp]['size'] <= 30:
                size_list[3] += 1
            elif 30 < tree_data[tmp]['size'] <= 50:
                size_list[4] += 1
            elif 50 < tree_data[tmp]['size'] <= 100:
                size_list[5] += 1
            elif 100 < tree_data[tmp]['size'] <= 200:
                size_list[6] += 1
            elif 200 < tree_data[tmp]['size'] <= 500:
                size_list[7] += 1
            elif 500 < tree_data[tmp]['size'] <= 1000:
                size_list[8] += 1
            elif 1000 < tree_data[tmp]['size']:
                size_list[9] += 1

            height_list[int(tree_data[tmp]['height'])] += 1

            if 0 < tree_data[tmp]['width'] <= 5:
                width_list[0] += 1
            elif 5 < tree_data[tmp]['width'] <= 10:
                width_list[1] += 1
            elif 10 < tree_data[tmp]['width'] <= 20:
                width_list[2] += 1
            elif 20 < tree_data[tmp]['width'] <= 30:
                width_list[3] += 1
            elif 30 < tree_data[tmp]['width'] <= 50:
                width_list[4] += 1
            elif 50 < tree_data[tmp]['width'] <= 100:
                width_list[5] += 1
            elif 100 < tree_data[tmp]['width'] <= 200:
                width_list[6] += 1
            elif 200 < tree_data[tmp]['width'] <= 500:
                width_list[7] += 1
            elif 500 < tree_data[tmp]['width'] <= 1000:
                width_list[8] += 1
            elif 1000 < tree_data[tmp]['width']:
                width_list[9] += 1
        print(query_result['index_list'])
        print(query_result['tree_list'][0])
        cur_result = []
        visualization = {}
        page_data_index = query_result['index_list']
        if len(query_result['index_list']) > 10:
            for i in range(0, 10):
                cur_result.append(tree_data[query_result['index_list'][i]])
        else:
            for i in range(0, len(query_result['index_list'])):
                cur_result.append(tree_data[query_result['index_list'][i]])
        if len(query_result['index_list']) > 0:
            visualization = tree_data[query_result['index_list'][0]]
        highlight_list = []
        for tree_list_index in query_result['index_list']:
            if str(tree_list_index) in tree_map:
                highlight_index = tree_map[str(tree_list_index)]
                if int(highlight_index) not in highlight_list:
                    highlight_list.append(int(highlight_index))
            else:
                if int(tree_list_index) not in highlight_list:
                    highlight_list.append(int(tree_list_index))
        result_data = {
                'result_num': len(query_result['index_list']),
                'visualization': visualization,
                'cur_result': cur_result,
                'reg_dict': reg_dict,
                'highlight_list': highlight_list,
                # 'highlight': query_result['tree_list'][0],
                'result': tmp_result,
                'highlightBar': {
                    'size': [
                        {
                            "x": "(0, 5]",
                            "y": size_list[0],
                        },
                        {
                            "x": "(5, 10]",
                            "y": size_list[1],
                        },
                        {
                            "x": "(10, 20]",
                            "y": size_list[2],
                        },
                        {
                            "x": "(20, 30]",
                            "y": size_list[3],
                        },
                        {
                            "x": "(30, 50]",
                            "y": size_list[4],
                        },
                        {
                            "x": "(50, 100]",
                            "y": size_list[5],
                        },
                        {
                            "x": "(100, 200]",
                            "y": size_list[6],
                        },
                        {
                            "x": "(200, 500]",
                            "y": size_list[7],
                        },
                        {
                            "x": "(500, 1000]",
                            "y": size_list[8],
                        },
                        {
                            "x": "(1000, *]",
                            "y": size_list[9],
                        }
                    ],
                    'height': [
                        {
                            "x": "1",
                            "y": height_list[1]
                        },
                        {
                            "x": "2",
                            "y": height_list[2]
                        },
                        {
                            "x": "3",
                            "y": height_list[3]
                        },
                        {
                            "x": "4",
                            "y": height_list[4]
                        },
                        {
                            "x": "5",
                            "y": height_list[5]
                        },
                        {
                            "x": "6",
                            "y": height_list[6]
                        },
                        {
                            "x": "7",
                            "y": height_list[7]
                        },
                        {
                            "x": "8",
                            "y": height_list[8]
                        },
                        {
                            "x": "9",
                            "y": height_list[9]
                        },
                        {
                            "x": "10",
                            "y": height_list[10]
                        },
                    ],
                    'width': [
                        {
                            "x": "(0, 5]",
                            "y": width_list[0],
                        },
                        {
                            "x": "(5, 10]",
                            "y": width_list[1],
                        },
                        {
                            "x": "(10, 20]",
                            "y": width_list[2],
                        },
                        {
                            "x": "(20, 30]",
                            "y": width_list[3],
                        },
                        {
                            "x": "(30, 50]",
                            "y": width_list[4],
                        },
                        {
                            "x": "(50, 100]",
                            "y": width_list[5],
                        },
                        {
                            "x": "(100, 200]",
                            "y": width_list[6],
                        },
                        {
                            "x": "(200, 500]",
                            "y": width_list[7],
                        },
                        {
                            "x": "(500, 1000]",
                            "y": width_list[8],
                        },
                        {
                            "x": "(1000, *]",
                            "y": width_list[9],
                        }
                    ]
                }
            }

        print("len: ", len(query_result['index_list']))
    elif json_hierarchicalParam['hierarchicalParam']['type'] == 3:
        page_index = json_hierarchicalParam['hierarchicalParam']['index']
        begin = (page_index-1)*10
        end = 0
        if begin+10 > len(page_data_index):
            end = len(page_data_index)
        else:
            end = begin+10
        cur_result = []
        for i in range(begin, end):
            cur_result.append(tree_data[page_data_index[i]])
        result_data = {
                'cur_result': cur_result,
                'visualization': cur_result[0]
        }
    elif json_hierarchicalParam['hierarchicalParam']['type'] == 4:
        reg_coding = json_hierarchicalParam['hierarchicalParam']['coding']
        tree_index = reg_dict[reg_coding]['tree_index']
        tmp_result_list = []
        for index in tree_index:
            tmp_result_list.append(tree_data[index])
        visualization = {}
        cur_result = []
        page_data_index = tree_index
        if len(tmp_result_list) > 10:
            for i in range(0, 10):
                cur_result.append(tmp_result_list[i])
        else:
            for i in range(0, len(tmp_result_list)):
                cur_result.append(tmp_result_list[i])
        if len(tmp_result_list) > 0:
            visualization = tmp_result_list[0]
        result_data = {
                'result_num': len(tmp_result_list),
                'visualization': visualization,
                'cur_result': cur_result,
            }

    return result_data


if __name__ == "__main__":
    print('run 0.0.0.0:14449')
    app.run(host='0.0.0.0', port=14449)
