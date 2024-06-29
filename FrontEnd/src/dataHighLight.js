
import * as d3 from 'd3'


function dataHighLight_In_and_Out(treevis, dataHighLight, bus, RootDes, is_hilight){
    if(dataHighLight==null || typeof dataHighLight == 'undefined' || !(dataHighLight instanceof Array) ){
      return;
    }
    else{        
      dataHighLight.forEach(ele=>{
        highLightInOut(treevis, ele, bus, RootDes, is_hilight);
      })
    }
}


function highLightInOut(treevis, tmpEle, bus, RootDes, is_hilight){
    if(!tmpEle['data'][0]){
      bus.$emit("brushed_data", [])
      return;
    }
    let tmpEleDataArray = tmpEle['data']
    let tmpEleDataType = tmpEle['type']
    if(tmpEle['type'] == 'treeOut' && is_hilight){
      let eiChildrenIndexList = []
      tmpEleDataArray.forEach(ei=>{
        eiChildrenIndexList = eiChildrenIndexList.concat(d3.hierarchy(ei).descendants().map(d=>d.data.data.nodeIndex))
      })
      eiChildrenIndexList = Array.from(new Set(eiChildrenIndexList))
      let sendHighLight = RootDes.filter(d=>eiChildrenIndexList.includes(d.data.data.nodeIndex)).map(d=>d.data)
      bus.$emit("brushed_data", sendHighLight)
    }else{
      bus.$emit("brushed_data", [])
    }
    tmpEleDataArray.forEach(ei=>{
      let eiChildrenIndexList = []
      eiChildrenIndexList = eiChildrenIndexList.concat(d3.hierarchy(ei).descendants().map(d=>d.data.data.nodeIndex))
      eiChildrenIndexList.forEach(child=>{
        d3.select('#' + treevis)
          .select('#node-id-' + child).classed(tmpEleDataType+'-highlight', is_hilight)
      })
    })
}

export default{
    install: function(Vue){
      Vue.prototype.dataHighLight_In_and_Out = (param1, param2, param3, param4, param5) => dataHighLight_In_and_Out(param1, param2, param3, param4, param5)
    }
}