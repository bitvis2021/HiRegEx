
function mouseovered(active){
    return function(d, i){
        d3.select(this).classed("rect--active", active);
        d3.select('.'+d.data.name+'st').classed("rect--active", active);
        d3.select('.'+d.data.name+'sdt').classed("rect--active", active);
        d3.select('.'+d.data.name+'vt').classed("rect--active", active);

        if(typeof d.ancestors === "function")
        {
          for(let j=0; j< Object.values(d.ancestors().map(d=>"."+d.data.name)).length; j++){
            d3.select(Object.values(d.ancestors().map(d=>"."+d.data.name+"int"))[j]).classed("rect--active", active);
            d3.select(Object.values(d.ancestors().map(d=>"."+d.data.name+"iptp"))[j]).classed("rect--active", active);
            d3.select(Object.values(d.ancestors().map(d=>"."+d.data.name+"rdt"))[j]).classed("label--active", active);
            d3.select(Object.values(d.ancestors().map(d=>"."+d.data.name+"rddt"))[j]).classed("label--active", active);
            d3.select(Object.values(d.ancestors().map(d=>"."+d.data.name+"nlt"))[j]).classed("label--active", active);
            d3.select(Object.values(d.ancestors().map(d=>"."+d.data.name+'ndt'))[j]).classed("label--active", active);
            d3.select(Object.values(d.ancestors().map(d=>"."+d.data.name+"icp"))[j]).classed("rect--active", active);
            d3.select(Object.values(d.ancestors().map(d=>"."+d.data.name+"sub"))[j]).classed("rect--active", active);
            d3.select(Object.values(d.ancestors().map(d=>"."+d.data.name+"cpk"))[j]).classed("rect--active", active);
          }
        }
        
        do d3.select(d.linkNode).classed("link--active", active).raise();
        while (d = d.parent);

    }
}

export default{
    install: function(Vue){
        Vue.prototype.mouseovered = (param) =>mouseovered(param)
    }
}