<template>
  <div class="overview-panel-view">
    <div class="dataset-part">
      <span class="dataset-text">Dataset</span>
        <div class="dataset-select">
          <el-select v-model="selectValue">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.value"
              :value="item.value">
            </el-option>
          </el-select>
      </div>
      <i class="el-icon-circle-plus-outline"></i>
    </div>
    <span class="projection-text">Projection</span>
    <div class="projection-part" ref="projectionPanel">
        <svg id="projection-chart" style="position: absolute; width: 100%; height: 100%;">
        </svg>
    </div>
    <span class="distribution-text">Distribution</span>
    <div class="distribution-part">
      <div class="distribution-div" id="size">
        <svg id="bar-size" style="width: 100%; height: 100%"></svg>
      </div>
      <div class="distribution-div" id="height">
        <svg id="bar-height" style="width: 100%; height: 100%"></svg>
      </div>
      <div class="distribution-div" id="width">
        <svg id="bar-width" style="width: 100%; height: 100%"></svg>
      </div>
    </div>

  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';


export default {
  name: 'OverviewPanel',
  components: {

  },
  props: {

  },
  data() {
    return {
      frontPoint: null,
      selectValue: "Citation",
      options:[
        {
          value: "Citation"
        },
        {
          value: "Repost"
        }
      ],
      condition_data: null,

      
    }
  },
  beforeMount(){
    this.condition_data = sysDatasetObj.getCondition()

  },
  mounted() {
    this.width = this.$refs.projectionPanel.clientWidth
    this.height = this.$refs.projectionPanel.clientHeight
    this.draw_projection_chart()
    this.draw_size_bar()
    this.draw_height_bar()
    this.draw_width_bar()
    
  },
  watch: {
      displayMode: function() {
        console.log('displayMode')
      },
      visPanelState: function(){
        d3.select('#bar-size-1').remove()
        d3.select('#bar-height-1').remove()
        d3.select('#bar-width-1').remove()
        this.draw_size_bar()
        this.draw_height_bar()
        this.draw_width_bar()
      }
  },
  computed: {
    ...mapState([
      'visPanelState'
    ]),
  },
  created(){

  },
  methods: {
    ...mapMutations([
      'DATA_QUERY_INDEX'
    ]),
    test: function(){
        var x = d3.scaleLinear()
            .domain([0,1])
            .range([0,500]);
          var x2 = x.copy(); // reference.

          var zoom = d3.zoom()
            .scaleExtent([1, 10])
            .on("zoom", zoomed);

          var svg = d3.select("svg")
            .call(zoom);
            
          var axis = d3.axisBottom().scale(x)
            
          var axisG = svg.append("g")
              .attr("transform", "translate(0,30)")
              .call(axis);
            
          function zoomed() {
            x = d3.event.transform.rescaleX(x2)
            axis.scale(x);
            axisG.call(axis);
          }
    },
    draw_projection_chart: function(){
      let self = this
      d3.csv('treeDataset/umap_GIN10_res.csv', d3.autoType)
        .then(function(data) {
          var margin = { top: 5, right: 5, bottom: 5, left: 5 },
              width = self.$refs.projectionPanel.clientWidth - margin.left - margin.right,
              height = self.$refs.projectionPanel.clientHeight - margin.top - margin.bottom;

          var x = d3.scaleLinear()
            .range([0, width]).nice();
          var y = d3.scaleLinear()
            .range([height, 0]).nice();
          

          var xMax = d3.max(data, function(d) { return d['x']; }) * 1.05,
              xMin = d3.min(data, function(d) { return d['x']; }),
              xMin = xMin > 0 ? 0 : xMin,
              yMax = d3.max(data, function(d) { return d['y']; }) * 1.05,
              yMin = d3.min(data, function(d) { return d['y']; }),
              yMin = yMin > 0 ? 0 : yMin;
          x.domain([xMin-2, xMax+2]);
          y.domain([yMin-2, yMax+1]);

          var xAxis = d3.axisBottom()
              .scale(x)
              .ticks(8)
              .tickSize(-height);

          var yAxis = d3.axisLeft()
              .scale(y)
              .ticks(8)
              .tickSize(-width);


          var zoomBeh = d3.zoom()
            .scaleExtent([0, 50])
            .on("zoom", zoom);
          
          var svg = d3.select(self.$el).select('#projection-chart')
            .append("g")
            .attr('id', 'distribute-chart')
            .attr("transform", "translate(5, 5)")
            .call(zoomBeh);
          
          svg.append("rect")
            .attr("class", "overview-rect")
            .attr("width", width)
            .attr("height", height);
          
          var xAxisG = svg.append("g")
            .classed("x axis", true)
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
          
          var yAxisG = svg.append("g")
            .classed("y axis", true)
            .call(yAxis)
          
          var objects = svg.append("svg")
            .attr("class", "overview-svg")
            .attr("width", width)
            .attr("height", height);

          objects.append("svg:line")
              .classed("axisLine hAxisLine", true)
              .attr("x1", 0)
              .attr("y1", 0)
              .attr("x2", width)
              .attr("y2", 0)
              .attr("transform", "translate(0," + height + ")");
          
          objects.append("svg:line")
            .classed("axisLine vAxisLine", true)
            .attr("x1", 0)
            .attr("y1", 0)
            .attr("x2", 0)
            .attr("y2", height);
          
          var rMax = d3.max(data, function(d) { return d['n']; }),
            rMin = d3.min(data, function(d) { return d['n']; });

          let logScale = d3.scaleLog()
            .domain([rMin, rMax])
            .range([3, 10]);

          objects.selectAll(".dot")
            .data(data)
          .enter()
          .append("circle")
            .attr("class","dot")
            .attr("id", function(d) { return "dot"+parseInt(d['m'])})
            .classed("dot-selected", false)
            .classed("dot-highlighted", false)
            .attr("transform", transform)
            .attr("m", function(d) {return d['m']})
            .attr("r", function(d){
              return logScale(d['n']);
            })
            .on('click', function(){
                self.DATA_QUERY_INDEX(parseInt(this.getAttribute("m")))
            });
          
          function zoom() {
            let transformEvent = d3.event.transform
            svg.selectAll(".dot")
                .attr("transform", d => transform(d, transformEvent));
          }

          function transform(d, transformEvent) {
            let poxList = [x(d['x']), y(d['y'])]
            if (typeof(transformEvent) !== 'object') {
              return "translate(" + poxList[0] + "," + poxList[1] + ")";
            }
            let posListUpdate = transformEvent.apply(poxList)
            return "translate(" + posListUpdate[0] + "," + posListUpdate[1] + ")";
          }
        })

    },
    draw_size_bar: function(){
      var self = this
      d3.csv('treeDataset/size.csv', d3.autoType)
        .then(function(data) {
            var margin = {top: 10, right: 10, bottom: 50, left: 35},
              width = document.getElementById("bar-size").clientWidth - margin.left - margin.right,
              height = document.getElementById("bar-size").clientHeight - margin.top - margin.bottom;

            var highlightData = sysDatasetObj.gethighlightBar()
            var highlightFlag = false
            if('size' in highlightData){
              highlightData = highlightData['size']
              highlightFlag = true
            }


            var svg = d3.select(self.$el).select("#bar-size")
                .append("g")
                .attr("id", 'bar-size-1')
                .attr("transform",
                      "translate(" + margin.left + ", " +  margin.right + ")");
            
            svg.append("text")
              .style("text-anchor", "middle")
              .attr("x", width-20)
              .attr("y", 12)
              .attr("font-size", "15px")
              .attr("font-weight", "bolder")
              .attr("fill", "#666666")
              .text("Size");

            var x = d3.scaleBand()
              .range([ 0, width ])
              .domain(data.map(function(d) { return d.x; }))
              .padding(0.2);
            svg.append("g")
              .attr("class", "x-axis")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(x))
              .selectAll("text")
                .attr("transform", "translate(-10,0)rotate(-45)")
                .style("text-anchor", "end");

            // Add Y axis
            var y = d3.scaleLinear()
              .domain([0, 1200])
              .range([ height, 0]);

            svg.append("g")
              .call(d3.axisLeft(y).ticks(4));

            // Bars
            svg.selectAll("mybar")
              .data(data)
              .enter()
              .append("rect")
                .attr("x", function(d) { return x(d.x); })
                .attr("y", function(d) { return y(d.y); })
                .attr("width", x.bandwidth())
                .attr("height", function(d) { return height - y(d.y); })
                .attr("fill", "#CCCCCC")   

            if(highlightFlag){
              svg.selectAll("highlightBar")
              .data(highlightData)
              .enter()
              .append("rect")
                .attr("x", function(d) { return x(d.x); })
                .attr("y", function(d) { return y(d.y); })
                .attr("width", x.bandwidth())
                .attr("height", function(d) { return height - y(d.y); })
                .attr("fill", "orange")   
            }


            svg.append("g")
            .selectAll("g")
            .data(data)
            .enter()
            .append('text')
            .attr("class", "tree-name")
            .attr("x", function(d) { return x(d.x); })
            .attr("y", function(d) { return y(d.y); })
            .attr("dx", "10")
            .attr("dy", '-1')
            .attr("text-anchor", "middle")
            .text(function(d){return d.y;
            })
            .attr('font-size', "10px")
            .attr('fill', '#808080');
              
        })
    },
    draw_height_bar: function(){
      var self = this
      d3.csv('treeDataset/height.csv', d3.autoType)
        .then(function(data) {
            var margin = {top: 10, right: 10, bottom: 50, left: 35},
              width = document.getElementById("bar-height").clientWidth - margin.left - margin.right,
              height = document.getElementById("bar-height").clientHeight - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select(self.$el).select("#bar-height")
                .append("g")
                .attr("id", 'bar-height-1')
                .attr("transform",
                      "translate(" + margin.left + ", " +  margin.right + ")");

            var highlightData = sysDatasetObj.gethighlightBar()
            var highlightFlag = false
            if('height' in highlightData){
              highlightData = highlightData['height']
              highlightFlag = true
            }
            
            svg.append("text")
              .style("text-anchor", "middle")
              .attr("x", width-20)
              .attr("y", 12)
              .attr("font-size", "15px")
              .attr("font-weight", "bolder")
              .attr("fill", "#666666")
              .text("Height");

            var x = d3.scaleBand()
              .range([ 0, width ])
              .domain(data.map(function(d) { return d.x; }))
              .padding(0.2);
            svg.append("g")
              .attr("class", "x-axis")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(x))
              .selectAll("text")
                .attr("transform", "translate(0,0)")
                .style("text-anchor", "middle");

            // Add Y axis
            var y = d3.scaleLinear()
              .domain([0, 1200])
              .range([ height, 0]);

            svg.append("g")
              .call(d3.axisLeft(y).ticks(4));

            // Bars
            svg.selectAll("mybar")
              .data(data)
              .enter()
              .append("rect")
                .attr("x", function(d) { return x(d.x); })
                .attr("y", function(d) { return y(d.y); })
                .attr("width", x.bandwidth())
                .attr("height", function(d) { return height - y(d.y); })
                .attr("fill", "#CCCCCC")
            
            if(highlightFlag){
              svg.selectAll("highlightBar")
              .data(highlightData)
              .enter()
              .append("rect")
                .attr("x", function(d) { return x(d.x); })
                .attr("y", function(d) { return y(d.y); })
                .attr("width", x.bandwidth())
                .attr("height", function(d) { return height - y(d.y); })
                .attr("fill", "orange")   
            }

            svg.append("g")
            .selectAll("g")
            .data(data)
            .enter()
            .append('text')
            .attr("class", "tree-name")
            .attr("x", function(d) { return x(d.x); })
            .attr("y", function(d) { return y(d.y); })
            .attr("dx", "10")
            .attr("dy", '-1')
            .attr("text-anchor", "middle")
            .text(function(d){return d.y;
            })
            .attr('font-size', "10px")
            .attr('fill', '#808080');
              
        })
    },
    draw_width_bar: function(){
      var self = this
      d3.csv('treeDataset/width.csv', d3.autoType)
        .then(function(data) {
            var margin = {top: 10, right: 10, bottom: 50, left: 35},
              width = document.getElementById("bar-width").clientWidth - margin.left - margin.right,
              height = document.getElementById("bar-width").clientHeight - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select(self.$el).select("#bar-width")
                .append("g")
                .attr("id", 'bar-width-1')
                .attr("transform",
                      "translate(" + margin.left + ", " +  margin.right + ")");
            
            var highlightData = sysDatasetObj.gethighlightBar()
            var highlightFlag = false
            if('width' in highlightData){
              highlightData = highlightData['width']
              highlightFlag = true
            }

            svg.append("text")
              .style("text-anchor", "middle")
              .attr("x", width-20)
              .attr("y", 12)
              .attr("font-size", "15px")
              .attr("font-weight", "bolder")
              .attr("fill", "#666666")
              .text("Width");

            var x = d3.scaleBand()
              .range([ 0, width ])
              .domain(data.map(function(d) { return d.x; }))
              .padding(0.2);
            svg.append("g")
              .attr("class", "x-axis")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(x))
              .selectAll("text")
                .attr("transform", "translate(-10,0)rotate(-45)")
                .style("text-anchor", "end");

            // Add Y axis
            var y = d3.scaleLinear()
              .domain([0, 1200])
              .range([ height, 0]);

            svg.append("g")
              .call(d3.axisLeft(y).ticks(4));

            // Bars
            svg.selectAll("mybar")
              .data(data)
              .enter()
              .append("rect")
                .attr("x", function(d) { return x(d.x); })
                .attr("y", function(d) { return y(d.y); })
                .attr("width", x.bandwidth())
                .attr("height", function(d) { return height - y(d.y); })
                .attr("fill", "#CCCCCC")

              if(highlightFlag){
              svg.selectAll("highlightBar")
              .data(highlightData)
              .enter()
              .append("rect")
                .attr("x", function(d) { return x(d.x); })
                .attr("y", function(d) { return y(d.y); })
                .attr("width", x.bandwidth())
                .attr("height", function(d) { return height - y(d.y); })
                .attr("fill", "orange")   
            }
 

            svg.append("g")
            .selectAll("g")
            .data(data)
            .enter()
            .append('text')
            .attr("class", "tree-name")
            .attr("x", function(d) { return x(d.x); })
            .attr("y", function(d) { return y(d.y); })
            .attr("dx", "10")
            .attr("dy", '-1')
            .attr("text-anchor", "middle")
            .text(function(d){return d.y;
            })
            .attr('font-size', "10px")
            .attr('fill', '#808080');
              
        })
    },


  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.overview-panel-view {
  position: absolute;
  top: 0%;
  left: 0%;
  right: 0%;
  bottom: 0%;
  .dataset-part{
    position:absolute;
    top: 1%;
    bottom: 90%;
    left: 0%;
    right: 0%;
    .dataset-text{
      position:absolute;
      top: 6%;
      left: 5%;
      font-size: 1rem;
      font-weight: bolder;
      color: black;
    }
    .dataset-select{
      position:absolute;
      top: 3%;
      left: 30%;
    }
    .el-icon-circle-plus-outline{
      position:absolute;
      top: 12%;
      left: 83%;
    }
  }
  .projection-text{
      position:absolute;
      top: 6%;
      left: 5%;
      font-size: 1rem;
      font-weight: bolder;
      color: black;
  }
  .projection-part{
    position: absolute;
    top: 8%;
    bottom: 60%;
    left: 0%;
    right: 0%;
  }
  .distribution-text{
      position:absolute;
      top: 40%;
      left: 5%;
      font-size: 1rem;
      font-weight: bolder;
      color: black;
  }
  .distribution-part{
    position: absolute;
    top: 43%;
    bottom: 2%;
    left: 0%;
    right: 0%;
    #size{
    .size-input1{
        position: absolute;
        top: 1%;
        left: 70%;
        width: 10%;
        border: 1px solid #bfc2c8 !important;
        border-radius: 2px;
        color: #606266;
    }
    .size-connect{
        position: absolute;
        top: 0%;
        left: 81.5%;
        font-size: 1.5rem;
        font-weight: 200;
        text-anchor: middle;
        color: #606266;
    }
    .size-input2{
        position: absolute;
        top: 1%;
        left: 87%;
        width: 10%;
        border: 1px solid #bfc2c8 !important;
        border-radius: 2px;
        color: #606266;
    }
  }
  #height{
    .height-input1{
        position: absolute;
        top: 36%;
        left: 70%;
        width: 10%;
        border: 1px solid #bfc2c8 !important;
        border-radius: 2px;
        color: #606266;
    }
    .height-connect{
        position: absolute;
        top: 35%;
        left: 81.5%;
        font-size: 1.5rem;
        font-weight: 200;
        text-anchor: middle;
        color: #606266;
    }
    .height-input2{
        position: absolute;
        top: 36%;
        left: 87%;
        width: 10%;
        border: 1px solid #bfc2c8 !important;
        border-radius: 2px;
        color: #606266;
    }
  }
  #width{
    .width-input1{
        position: absolute;
        top: 70%;
        left: 70%;
        width: 10%;
        border: 1px solid #bfc2c8 !important;
        border-radius: 2px;
        color: #606266;
    }
    .width-connect{
        position: absolute;
        top: 69%;
        left: 81.5%;
        font-size: 1.5rem;
        font-weight: 200;
        text-anchor: middle;
        color: #606266;
    }
    .width-input2{
        position: absolute;
        top: 70%;
        left: 87%;
        width: 10%;
        border: 1px solid #bfc2c8 !important;
        border-radius: 2px;
        color: #606266;
    }
  }
  }
}

