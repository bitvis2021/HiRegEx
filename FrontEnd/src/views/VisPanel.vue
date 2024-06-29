<template>
  <div class="vis-panel-view">
     <span class="title-text">Tree Visualization</span>
     <span class="size-text">size:{{treeSize}}</span>
     <span class="height-text">height:{{treeHeight}}</span>
     <span class="width-text">width:{{treeWidth}}</span>
    <div class="node-link-tree-panel" ref="nodeLinkPanel">
        <svg id="node-link-tree" style="position: absolute; width: 100%; height: 100%;">
        </svg>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';


export default {
  name: 'VisPanel',
  components: {

  },
  props: {

  },
  data() {
    return {
      treeSize: 0,
      treeHeight: 0,
      treeWidth: 0,
      options: [],
      value: '',
      initalLabel: '',
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

        d3.select(this.$el).select('#node-link-tree').selectAll('*').remove()
        let tmpData = sysDatasetObj.getVisData()
        if('data' in tmpData){
          this.width = this.$refs.nodeLinkPanel.clientWidth
          this.height = this.$refs.nodeLinkPanel.clientHeight
          this.initalLabel = sysDatasetObj.getVisData()['data']['doi']
          this.draw_node_link_tree(this.width, this.height, tmpData)
        }
        else{
          this.treeSize = 0
          this.treeHeight = 0
          this.treeWidth = 0
        }
      },
      visTreeDataState: function(){
        d3.select(this.$el).select('#node-link-tree').selectAll('*').remove()
        let tmpData = sysDatasetObj.getVisTreeData()
        if('data' in tmpData){
          this.width = this.$refs.nodeLinkPanel.clientWidth
          this.height = this.$refs.nodeLinkPanel.clientHeight
          this.initalLabel = sysDatasetObj.getVisTreeData()['data']['doi']
          this.draw_node_link_tree(this.width, this.height, tmpData)
        }
        else{
          this.treeSize = 0
          this.treeHeight = 0
          this.treeWidth = 0
        }
      }
  },
  computed: {
    ...mapState([
      'displayMode',
      'visPanelState',
      'visTreeDataState',

    ]),
  },
  created(){

  },
  methods: {
    ...mapMutations([
      'DATA_QUERY_INDEX'
    ]),
    treeChange: function(command){
       this.DATA_QUERY_INDEX(parseInt(this.value))
    },
    draw_node_link_tree: function(width, height, data){
        let self = this

        let data_index = sysDatasetObj.getSameTree(parseInt(data['index'])-1)
        d3.selectAll(".dot").classed("dot-highlighted", false)

        let tmp_transform = d3.select('#dot'+data_index).attr("transform")
        let tmp_data = d3.select('#dot'+data_index).data()

        let tmp_x = +d3.select('#dot'+data_index).attr("x")
        let tmp_y = +d3.select('#dot'+data_index).attr("y")
        let tmp_r = +d3.select('#dot'+data_index).attr("r")

        let tmp_selected = d3.select('#dot'+data_index).attr("class")
        let dot_selected_flag = false
        if (tmp_selected.search(/dot-selected/) != -1){
            dot_selected_flag = true
        }
        
        d3.select('#dot'+data_index).remove()

        d3.select(".overview-svg")
        .selectAll('#dot'+data_index)
            .data(tmp_data)
            .enter()
            .append("circle")
            .attr("class","dot")
            .attr("id", function(d) { return "dot"+data_index})
            .classed("dot-highlighted", true)
            .classed("dot-selected", dot_selected_flag)
            .attr("transform", function(d){
              return tmp_transform;
            })
            .attr("m", function(d) {return d['m']})
            .attr("r", function(){
              return tmp_r;
            })
            .on('click', function(){
                self.DATA_QUERY_INDEX(parseInt(this.getAttribute("m")))
            });

        self.treeSize = data['size']
        self.treeHeight = data['height']
        self.treeWidth = data['width']
        data = data['data']

        let scale = 300

        let isVertical = 1;
        let min_width_height = Math.min(width, height);
        let trbl = (min_width_height * 20) / scale;
        let margin = { top: trbl, right: trbl, bottom: trbl, left: trbl };
        let innerWidth = width - 40;
        let innerHeight = height - 47;

        let r = (min_width_height * 3)/ scale;
        let r_min = (min_width_height * 2.5)/ scale;
        let r_max = (min_width_height * 3.5)/ scale;
        let strokeWidth = (min_width_height * r/5) / scale;
        let strokeOpacity = (min_width_height *0.4) / scale;

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

        const svg = d3.select(self.$el).select('#node-link-tree')

        svg.selectAll('.vis-tree-name').remove();
        svg.append("text")
          .attr("class", "vis-tree-name")
          .attr("y", height-5)
          .attr("x", width/2)
          .attr("text-anchor", "middle")
          .attr("font-size", "20")
          .attr("fill", "#808080")
          .text(data['doi']);

        let t = svg.transition()
            .duration(750)

        let g = svg.append('g')
            .attr('id', 'g-level-1')
            .attr('transform', `translate(${20}, ${10})`);

        let path_logScale = d3.scaleLog()
            .domain([1, 2000])
            .range([5, 1]);

        if(isVertical)
        {
            g.append('g')
            .attr('id', 'g-level-1-path')
            .attr('class', 'gLink')
            .attr('stroke-opacity', 0.2)
            .attr('stroke-width', function(){
              return path_logScale(self.treeSize)
            })
            .attr("stroke", "red !important")
            .attr("style", "fill: red !important")
            .selectAll('path')
            .data(root.links(), function(d, i) {
            })
            .join(
                enter => enter.append('path')
                .attr("stroke", "red !important")
                .attr("fill", "red !important")
                .each(function(d){d.target.linkNode=self;})
                .attr('d', d=>`M${d.source.x} ${d.source.y} L ${d.target.x} ${d.target.y}`),
                update => update
                .call(update => update.transition(t)
                .each(function(d){d.target.linkNode=self;})
                .attr('d', d=>`M${d.source.x} ${d.source.y} L ${d.target.x} ${d.target.y}`)),
                exit => exit
                .remove()
            );

            let g_node_stoke = g.append('g')
                       .attr("class", "g-nodes-stroke")

            // 保留
            let node = g.append('g')
            .attr('id', 'g-level-1-node')
            .selectAll('g')
            .data(RootDes, function(d, i) {
            })
            .join(
                enter => enter.append('g')
                .attr("transform", d => `translate(${d.x},${d.y})`),
                update => update
                .call(update => update.transition(t)
                .attr("transform", d => `translate(${d.x},${d.y})`)),
                exit => exit
                .remove()
            )
            let logScale = d3.scaleLog()
            .domain([1, 2000])
            .range([10, 5]);

            
            let node_stroke = []

            d3.select(self.$el).select('#node_link_tree').selectAll('.tree-node').remove();

            node.append("g")
            .attr("id", d=>"node-stroke-"+d['data'].index)
            .append("circle")
            .attr('class', 'tree-node')
            .attr('id', d=> 'node-id-' + d['data'].index)
            .attr("fill", function(d){
              if('color_flag' in d['data'] && d['data']['color_flag']){
                for(let i=0; i<d['data']['color'].length; i++){
                  let tmp = {}
                  tmp['node_data'] = d 
                  tmp['index'] = d['data']['index']
                  tmp['color'] = d['data']['color'][i]
                  tmp['x'] = d.x
                  tmp['y'] = d.y
                  tmp['r'] = logScale(self.treeSize)*0.75 + i*2 + 1
                  node_stroke.push(tmp)
                }
                return "white"
              }
              return "steelblue"
            })
            .attr("r", function(d){
              return logScale(self.treeSize)
            })
            .call(self.tooltip_ele("node-link-tree"))


            for(let tmp_stroke of node_stroke){
              d3.select('#node-stroke-'+tmp_stroke['index']).append("circle")
              .attr("stroke", tmp_stroke['color'])
              .attr("stroke-width", '2')
              .attr("r", tmp_stroke['r'])
              .attr("fill-opacity", '0')
              .attr("transform", d => `translate(${0},${0})`)
              .call(self.tooltip_ele("node-link-tree"))
            }


        }

    }

  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.vis-panel-view{
  position: absolute;
  top: 0%;
  left: 0%;
  right: 0%;
  bottom: 0%;
  .title-text{
    position: absolute;
    font-size: 1rem;
    font-weight: bolder;
    color: black;
    top: 5px;
    left: 5px;
  }
  .size-text{
    position: absolute;
    font-size: 1rem;
    color: #808080;
    top: 30px;
    left: 5px;
  }
  .height-text{
    position: absolute;
    font-size: 1rem;
    color: #808080;
    top: 50px;
    left: 5px;
  }
  .width-text{
    position: absolute;
    font-size: 1rem;
    color: #808080;
    top: 70px;
    left: 5px;
  }
  .node-link-tree-panel {
    position: absolute;
    top: 2%;
    bottom: 2%;
    left: 2%;
    right: 2%;
  }
  .tree-select{
    position: absolute;
    top: 5px;
    right: 5px;
    width: 100px;

  }
}

</style>