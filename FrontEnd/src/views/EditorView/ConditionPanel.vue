<template>
  <div class="condition-panel-view">
            <span class="elecomp-text">Element Composition</span>
            <div style="position: absolute; top:10%; width: 100%; height: 22%;">
                <ElementComposition :elementCompositionExpression="condition_data['ElementComposition']"></ElementComposition>
            </div>

        <span class="aggregation-text">Aggregation</span>
            <el-select class="aggregation-op-select" v-model="condition_data['Aggregation']['op']" filterable placeholder="">
                <el-option v-for="item in aggregation_op_list" :key="item" :label="item" :value="item">
                </el-option>
             </el-select>
            <el-select class="aggregation-attr-select" v-model="condition_data['Aggregation']['attribute']" filterable placeholder="">
                <el-option v-for="item in aggregation_attr_list" :key="item" :label="item" :value="item">
                </el-option>
             </el-select>
            <span class="aggregation-attr-symbol">∈</span>
            <input class="aggregation-attr-input1" type="text" name="ticketNum" v-model="condition_data['Aggregation']['value'][0]">
            <span class="aggregation-attr-connect">~</span>
            <input class="aggregation-attr-input2" type="text" name="ticketNum" v-model="condition_data['Aggregation']['value'][1]">
        

        <span class="size-text">Size</span>
            <el-slider class="size-slider" v-model="size" :step="5" :min="0" :max="1500" range ></el-slider>
            <input class="size-input1" type="text" name="ticketNum1" v-model="condition_data['Size'][0]">
            <span class="size-connect">~</span>
            <input class="size-input2" type="text" name="ticketNum2" v-model="condition_data['Size'][1]">

        <span class="height-text">Height</span>
            <el-slider class="height-slider" v-model="height" :step="5" :min="0" :max="10" range ></el-slider>
            <input class="height-input1" type="text" name="ticketNum3" v-model="condition_data['Height'][0]">
            <span class="height-connect">~</span>
            <input class="height-input2" type="text" name="ticketNum4" v-model="condition_data['Height'][1]">

        <span class="width-text">width</span>
            <el-slider class="width-slider" v-model="width" :step="5" :min="0" :max="1500" range ></el-slider>
            <input class="width-input1" type="text" name="ticketNum5" v-model="condition_data['Width'][0]">
            <span class="width-connect">~</span>
            <input class="width-input2" type="text" name="ticketNum6" v-model="condition_data['Width'][1]">
        <span class="balanced-text">Balanced</span>
            <el-switch class="balanced-switch" v-model="balanced" active-color="steelbule" inactive-color="grey"></el-switch>
        <div class="commit-delete-btn">
            <svg t="1646724379273" v-on:click="resetCondition" class="reset-button operation" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4124" width="25" height="25"><path style="fill:#4D4D4D" d="M934.4 206.933333c-17.066667-4.266667-34.133333 6.4-38.4 23.466667l-23.466667 87.466667C797.866667 183.466667 654.933333 96 497.066667 96 264.533333 96 74.666667 281.6 74.666667 512s189.866667 416 422.4 416c179.2 0 339.2-110.933333 398.933333-275.2 6.4-17.066667-2.133333-34.133333-19.2-40.533333-17.066667-6.4-34.133333 2.133333-40.533333 19.2-51.2 138.666667-187.733333 232.533333-339.2 232.533333C298.666667 864 138.666667 706.133333 138.666667 512S300.8 160 497.066667 160c145.066667 0 277.333333 87.466667 330.666666 217.6l-128-36.266667c-17.066667-4.266667-34.133333 6.4-38.4 23.466667-4.266667 17.066667 6.4 34.133333 23.466667 38.4l185.6 49.066667c2.133333 0 6.4 2.133333 8.533333 2.133333 6.4 0 10.666667-2.133333 17.066667-4.266667 6.4-4.266667 12.8-10.666667 14.933333-19.2l49.066667-185.6c0-17.066667-8.533333-34.133333-25.6-38.4z" p-id="4125"></path></svg>
        </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import ElementComposition from './ElementComposition.vue'
import { getComponentKey } from '@/utils/componentkey.js'

