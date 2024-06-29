<template>
  <div class="node-define-panel-view">
    <div class="node-definition-content">
        <div class="attribute" style="display: flex;">


                <span style="margin-left: 60px; margin-top: 0px;"> name:</span>
                <el-input v-model="nodeName" @input="change($event)" style="width: 25%; margin-left: 10px; margin-top: 2px;" size="mini" ></el-input>
                <span style="margin-left: 20px; margin-top: 0px;">color:</span>
                <el-color-picker v-model="nodeColor" style="margin-left: 10px; margin-top: 2px;"></el-color-picker>
                <i class="el-icon-close operation" @click="closeNodeDefine()"></i>

        </div>
        <div class="query">
            <div class="query-title">
                <el-row :gutter="16" style="text-align:center;">
                    <el-col :span="7" :offset="1">attribute</el-col>
                    <el-col :span="7">operation</el-col>
                    <el-col :span="7">value</el-col>
                </el-row>
            </div>
            <div class="query-content">
                <div v-for="(queryItem,index) in queryList" :key="computeQueryKey(index)">
                    <el-row :gutter="16">
                        <el-col :span="7" :offset="1">
                            <el-select v-model="queryItem.queryAttribute" filterable placeholder="">
                                <el-option v-for="item in attributeListCopy" :key="item" :label="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="7">
                            <el-select v-model="queryItem.queryOperation" filterable placeholder="">
                                <el-option v-for="item in queryOperationList" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="7">
                            <el-input v-model="queryItem.queryValue" placeholder="" clearable @input="change($event)"></el-input>
                        </el-col>
                        <el-col :span="2">
                            <svg t="1646725673402" class="icon-delete" @click="attributeDelete(index)" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3143" width="22" height="22"><path d="M512 74.666667C270.933333 74.666667 74.666667 270.933333 74.666667 512S270.933333 949.333333 512 949.333333 949.333333 753.066667 949.333333 512 753.066667 74.666667 512 74.666667z m0 810.666666c-204.8 0-373.333333-168.533333-373.333333-373.333333S307.2 138.666667 512 138.666667 885.333333 307.2 885.333333 512 716.8 885.333333 512 885.333333z" p-id="3144"></path><path d="M657.066667 360.533333c-12.8-12.8-32-12.8-44.8 0l-102.4 102.4-102.4-102.4c-12.8-12.8-32-12.8-44.8 0-12.8 12.8-12.8 32 0 44.8l102.4 102.4-102.4 102.4c-12.8 12.8-12.8 32 0 44.8 6.4 6.4 14.933333 8.533333 23.466666 8.533334s17.066667-2.133333 23.466667-8.533334l102.4-102.4 102.4 102.4c6.4 6.4 14.933333 8.533333 23.466667 8.533334s17.066667-2.133333 23.466666-8.533334c12.8-12.8 12.8-32 0-44.8l-106.666666-100.266666 102.4-102.4c12.8-12.8 12.8-34.133333 0-46.933334z" p-id="3145"></path></svg>
                        </el-col>                
                    </el-row>
                </div>
                <el-row :gutter="20">
                    <el-col :offset="5" :span="8">
                        <el-button class="query-button" v-on:click="queryAdd"> + </el-button>
                    </el-col>
                    <el-col :span="8">
                        <el-button class="commit-button" v-on:click="commitNode"> commit </el-button>
                    </el-col>
                    <el-col :span="4"></el-col>
                </el-row>
            </div>
        </div>
    </div>

  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';


