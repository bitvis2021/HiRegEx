<template>
<div class="re-elementComposition">
    <a class="elecomp-text">EleComp:</a>
    <div v-for="(item1, index1) of elementCompositionExpression" :key="computeExistKey(index1)" style="height: 90%; display: flex; flex-direction: row;">
                <svg style="width:51px;">
                    <text v-if="item1['type']=='exist'" :transform="commonTransform1(item1, index1)" style="alignment-baseline: hanging; font-size: 30px">∃</text>
                    <text v-if="item1['type']=='all'" :transform="commonTransform2(item1, index1)" style="alignment-baseline: hanging; font-size: 30px">∀</text>
                    <EleNode :nodeExpression="item1['node']"></EleNode>
                </svg>
                <div class="input-list" style="display:flex; flex-direction:column; left:0px; width:8px;">
                  <input v-if="item1['type']=='exist'" class="attr-input1" type="text" name="ticketNum" v-model="item1['repeat'][0]">
                  <input v-if="item1['type']=='exist'" class="attr-input2" type="text" name="ticketNum" v-model="item1['repeat'][1]">
                </div>
                <svg v-if="item1['type']=='exist'" style="position:relative; width: 2%; left: 13px; width:31px;">
                  <path :d="pathCompute" style=" stroke: #000000; stroke-width: 3px; fill: none;"/>
                </svg>
                <svg v-if="item1['type']=='all'" style="position:relative; width: 2%; left: 13px;  width:31px;">
                  <path :d="pathCompute" style=" stroke: #000000; stroke-width: 3px; fill: none;"/>
                </svg>
    </div>
    <el-tooltip class="navitem" key="add" content="add component" effect="light" style="position:relative; left: 0px; margin-top: 5px;">
            <div slot="content">
              <span class="navitem" @click="addExist()">
                  Exist
              </span>
              <span class="navitem" @click="addAll()">
                  All
              </span>
            </div>
            <i class="el-icon-circle-plus-outline"></i>
    </el-tooltip>
</div>
</template>

<script>
    import { mapState, mapMutations } from 'vuex';
    import EleNode from './EleNode.vue';

export default {
  name: 'ElementComposition',
  components: {
    EleNode
  },
  props: {
    elementCompositionExpression:{
      type: Array
    }
  },
  data() {
    return {
        test: 100,
        visible: false,

    }
  },
  beforeMount(){
    console.log('elementCompositionExpression', this.elementCompositionExpression)
  },
  mounted() {
  },
  computed: {
    ...mapState([
      'displayMode',
      'selectedDom',
    ]),
    pathCompute(){
      var x1 = 0
      var y1 = 3
      var x2 = 0
      var y2 = 27
    	return ( "M " +  x1 + " " +  y1 +
         		" L " + x2 + " " + y2 );
    },
    pathTranslate(){
      return "translate(75, 0)" 
    }
   
  },
    watch: {
      displayMode: function() {
        console.log('displayMode')
      },
  },
  methods: {
    ...mapMutations([
      'UPDATE_SELECTED_DOM',
      'UPDATE_NODE_DEFINITION_STATE',
    ]),
    computeExistKey(d){
        return 'exist' + d
    },
    computeAllKey(d){
        return 'all' + d
    },
    computeExistItemKey(d){
        return 'existItem' + d
    },
    commonTransform1(test, index){
        return `translate(${0}, ${0})`
    },
    commonTransform2(x, y){
        return `translate(${0}, ${0})`
    },
    leftBracketCompute(x1, y1, x2, y2)
	{
            var qx = x1-(y2-y1)/3
            var qy = (y2+y1)/2

    	return ( "M " +  x1 + " " +  y1 +
         		" Q " + qx + " " + qy + " " + x2 + " " + y2 );
    },
    rightBracketCompute(x1, y1, x2, y2)
	{
        var qx = x1+(y2-y1)/3
        var qy = (y2+y1)/2

    	return ( "M " +  x1 + " " +  y1 +
         		" Q " + qx + " " + qy + " " + x2 + " " + y2 );
    },
    updateSelectedElementComposition() {
        this.UPDATE_SELECTED_DOM(this.elementCompositionExpression)
    },
    updateSelectedExist(d) {
        this.UPDATE_NODE_DEFINITION_STATE(true)
        this.UPDATE_SELECTED_DOM(d)
    },
    updateSelectedAll(d){
      this.UPDATE_NODE_DEFINITION_STATE(true)
      this.UPDATE_SELECTED_DOM(d)
    },
    selectedStyle(d){
        if(d.key == this.selectedDomKey){
            return ( "fill: red !important; " + 
                     "stroke-width: 0px;");
        }
    },
    elementCompositionCheck(){
      if(this.elementCompositionExpression['exist']['composition'].length + this.elementCompositionExpression['all']['composition'].length>0)
        return true
      return false
    },
    addExist(){
      sysDatasetObj.addExist()
    },
    addAll(){
      sysDatasetObj.addAll()
    }

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.re-elementComposition {
    position: absolute;
    top:0%;
    left: 0%;
    height: 100%;
    width: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: row;
    .elecomp-text{
      margin-left: 5px;
      margin-top: 3px;
      margin-right: 20px;
      font-size: 1rem;
      font-weight: bold;
      color: black;
    }
    .attr-input1{
        width: 18px;
        height: 10px;
        background-color: transparent;
        border: 0;
        outline: none;
        font-size: 5px;
    }
    .attr-connect{
        font-size: 1.5rem;
        font-weight: 200;
        text-anchor: middle;
        color: #606266;
    }
    .attr-input2{
        width: 18px;
        height: 10px;
        margin-top: 8px;
        background-color: transparent;
        border: 0;
        outline: none;
        font-size: 5px;
    }
    .ele-add-icon{
      cursor: pointer;
      &:hover{
          fill: steelblue;
      }
    }
    .navitem {
      height: 1em;
      font-size: 20px;
      cursor: pointer;
      &:hover {
        background: #eeeeee;
      }
    }


}
</style>
