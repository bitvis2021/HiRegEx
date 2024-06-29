<template>
  <div id="app" v-loading="loadingData">
    <el-menu
        class="el-menu-demo"
        mode="horizontal"
        background-color="#676767"
        text-color="#fff"
        :default-active="activeIndex"
        active-text-color="#ffd04b">
        <el-menu-item class='labelIcon' id="title">
          {{appName}}
        </el-menu-item> 
    </el-menu>
    <div class = "content-container" v-if="!loadingData">
      <div class="overview-panel">
        <OverviewPanel></OverviewPanel>
      </div>
      <div class="vis-panel">
        <VisPanel></VisPanel>
      </div>

      <div class="editor-panel">
        <EditorPanel></EditorPanel>
      </div>
      <div class="regs-panel">
         <RegRecommendPanel></RegRecommendPanel>
      </div>

      <div class="trees-panel">
        <RecommendPanel></RecommendPanel>
      </div>
    </div>
  </div>
</template>

<script>

import { mapState, mapMutations } from 'vuex';
import OverviewPanel from './views/OverviewPanel.vue'
import VisPanel from './views/VisPanel.vue'
import RecommendPanel from './views/RecommendPanel.vue'
import EditorPanel from './views/EditorPanel.vue'
import RegRecommendPanel from './views/RegRecommendationPanel.vue'

import { loadHierarchicalData } from './data/dataloading.js'
import { Dataset}  from './data/dataset.js'
import { getHierarchyData } from './communication/communicator.js'
import { getComponentKey } from '@/utils/componentkey.js'
  import { readFile } from 'fs';
  import * as fs from 'fs';

