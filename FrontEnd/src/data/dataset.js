export function Dataset () {
    this.hierarchyData = {}
    this.regexDataList = []
    this.curIndex = 0
    this.hierarchyDataIn = []
    this.hierarchyDataOut = []
    this.connection = []
    this.initialData = {}
    this.nodeRegexList = []

    this.visData = {}
    this.visList = []
    this.regex = {}

    this.Condition = {}
    this.Regex

    this.selectedDomKey = -1

    this.selectedBranch = {}
    this.branchIndex = -2

    this.selectedOr = {}
    this.orIndex = -2

    this.edgeInfo = []
    this.regexIndex = 0
    this.resultList = []
    this.highlightBar = {

    }
    this.regDict = {

    }
    this.resultNum = 0
    this.curResult = []

    this.visTreeDataIndex = 0

    this.same_tree = {}

}

import { getComponentKey } from '@/utils/componentkey.js'
import { loadHierarchicalData } from '@/data/dataloading.js'
import { tychei } from 'seedrandom'

Dataset.prototype = {
    init: function() {
      
      this.Condition = {
        'ElementComposition': [
        ],
        'Aggregation': {
        'op': '',
        'attribute': '',
        'value': ['', '']
        },
        'Size': [0, 7188],
        'Height': [0, 10],
        'Width': [0, 2000],
        'Balanced': true,
      }
    },
    initData: function(data){
      this.initialData = data
    },
    returnInitData: function(){
      return this.initialData
    },
    initialRegexNode: function(){
        let regex = {
            "target":{
              "type": "target",
              "composition":[
                {
                  "type": "path",
                  "repeat": [1,1],
                  "key": getComponentKey(),
                  "composition":[
                    // {          
                    //     "type": "node",
                    //     "repeat": [1,1],
                    //     "data": {},
                    //     "key": getComponentKey()
                    // }
                  ]
                }
              ]
    
            },
            "condition": {
              "attribute": "size",
              "op": "max",
              "value": ""
            },
            "regexName": 'untitled'
        }
        let tmpData1 = {}
        let tmpData2 = [[]]
        let tmpList = []
        let tmpNodeList = [
          {
            'data':{},
            'nodeName':'.',
            'nodeColor': '#8E9898',
          },
          {
            'data':{"depth":{"op":"=","value":0}},
            'nodeName':'^',
            'nodeColor': '#D2BA4D',
          },
          {
            'data':{"degree":{"op":"=","value":0}},
            'nodeName':'$',
            'nodeColor': '#38B03F',
          }
        ]
        this.hierarchyDataIn.push(tmpData1)
        this.hierarchyDataOut.push(tmpData2)
        this.regexDataList.push(regex)
        this.connection.push(tmpList)
        this.nodeRegexList.push(tmpNodeList)
        this.curIndex = this.curIndex + 1
        return this.curIndex - 1
    },
    resetRegex: function(index){
      let tmpName = this.regexDataList[index]['regexName']
        this.regexDataList[index] = {
            "target":{
              "type": "target",
              "composition":[
                {
                  "type": "path",
                  "repeat": [1,1],
                  "key": getComponentKey(),
                  "composition":[
                    // {          
                    //     "type": "node",
                    //     "repeat": [1,1],
                    //     "data": {},
                    //     "key": getComponentKey()
                    // }
                  ]
                }
              ]
    
            },
            "condition": {
              "attribute": "size",
              "op": "max",
              "value": ""
            },
            "dataIndex": index,
            "regexName": tmpName
          }
    },
    returnRegex: function(index){
        return this.regexDataList[index]
    },
    returnRegexContent: function(index){
      return this.regexDataList[index]['regexContent']
  },
    returnHierarchyDataIn: function(index) {
      if(Object.keys(this.hierarchyDataIn[index]).length == 0){
        return [this.initialData]
      }
      else{
        let tmpList = []
        for(let key in this.hierarchyDataIn[index]){
          for(let tmpTree of this.hierarchyDataIn[index][key]){
            tmpList.push(tmpTree)
          }
        }
        return tmpList
      }
      
    },
    
    updateHierarchyDataOut: function(processed_hierarchy_data, index) {
      this.hierarchyDataOut[index] = processed_hierarchy_data['data']
    },
    returnHierarchyDataOut: function(index) {
      return this.hierarchyDataOut[index]
    },

    DataOut2DataIn: function(indexOut, indexIn) {
      this.connection[indexOut].push(indexIn)
      this.hierarchyDataIn[indexIn][indexOut] = []
      for(let item of this.hierarchyDataOut[indexOut]){
        for(let tmpTree of item){
          this.hierarchyDataIn[indexIn][indexOut].push(tmpTree)
        }
      }
    },

    DataOutFlow: function(index){
      for(let nextIndex of this.connection[index]){
        this.hierarchyDataIn[nextIndex][index] = []
        for(let item of this.hierarchyDataOut[index]){
          for(let tmpTree of item){
            this.hierarchyDataIn[nextIndex][index].push(tmpTree)
          }
        }
      }
    },
    returnConnection: function(index){
      return this.connection[index]
    },

    UpdataNodeList: function(node, index){
      let flag = true
      for(let tmpNode of this.nodeRegexList[index]){
        let len1 = Object.keys(node['data']).length
        let len2 =  Object.keys(tmpNode['data']).length
        if(len1==0 && len2==0){
          if(node['nodeName']==tmpNode['nodeName'] && node['nodeColor']==tmpNode['nodeColor']){
            flag = false 
            break
          }
        }
        else if(len1==len2){
          let tmpData = tmpNode['data']
          let tmpFlag = true
          for(let tmpKey in tmpData){
            if(tmpKey in node['data']){
              if(tmpData[tmpKey]['op']==node['data'][tmpKey]['op']){
                if(tmpData[tmpKey]['value']==node['data'][tmpKey]['value']){
                  continue                  
                }
              }
            }  
            tmpFlag = false
            break
          }
          if(tmpFlag){
            if(node['nodeName']==tmpNode['nodeName'] && node['nodeColor']==tmpNode['nodeColor']){
              flag = false 
              break
            }
          }
        }
      }
      if(flag){
        let tmpNode = {
          'type': 'listNode',
          'data':{},
          'nodeName':'',
          'nodeColor': '',
        }
        tmpNode['nodeName'] = node['nodeName']
        tmpNode['nodeColor'] = node['nodeColor']
        tmpNode['data'] = JSON.parse(JSON.stringify(node['data']))
        tmpNode['key'] = getComponentKey()     
        this.nodeRegexList[index].push(tmpNode)
        
      }
      //this.nodeRegexList[index].push(node)
    },
    returnNodeList: function(index){
      return this.nodeRegexList[index]
    },
    updateRegexName: function(name, index){
      this.regexDataList[index]['regexName'] = name
    },
    returnRegexName: function(index){
      return this.regexDataList[index]['regexName']
    },

    deleteDataConnection: function(indexOut, indexIn){
      this.connection[indexOut].map((val, i) => {
        if(val == indexIn){
          this.connection[indexOut].splice(i ,1)
        }
      })
      delete this.hierarchyDataIn[indexIn][indexOut]
    },
    deleteDataNode: function(index){
      for(let key in this.hierarchyDataIn[index]){
        this.deleteDataConnection(key, index)
      }
      for(let tmpIndex of this.connection[index]){
        this.deleteDataConnection(index, tmpIndex)
      }
    },

    updateVis: function(data){
      this.visData = data
    },
    updateVisList: function(data){
      this.visList = data
    },
    getVisData: function(){
      return this.visData
    },
    getVisList: function(){
      return this.getVisList
    },
    getCondition: function(){
      return this.Condition
    },
    addExist: function(){
      let tmpExist = {
          'type':'exist',
          'repeat': ['1', '*'],
          'node':{
              'type': 'node',
              'eleFlag': true,
              'nodeName': '.',
              'nodeColor': '#ABABAB',
              'data':[

              ],
              "key": getComponentKey()
          }
      }
      this.Condition['ElementComposition'].push(tmpExist)
    },
    addAll: function(){
      let tmpAll =  {
        'type':'all',
        'node':{
            'type': 'node',
            'eleFlag': true,
            'nodeName': '.',
            'nodeColor': '#ABABAB',
            'data':[

            ],
            "key": getComponentKey()
        },
    }
      this.Condition['ElementComposition'].push(tmpAll)
    },
    deleteEleNode: function(){
      for(let i=0;i<this.Condition.ElementComposition.length; i++){
        if(this.Condition.ElementComposition[i]['node']['key'] == this.selectedDomKey){
          this.Condition.ElementComposition.splice(i, 1)
        }
      }
    },
    updateSelectedDomKey: function(key){
      this.selectedDomKey = key
    },
    getSelectedDomKey: function(){
      return this.selectedDomKey
    },
    updateSelectedBranch: function(branch, index){
      this.selectedBranch = branch
      this.branchIndex = index
    },
    getSelectedBranch: function(){
      return this.selectedBranch
    },
    getSelectedBranchIndex: function(){
      return this.branchIndex 
    },
    updateSelectedOr: function(or, index){
      this.selectedOr = or
      this.orIndex = index
    },
    getSelectedOr: function(){
      return this.selectedOr
    },
    getSelectedOrIndex: function(){
      return this.orIndex 
    },
    getRegexIndex: function(){
      this.regexIndex += 1
      return this.regexIndex-1 
    },
    addEdge: function(index1, index2){
      var flag = 1
      for(let i=0; i<this.edgeInfo.length; i++){
        if(this.edgeInfo[i][0] == index1 && this.edgeInfo[i][1] == index2){
          flag = -1
          break
        }
      }
      if(flag == 1)
        this.edgeInfo.push([index1, index2])
    },
    deleteEdge: function(index){
      for(let i=this.edgeInfo.length-1; i>=0; i--){
        if(this.edgeInfo[i][0] == index || this.edgeInfo[i][1] == index){
          this.edgeInfo.splice(i, 1)
        }
      }
    },
    deleteEdge1: function(index1, index2){
      for(let i=this.edgeInfo.length-1; i>=0; i--){
        if(this.edgeInfo[i][0] == index1 || this.edgeInfo[i][1] == index2){
          this.edgeInfo.splice(i, 1)
        }
      }
    },
    getEdgeInfo: function(){
      return this.edgeInfo
    },
    updateRegex: function(regex){
      this.Regex = regex
    },
    getRegex: function(){
      return this.Regex
    },
    updateResultList: function(data){
      this.queryList = data
    },
    getResultList: function(){
      return this.queryList
    },
    updatehighlightBar: function(data){
      this.highlightBar = data
    },
    gethighlightBar: function(){
      return this.highlightBar
    },
    updateRegDict: function(data){
      this.regDict = data
    },
    getRegDict: function(){
      return this.regDict
    },
    updateResultNum: function(data){
      this.resultNum = data
    },
    getResultNum: function(){
      return this.resultNum
    },
    updateCurResult: function(data){
      this.curResult = data
    },
    getCurResult: function(){
      return this.curResult
    },
    updateVisTree: function(index){
      console.log("visTreeDataIndex", this.visTreeDataIndex)
      this.visTreeDataIndex = index
    },
    getVisTreeData: function(){
      return this.curResult[this.visTreeDataIndex]
    },
    updateSameTree: function(data){
      this.same_tree = data
    },
    getSameTree: function(index){
      if(index in this.same_tree)
        return this.same_tree[index]
      else 
        return index
    }



}