<template>
  <div class="regex-panel-view">
    <DataFlowView></DataFlowView>
    <div class="repeatCommit" v-if="repeatState" v-drag>
      <span class="repeatTitle">repeat</span>
      <span class="repeat-text1">min:</span>
      <input class="repeat-input1" type="text" name="ticketNum" v-model="selectedDom['repeat'][0]">
      <span class="repeat-text2">max:</span>
      <input class="repeat-input2" type="text" name="ticketNum" v-model="selectedDom['repeat'][1]">
      <i class="el-icon-close operation" @click="closeReView()"></i>
    </div>

  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import DataFlowView from '../DataFlowView.vue'

export default {
  name: 'RegexPanel',
  components: {
    DataFlowView
  },
  props: {

  },
  data() {
    return {
      regex: null,
    }
  },
  beforeMount(){
    this.regex = sysDatasetObj.getRegex()
  },
  mounted() {

  },
  watch: {
      displayMode: function() {
        console.log('displayMode')
      },
  },
  computed: {
    ...mapState([
      'displayMode',
      'repeatState',
      'selectedDom'

    ]),
  },
  created(){

  },
  methods: {
    ...mapMutations([
        'DATA_QUERY_REGEX',
        'UPDATE_REPEAT_STATE'
    ]),
    query: function(){
        this.DATA_QUERY_REGEX()
    },
    closeReView(){
      this.UPDATE_REPEAT_STATE(false)
    }


  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.regex-panel-view {
    position: absolute;
    top: 0%;
    height: 100%;
    width: 100%;
    left: 0%;

    .repeatCommit{
      border-radius: 10px;
      border: 1px solid #d3d3d3;
      box-shadow: 2px 2px 1px #d3d3d3;
      background-color: white;
      position: absolute;
      margin-left: auto;
      margin-right: auto;
      font-size: 12px;
      width: 200px; 
      height: 100px; 
      top: 30%; 
      left: 30%;
      .repeatTitle{
        vertical-align: middle;
        position: absolute;
        top: 1px;
        height: 1.3rem;
        width: 100%;
        text-align: center;
        justify-content: center;
        font-size: 1rem;
        font-weight: bolder;
         color: #808080;
        border-bottom: 1px solid #dfdfdf;
      }
      .el-icon-close{
      position: absolute;
      font-size: 18px;
      font-weight: bolder;
      left: 85%;
      top: 4px;
      color: #808080;
      cursor: pointer;
        &:hover{
          color: steelblue;
        }
      }
      .repeat-text1{
        position:absolute;
        top: 30px;
        left: 60px;
        font-size: 1rem;
        text-align: right;
        font-weight: bolder;
        color: #808080;
      }
      .repeat-input1{
            position: absolute;
            top: 33px;
            left: 100px;
            width: 40px;
            border: 1px solid #bfc2c8 !important;
            border-radius: 2px;
            color: #606266;
      }
      .repeat-text2{
        position:absolute;
        top: 60px;
        left: 56.5px;
        text-align: right;
        font-size: 1rem;
        font-weight: bolder;
        color: #808080;
      }
      .repeat-input2{
            position: absolute;
            top: 63px;
            left: 100px;
            width: 40px;
            border: 1px solid #bfc2c8 !important;
            border-radius: 2px;
            color: #606266;
      }
    }


}

</style>