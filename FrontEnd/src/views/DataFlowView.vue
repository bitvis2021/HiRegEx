<template>
  <div class="dataflow-view">
      <div id="page">
      <div id="header">
        <span class="header-title">
          Visual Editor
        </span>

      </div>
      <div class="container">
        <div class="flowchart-container">
          <flowchart
            ref="chart"
            :nodes="nodes"
            :connections="connections"
            @editnode="handleEditNode"
            :width="'100%'"
            :height="500"
            :readonly="false"
            :excludeShownAttrArray="excludeShownAttrArray"
            >
          </flowchart>
        </div>

      </div>
            <div id="btn-list">
              <svg class="btnIcon" xmlns="http://www.w3.org/2000/svg" id="addNode" @click="addComponent(componentList[1])" viewBox="0 0 108.64 108.64" width="35px" height="35px"><g id="图层_2" data-name="图层 2"><g id="图层_1-2" data-name="图层 1"><rect class="cls-1" x="0.5" y="0.5" width="107.64" height="107.64" rx="10" style="fill:#f8f8f8;"/><rect class="cls-2" x="0.5" y="0.5" width="107.64" height="107.64" rx="10" style="fill:none;stroke:#6b6b6b;stroke-miterlimit:10;"/><path class="cls-3" d="M46.35,53.82h-16v-16a2,2,0,0,0-4,0v16h-16a2,2,0,0,0,0,4h16v16a2,2,0,0,0,4,0v-16h16a2,2,0,0,0,0-4Z"/><text class="cls-4" transform="translate(48.35 82.22)" style="font-size:72px;font-family:Lato-Italic, Lato;font-style:italic;">N</text></g></g></svg>
              <svg class="btnIcon" xmlns="http://www.w3.org/2000/svg" id="addBranch" @click="addComponent(componentList[2])" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 108.64 108.64" width="35px" height="35px"><defs><clipPath id="clip-path"><rect class="cls-1" x="48.8" y="22.82" width="48.75" height="65"/></clipPath></defs><g id="图层_2" data-name="图层 2"><g id="图层_1-2" data-name="图层 1"><rect style="fill:#f8f8f8;" class="cls-2" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><rect style="stroke:#6b6b6b;stroke-miterlimit:10; fill:none;" class="cls-3" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><g class="cls-4" style="clip-path:url(#clip-path);"><path class="cls-5" style="fill:#2c2c2c;" d="M56.94,76.09a3.55,3.55,0,1,1-3.55,3.54,3.55,3.55,0,0,1,3.55-3.54ZM69.62,30.93a3.54,3.54,0,1,1,3.55,3.55,3.55,3.55,0,0,1-3.55-3.55ZM93,79.63a3.55,3.55,0,1,1-3.55-3.54A3.55,3.55,0,0,1,93,79.63Zm-44.13,0a8.12,8.12,0,1,0,10.39-7.79V63.72l14-13.85,14,13.88v8.12a8.12,8.12,0,1,0,4.57,0v-10L75.5,45.68V38.81a8.11,8.11,0,1,0-4.58,0v6.81L54.69,61.86v10a8.12,8.12,0,0,0-5.87,7.79Z"/></g><path class="cls-5" d="M45.05,53.82h-16v-16a2,2,0,0,0-4,0v16h-16a2,2,0,0,0,0,4h16v16a2,2,0,0,0,4,0v-16h16a2,2,0,0,0,0-4Z"/></g></g></svg>
              <svg class="btnIcon" xmlns="http://www.w3.org/2000/svg" id="And" @click="concatClick" viewBox="0 0 108.64 108.64" width="35px" height="35px"><g id="图层_2" data-name="图层 2"><g id="图层_1-2" data-name="图层 1"><rect class="cls-1" style="fill:#f8f8f8;" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><rect class="cls-2" style="fill:none;stroke:#6b6b6b;stroke-miterlimit:10;" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><path class="cls-3" style="fill:#2c2c2c;" d="M77.57,60.82l4.49,4.76q-4.86,4.31-7.78,6.59,5.31,5.31,12.45,13H77.57l-8.42-8.78q-8.24,6.23-13.37,8.33a29.15,29.15,0,0,1-11.17,2.1,17.2,17.2,0,0,1-12.13-4.35,13.93,13.93,0,0,1-4.71-10.66A18.11,18.11,0,0,1,32,60.23a69.48,69.48,0,0,1,11.62-11A55.53,55.53,0,0,1,36.79,40a13.51,13.51,0,0,1-1.7-6.27,10.49,10.49,0,0,1,4.21-8.56,16.53,16.53,0,0,1,10.58-3.34,15.09,15.09,0,0,1,10.39,3.57,10.86,10.86,0,0,1,4,8.33A13.57,13.57,0,0,1,62,40.86q-2.33,3.77-9.2,9.53L69.6,67.69c2.71-2.24,5.36-4.52,8-6.87ZM48.73,45.44q8.88-7,8.88-11.72a4.9,4.9,0,0,0-2.24-4,9.17,9.17,0,0,0-5.68-1.69A9.55,9.55,0,0,0,44,29.7,5.07,5.07,0,0,0,41.68,34q0,3.66,7,11.44Zm-.82,8.79q-8.52,6.41-11,10.12a12.76,12.76,0,0,0-2.52,7.14,8.41,8.41,0,0,0,3.21,6.31A10.69,10.69,0,0,0,45,80.69a20.33,20.33,0,0,0,8.51-2,72,72,0,0,0,11.17-6.91Z"/></g></g></svg>
              <svg class="btnIcon" xmlns="http://www.w3.org/2000/svg" id="Or" @click="orClick" viewBox="0 0 108.64 108.64" width="35px" height="35px"><g id="图层_2" data-name="图层 2"><g id="图层_1-2" data-name="图层 1"><rect class="cls-1" style="fill:#f8f8f8;" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><rect class="cls-2" style="fill:none;stroke:#6b6b6b;stroke-miterlimit:10;" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><path style="fill:#2c2c2c;" class="cls-3" d="M49.3,23.32v65h-5v-65Zm15,0v65h-5v-65Z"/></g></g></svg>
              <svg class="btnIcon" xmlns="http://www.w3.org/2000/svg" id="Not" @click="notClick" viewBox="0 0 108.64 108.64" width="35px" height="35px"><g id="图层_2" data-name="图层 2"><g id="图层_1-2" data-name="图层 1"><rect class="cls-1" style="fill:#f8f8f8;" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><rect class="cls-2" style="fill:none;stroke:#6b6b6b;stroke-miterlimit:10;" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><path class="cls-3" style="fill:#2c2c2c;" d="M52.17,64.48a4,4,0,0,0,7.8,0l2.6-35.75a6.51,6.51,0,0,0-6.5-6.5,6.67,6.67,0,0,0-6.5,7.15Zm3.9,9.75a6.5,6.5,0,1,0,6.5,6.5,6.15,6.15,0,0,0-6.5-6.5Z"/></g></g></svg>
              <svg class="btnIcon" xmlns="http://www.w3.org/2000/svg" id="Repeat" @click="upperClick" viewBox="0 0 108.64 108.64" width="35px" height="35px"><g id="图层_2" data-name="图层 2"><g id="图层_1-2" data-name="图层 1"><rect class="cls-1" style="fill:#f8f8f8;" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><rect class="cls-2" style="fill:none;stroke:#6b6b6b;stroke-miterlimit:10;" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><text class="cls-3" style="font-size:72px;font-family:Lato-Italic, Lato;font-style:italic;" transform="translate(19.01 80.72)">N</text><text class="cls-4" transform="translate(72.28 67.19)" style="fill:#2c2c2c;font-size:60px;font-family:Lato-Bold, Lato;font-weight:700;">*</text></g></g></svg>
              <svg class="btnIcon" xmlns="http://www.w3.org/2000/svg" id="Delete" @click="$refs.chart.remove(); eleNodeRemove()" viewBox="0 0 108.64 108.64" width="35px" height="35px"><g id="图层_2" data-name="图层 2"><g id="图层_1-2" data-name="图层 1"><rect class="cls-1" style="fill:#f8f8f8;" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><rect class="cls-2" style="fill:none;stroke:#6b6b6b;stroke-miterlimit:10;" x="0.5" y="0.5" width="107.64" height="107.64" rx="10"/><path class="cls-3" d="M62.42,73.4a2.32,2.32,0,0,1-2.32-2.33V45.53a2.32,2.32,0,1,1,4.64,0V71.06a2.33,2.33,0,0,1-2.32,2.34Z"/><path class="cls-3" d="M48.49,73.4a2.32,2.32,0,0,1-2.32-2.33V45.53a2.32,2.32,0,0,1,4.64,0V71.06a2.33,2.33,0,0,1-2.32,2.34Z"/><path class="cls-3" style="fill:#2c2c2c;" d="M85.64,33.93H74V29.28a6.94,6.94,0,0,0-6.92-7H43.85a7,7,0,0,0-7,7v4.65H25.28a2.32,2.32,0,0,0,0,4.64H85.64a2.32,2.32,0,0,0,0-4.64ZM41.53,29.28A2.33,2.33,0,0,1,43.85,27H67.12a2.27,2.27,0,0,1,2.27,2.32v4.65H41.53Z"/><path class="cls-3" d="M71.72,87.32H39.22a7,7,0,0,1-7-7V45.51a2.32,2.32,0,1,1,4.64,0V80.36a2.33,2.33,0,0,0,2.32,2.32H71.73a2.32,2.32,0,0,0,2.32-2.32V45.59a2.32,2.32,0,1,1,4.64,0V80.36a7,7,0,0,1-7,7Z"/></g></g></svg>
          </div>
  </div>
  </div>
  