export default {
  name: 'ConditionPanel',
  components: {
    ElementComposition
  },
  props: {

  },
  data() {
    return {
        attr_min: 20,
        attr_max: 30,
        aggregation_op: '',
        aggregation_op_list:['mean', 'sum', 'max', 'min'],
        aggregation_attr: '',
        aggregation_attr_list:['degree', 'depth', 'height', 'citationCount', 'year'],
        size: [0, 1500],
        size_min: 20,
        size_max: 30,
        height: [0, 1500],
        height_min: 2,
        height_max: 5,
        width: [0, 1500],
        width_min: 20,
        width_max: 30,
        balanced: true,

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
      }
  },
  computed: {
    ...mapState([
      'displayMode',
      'treeViewState'
    ]),
  },
  created(){

  },
  methods: {
    resetCondition: function(){

    },
    commitCondition: function(){
        this.condition_data['ElementComposition']
        console.log("condition_data", this.condition_data)
    },

  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.condition-panel-view {
    position: absolute;
    top: 0%;
    left: 0%;
    right: 0%;
    bottom: 0%;
    .elecomp-text{
            position: absolute;
            top: 2%;
            left: 5%;
            font-size: 1rem;
            font-weight: bolder;
            color: #808080;
        }
        .aggregation-text{
            position: absolute;
            top: 32%;
            left: 5%;
            font-size: 1rem;
            font-weight: bolder;
            color: #808080;
        }
        .aggregation-op-select{
            position: absolute;
            top: 41%;
            left: 15%;
            width: 25%;
            font-size: 1rem;
            font-weight: bolder;
            color: #808080;
        }
        .aggregation-attr-select{
            position: absolute;
            top: 41%;
            left: 45%;
            width: 25%;
            font-size: 1rem;
            font-weight: bolder;
            color: #808080;
        }
        .aggregation-attr-symbol{
            position: absolute;
            top: 42.5%;
            left: 72.5%;
            width: 5%;
            color: #606266;
        }
        .aggregation-attr-input1{
            position: absolute;
            top: 43%;
            left: 78%;
            width: 5%;
            border: 1px solid #bfc2c8 !important;
            border-radius: 2px;
            color: #606266;
        }
        .aggregation-attr-connect{
            position: absolute;
            top: 41%;
            left: 84.5%;
            font-size: 1.5rem;
            font-weight: 200;
            text-anchor: middle;
            color: #606266;
        }
        .aggregation-attr-input2{
            position: absolute;
            top: 43%;
            left: 89%;
            width: 5%;
            border: 1px solid #bfc2c8 !important;
            border-radius: 2px;
            color: #606266;
        }

            .size-text{
                position: absolute;
                top: 55%;
                left: 5%;
                font-size: 1rem;
                font-weight: bolder;
                color: #808080;
            }
            .size-slider{
                position: absolute;
                top: 53%;
                left: 25%;
                width: 48%;
            }
            .size-text1{
                position: absolute;
                top: 52.7%;
                left: 77.5%;
                font-size: 1.7rem;
                font-weight: 400;
                text-anchor: middle;
            }
            .size-input1{
                position: absolute;
                top: 55.5%;
                left: 78%;
                width: 5%;
                border: 1px solid #bfc2c8 !important;
                border-radius: 2px;
                color: #606266;
            }
            .size-connect{
                position: absolute;
                top: 53.5%;
                left: 84.5%;
                font-size: 1.5rem;
                font-weight: 200;
                text-anchor: middle;
                color: #606266;
            }
            .size-input2{
                position: absolute;
                top: 55.5%;
                left: 89%;
                width: 5%;
                border: 1px solid #bfc2c8 !important;
                border-radius: 2px;
                color: #606266;
            }

        .height-text{
            position: absolute;
            top: 65%;
            left: 5%;
            font-size: 1rem;
            font-weight: bolder;
            color: #808080;
        }
            .height-slider{
                position: absolute;
                top: 63%;
                left: 25%;
                width: 48%;
            }
            .height-text1{
                position: absolute;
                top: 62.7%;
                left: 77.5%;
                font-size: 1.7rem;
                font-weight: 400;
                text-anchor: middle;
            }
            .height-input1{
                position: absolute;
                top: 65.5%;
                left: 78%;
                width: 5%;
                border: 1px solid #bfc2c8 !important;
                border-radius: 2px;
                color: #606266;
            }
            .height-connect{
                position: absolute;
                top: 63.5%;
                left: 84.5%;
                font-size: 1.5rem;
                font-weight: 200;
                text-anchor: middle;
                color: #606266;
            }
            .height-input2{
                position: absolute;
                top: 65.5%;
                left: 89%;
                width: 5%;
                border: 1px solid #bfc2c8 !important;
                border-radius: 2px;
                color: #606266;
            }

        .width-text{
            position: absolute;
            top: 75%;
            left: 5%;
            font-size: 1rem;
            font-weight: bolder;
            color: #808080;
        }
            .width-slider{
                position: absolute;
                top: 73%;
                left: 25%;
                width: 48%;
            }
            .width-text1{
                position: absolute;
                top: 72.7%;
                left: 77.5%;
                font-size: 1.7rem;
                font-weight: 400;
                text-anchor: middle;
            }
            .width-input1{
                position: absolute;
                top: 75.5%;
                left: 78%;
                width: 5%;
                border: 1px solid #bfc2c8 !important;
                border-radius: 2px;
                color: #606266;
            }
            .width-connect{
                position: absolute;
                top: 73.5%;
                left: 84.5%;
                font-size: 1.5rem;
                font-weight: 200;
                text-anchor: middle;
                color: #606266;
            }
            .width-input2{
                position: absolute;
                top: 75.5%;
                left: 89%;
                width: 5%;
                border: 1px solid #bfc2c8 !important;
                border-radius: 2px;
                color: #606266;
            }
        .balanced-text{
            position: absolute;
            top: 85%;
            left: 5%;
            font-size: 1rem;
            font-weight: bolder;
            color: #808080;
        }
        .balanced-switch{
            position: absolute;
            top: 85.5%;
            left: 30%;
        }
    .commit-delete-btn{
    position: absolute;
    top: 0%;
    left: 75%;
    right: 0%;
    display: flex;
    justify-content: center;
    .operation {
      cursor: pointer;
      &:hover{
        fill: steelblue;
      }
    }
    .reset-button{
        border: 1px #ddd bold;
        font-size: 14px;
        text-align: center !important;
        margin-top: 8px;
        margin-left: 50px;
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
    }
  }

}

</style>
<style scoped lang="less">
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
</style>