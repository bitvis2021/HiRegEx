<template>
  <div class="reg-recommend-panel-view">
    <span class="recommend-title">Recommendation</span>
    <div class="reg-list">
    
    </div>

  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'RegRecommendPanel',
  components: {

  },
  props: {

  },
  data() {
    return {
        tmp_list: [0,1,2,3,4,5,6,7,8,9],
        recommend_list: [],
        reg_list: [],
        key_list: [],
        num: 10,
        marks:{
            0:'0',
            5:'5',
            10:'10',
            15:'15',
            20:'20'
        },
        similarity: true,
        max_height: 0,
      
    }
  },
  beforeMount(){

  },
  mounted() {

  },
  watch: {
      displayMode: function() {
        console.log('displayMode')
      },
      regPanelState: function(){
        d3.select(this.$el).selectAll("svg").remove()
        let tmp_dict = sysDatasetObj.getRegDict()
        console.log("tmp_dict", tmp_dict)
        this.reg_list = []
        this.key_list = []
        this.tmp_list = []
        let tmp_index = 0
        for(let key in tmp_dict){
            this.reg_list.push(tmp_dict[key])
            this.key_list.push(key)
            this.tmp_list.push(tmp_index)
            d3.select(this.$el).select(".reg-list")
                .append("svg")
                .attr("id", 'svg-'+tmp_index)
                .attr("style", 'position: relative; width: 100%; height: 100%;')
            tmp_index += 1
        }

        this.draw_reg_list()
      },
      visPanelState: function(){

        
      },
  },
  computed: {
    ...mapState([
      'displayMode',
      'visPanelState',
      'regPanelState'

    ]),
  },
  created(){

  },
  methods: {
    ...mapMutations([
        'DATA_QUERY_INDEX',
        'DATA_QUERY_CODING'
    ]),

    compute_node_position1: function(root){
        
        root['width'] = 25
        if(root['type'] == 'node')
            root['height'] = 25
        else
            root['height'] = root['composition'].length * (25+5)
        if(root['children'].length==0){
            root['box_width'] = root['width']
            return
        }
        for(let child_node of root['children']){
            this.compute_node_position1(child_node)
        } 
        let children_width = 0
        for(let child_node of root['children']){
            children_width += child_node['box_width'] + 18
        }
        children_width -= 18
        root['box_width'] = children_width>root['width'] ? children_width : root['width']
        let relative_x = root['width']/2 - children_width/2
        for(let child_node of root['children']){
            child_node['relative_x'] = relative_x + child_node['box_width']/2 - child_node['width']/2
            relative_x += child_node['box_width'] + 18
        }
    },

    compute_node_position2: function(root){
        if(root['y'] + root['height'] > this.max_height){
            this. max_height = root['y'] + root['height']
        }
        for(let child_node of root['children']){
            child_node['x'] = root['x'] + child_node['relative_x']
            child_node['y'] = root['y'] + root['height'] + 15
            this.compute_node_position2(child_node)
        }
    },
    draw_reg_list: function(){
            let self = this
            self.max_height = 0
            for(var i = 0; i < self.reg_list.length; i++){
                let width = document.getElementById("svg-"+i).clientWidth
                let reg = self.reg_list[i]['reg']
                let node_width = 25
                let node_margin = {height: 10, width: 10}
                reg['composition'] = []
                reg['x'] = width/2 - node_width/2
                reg['y'] = 10
                self.compute_node_position1(reg)
                self.compute_node_position2(reg, width/2 - node_width/2)

            }
            for(var i=0; i<self.reg_list.length; i++){
                let width = document.getElementById("svg-"+i).clientWidth
                let height = self.max_height + 20
                console.log("height: ",height)
                let reg = self.reg_list[i]['reg']
                d3.select(self.$el).select('#svg-'+i).selectAll('*').remove();
                const svg = d3.select(self.$el).select('#svg-'+i)
                    .attr("style", function(){
                        return "width: " + width + " !important;" +
                            "height: " + height + " !important;"
                    })
                self.draw_node(reg, svg)
                svg.append("path")
                    .attr('d', function(){
                    var x0 = width
                    var y0 = 0
                    var x1 = width
                    var y1 = height


                    return "M " +  x0 + " " +  y0 +
                            " L " + x1+ " " + y1;
                    })
                    .attr('style','stroke: #c4bbbb; stroke-width: 2px; fill: none;')
                svg.append("text")
                    .attr('x', width/2)
                    .attr('y', height-5)
                    .attr('font-size', '12px')
                    .attr('text-anchor', "middle")
                    .attr("alignment-baseline", "middle")
                    .text(() => "Num: " + self.reg_list[i]['num'])
                svg.append("rect")
                .attr("class", "rect-none")
                .attr("width", width-8)
                .attr("height", height-1)
                .attr("transform", "translate(4,1)")
                .attr("fill-opacity", '0')
                .attr("reg_coding", self.key_list[i])
                .attr("style", "cursor: pointer;")
                .attr('stroke', '#f4606c')
                .attr('stroke-opacity', '0')
                .attr('stroke-dasharray', '4 2')
                .attr('stroke-width', '1.5')
                .on("click", function(){
                    self.DATA_QUERY_CODING(this.getAttribute("reg_coding"))
                    d3.selectAll('.rect-none').attr('fill-opacity', '0')
                    // this.setAttribute('stroke-opacity', '1')
                    this.setAttribute('fill-opacity', '0.1')
                })
                
            }


    },
    draw_node: function(node, svg){
        if(node['type'] == 'node'){
            svg.append('rect')
            .attr('class', 'unselectable title')
            .attr('x', node['x'])
            .attr('y', node['y'])
            .attr('width', 25)
            .attr('height', 25)
            .attr('style', function(){
                return (
                    "stroke: #c4bbbb; !important;" + 
                    "fill: " + node['nodeColor'] + "; " + 
                        "stroke-dasharray: 0 0; " + 
                        "stroke-width: 1;"
                )
            })

            if('nodeName' in node){
                if(node['nodeName'] == '.'){
                    svg.append('text')
                    .attr('class', 'new11')
                    .attr('x', node['x']  + 12.5)
                    .attr('y', node['y'] + 7.5 )
                    .attr('fill', 'white')
                    .attr('font-size', '30')
                    .attr('text-anchor', "middle")
                    .attr("alignment-baseline", "middle")
                    .attr('class', 'unselectable title')
                    .text(() => node['nodeName'])
                }
                else{
                    svg.append('text')
                    .attr('class', 'new11')
                    .attr('x', node['x']  + 12.5)
                    .attr('y', node['y'] + 12.5 + 2)
                    .attr('fill', 'white')
                    .attr('font-size', '16')
                    .attr('text-anchor', "middle")
                    .attr("alignment-baseline", "middle")
                    .attr('class', 'unselectable title')
                    .text(() => node['nodeName'])
                }
            }

            for(let child_node of node['children']){
                this.draw_node(child_node, svg)
            }
        }
        else if(node['type'] == 'branch'){
        let curX = node['x']
        let curY = node['y']

        svg.append('path')
        .attr('class', 'bPath')
        .attr('d', function(){
          var x0 = curX
          var y0 = curY + 5
          var x1 = curX + 12.5
          var y1 = curY
          var x2 = curX + 25
          var y2 = curY + 5

          return "M " +  x0 + " " +  y0 +
                " L " + x1+ " " + y1 + 
                " L " + x2+ " " + y2
        })
        .attr('style','stroke: #c4bbbb; stroke-width: 1px; fill: none;')

        svg.append('text')
        .attr('x', curX)
        .attr('y', curY-4)
        .attr('font-size', '9px')
        .attr('alignment-baseline', 'hanging')
        .attr('text-anchor', 'middle')
        .attr('font-weight', 'bold')
        .attr('fill', '#2c2c2c')
        .text(() => node['repeat'][0])
        
        if(node['repeat'][1] == '*'){
            svg.append('text')
            .attr('x', curX+23)
            .attr('y', curY-4)
            .attr('font-size', '12px')
            .attr('alignment-baseline', 'hanging')
            .attr('text-anchor', 'middle')
            .attr('font-weight', 'bold')
            .attr('fill', '#2c2c2c')
            .text(() => node['repeat'][1])
        }
        else{
            svg.append('text')
            .attr('x', curX+23)
            .attr('y', curY-4)
            .attr('font-size', '9px')
            .attr('alignment-baseline', 'hanging')
            .attr('text-anchor', 'middle')
            .attr('font-weight', 'bold')
            .attr('fill', '#2c2c2c')
            .text(() => node['repeat'][1])
        }



        curY += 5
        
        for(let i in node['composition']){
          if(node['composition'][i]['type'] == 'node'){
            if('notFlag' in node['composition'][i] && node['composition'][i]['notFlag']){
              svg.append('path')
              .attr('d', function(){
                var x1 = curX-4
                var y1 = curY+5
            
                return ( "M " + x1 + " " + y1 +
                        "v " + 27);
              })
              .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
              svg.append('circle')
              .attr('cx', curX-4)
              .attr('cy', curY+37)
              .attr('r', '1')
              .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
            
            }

            svg.append('rect')
              .attr('class', 'unselectable title')
              .attr('x', curX)
              .attr('y', curY)
              .attr('width', 25)
              .attr('height', 25)
              .attr('style', function(){
                  return (
                   
                    "stroke: #c4bbbb; !important;" + 
                    "fill: " + node['composition'][i]['nodeColor'] + "; " + 
                        "stroke-dasharray: 0 0; " + 
                        "stroke-width: 1;"
                  )
              })
            if('nodeName' in node['composition'][i]){
                if(node['composition'][i]['nodeName'] == '.'){
                    svg.append('text')
                    .attr('class', 'new11')
                    .attr('x', curX + 12.5)
                    .attr('y', curY + 7.5 )
                    .attr('fill', 'white')
                    .attr('font-size', '30')
                    .attr('text-anchor', "middle")
                    .attr("alignment-baseline", "middle")
                    .attr('class', 'unselectable title')
                    .text(() => node['composition'][i]['nodeName'])
                }
                else{
                    svg.append('text')
                    .attr('class', 'new11')
                    .attr('x', curX + 12.5)
                    .attr('y', curY + 12.5 + 2)
                    .attr('fill', 'white')
                    .attr('font-size', '16')
                    .attr('text-anchor', "middle")
                    .attr("alignment-baseline", "middle")
                    .attr('class', 'unselectable title')
                    .text(() => node['composition'][i]['nodeName'])
                }
            }

            if(!(node['composition'][i]['repeat'][0] == 1 && node['composition'][i]['repeat'][1] == 1)){
              svg.append('path')
              .attr('class', 'bPath')
              .attr('d', function(){
                var x1 = curX + 25 + 2;
                var y1 = curY + 9;
                var x2 = curX + 25 + 2;
                var y2 = curY + 16;
                var r = 5;
                return 'M ' + x1 + ',' + y1 + ' ' + 'A ' + r + ',' + r + ' ' + '0 ' + '1,1' + ' ' + x2 + ',' + y2;
              })
              .attr('style','stroke: #2c2c2c; stroke-width: 1px; fill: none;')

              svg.append('path')
              .attr('class', 'bPath')
              .attr('d', function(){
                var x0 = curX + 25 + 2
                var y0 = curY + 16
                var x1 = x0 + 2.5
                var y1 = y0 + 3

                return "M " +  x1 + "," +  y1 +
                  " L " + x0 + "," + y0 ;
              })
              .attr('style','stroke: #2c2c2c; stroke-width: 1px; fill: none;')

                svg.append('text')
                .attr('x', curX + 25 + 4)
                .attr('y', curY )
                .attr('font-size', '7px')
                .attr('alignment-baseline', 'hanging')
                    .attr('font-weight', 'bold')
                    .attr('fill', '#2c2c2c')
                .text(() => node['composition'][i]['repeat'][0])
                if(node['composition'][i]['repeat'][1] == '*'){
                    svg.append('text')
                    .attr('x', curX + 25 + 4)
                    .attr('y', curY + 19)
                    .attr('font-size', '10px')
                    .attr('alignment-baseline', 'hanging')
                        .attr('font-weight', 'bold')
                        .attr('fill', '#2c2c2c')
                    .text(() => node['composition'][i]['repeat'][1])
                }
                else{
                    svg.append('text')
                    .attr('x', curX + 25 + 4)
                    .attr('y', curY + 19)
                    .attr('font-size', '7px')
                    .attr('alignment-baseline', 'hanging')
                        .attr('font-weight', 'bold')
                        .attr('fill', '#2c2c2c')
                    .text(() => node['composition'][i]['repeat'][1])
                }

            }

            curY = curY + 20 + 5


          }

        }
        for(let child_node of node['children']){
                this.draw_node(child_node, svg)
        }
        }

        if(node['children'].length > 0){
            let node_bottom_x = node['x'] + 12.5
            let node_bottom_y = node['y'] + node['height']
            svg.append('path')
            .attr('d', function(){
                let x0 = node_bottom_x
                let y0 = node_bottom_y
                let x1 = node_bottom_x
                let y1 = node_bottom_y + 7.5
                return "M " +  x0 + " " +  y0 +
                        " L " + x1+ " " + y1;
            })
            .attr('style','stroke: #c4bbbb; stroke-width: 1px; fill: none;')

            let x_left = 10000
            let x_right = 0
            for(let child_node of node['children']){
                svg.append('path')
                .attr('d', function(){
                    let x0 = child_node['x'] + 12.5
                    let y0 = node_bottom_y + 7.5
                    let x1 = child_node['x'] + 12.5
                    let y1 = node_bottom_y + 15
                    x_left = x0<x_left ? x0 : x_left
                    x_right = x0>x_right? x0 : x_right
                    return "M " +  x0 + " " +  y0 +
                            " L " + x1+ " " + y1;
                })
                .attr('style','stroke: #c4bbbb; stroke-width: 1px; fill: none;')
            }
            svg.append('path')
            .attr('d', function(){
                let x0 = x_left
                let y0 = node_bottom_y + 7.5
                let x1 = x_right
                let y1 = node_bottom_y + 7.5
                return "M " +  x0 + " " +  y0 +
                        " L " + x1+ " " + y1;
            })
            .attr('style','stroke: #c4bbbb; stroke-width: 1px; fill: none;')

        }

    },


  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.reg-recommend-panel-view{
    position: absolute;
    top: 0%;
    bottom: 0%;
    left: 0%;
    right: 0%;
    .recommend-title{
        position: absolute;
        font-size: 1rem;
        font-weight: bolder;
        color: black;
        top: 5px;
        left: 5px;
    }
    .num-text{
        position: absolute;
        font-size: 1rem;
        font-weight: bolder;
        color: #808080;
        top: 30px;
        left: 8%;
    }
    .num-slider{
        position: absolute;
        top: 23px;
        left: 20%;
        width: 30%;
        height: 15px;
    }
    .reg-list {
        position: absolute;
        top: 7%;
        bottom: 0%;
        left: 0%;
        right: 0%;
        overflow-y: auto;
        display: grid;
        grid-template-columns: 33% 33% 33%;
        padding: 10px;
        grid-column-gap: 0px;
        grid-row-gap: 5px;
    }
}

</style>