export default {
  name: 'app',
  components: {
    OverviewPanel,VisPanel,RecommendPanel,EditorPanel,RegRecommendPanel
  },
  data() {
    return {
      appName: "TreeQueryER",
      operationArray: ['data'],
      activeIndex: '',
      loadingData: false,
      curIndex: 0,
    }
  },
  computed: {
    ...mapState([
      'displayMode',
      'curRegex',
      'regexCommitState',
      'attributeList',
      'regexViewState',
      'visViewState',
      'curRegexIndex',
      'curConnectionNode',
      'connectionState',

      'queryStateIndex',
      'queryStateRegex',
      'queryIndex',
      'queryPage',
      'queryStatePage',
      'queryStateCoding',
      'queryCoding',
    ]),
  },
  watch:{
    regexCommitState: function(){
      this.regexQuery(this.curRegexIndex)
    },
    connectionState: function(){
      this.regexQuery(this.curConnectionNode)
    },

    queryStateIndex: function(){
      this.dataQuery1(this.queryIndex)
    },
    queryStateRegex: function(){
      this.dataQuery2()
    },
    queryStatePage: function(){
      this.dataQuery3(this.queryPage)
    },
    queryStateCoding: function(){
      this.dataQuery4(this.queryCoding)
    }

  },
  beforeMount() {
    let self = this
    window.sysDatasetObj = new Dataset()
    sysDatasetObj.init()
    loadHierarchicalData('treeDataset/new_same_tree1.json', function(data){
    sysDatasetObj.updateSameTree(data)
    })
  },
  mounted() {

  },
  methods: {
    ...mapMutations([
      'UPDATE_ATTRIBUTE_LIST_NUMBER',
      'UPDATE_ATTRIBUTE_LIST_STRING',
      'UPDATE_ATTRIBUTE_LIST_BOOLEAN',
      'UPDATE_VISVIEW',

      'DATA_QUERY_INDEX',
      'UPDATE_VIS_PANEL',
      'UPDATE_REG_PANEL',
      'UPDATE_TREE_LIST'
    ]),
    iconClass(operation) {
      return 'icon-' + operation
    },
    REViewStyle(){
      if(this.regexViewState){
        return "position: absolute; " + 
          "top: 40%; " +
          "left: 0%; " +
          "bottom: 0%; " +
          "right: 0%; "
      }
      else{
        return "position: absolute; " + 
          "top: 40%; " +
          "left: 0%; " +
          "bottom: 0%; " +
          "right: 0%; " +
          "display:none; !important"
      }
    },
    VisViewStyle(){
      if(this.visViewState){
        return "position: absolute; " + 
          "top: 40%; " +
          "left: 0%; " +
          "bottom: 0%; " +
          "right: 0%; "
      }
      else{
        return "position: absolute; " + 
          "top: 100%; " +
          "left: 0%; " +
          "bottom: 0%; " +
          "right: 0%; "
      }
    },
    regexQuery(regexIndex){
      let self = this
      let hierarchyDataDeferObj = $.Deferred()
      $.when(hierarchyDataDeferObj).then(function() {
        self.loadingData = false
      })
      
      let hierarchicalParam = {
        'regex': sysDatasetObj.returnRegex(regexIndex),
        'hierarchyData': sysDatasetObj.returnHierarchyDataIn(regexIndex)
      }
      getHierarchyData(hierarchicalParam, function(processed_hierarchy_data) {
        sysDatasetObj.updateHierarchyDataOut(processed_hierarchy_data, regexIndex)
        hierarchyDataDeferObj.resolve()
        self.UPDATE_VISVIEW()
        sysDatasetObj.DataOutFlow(regexIndex)
        let tmpIndexList = sysDatasetObj.returnConnection(regexIndex)
        for(let tmpIndex of tmpIndexList){
          self.regexQuery(tmpIndex)
        }
      })
    },

    dataQuery1(queryIndex){
      let self = this
      let hierarchyDataDeferObj = $.Deferred()
      $.when(hierarchyDataDeferObj).then(function() {
        self.loadingData = false
      })
      let hierarchicalParam = {
        'type': 1,
        'index': queryIndex
      }
      getHierarchyData(hierarchicalParam, function(processed_hierarchy_data) {
        sysDatasetObj.updateVis(processed_hierarchy_data['visualization'])
        sysDatasetObj.updateResultNum(processed_hierarchy_data['list_num'])
        sysDatasetObj.updateCurResult(processed_hierarchy_data['vis_list'])
        hierarchyDataDeferObj.resolve()
        self.UPDATE_VIS_PANEL()
      })

    },
    dataQuery2(){
      let self = this
      let hierarchyDataDeferObj = $.Deferred()
      $.when(hierarchyDataDeferObj).then(function() {
        self.loadingData = false
      })
      let hierarchicalParam = {
        'type': 2,
        'regex':sysDatasetObj.getRegex(),
        'condition':sysDatasetObj.getCondition(),
      }
      console.log("hierarchicalParam", hierarchicalParam)
      getHierarchyData(hierarchicalParam, function(processed_hierarchy_data) {
        console.log("processed_hierarchy_data: ",processed_hierarchy_data)
        sysDatasetObj.updateVis(processed_hierarchy_data['visualization'])
        sysDatasetObj.updateResultList(processed_hierarchy_data['result'])
        sysDatasetObj.updatehighlightBar(processed_hierarchy_data['highlightBar'])
        sysDatasetObj.updateRegDict(processed_hierarchy_data['reg_dict'])
        sysDatasetObj.updateResultNum(processed_hierarchy_data['result_num'])
        sysDatasetObj.updateCurResult(processed_hierarchy_data['cur_result'])
        let highlight_list = processed_hierarchy_data['highlight_list']
        d3.selectAll(".dot").classed("dot-selected", false)
        for(let data_index of highlight_list){
          d3.select("#dot"+data_index).classed("dot-selected", true)

          let tmp_transform = d3.select('#dot'+data_index).attr("transform")
          let tmp_data = d3.select('#dot'+data_index).data()

          let tmp_x = +d3.select('#dot'+data_index).attr("x")
          let tmp_y = +d3.select('#dot'+data_index).attr("y")
          let tmp_r = +d3.select('#dot'+data_index).attr("r")
          
          d3.select('#dot'+data_index).remove()

          d3.select(".overview-svg")
          .selectAll('#dot'+data_index)
              .data(tmp_data)
              .enter()
              .append("circle")
              .attr("class","dot")
              .attr("id", function(d) { return "dot"+data_index})
              .classed("dot-selected", true)
              .attr("transform", function(d){
                return tmp_transform;
              })
              .attr("m", function(d) {return d['m']})
              .attr("r", function(){
                return tmp_r;
              })
              .on('click', function(){
                  self.DATA_QUERY_INDEX(parseInt(this.getAttribute("m")))
              });
        }
        hierarchyDataDeferObj.resolve()
        self.UPDATE_VIS_PANEL()
        self.UPDATE_REG_PANEL()

      })
    },
    dataQuery3(page_index){
        let self = this
        let hierarchyDataDeferObj = $.Deferred()
        $.when(hierarchyDataDeferObj).then(function() {
          self.loadingData = false
        })
        let hierarchicalParam = {
          'type': 3,
          'index': page_index
        }
        getHierarchyData(hierarchicalParam, function(processed_hierarchy_data) {
          sysDatasetObj.updateCurResult(processed_hierarchy_data['cur_result'])
          sysDatasetObj.updateVis(processed_hierarchy_data['visualization'])
          hierarchyDataDeferObj.resolve()
          self.UPDATE_TREE_LIST()
        })
    },
    dataQuery4(reg_coding){
        let self = this
        let hierarchyDataDeferObj = $.Deferred()
        $.when(hierarchyDataDeferObj).then(function() {
          self.loadingData = false
        })
        let hierarchicalParam = {
          'type': 4,
          'coding': reg_coding
        }
        getHierarchyData(hierarchicalParam, function(processed_hierarchy_data) {
          sysDatasetObj.updateVis(processed_hierarchy_data['visualization'])
          sysDatasetObj.updateResultNum(processed_hierarchy_data['result_num'])
          sysDatasetObj.updateCurResult(processed_hierarchy_data['cur_result'])
          hierarchyDataDeferObj.resolve()
          self.UPDATE_VIS_PANEL()
        })
    }
  },
}
</script>