export default {
  name: 'NodeDefinePanel',
  components: {

  },
  props: {

  },
  data() {
    return {
        sizeForm: {
          name: '',
          label: '',
          shape: '',
          color: '#fff'
        },
        queryList: [
            {
                queryAttribute: '',
                queryOperation: '',
                queryValue: ''
            }
        ],
        queryOperationList: [{
            value: '=',
            label: '='
            }, {
            value: '>',
            label: '>'
            }, {
            value: '>=',
            label: '>='
            }, {
            value: '<',
            label: '<'
            }, {
            value: '<=',
            label: '<='
            },{
            value: '⊂',
            label: '⊂'
            }],
        queryOperation: '',
        queryValue: '',
        nodeName: "",
        nodeColor: "#FFFFFF",
        attributeListCopy: [],
      
    }
  },
  beforeMount(){
    this.attributeListCopy.push('degree')
    this.attributeListCopy.push('height')
    this.attributeListCopy.push('depth')
    this.attributeListCopy.push('countries')
    this.attributeListCopy.push('citationCount')
    this.attributeListCopy.push('year')
    this.attributeListCopy.push('keywords')
    this.queryUpdate()

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
      'selectedDom',

    ]),
  },
  created(){

  },
  methods: {
    ...mapMutations([
      'RESET_DOM_KEY_STATE',
      'UPDATE_RETREE_DATA_STATE',
      'UPDATE_NODE_LIST',
      'UPDATE_REGEX_CONTENT',
      'UPDATE_CONDITION_STATE',
      'UPDATE_NODE_DEFINITION_STATE'
    ]),
    closeNodeDefine(){
        this.UPDATE_CONDITION_STATE(true)
    },
    queryAdd() {
        var tmpDict = {
            queryAttribute: '',
            queryOperation: '',
            queryValue: ''
        }
        this.queryList.push(tmpDict)
    },
    commitNode(){
        if(this.selectedDom){
            if(this.selectedDom['type'] == 'node'){
                this.selectedDom['definition'] = true
                this.selectedDom['nodeName'] = this.nodeName
                if(!this.nodeColor){
                    this.nodeColor = '#FFFFFF'
                }
                this.selectedDom['nodeColor'] = this.nodeColor
                this.selectedDom['data'] = []
                for(let item of this.queryList){
                    this.selectedDom['data'].push(item)
                }
                this.UPDATE_CONDITION_STATE(true)
                this.UPDATE_NODE_DEFINITION_STATE()
            }
        }
        
    },
    computeQueryKey(d){
        return "queryList" + d  
    },
    queryUpdate(){
        if(this.selectedDom){
            if(this.selectedDom['type'] == 'node'){
                this.nodeName = this.selectedDom['nodeName']
                this.nodeColor = this.selectedDom['nodeColor']
                this.queryList.splice(0, this.queryList.length)
                for(let item of this.selectedDom['data']){
                    this.queryList.push(item)              
                }
            }
        }
        else if(this.selectedListNode){
            this.nodeName = this.selectedListNode['nodeName']
            this.nodeColor = this.selectedListNode['nodeColor']
            this.queryList.splice(0, this.queryList.length)
            for(let item of this.selectedListNode['data']){
                this.queryList.push(item)              
            }
        }
        else{
            this.queryList = []
            this.sizeForm = {}
            this.nodeName = ''
        }
    },
    attributeDelete(index){
        this.queryList.splice(index, 1)
    },
    change(e){
        this.$forceUpdate()
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.node-define-panel-view {
    position: absolute;
    top: 0%;
    left: 0%;
    right: 0%;
    bottom: 0%;
        .node-definition-content {
        position: absolute;
        top: 0%;
        width: 100%;
        height: 100%;
        left: 0%;
        bottom: 0%;
        display: flex;
        flex-direction: column;
        font-size: 1rem;
        font-weight: bolder;
        color: #808080;
        .name-color-text{
            text-align: center;
            font-weight: bold !important;
            font-family: 'Avenir', Helvetica, Arial, sans-serif;
            line-height: 20px !important;   
        }
        .text-attribute{
            left: 5%;
            font-size:20px;
            font-family: Sans-serif;
            color: #606266;
            font-weight: bold;
            top: 5%;
        }
        .attribute {
            padding: 5px 0 5px 20px;
            position: absolute;
            top:0;
            height: 22px;
            width: 100%;
            border-bottom: 1px #ddd solid;
            .el-icon-close{
                position: absolute;
                font-size: 18px;
                font-weight: bolder;
                left: 88%;
                top: 8px;
                color: #808080;
                cursor: pointer;
                    &:hover{
                    color: steelblue;
                    }
                }
        }
        .query{
            position:absolute;
            top: 30px;
            width: 100%;
            padding: 10px;  
            .query-title{
                width: 95%;
            } 
            .query-content{
                width: 95%;
                height: 65px;
                overflow-y: auto;
                .icon-delete{
                    cursor: pointer;
                    &:hover{
                        fill: steelblue;
                    }
                }
            }

        }
        .query-button{
            border: 1px #ddd dashed;
            font-size: 20px;
            text-align: center !important;
            margin-top: 5px;
            height: 20px !important;
            line-height: 20px !important;
            width: 80px;
        }
        .commit-button{
            border: 1px #ddd bold;
            font-size: 16px;
            text-align: center !important;
            margin-top: 5px;
            height: 20px !important;
            line-height: 0px !important;
            font-family: 'Avenir', Helvetica, Arial, sans-serif;
            padding: 0px;
            width: 80px;
        }
    }    

}

</style>
<style scoped lang="less">
    @input-line-height: 20px;

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
        height: 10px;
    }
    /deep/.query-button {
        padding: 0 !important;
    }
    /deep/.el-color-picker__trigger{
        height: 20px !important;
        width: 20px !important;
        padding: 0 !important;
    }
    /deep/.el-row{
        margin-bottom: 5px !important;
    }
</style>