<template>
    <svg class="re-node">
        <rect class="node-rect" :class="{'highlighted': getNodeHighlightState, 'defined': getNodeDefineState}" 
            :style="nodeStyle()"
            width="30" height="30" 
            :transform="nodeTransform" 
            :key = "rectKey"
            @click="updateSelectedNode"/>
        <text 
            :v-if="checkName()"
            class="node-name"
            :style="nameStyle()"
            :transform="nameTransform" 
            text-anchor= "middle"
            alignment-baseline= "middle"
            @click="updateSelectedNode">
            {{nodeExpression['nodeName']}}
        </text>
        <rect class="node-rect-opacity"
            width="30" height="30" 
            :transform="nodeTransform" 
            :key = "rectKey1"
            @click="updateSelectedNode"/>


    </svg>
    
</template>

<script>
    import { mapState, mapMutations } from 'vuex';

export default {
  name: 'EleNode',
  components: {
    
  },
  props: {
    nodeExpression:{
      type: Object
    }
  },
  data() {
    return {
        rectKey: 0,
        rectKey1: 1,
    }
  },
  mounted() {

  },
  watch: {
      displayMode: function() {
        console.log('displayMode')
      },
      nodeDefinitionState: function(){
        this.rectKey = (this.rectKey + 1) % 2
        this.rectKey1 = (this.rectKey1 + 1)%2
      },
      selectedDomKey: function(){
      }

  },
  computed: {
    ...mapState([
      'displayMode',
      'selectedDom',
      'selectedDomKey',
      'nodeDefinitionState'
    ]),
    getNodeHighlightState () {
        return this.nodeExpression.key === this.selectedDomKey
    },
    getNodeDefineState(){
        if('definition' in this.nodeExpression){
            if(this.nodeExpression['definition'])
                return true
        }
    },
    nodeTransform(){
        return `translate(${20}, ${1})`
    },
    nameTransform(){
        if(this.nodeExpression['nodeName'] == '.')
            return `translate(${35}, ${9})`
        return `translate(${35}, ${18})`
    }
   
  },
  methods: {
    ...mapMutations([
      'UPDATE_SELECTED_DOM',
      'UPDATE_NODE_DEFINITION_STATE',
      'UPDATE_REPEAT_DOM',
      'UPDATE_SELECTED_PART',
      'UPDATE_CONDITION_STATE'
    ]),

    checkName(){
        if('nodeName' in this.nodeExpression){
            return true
        }
        return false
    },
    updateSelectedNode() {
        sysDatasetObj.updateSelectedDomKey(this.nodeExpression['key'])
        this.UPDATE_SELECTED_DOM(this.nodeExpression)
        this.UPDATE_CONDITION_STATE(false)
        this.UPDATE_NODE_DEFINITION_STATE()
    },
    nodeStyle(){
        let tmpKey = sysDatasetObj.getSelectedDomKey()
        if(this.nodeExpression.key === tmpKey){
            return ( 
                        "fill: " + this.nodeExpression['nodeColor'] + "; "+
                        "stroke-dasharray: 0 0; " + 
                        "stroke-width: 1;"+
                        "stroke: red;"
            )
        }
        return (
            "fill: " + this.nodeExpression['nodeColor'] + "; " + 
            "stroke-dasharray: 0 0; " + 
            "stroke-width: 1;"
        )

    },
    nameStyle(){
        if(this.nodeExpression['nodeName'] == '.'){
            return "fill: white !important; font-size: 40px;"
        }
        else 
            return "fill: white !important; font-size: 18px;"
    }

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.re-node {
  height: 100%;
  width: 30%;

}
path {
    stroke: #000000;
    stroke-width: 2px;
    fill: none;
}
.node-rect {
    stroke: #c4bbbb;
    stroke-width: 2;
    stroke-dasharray: 4 2;
    fill: rgb(255, 255, 255);
}
.node-rect-opacity{
    opacity: 0;
    cursor: pointer;
}
.upper-rect {
    stroke: #c4bbbb;
    stroke-width: 2;
    stroke-dasharray: 2 1.67 3 1.67 3 1.67 2 0.0001;
    fill: white;
}
.repeat-rect{
    opacity: 0;
}
</style>

<style scoped lang="less">

</style>
