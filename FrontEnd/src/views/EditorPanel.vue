<template>
  <div class="editor-panel-view">
    <div class="regex-constructor">
        <RegexPanel></RegexPanel>
    </div>
    <div class="elecomp-constructor">
        <ElementComposition :elementCompositionExpression="condition_data['ElementComposition']"></ElementComposition>
    </div>
    <div class="node-constructor" v-if="!conditionState">
        <NodeDefinePanel></NodeDefinePanel>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import ConditionPanel from './EditorView/ConditionPanel.vue'
import NodeDefinePanel from './EditorView/NodeDefinePanel.vue'
import RegexPanel from './EditorView/RegexPanel.vue'
import ElementComposition from './EditorView/ElementComposition.vue'

export default {
  name: 'EditorPanel',
  components: {
    ConditionPanel, NodeDefinePanel, RegexPanel, ElementComposition
  },
  props: {

  },
  data() {
    return {
      condition_data: null,
    }
  },
  beforeMount(){
      this.condition_data = sysDatasetObj.getCondition()
  },
  mounted() {

  },
  watch: {
      displayMode: function() {
        console.log('displayMode')
      },
      conditiionState: function(){
        console.log("conditiionState1")
      }
  },
  computed: {
    ...mapState([
    'displayMode',
    'conditionState',
    ]),
  },
  created(){

  },
  methods: {

  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@input-line-height: 20px;
.editor-panel-view {
    position: absolute;
    top: 0%;
    left: 0%;
    right: 0%;
    bottom: 0%;
    .regex-constructor {
        position: absolute;
        top:0%;
        bottom: 0%;
        left: 0%;
        right: 0%;
    }
    .elecomp-constructor{
      position: absolute;
      top: 8%;
      height: 8%;
      left: 0%;
      right: 0%;
      background-color: white;
      // border-top: 1.5px rgb(221, 221, 221) solid;
      // border-bottom: 1.5px rgb(221, 221, 221) solid;
      // box-shadow: 0px -1px 5px rgb(221, 221, 221);
    }
    .node-constructor {
        position: absolute;
        top: 70%;
        bottom: 0%;
        left: 0%;
        right: 0%;
        background-color: white;
        border-top: 1.5px rgb(221, 221, 221) solid;
        box-shadow: 0px -1px 5px rgb(221, 221, 221);
    }
}

</style>
<!-- <style scoped lang="less">
    @input-line-height: 30px;
    /deep/.el-input__inner {
        line-height: @input-line-height !important;
        height: @input-line-height !important;
    }
    /deep/.el-input__icon {
        line-height: @input-line-height !important;
    }
    /deep/.el-input--mini{
        font-size: 15px !important;
        font-weight: bold !important;
    }
</style> -->