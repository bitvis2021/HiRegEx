
import * as d3 from "d3"
//添加tooltip
d3.helper = {};

d3.helper.tooltip = function(treesvgid, left=10, top=10){
    let tooltipDiv;
    let bodyNode = d3.select('body').node();
    function tooltip(selection){
      selection.on('mouseover.tooltip', function(pD, pI){
        let absoluteMousePos = d3.mouse(bodyNode);
        // Clean up lost tooltips
        d3.select('#'+treesvgid)
          .select('#g-level-1')
          .selectAll('.tooltip').remove();
        // Append tooltip
        if(treesvgid == 'node-link-tree'){
          tooltipDiv = d3.select('#'+treesvgid)
          .select('#g-level-1')
          .append('g')
            .attr('class', 'tooltip')
        }

        let indexCount = 0
        let name = "name"
        let show_list = []
        Object.keys(pD.data).forEach(d=>{
          if(d !='children' && d != 'abstract' && d != 'refList' && d!='affiliation'){
            show_list.push({name:d, index:indexCount}); indexCount += 1;
          }
            
        })
        tooltipDiv.append('g')
        .attr('id', 'text-g1')
        .selectAll('text')
          .data(show_list)
          .join(
            enter => enter.append('text')
            .attr("font-family", "sans-serif")
            .attr("font-size", '0.5em')
            .attr("text-anchor", "start")
            
          .append('tspan')

            .attr("dy",d=>`${10 + 15 * d.index}`)
            .attr("dx", 10)
            .attr("fill","#d6d4d4")
            .text(d=>`${d.name} : ${pD.data[d.name]}`)
          )

        tooltipDiv.append('rect')
        .attr("class", "treevis-tooltip-rect")
        .attr('height', 15 * show_list.length) 
        .attr('width', function(){
          return document.getElementById("text-g1").getBoundingClientRect()['width']+20
        })
        .attr('rx',5)
        .attr('ry',5)
        .attr('stroke', 'black')
        .attr('stroke-width', 1)
        .attr('stroke-opacity', 0.1)
        .attr('fill', '#464545')
        
        tooltipDiv.append('g')
        .attr('id', 'text-g2')
        .selectAll('text')
          .data(show_list)
          .join(
            enter => enter.append('text')
            .attr("font-family", "sans-serif")
            .attr("font-size", '0.5em')
            .attr("text-anchor", "start")
            
          .append('tspan')

            .attr("dy",d=>`${10 + 15 * d.index}`)
            .attr("dx", 10)
            .attr("fill","#d6d4d4")
            .text(d=>`${d.name} : ${pD.data[d.name]}`)
          )
          let outWidth = document.getElementById("node-link-tree").getBoundingClientRect()['width'] - 10
          let outHeight = document.getElementById("node-link-tree").getBoundingClientRect()['height'] - 10
          let tmpWidth = document.getElementById("text-g1").getBoundingClientRect()['width']+20
          let tmpHeight = 15 * show_list.length
          let tmpX = 0
          let tmpY = 0
          if(pD.x - tmpWidth/2 < 0){
            tmpX = 10
          }
          else if(pD.x + tmpWidth/2 > outWidth){
            tmpX = outWidth-tmpWidth
          }
          else{
            tmpX = pD.x - tmpWidth/2
          }

          if(pD.y + 10 + tmpHeight > outHeight){
            if(pD.y - 10 - tmpHeight > 0){
              tmpY = pD.y - 10 - tmpHeight
            }
            else if(pD.y + 10 - outHeight - (tmpHeight + 10 - pD.y) > 0){
              tmpY = pD.y - 10 - tmpHeight
            }
            else{
              tmpY = pD.y + 10
            }
          }
          else{
            tmpY = pD.y + 10
          }
          tooltipDiv.attr("transform", `translate(${tmpX},${tmpY})`)
         


        
                  


      })
      .on('mousemove.tooltip', function(pD, pI){

      })
      .on('mouseout.tooltip', function(pD, pI){
        // Remove tooltip
        tooltipDiv.remove();
      });
    }
    tooltip.attr = function(_x){
      if (!arguments.length) return attrs;
      attrs = _x;
      return this;
    };
    tooltip.style = function(_x){
      if (!arguments.length) return styles;
      styles = _x;
      return this;
    };
    return tooltip;
};

export default{
    install: function(Vue){
      Vue.prototype.tooltip_ele = (param1, param2, param3) =>d3.helper.tooltip(param1, param2, param3)
    }
}