</style>
<style scoped lang="less">
  /deep/.el-input__inner{  
    height: 30px;   
    width: 150px;
  }

</style>
<style lang="less">

.overview-rect {
  fill: transparent;
  shape-rendering: crispEdges;
}

.axis path,
.axis line {
  fill: none;
  stroke: rgba(0, 0, 0, 0.1);
  shape-rendering: crispEdges;
}

.axisLine {
  fill: none;
  shape-rendering: crispEdges;
  stroke: rgba(0, 0, 0, 0.5);
  stroke-width: 2px;
}

.dot {
  fill: steelblue;
  stroke: white;
  stroke-width: 1px;
  fill-opacity: 0.8;
  &.dot-selected{
    fill: orange !important;
    fill-opacity: 1 !important;
  }
  &.dot-highlighted{
    fill: red !important;
    fill-opacity: 1 !important;
  }
}

.d3-tip {
  line-height: 1;
  font-weight: bold;
  padding: 12px;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  border-radius: 2px;
}

/* Creates a small triangle extender for the tooltip */
.d3-tip:after {
  box-sizing: border-box;
  display: inline;
  font-size: 10px;
  width: 100%;
  line-height: 1;
  color: rgba(0, 0, 0, 0.8);
  content: "\25BC";
  position: absolute;
  text-align: center;
}

/* Style northward tooltips differently */
.d3-tip.n:after {
  margin: -1px 0 0 0;
  top: 100%;
  left: 0;
}
.x.axis text{
  opacity: 0;
  font-size: 0;
}
.y.axis text{
  opacity: 0;
  font-size: 0;
}
.axisLine{
  opacity: 0;
}
</style>>