</template>


<script>

import { mapState, mapMutations } from 'vuex';
import Flowchart from "./flowchart/Flowchart";
import { getComponentKey } from '../utils/componentkey';


export default {
  name: 'DataFlowView',
  components: {
    Flowchart,
  },
  props: {

  },
  data() {
      return {
        nodes: [],
        connections: [],
        nodeForm: { target: null },
        connectionForm: { target: null, operation: null },
        defaultX: 10,
        defaultY: 55,
        defaultWidth: 45,
        defaultHeight: 45,
        componentList: [
          {type: 'data', color: '#fdbf6f', name: 'data'},
          {type: 'query', color: '#ff7f00', name: 'query'},
          {type: 'vis', color: '#cab2d6', name: 'vis'},
        ],
        excludeShownAttrArray: ['type', 'color', 'render', 'width', 'height', 'x', 'y', 'name', 'id'],
        visible: false,

      }
  },
 async mounted() {},
    computed: {
    ...mapState([
      'initialData',
      'selectedDom'
    ]),
   
  },
  methods: {
    ...mapMutations([
      'UPDATE_CURRENT_REGEX',
      'DELETE_REGEX_LIST',
      'SHOW_REVIEW',
      'SHOW_VISVIEW',
      'UPDATE_CURRENT_DATA',
      'UPDATE_REVIEW_DATA',
      'UPDATE_REPEAT_STATE'
    ]),
    concatClick(){
      var branch= sysDatasetObj.getSelectedBranch()
      var index = sysDatasetObj.getSelectedBranchIndex()
      var newNode =  {
              'type': 'node',
              'repeat': [1, 1],
              'key': getComponentKey(),
              'nodeName': '.',
              'nodeColor': '#ABABAB',
              'data': {

              }
            }   
      branch['composition'].splice(index+1, 0, newNode)
    },
    upperClick(){
      this.UPDATE_REPEAT_STATE(true)
    },
    orClick(){
      var Or = sysDatasetObj.getSelectedOr()
      var index = sysDatasetObj.getSelectedOrIndex()
      if(index == -1){
        Or['type'] = 'or'
        Or['composition'] = [
          {
            'type': 'node',
            'repeat': [1, 1],
            'data': JSON.parse(JSON.stringify(Or['data'])),
            'nodeName': Or['nodeName'],
            'nodeColor': Or['nodeColor'],
            'key': getComponentKey()
          },
          {
            'type': 'node',
            'repeat': [1, 1],
            'nodeName': '.',
            'nodeColor': '#ABABAB',
            'data': {

            },
            'key': getComponentKey()
          }
        ]
        if('definition' in Or && Or['definition']){
          Or['composition'][0]['definition'] = Or['definition']
          Or['composition'][0]['nodeName'] = Or['nodeName']
          Or['composition'][0]['nodeColor'] = Or['nodeColor']
        }
        if('notFlag' in Or && Or['notFlag']){
          Or['composition'][0]['notFlag'] = Or['notFlag']
        }
        delete Or['data']
      }
      else if(index != -2){
              var newNode =  {
              'type': 'node',
              'repeat': [1, 1],
              'key': getComponentKey(),
              'nodeName': '.',
              'nodeColor': '#ABABAB',
              'data': {

              }
            }   
        Or['composition'].splice(index+1, 0, newNode)
      }
    },
    notClick(){
      if(!('notFlag' in this.selectedDom)){
        this.selectedDom['notFlag'] = true
      }
      else{
        this.selectedDom['notFlag'] = !this.selectedDom['notFlag']
      }

    },
    eleNodeRemove(){
      if('eleFlag' in this.selectedDom && this.selectedDom['eleFlag']){
        sysDatasetObj.deleteEleNode()
      }
    },
    handleEditNode(node) {
      // edit the detailed information of nodes when clicking "edit" button
      // specifically, show the dialog of editing nodes' detailed information
      this.nodeForm.target = node;
      if(node['type'] == 'query'){
        //this.nodeDialogVisible = true;
        this.UPDATE_REVIEW_DATA()
        this.SHOW_REVIEW()    
      }
    },
    handleAddComponent(componentObj) {
      // The component object contains
      // 1. name
      // 2. type
      // 3. color
      // 4. many attributes in attribute list [['attribute1'], ['attribute2'], ...]
      this.componentList.push(componentObj)
    },

    addComponent(component) {
      // add new component in the component list
      let defaultX = this.defaultX, defaultY = this.defaultY, 
          defaultWidth = this.defaultWidth, defaultHeight = this.defaultHeight
      let initComponent = {}
      // id, x, y, width, height, name, type, and color are required attributes
      initComponent['id'] = +new Date()
      initComponent['x'] = defaultX
      initComponent['y'] = defaultY
      initComponent['width'] = defaultWidth
      initComponent['height'] = defaultHeight
      // defualt attributes are name, type, and color
      initComponent['name'] = component.name
      initComponent['type'] = component.type
      initComponent['color'] = component.color
      if(component['type'] == 'query'){   
        initComponent['regex'] =  {
              'type': 'node',
              'repeat': [1, 1],
              'key': getComponentKey(),
              'nodeName': '.',
              'nodeColor': '#ABABAB',
              'data': {

              }
          }  
        initComponent['regexIndex'] = sysDatasetObj.getRegexIndex() 
      }
      else if(component['type'] == 'vis'){
          initComponent['regex'] = {
          'type': 'branch',
          'key': getComponentKey(),
          'repeat': [1 ,1],
          'composition': [
            {
              'type': 'node',
              'repeat': [1, 1],
              'key': getComponentKey(),
              'nodeName': '.',
              'nodeColor': '#ABABAB',
              'data': {

              }
            },
            ]
          }
          initComponent['regexIndex'] = sysDatasetObj.getRegexIndex()   
      }

      // the attributes in the attribute list is the optional attribute
      if (typeof(component.attributes) !== 'undefined') {
        for (let i = 0; i < component.attributes.length; i++) {
          let attrName = component.attributes[i]
          initComponent[attrName] = ""
        }
      }
      this.$refs.chart.add(initComponent)
    },

  },
};
</script>
<style lang="less" scoped>
@header-height: 1rem;
@component-div-width: 0px;
@description-div-width: 0px;
@description-div-margin: 10px;
.dataflow-view {
  height: 100%;
  width: 100%;
  #page{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgb(255, 255, 255);
  overflow-y: hidden;
  #header {
    position: absolute;
    top: 0%;
    left: 0%;
    width: 100%;
    height: 2rem;
    line-height: @header-height;
    font-size: 1rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    .header-title {
      margin-left: 5px;
      font-size: 1rem;
      font-weight: bolder;
      color: black;
      top: 5px;
      left: 5px;
    }
    .navitem {
      display: inline-block;
      cursor: pointer;
      margin: 0px 10px;
      padding: 2px;
      &:hover {
        background: #eeeeee;
      }
    }
    .navtitle {
      cursor: pointer;
    }
    .el-button{
      font-family:element-icons !important;
      font-weight:330 !important;
      font-size:25px !important;
      color:white !important;
    }
  }
  .container {
    position: absolute;
    top: 2rem;
    width: 100%;
    bottom: 0%;
    left: 0%;
    .flowchart-container {
      position: absolute;
      right: 0;
      top: 0%;
      bottom: 0%;
      left:0;
    }
  }
  #btn-list{
    position: absolute;
    right: 10px;
    top: 70px;
    display: flex;
    flex-direction: column;
    justify-content: center;
      .btnIcon{
          margin-top: 10px;
          cursor: pointer;
        }
    }
  }
}
#toolbar {
  margin-bottom: 10px;
}

.title {
  margin-top: 10px;
  margin-bottom: 0;
}

.subtitle {
  margin-bottom: 10px;
}

#toolbar > button {
  margin-right: 4px;
}
</style>



