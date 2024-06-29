<template>
  <div class="recommend-panel-view">
    <span class="recommend-title">Query Results ({{tree_num}} trees)</span>
    <div class="page_list">
        <el-pagination
            layout="prev, pager, next"
            :total="tree_num"
            @current-change="pageChange"
            :current-page="current_page">
        </el-pagination>
    </div>
    <div class="tree-list">
        <div v-for="tree in tmp_list" :key="tree" class="tree-item">
            <svg v-bind:id="'svg-' + tree" style="position: relative; width: 100%; height: 100%;">
                <g v-bind:id="'g-level-1-'+tree">
                    <g v-bind:id="'g-level-1-path-'+tree"></g>
                    <g v-bind:id="'g-level-1-node-'+tree"></g>
                </g>
            </svg>
        </div>
    
    </div>

  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'RecommendPanel',
  components: {

  },
  props: {

  },
  data() {
    return {
        tmp_list: [0,1,2,3,4,5,6,7,8,9],
        recommend_list: [],
        num: 10,
        marks:{
            0:'0',
            5:'5',
            10:'10',
            15:'15',
            20:'20'
        },
        similarity: true,
        tree_num: 0,
        current_page: 1,
        tree_size: 0,
      
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
      visPanelState: function(){
        this.current_page = 1
        this.recommend_list = sysDatasetObj.getCurResult()
        this.tree_num = sysDatasetObj.getResultNum()
        this.draw_node_link_tree_list()
      },
      treeListState: function(){
        this.recommend_list = sysDatasetObj.getCurResult()
        this.tree_num = sysDatasetObj.getResultNum()
        this.draw_node_link_tree_list()
      }
  },
  computed: {
    ...mapState([
      'displayMode',
      'visPanelState',
      'treeListState'

    ]),
  },
  created(){

  },
  methods: {
    ...mapMutations([
        'UPDATE_VIS_TREE',
        'DATA_QUERY_PAGE'
    ]),
    pageChange: function(page_index){
        this.current_page = page_index
        this.DATA_QUERY_PAGE(page_index)
    },
    draw_node_link_tree_list: function(){
        let self = this
        for(var i=0; i<self.tmp_list.length; i++){
            d3.select(self.$el).select('#svg-'+i).selectAll('*').remove();
            
        }
        for(var i = 0; i < self.recommend_list.length; i++){

            let width = 143
            let height = 130
            let data = self.recommend_list[i]['data']
            self.tree_size = self.recommend_list[i]['size']

            console.log("width: ", width, "height: ", height)

            let scale = 300

            let isVertical = 1;
            let min_width_height = Math.min(width, height);
            let trbl = (min_width_height * 20) / scale;
            let margin = { top: trbl, right: trbl, bottom: 20, left: trbl };
            let innerWidth = width - 10;
            let innerHeight = height - 25;

            let r = (min_width_height * 3)/ scale;
            let r_min = (min_width_height * 2.5)/ scale;
            let r_max = (min_width_height * 3.5)/ scale;
            let strokeWidth = (min_width_height * r) / scale;
            let strokeOpacity = (min_width_height ) / scale;

            let degree_max = 0
            let root = d3.tree().size([innerWidth, innerHeight]) (
                d3.hierarchy(data)
                    .eachBefore(d=>{
                })
            );

            let DimGray = d3.rgb(105,105,105)
            let linear = d3.scaleLinear().domain([0, root.height]).range([1, 0])
            let color = d3.interpolate(DimGray, DimGray)

            self.RootDes = root.descendants()
            let RootDes = self.RootDes

            const svg = d3.select(self.$el).select('#svg-'+i)
            let tmp_g = svg.append('g')
                            .attr("id", "g-level-1-"+i)
            tmp_g.append("g")
                .attr("id", "g-level-1-path-"+i)
            tmp_g.append("g")
                .attr("id", "g-level-1-node-"+i)


           svg.selectAll('.tree-name').remove();

            svg.append("text")
            .attr("class", "tree-name")
            .attr("y", height-4)
            .attr("x", width/2)
            .attr("text-anchor", "middle")
            .attr("font-size", "10")
            .attr("fill", "#808080")
            .text(self.recommend_list[i]['data']['doi']);


            svg.append('path')
                .attr("class", "text-path")
                .attr("id", "text-path"+i)
                .classed("text-path-selected", false)
                .attr("d", function(){
                    let x0 = 1
                    let y0 = height -15
                    let x1 = width-1
                    let y1 = height - 15
                    return "M " +  x0 + " " +  y0 +
                            " L " + x1+ " " + y1;
                })

            svg.append("rect")
            .attr("class", "rect-none")
            .attr("id", "rect-none"+i)
            .attr("width", width-2)
            .attr("height", height-16.5)
            .attr("transform", "translate(1,1)")
            .attr("fill-opacity", '0')
            .attr("treeindex", i)
            .attr("style", "cursor: pointer;")
            .attr('stroke', '#f4606c')
            .attr('stroke-opacity', '0')
            .attr('stroke-dasharray', '4 2')
            .attr('stroke-width', '1.5')
            .on("click", function(){
                 sysDatasetObj.updateVisTree(this.getAttribute("treeindex"))
                 self.UPDATE_VIS_TREE()
                 let tmp = '#text-path'+this.getAttribute("treeindex")
                 d3.select(self.$el).selectAll('.text-path').classed("text-path-selected", false)
                 d3.select(self.$el).select(tmp).classed("text-path-selected", true)
            })


            let t = svg.transition()
                .duration(750)

            let g = svg.select('#g-level-1-'+i)
                .attr('transform', `translate(${5}, ${5})`);

            let path_logScale = d3.scaleLog()
            .domain([1, 2000])
            .range([1.5, 0.3]);

            if(isVertical)
            {
                g.select('#g-level-1-path-'+i)
                .attr('class', 'gLink')
                .attr('stroke-opacity', 0.2)
                .attr('stroke-width', function(){
                    return path_logScale(self.tree_size)
                })
                .selectAll('path')
                .data(root.links(), function(d, i) {
                })
                .join(
                    enter => enter.append('path')
                    .each(function(d){d.target.linkNode=self;})
                    .attr('d', d=>`M${d.source.x} ${d.source.y} L ${d.target.x} ${d.target.y}`),
                    update => update
                    .call(update => update.transition(t)
                    .each(function(d){d.target.linkNode=self;})
                    .attr('d', d=>`M${d.source.x} ${d.source.y} L ${d.target.x} ${d.target.y}`)),
                    exit => exit
                    .remove()
                );

                let node = g.select('#g-level-1-node-'+i)
                .attr('class', 'brush')
                .selectAll('a')
                .data(RootDes, function(d, i) {
                })
                .join(
                    enter => enter.append('a')
                    .attr("transform", d => `translate(${d.x},${d.y})`),
                    update => update
                    .call(update => update.transition(t)
                    .attr("transform", d => `translate(${d.x},${d.y})`)),
                    exit => exit
                    .remove()
                )

                let logScale = d3.scaleLog()
                    .domain([1, 2000])
                    .range([3, 1]);
                d3.select(self.$el).select('#svg-'+i).selectAll('.tree-node').remove();
                node.append("circle")
                .attr('class', 'tree-node')
                .attr('id', d=> 'node-id-' + d.nodeIndex)
                .attr("fill", "steelblue")
                .attr("r", function(){
                    return logScale(self.tree_size)
                })
                .call(self.tooltip_ele("node_link_tree"));

            }

        }
        d3.select(self.$el).selectAll('.text-path').classed("text-path-selected", false)
        d3.select(self.$el).select('#text-path0').classed("text-path-selected", true)
    }

  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.recommend-panel-view{
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
    .page_list{
        position: absolute;
        top: 0.1rem;
        right: 0px;
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
    .similarity-text{
        position: absolute;
        font-size: 1rem;
        font-weight: bolder;
        color: #808080;
        top: 30px;
        left: 68%;
    }
    .similarity-switch{
        position: absolute;
        top: 30px;
        left: 85%;
    }
    .tree-list {
        position: absolute;
        top: 10%;
        bottom: 3%;
        left: 0%;
        right: 0%;
        overflow-y: auto;
        display: grid;
        grid-template-columns: 19.5% 19.5% 19.5% 19.5% 19.5%;
        padding: 10px;
        grid-column-gap: 5px;
        grid-row-gap: 5px;
        .tree-item{
            height: 135px;
        }

    }
}

</style>

<style lang="less">
.text-path{
    stroke: #c4bbbb;
    stroke-width: 1px; 
    fill: none;
    &.text-path-selected{
        stroke: red !important;
    }
}
</style>