<style lang="less">
html {
  font-size: 100%;
}
@menu-height: 2rem;
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  position: absolute;
  top: 0%;
  bottom: 0%;
  left: 0%;
  right: 0%;
  background-color: rgb(218, 218, 218);
  .el-menu.el-menu--horizontal {
    .el-menu-item {
      height: @menu-height;
      line-height: @menu-height;
    }
    .el-menu-item {
      border-bottom-color: rgb(84, 92, 100) !important;
      font-weight: bolder;
      font-size: 1rem;
      color: #dadada !important;
      padding: 0 10px;
      .icon {
        color: #dadada !important;
      }
    }
  }
  .labelIcon {
    font-size: 1rem;
  }
  .content-container {
    position: absolute;
    top: @menu-height;
    left: 0%;
    bottom: 0%;
    right: 0%;
    .overview-panel{
      position: absolute;
      top: 0px;
      left: 0px;
      bottom: 0px;
      right: 80%;
      background-color: white;
      border-right: 1px #ddd solid;
    }
    .vis-panel{
      position: absolute;
      top: 0px;
      left: 20%;
      bottom: 40%;
      right: 30%;
      background-color: white;
    }
    .editor-panel{
      position: absolute;
      top: 0px;
      left: 70%;
      bottom: 40%;
      right: 0px;
      background-color: white;
      border-left: 1px #ddd solid;
    }
    .regs-panel{
      position: absolute;
      top: 60%;
      left: 70%;
      bottom: 0px;
      right: 0px;
      background-color: white;
      border-left: 1px #ddd solid;
      border-top: 1px #ddd solid;;
    }
    .trees-panel{
      position: absolute;
      top: 60%;
      left: 20%;
      bottom: 0px;
      right: 30%;
      background-color: white;
      border-top: 1px #ddd solid;
    }

  }
  	.node {
		cursor: pointer;
	}

	.node circle {
	  fill: #fff;
	  stroke: rgb(70, 90, 180);
	  stroke-width: 3px;
	}

	.link {
	  fill: none;
	  stroke: #ccc;
	  stroke-width: 2px;
	}
}

.gLink{
  fill: none;
  stroke: #555;
}
</style>
