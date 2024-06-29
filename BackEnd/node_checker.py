class NodeChecker:

    def judge(self, node, regex):
        res = []
        if 'coding' in regex and regex['coding'] == '*':
            return [[node['index']]]
        for item in regex['data']:
            attribute = item['queryAttribute']
            op = item['queryOperation']
            value = item['queryValue']
            if op == '=':
                if float(value) != float(node[attribute]):
                    return res
            elif op == '>':
                if float(value) >= float(node[attribute]):
                    return res
            elif op == '>=':
                if float(value) > float(node[attribute]):
                    return res
            elif op == '<':
                if float(value) <= float(node[attribute]):
                    return res
            elif op == '<=':
                if float(value) < float(node[attribute]):
                    return res
            elif op == '⊂':
                tmp1 = str.lower(value)
                tmp2 = str.lower(node[attribute])
                if tmp1 not in tmp2:
                    return res
        if not node['color_flag']:
            node['color'].append(regex['nodeColor'])
        res.append([node['index']])
        return res

    def find(self, tree, regex):
        res = []
        if self.judge(tree, regex):
            res.append([tree])
        for child in tree['children']:
            res.extend(self.find(child, regex))
        return res
