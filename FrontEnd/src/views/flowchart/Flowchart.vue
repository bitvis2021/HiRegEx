<template>
  <div
    id="chart"
    tabindex="0"
    :style="{ cursor: cursor }"
    @mousemove="handleChartMouseMove"
    @mouseup="handleChartMouseUp"
    @mousewheel="handleChartMouseWheel"
    @mousedown="handleChartMouseDown($event)">
    <svg id="svg" ref="flowChartCanvas">
      <rect class="selection" height="0" width="0"></rect>
    </svg>
    <el-button class="query-btn" size="mini" @click="query">Query</el-button>
  </div>

</template>
<style lang="less" src="./index.less"></style>
<script>
import { line2, lineTo } from "../../utils/svg";
import { mapState, mapMutations } from 'vuex'
import * as d3 from "d3";

import {
  roundTo20,
  between,
  distanceOfPointToLine, 
  getEdgeOfPoints,
  pointRectangleIntersection,
} from "../../utils/math";
import render from "./render";

export default {
  name: "flowchart",
  props: {
    nodes: {
      type: Array,
      default: () => [],
    },
    connections: {
      type: Array,
      default: () => [],
    },
    width: {
      type: [String, Number],
      default: 800,
    },
    height: {
      type: [String, Number],
      default: 600,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    excludeShownAttrArray: {
      type: Array,
      default: [],
    }
  },
  data() {
    return {
      internalNodes: [],
      internalConnections: [],
      connectingInfo: {
        source: null,
        sourcePosition: null,
      },
      selectionInfo: null,
      currentNodes: [],
      currentConnections: [],
      /**
       * Mouse position(relative to chart div)
       */
      cursorToChartOffset: { x: 0, y: 0 },
      clickedOnce: false,
      pathClickedOnce: false,
      /**
       * lines of all internalConnections
       */
      lines: [],
      canvasId: "svg",
      regexContent: "",
      regexContentFlag: false,
    };
  },
  watch: {
    conditionState: function(){
      console.log("conditionState")
    }
  },
  computed: {
    ...mapState([
      'regexContentState',
      'curRegexIndex',
      'selectedDomKey',
      'selectedDom',
      'visPanelState'
    ]),
  },
  methods: {
    ...mapMutations([
      'UPDATE_VISVIEW',
      'UPDATE_CURRENT_REGEX',
      'UPDATE_CONNECTION',
      'UPDATE_SELECTED_DOM',
      'UPDATE_CONDITION_STATE',
      'GET_SELECTEDKEY',
      'DATA_QUERY_REGEX',
      'UPDATE_NODE_DEFINITION_STATE'
    ]),

    query(){
      var edgeInfo = sysDatasetObj.getEdgeInfo()
      console.log("edgeInfo: ", edgeInfo)
      var rootNode = {
        'type': 'node',
        'repeat': [1 ,1],
        'data': {

        },
        'children':[

        ]
      }
      for(let i=0; i<this.internalNodes.length; i++){
        this.internalNodes[i]['regex']['children'] = []
      }
      for(let i=0; i<edgeInfo.length; i++){
        var curI = null
        var curJ = null
        for(let i1=0; i1<this.internalNodes.length; i1++){
          if(edgeInfo[i][0] == this.internalNodes[i1]['regexIndex']){
            curI = this.internalNodes[i1]['regex']  
          }
          if(edgeInfo[i][1] == this.internalNodes[i1]['regexIndex']){
            curJ = this.internalNodes[i1]['regex']  
          }
        }
        curI['children'].push(curJ)
      }
      if(edgeInfo.length == 0 && this.internalNodes.length == 1){
        rootNode = this.internalNodes[0]['regex']
      }
      for(let i=0; i<edgeInfo.length; i++){
        var flag = 1
        for(let j=0; j<edgeInfo.length; j++){
          if(edgeInfo[i][0] == edgeInfo[j][1]){
            flag = -1
            break
          }
        }
        if(flag != -1){
          for(let k=0; k<this.internalNodes.length; k++){
            if(this.internalNodes[k]['regexIndex'] == edgeInfo[i][0]){
              rootNode = this.internalNodes[k]['regex']
              break
            }
          }
          break
        }
      }
      sysDatasetObj.updateRegex(rootNode)
      this.DATA_QUERY_REGEX()
    },
    add(node) {
      if (this.readonly) {
        return;
      }
      this.internalNodes.push(node);
    },
    editNode(node) {
      if (this.readonly) {
        return;
      }
      this.$emit("editnode", node);
    },
    handleChartMouseWheel(event) {
      event.stopPropagation();
      event.preventDefault();
      if (event.ctrlKey) {
        let svg = document.getElementById("svg");
        let zoom = parseFloat(svg.style.zoom || 1);
        if (event.deltaY > 0 && zoom === 0.1) {
          return;
        }
        zoom -= event.deltaY / 100 / 10;
        svg.style.zoom = zoom;
      }
    },
    async handleChartMouseUp() {
      if (this.connectingInfo.source) {
        if (this.hoveredConnector) {
          if (this.connectingInfo.source.id !== this.hoveredConnector.node.id) {
            // Node can't connect to itself
            let tempId = +new Date();
            let conn = {
              source: {
                id: this.connectingInfo.source.id,
                position: this.connectingInfo.sourcePosition,
              },
              destination: {
                id: this.hoveredConnector.node.id,
                position: this.hoveredConnector.position,
              },
              id: tempId,
              type: "pass",
              name: "Pass",
            };
            let tmpSource = this.internalNodes.filter((item) => item.id === conn['source']['id'])[0]
            let tmpDestination = this.internalNodes.filter((item) => item.id === conn['destination']['id'])[0]
            sysDatasetObj.addEdge(tmpSource['regexIndex'], tmpDestination['regexIndex'])
            
            this.internalConnections.push(conn)
          }
        }
        this.connectingInfo.source = null;
        this.connectingInfo.sourcePosition = null;
      }
      if (this.selectionInfo) {
        this.selectionInfo = null;
      }
      this.regexContentFlag = false
      
    },
    async handleChartMouseMove(event) {
      // calc offset of cursor to chart
      let svg = document.getElementById("svg");
      let zoom = svg.style.zoom; // the size ratio of the whole canvas
      if (zoom.length == 0) {
        zoom = 1
      }
      zoom = parseFloat(zoom)
      let boundingClientRect = event.currentTarget.getBoundingClientRect();
      let actualX = event.pageX - boundingClientRect.left - window.scrollX;  
      actualX = actualX / zoom
      this.cursorToChartOffset.x = Math.trunc(actualX);
      let actualY = event.pageY - boundingClientRect.top - window.scrollY;
      actualY = actualY / zoom
      this.cursorToChartOffset.y = Math.trunc(actualY);
      if (this.connectingInfo.source) {
        await this.renderConnections();

        d3.selectAll("#svg .connector").classed("active", true);

        let sourceOffset = this.getNodeConnectorOffset(
          this.connectingInfo.source.id,
          this.connectingInfo.sourcePosition
        );
        let destinationPosition = this.hoveredConnector
          ? this.hoveredConnector.position
          : null;
        this.arrowTo(
          sourceOffset.x,
          sourceOffset.y,
          this.cursorToChartOffset.x,
          this.cursorToChartOffset.y,
          this.connectingInfo.sourcePosition,
          false,
          destinationPosition
        );
      }
    },
    handleChartMouseDown(event) {
      if (event.ctrlKey) {
        return;
      }
      sysDatasetObj.updateSelectedDomKey(-1)
      this.UPDATE_NODE_DEFINITION_STATE()
      this.selectionInfo = { x: event.offsetX, y: event.offsetY };
    },
    getConnectorPosition(node) {
      //const halfWidth = node.width / 2;
      const halfWidth = 20 + 5;
      const halfHeight = node.height / 2;
      let top = { x: node.x + halfWidth, y: node.y };
      let left = { x: node.x, y: node.y + halfHeight };
      let bottom = { x: node.x + halfWidth, y: node.y + node.height };
      let right = { x: node.x + node.width, y: node.y + halfHeight };
      return { left, right, top, bottom };
    },
    renderSelection() {
      let that = this;
      // render selection rectangle
      if (that.selectionInfo) {
        that.currentNodes.splice(0, that.currentNodes.length);
        that.currentConnections.splice(0, that.currentConnections.length);
        let edge = getEdgeOfPoints([
          { x: that.selectionInfo.x, y: that.selectionInfo.y },
          { x: that.cursorToChartOffset.x, y: that.cursorToChartOffset.y },
        ]);
        let svg = d3.select("#svg");
        let rect = svg.select(".selection").classed("active", true);
        rect
          .attr("x", edge.start.x)
          .attr("y", edge.start.y)
          .attr("width", edge.end.x - edge.start.x)
          .attr("height", edge.end.y - edge.start.y);

        that.internalNodes.forEach((item) => {
          let points = [
            { x: item.x, y: item.y },
            { x: item.x, y: item.y + item.height },
            { x: item.x + item.width, y: item.y },
            { x: item.x + item.width, y: item.y + item.height },
          ];
          if (
            points.every((point) => pointRectangleIntersection(point, edge))
          ) {
            that.currentNodes.push(item);
          }
        });
        that.lines.forEach((line) => {
          let points = [
            { x: line.sourceX, y: line.sourceY },
            { x: line.destinationX, y: line.destinationY },
          ];
          if (
            points.every((point) => pointRectangleIntersection(point, edge)) &&
            that.currentConnections.every((item) => item.id !== line.id)
          ) {
            let connection = that.internalConnections.filter(
              (conn) => conn.id === line.id
            )[0];
            that.currentConnections.push(connection);
          }
        });
      } else {
        d3.selectAll("#svg > .selection").classed("active", false);
      }
    },
    renderConnections() {
      let that = this;
      return new Promise(function (resolve) {
        that.$nextTick(function () {
          d3.selectAll("#svg > g.connection").remove();
          // render lines
          that.lines = [];
          that.internalConnections.forEach((conn) => {
            let sourcePosition = that.getNodeConnectorOffset(
              conn.source.id,
              conn.source.position
            );
            let destinationPosition = that.getNodeConnectorOffset(
              conn.destination.id,
              conn.destination.position
            );
            let colors = {
              pass: "#888888",
              reject: "red",
            };
            let connectionSelected = that.currentConnections.filter((item) => item === conn).length > 0
            if (connectionSelected) {
              colors = {
                pass: "#888888",
                reject: "darkred",
              };
            }
            let result = that.arrowTo(
              sourcePosition.x,
              sourcePosition.y,
              destinationPosition.x,
              destinationPosition.y,
              conn.source.position,
              conn.destination.position,
              connectionSelected,
              colors[conn.type]
            );
            for (const path of result.paths) {
              path.on("mousedown", function () {
                d3.event.stopPropagation();
                if (that.pathClickedOnce) {
                  that.editConnection(conn);
                } else {
                  let timer = setTimeout(function () {
                    that.pathClickedOnce = false;
                    clearTimeout(timer);
                  }, 300);
                  that.pathClickedOnce = true;
                }
                that.currentNodes.splice(0, that.currentNodes.length);
                that.currentConnections.splice(0, that.currentConnections.length);
                that.currentConnections.push(conn);
              });
            }
            for (const line of result.lines) {
              that.lines.push({
                sourceX: line.sourceX,
                sourceY: line.sourceY,
                destinationX: line.destinationX,
                destinationY: line.destinationY,
                id: conn.id,
              });
            }
          });
          resolve();
        });
      });
    },
    renderNodes() {
      let that = this;
      return new Promise(function (resolve) {
        d3.selectAll("#svg > g.node").remove();

        // render nodes
        that.internalNodes.forEach((node) => {
          that.renderNode(
            node,
            that.currentNodes.filter((item) => item === node).length > 0
          );
        });

        resolve();
      });
    },
    getNodeConnectorOffset(nodeId, connectorPosition) {
      let node = this.internalNodes.filter((item) => item.id === nodeId)[0];
      return this.getConnectorPosition(node)[connectorPosition];
    },
    append(element) {
      let svg = d3.select("#svg");
      return svg.insert(element, ".selection");
    },
    guideLineTo(x1, y1, x2, y2) {
      let g = this.append("g");
      g.classed("guideline", true);
      lineTo(g, x1, y1, x2, y2, 1, "#a3a3a3", [5, 3]);
    },
    arrowTo(x1, y1, x2, y2, startPosition, endPosition, connectionSelected, color) {
      let g = this.append("g");
      g.classed("connection", true);
      if (connectionSelected) {
        line2(g, x1, y1, x2, y2, startPosition, endPosition, 2.5, color || "#a3a3a3", true);
      } else {
        line2(g, x1, y1, x2, y2, startPosition, endPosition, 1, color || "#a3a3a3", true);
      } 
      // a 5px cover to make mouse operation conveniently
      return line2(
        g,
        x1,
        y1,
        x2,
        y2,
        startPosition,
        endPosition,
        5,
        "transparent",
        false
      );
    },
    renderNode(node, isSelected) {
      let that = this;
      let g = that.append("g").attr("cursor", "move").classed("node", true);

      node.render = render;
      node.render(g, node, isSelected, this.excludeShownAttrArray);

      let drag = d3
        .drag()
        .on("start", function () {
          // handle mousedown
          let isNotCurrentNode =
            that.currentNodes.filter((item) => item === node).length === 0;
          if (isNotCurrentNode) {
            that.currentConnections.splice(0, that.currentConnections.length);
            that.currentNodes.splice(0, that.currentNodes.length);
            that.currentNodes.push(node);
          }
          // the drag event and click event is conflicted, 
          // so handle the drag start function of the selected nodes is equal to the double click event
          if (that.clickedOnce) {
            that.currentNodes.splice(0, that.currentNodes.length);
            that.editNode(node);
          } else {

            let timer = setTimeout(function () {
              that.clickedOnce = false;
              clearTimeout(timer);
            }, 300);
            that.clickedOnce = true;
          }
        })
        .on("drag", async function () {
          if (that.readonly) {
            return;
          }

          let zoom = parseFloat(document.getElementById("svg").style.zoom || 1);
          for (let currentNode of that.currentNodes) {
            currentNode.x += d3.event.dx / zoom;
            currentNode.y += d3.event.dy / zoom;
          }

          d3.selectAll("#svg > g.guideline").remove();
          let edge = that.getCurrentNodesEdge();
          let expectX = Math.round(Math.round(edge.start.x) / 10) * 10;
          let expectY = Math.round(Math.round(edge.start.y) / 10) * 10;
          that.internalNodes.forEach((item) => {
            if (
              that.currentNodes.filter((currentNode) => currentNode === item)
                .length === 0
            ) {
              if (item.x === expectX) {
                // vertical guideline
                if (item.y < expectY) {
                  that.guideLineTo(
                    item.x,
                    item.y + item.height,
                    expectX,
                    expectY
                  );
                } else {
                  that.guideLineTo(
                    expectX,
                    expectY + item.height,
                    item.x,
                    item.y
                  );
                }
              }
              if (item.y === expectY) {
                // horizontal guideline
                if (item.x < expectX) {
                  that.guideLineTo(
                    item.x + item.width,
                    item.y,
                    expectX,
                    expectY
                  );
                } else {
                  that.guideLineTo(
                    expectX + item.width,
                    expectY,
                    item.x,
                    item.y
                  );
                }
              }
            }
          });
        })
        .on("end", function () {
          d3.selectAll("#svg > g.guideline").remove();
          for (let currentNode of that.currentNodes) {
            currentNode.x = Math.round(Math.round(currentNode.x) / 10) * 10;
            currentNode.y = Math.round(Math.round(currentNode.y) / 10) * 10;
          }
        });
      g.call(drag);
      g.on("mousedown", function () {
        // handle ctrl+mousedown
        if (!d3.event.ctrlKey) {
          return;
        }
        let isNotCurrentNode =
          that.currentNodes.filter((item) => item === node).length === 0;
        if (isNotCurrentNode) {
          that.currentNodes.push(node);
        } else {
          that.currentNodes.splice(that.currentNodes.indexOf(node), 1);
        }
      });
      if(node['regex']['type'] == 'node'){
        var curX = node.x + 5
        var curY = node.y + 5
        var eleWidth = 5
        var eleHeight = 5
        if('notFlag' in node['regex'] && node['regex']['notFlag']){
          g.append('path')
          .attr('d', function(){
            var x1 = curX-3
            var y1 = curY+5
        
            return ( "M " + x1 + " " + y1 +
                    "v " + 23);
          })
          .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
          g.append('circle')
          .attr('cx', curX-3)
          .attr('cy', curY+33)
          .attr('r', '0.7')
           .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
        
        }

        g.append('rect')
        .attr('class', 'unselectable title')
        .attr('id', 'rect'+node['regex']['key'])
        .attr('x', curX)
        .attr('y', curY)
        .attr('width', 40)
        .attr('height', 40)
        .attr('style', function(){
            let tmpKey = sysDatasetObj.getSelectedDomKey()
            if(node['regex']['key'] === tmpKey){
                return ( 
                        "stroke: red !important;" + 
                        "fill: " + node['regex']['nodeColor'] + "; "+
                        "stroke-dasharray: 0 0; " + 
                        "stroke-width: 1;"
                )
            }
            return (
              "stroke: #c4bbbb; !important;" + 
              "fill: " + node['regex']['nodeColor'] + "; " + 
                "stroke-dasharray: 0 0; " + 
                "stroke-width: 1;"
            )
        })
        .on('click', function(){
          d3.select(this)
          .attr('style', function(){
                                 return (     
                      "stroke: red !important;" + 
                      "fill: " + node['regex']['nodeColor'] + "; "+
                      "stroke-dasharray: 0 0; " + 
                      "stroke-width: 1;"
                    )
          })
          sysDatasetObj.updateSelectedDomKey(node['regex']['key'])
          sysDatasetObj.updateSelectedOr(node['regex'], -1)
          that.UPDATE_CONDITION_STATE(false)
          that.UPDATE_SELECTED_DOM(node['regex'])
        })
        if('nodeName' in node['regex']){
          if(node['regex']['nodeName'] == '.'){
            g.append('text')
            .attr('class', 'new11')
            .attr('x', curX + 20)
            .attr('y', curY + 12)
            .attr('fill', 'white')
            .attr('font-size', '50px')
            .attr('text-anchor', "middle")
            .attr("alignment-baseline", "middle")
            .attr('class', 'unselectable title')
            .text(() => node['regex']['nodeName'])
            .on('click', function(){
              d3.select('#rect'+node['regex']['key'])
                .attr('style', function(){
                                      return (     
                            "stroke: red !important;" + 
                            "fill: " + node['regex']['nodeColor'] + "; "+
                            "stroke-dasharray: 0 0; " + 
                            "stroke-width: 1;"
                          )
                })
              sysDatasetObj.updateSelectedDomKey(node['regex']['key'])
              sysDatasetObj.updateSelectedOr(node['regex'], -1)
              that.UPDATE_CONDITION_STATE(false)
              that.UPDATE_SELECTED_DOM(node['regex'])
            })
          }
          else{
            g.append('text')
            .attr('class', 'new11')
            .attr('x', curX + 20)
            .attr('y', curY + 20 + 2.5)
            .attr('fill', 'white')
            .attr('font-size', '20px')
            .attr('text-anchor', "middle")
            .attr("alignment-baseline", "middle")
            .attr('class', 'unselectable title')
            .text(() => node['regex']['nodeName'])
            .on('click', function(){
              d3.select('#rect'+node['regex']['key'])
                .attr('style', function(){
                                      return (     
                            "stroke: red !important;" + 
                            "fill: " + node['regex']['nodeColor'] + "; "+
                            "stroke-dasharray: 0 0; " + 
                            "stroke-width: 1;"
                          )
                })
              sysDatasetObj.updateSelectedDomKey(node['regex']['key'])
              sysDatasetObj.updateSelectedOr(node['regex'], -1)
              that.UPDATE_CONDITION_STATE(false)
              that.UPDATE_SELECTED_DOM(node['regex'])
            })
          }
          
        }
        node.width = eleWidth + 40 + 5
        node.height = eleHeight + 40 + 5
      }
      else if(node['regex']['type'] == 'or'){
        let eleWidth = 0
        let curX = node.x
        let curY = node.y
        g.append('path')
        .attr('class', 'path-'+node['regex']['key'])
        .attr('d', function(){
          var x1 = curX + 15
          var y1 = curY + 2.5
          var x2 = curX + 15
          var y2 = curY + 44.5

          var qx = x1-(y2-y1)/3
          var qy = (y2+y1)/2

          return ( "M " +  x1 + " " +  y1 +
                " Q " + qx + " " + qy + " " + x2 + " " + y2 );
        })
        .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')

        g.append('rect')
        .attr('width', '18')
        .attr('height', '42')
        .attr('transform', function(){
          var x1 = curX + 15
          var y1 = curY + 2.5
          var x2 = curX + 15
          var y2 = curY + 44.5

          var qx = x1-(y2-y1)/3 + 5
          var qy = (y2+y1)/2
          return `translate(${qx}, ${y1})`
        })
        .attr('opacity', '0')
        .on('click', function(){
           that.UPDATE_SELECTED_DOM(node['regex'])
            d3.selectAll('.path-'+node['regex']['key'])
              .attr('style', 'stroke: red; stroke-width: 2px; fill: none;')
            })
        curX = curX + 15
        eleWidth += 15

        for(let i in node['regex']['composition']){
          if(i!=0){
            g.append('path')
            .attr('d', function(){
              var x1 = curX+10
              var y1 = curY+3
    	        return ( "M " +  x1 + " " +  y1 +
         		      " v " + 42);
            })
            .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
            curX += 10
            eleWidth += 5
          }
            if('notFlag' in node['regex']['composition'][i] && node['regex']['composition'][i]['notFlag']){
              g.append('path')
              .attr('d', function(){
                var x1 = curX+7
                var y1 = curY+5
            
                return ( "M " + x1 + " " + y1 +
                        "v " + 32);
              })
              .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
              g.append('circle')
              .attr('cx', curX+7)
              .attr('cy', curY+40)
              .attr('r', '1')
              .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
            
              curX += 3
              eleWidth += 3
            }
            g.append('rect')
              .attr('class', 'unselectable title')
              .attr('id', 'rect'+node['regex']['composition'][i]['key'])
              .attr('x', curX+10)
              .attr('y', curY+3)
              .attr('width', 42)
              .attr('height', 42)
              .attr('style', function(){
                  let tmpKey = sysDatasetObj.getSelectedDomKey()
                  if('definition' in node['regex']['composition'][i]){
                      if(node['regex']['composition'][i]['definition']){
                          if(node['regex']['composition'][i]['key'] === tmpKey){
                              return ( 
                                      "stroke: red !important;" + 
                                      "fill: " + node['regex']['composition'][i]['nodeColor'] + "; "+
                                      "stroke-dasharray: 0 0; " + 
                                      "stroke-width: 1;"
                              )
                          }
                          return (
                            "stroke: #c4bbbb; !important;" + 
                            "fill: " + node['regex']['composition'][i]['nodeColor'] + "; " + 
                              "stroke-dasharray: 0 0; " + 
                              "stroke-width: 1;"
                          )

                      }
                  }
                  if('key' in node['regex']['composition'][i] && node['regex']['composition'][i].key === tmpKey){
                        return ( "stroke: red !important; "+                
                          "stroke-width: 2; " + 
                          "stroke-dasharray: 4 2;" + 
                          "fill: white; ");
                  }
                  return (
                      "stroke: #c4bbbb; " + 
                      "stroke-width: 2; " + 
                      "stroke-dasharray: 4 2;" + 
                      "fill: white; "
                  )
              })
              .on('click', function(){
                d3.select(this)
                .attr('style', function(){
                    if('definition' in node['regex']['composition'][i]){
                        if(node['regex']['composition'][i]['definition']){
                          return (     
                            "stroke: red !important;" + 
                            "fill: " + node['regex']['composition'][i]['nodeColor'] + "; "+
                            "stroke-dasharray: 0 0; " + 
                            "stroke-width: 1;"
                          )
                        }
                    }
                    return (
                          "stroke: red !important;" + 
                          "stroke-width: 2; " + 
                          "stroke-dasharray: 4 2;" + 
                          "fill: white; "
                      )
                })
                that.UPDATE_CONDITION_STATE(false)
                that.UPDATE_SELECTED_DOM(node['regex']['composition'][i])
                sysDatasetObj.updateSelectedOr(node['regex'], i)
              })
            if('nodeName' in node['regex']['composition'][i]){
              g.append('text')
              .attr('class', 'new11')
              .attr('x', curX + 31)
              .attr('y', curY + 24)
              .attr('fill', 'white')
              .attr('font-size', '18px !important')
              .attr('text-anchor', "middle")
              .attr("alignment-baseline", "middle")
              .attr('class', 'unselectable title')
              .text(() => node['regex']['composition'][i]['nodeName'])
              .on('click', function(){
                  d3.select('#rect'+node['regex']['composition'][i]['key'])
                  .attr('style', function(){
                  if('definition' in node['regex']['composition'][i]){
                      if(node['regex']['composition'][i]['definition']){
                        return (     
                          "stroke: red !important;" + 
                          "fill: " + node['regex']['composition'][i]['nodeColor'] + "; "+
                          "stroke-dasharray: 0 0; " + 
                          "stroke-width: 1;"
                        )
                      }
                  }
                  return (
                      "stroke: red !important;" + 
                      "stroke-width: 2; " + 
                      "stroke-dasharray: 4 2;" + 
                      "fill: white; "
                  )
              })
                that.UPDATE_CONDITION_STATE(false)
                that.UPDATE_SELECTED_DOM(node['regex']['composition'][i])
                sysDatasetObj.updateSelectedOr(node['regex'], i)
              })
            }
            curX = curX + 52
            eleWidth += 52
            if(!(node['regex']['composition'][i]['repeat'][0] == 1 && node['regex']['composition'][i]['repeat'][1] == 1)){
              g.append('text')
              .attr('x', curX + 5)
              .attr('y', curY + 2)
              .attr('font-size', '15px')
              .attr('alignment-baseline', 'hanging')
              .text(() => node['regex']['composition'][i]['repeat'][0] + '..' + node['regex']['composition'][i]['repeat'][1])
              curX = curX + 30
              eleWidth += 30
            }
        }
        g.append('path')
          .attr('class', 'path-'+node['regex']['key'])
          .attr('d', function(){
            var x1 = curX + 10
            var y1 = curY + 2.5
            var x2 = curX + 10
            var y2 = curY + 44.5

            var qx = x1+(y2-y1)/3
            var qy = (y2+y1)/2

            return ( "M " +  x1 + " " +  y1 +
                  " Q " + qx + " " + qy + " " + x2 + " " + y2 );
          })
          .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
          
          g.append('rect')
            .attr('width', '18')
            .attr('height', '42')
            .attr('transform', function(){
              var x1 = curX + 10
              var y1 = curY + 2.5
              var x2 = curX + 10
              var y2 = curY + 44.5

              var qx = x1-5
              var qy = (y2+y1)/2
              return `translate(${qx}, ${y1})`
            })
            .attr('opacity', '0')
            .on('click', function(){
              that.UPDATE_SELECTED_DOM(node['regex'])
                d3.selectAll('.path-'+node['regex']['key'])
                  .attr('style', 'stroke: red; stroke-width: 2px; fill: none;')
                })

        curX = curX + 15
        eleWidth += 15

        if(!(node['regex']['repeat'][0] == 1 && node['regex']['repeat'][1] == 1)){
              g.append('text')
              .attr('x', curX + 5)
              .attr('y', curY + 2)
              .attr('font-size', '15px')
              .attr('alignment-baseline', 'hanging')
              .text(() => node['regex']['repeat'][0] + '..' + node['regex']['repeat'][1])
              curX = curX + 30
              eleWidth += 30
        }

        node.width = 15 + eleWidth

      }
      else if(node['regex']['type'] == 'branch'){
        let eleWidth = 5
        let eleHeight = 5
        let curX = node.x + 5
        let curY = node.y + 5

        g.append('path')
        .attr('class', 'bPath-'+node['regex']['key'])
        .attr('d', function(){
          var x0 = curX
          var y0 = curY + 10
          var x1 = curX + 20
          var y1 = curY
          var x2 = curX + 40
          var y2 = curY + 10

          return "M " +  x0 + " " +  y0 +
                " L " + x1+ " " + y1 + 
                " L " + x2+ " " + y2
        })
        .attr('style','stroke: #c4bbbb; stroke-width: 2px; fill: none;')


        g.append('text')
          .attr('x', curX+1)
          .attr('y', curY-4)
          .attr('font-size', '14px')
          .attr('alignment-baseline', 'hanging')
          .attr('text-anchor', 'middle')
          .attr('font-weight', 'bold')
          .attr('fill', '#2c2c2c')
          .text(() => node['regex']['repeat'][0])
        
        if(node['regex']['repeat'][1] == '*'){
          g.append('text')
            .attr('x', curX+38)
            .attr('y', curY-2)
            .attr('font-size', '18px')
            .attr('alignment-baseline', 'hanging')
            .attr('text-anchor', 'middle')
            .attr('font-weight', 'bold')
            .attr('fill', '#2c2c2c')
            .text(() => node['regex']['repeat'][1])
        }
        else{
          g.append('text')
          .attr('x', curX+38)
          .attr('y', curY-4)
          .attr('font-size', '14px')
          .attr('alignment-baseline', 'hanging')
          .attr('text-anchor', 'middle')
          .attr('font-weight', 'bold')
          .attr('fill', '#2c2c2c')
          .text(() => node['regex']['repeat'][1])
        }



        g.append('rect')
          .attr('width', '40')
          .attr('height', '10')
          .attr('transform', function(){
          var x = curX
          var y = curY
          return `translate(${x}, ${y})`
          })
          .attr('opacity', '0')
          .on('click', function(){
            that.UPDATE_SELECTED_DOM(node['regex'])
              d3.selectAll('.bPath-'+node['regex']['key'])
                .attr('style', 'stroke: red; stroke-width: 2px; fill: none;')
              })

        curY += 15
        eleHeight += 15


        
        for(let i in node['regex']['composition']){
          if(node['regex']['composition'][i]['type'] == 'node'){
            if('notFlag' in node['regex']['composition'][i] && node['regex']['composition'][i]['notFlag']){
              g.append('path')
                .attr('d', function(){
                  var x1 = curX-3
                  var y1 = curY+5
              
                  return ( "M " + x1 + " " + y1 +
                          "v " + 23);
                })
              .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
              g.append('circle')
              .attr('cx', curX-3)
              .attr('cy', curY+33)
              .attr('r', '0.7')
              .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
            
            }

            g.append('rect')
              .attr('class', 'unselectable title')
              .attr('id', 'rect'+node['regex']['composition'][i]['key'])
              .attr('x', curX)
              .attr('y', curY)
              .attr('width', 40)
              .attr('height', 40)
              .attr('style', function(){
                  let tmpKey = sysDatasetObj.getSelectedDomKey()
                    if(node['regex']['composition'][i]['key'] === tmpKey){
                        return ( 
                                "stroke: red !important;" + 
                                "fill: " + node['regex']['composition'][i]['nodeColor'] + "; "+
                                "stroke-dasharray: 0 0; " + 
                                "stroke-width: 1;"
                        )
                    }
                    return (
                      "stroke: #c4bbbb; !important;" + 
                      "fill: " + node['regex']['composition'][i]['nodeColor'] + "; " + 
                        "stroke-dasharray: 0 0; " + 
                        "stroke-width: 1;"
                    )
                  if('definition' in node['regex']['composition'][i]){
                      if(node['regex']['composition'][i]['definition']){
                          if(node['regex']['composition'][i]['key'] === tmpKey){
                              return ( 
                                      "stroke: red !important;" + 
                                      "fill: " + node['regex']['composition'][i]['nodeColor'] + "; "+
                                      "stroke-dasharray: 0 0; " + 
                                      "stroke-width: 1;"
                              )
                          }
                          return (
                            "stroke: #c4bbbb; !important;" + 
                            "fill: " + node['regex']['composition'][i]['nodeColor'] + "; " + 
                              "stroke-dasharray: 0 0; " + 
                              "stroke-width: 1;"
                          )

                      }
                  }
                  if('key' in node['regex']['composition'][i] && node['regex']['composition'][i].key === tmpKey){
                        return ( "stroke: red !important; "+                
                          "stroke-width: 2; " + 
                          "stroke-dasharray: 4 2;" + 
                          "fill: white; ");
                  }
                  return (
                      "stroke: #c4bbbb; " + 
                      "stroke-width: 2; " + 
                      "stroke-dasharray: 4 2;" + 
                      "fill: white; "
                  )
              })
              .on('click', function(){
                d3.select(this)
                .attr('style', function(){
                                            return (     
                            "stroke: red !important;" + 
                            "fill: " + node['regex']['composition'][i]['nodeColor'] + "; "+
                            "stroke-dasharray: 0 0; " + 
                            "stroke-width: 1;"
                          )
                    if('definition' in node['regex']['composition'][i]){
                        if(node['regex']['composition'][i]['definition']){
                          return (     
                            "stroke: red !important;" + 
                            "fill: " + node['regex']['composition'][i]['nodeColor'] + "; "+
                            "stroke-dasharray: 0 0; " + 
                            "stroke-width: 1;"
                          )
                        }
                    }
                    return (
                          "stroke: red !important;" + 
                          "stroke-width: 2; " + 
                          "stroke-dasharray: 4 2;" + 
                          "fill: white; "
                      )
                })
                that.UPDATE_CONDITION_STATE(false)
                that.UPDATE_SELECTED_DOM(node['regex']['composition'][i])
                sysDatasetObj.updateSelectedBranch(node['regex'], i)
                sysDatasetObj.updateSelectedOr(node['regex']['composition'][i], -1)
              })
            if('nodeName' in node['regex']['composition'][i]){
              if(node['regex']['composition'][i]['nodeName'] == '.'){
                g.append('text')
                .attr('class', 'new11')
                .attr('x', curX + 20)
                .attr('y', curY + 12)
                .attr('fill', 'white')
                .attr('font-size', '50px')
                .attr('text-anchor', "middle")
                .attr("alignment-baseline", "middle")
                .attr('class', 'unselectable title')
                .text(() => node['regex']['composition'][i]['nodeName'])
                .on('click', function(){
                    d3.select('#rect'+node['regex']['composition'][i]['key'])
                    .attr('style', function(){
                                          return (     
                            "stroke: red !important;" + 
                            "fill: " + node['regex']['composition'][i]['nodeColor'] + "; "+
                            "stroke-dasharray: 0 0; " + 
                            "stroke-width: 1;"
                          )
                })
                  that.UPDATE_CONDITION_STATE(false)
                  that.UPDATE_SELECTED_DOM(node['regex']['composition'][i])
                  sysDatasetObj.updateSelectedBranch(node['regex'], i)
                  sysDatasetObj.updateSelectedOr(node['regex']['composition'][i], -1)
                })
              }
              else{
                g.append('text')
                .attr('class', 'new11')
                .attr('x', curX + 20)
                .attr('y', curY + 20 + 2.5)
                .attr('fill', 'white')
                .attr('font-size', '20px')
                .attr('text-anchor', "middle")
                .attr("alignment-baseline", "middle")
                .attr('class', 'unselectable title')
                .text(() => node['regex']['composition'][i]['nodeName'])
                .on('click', function(){
                    d3.select('#rect'+node['regex']['composition'][i]['key'])
                    .attr('style', function(){
                                          return (     
                            "stroke: red !important;" + 
                            "fill: " + node['regex']['composition'][i]['nodeColor'] + "; "+
                            "stroke-dasharray: 0 0; " + 
                            "stroke-width: 1;"
                          )
                })
                  that.UPDATE_CONDITION_STATE(false)
                  that.UPDATE_SELECTED_DOM(node['regex']['composition'][i])
                  sysDatasetObj.updateSelectedBranch(node['regex'], i)
                  sysDatasetObj.updateSelectedOr(node['regex']['composition'][i], -1)
                })
              }
            }


            if(!(node['regex']['composition'][i]['repeat'][0] == 1 && node['regex']['composition'][i]['repeat'][1] == 1)){
              g.append('path')
              .attr('class', '1bPath-'+node['regex']['key'])
              .attr('d', function(){
                var x1 = curX + 40 + 3;
                var y1 = curY + 16;
                var x2 = curX + 40 + 3;
                var y2 = curY + 24;
                var r = 7;
                eleWidth = 5 + 15;
                return 'M ' + x1 + ',' + y1 + ' ' + 'A ' + r + ',' + r + ' ' + '0 ' + '1,1' + ' ' + x2 + ',' + y2;
              })
              .attr('style','stroke: #000000; stroke-width: 1.5px; fill: none;')

              g.append('path')
              .attr('class', '1bPath-'+node['regex']['key'])
              .attr('d', function(){
                var x0 = curX + 40 + 3
                var y0 = curY + 24
                var x1 = x0 + 4
                var y1 = y0 + 6

                return "M " +  x1 + "," +  y1 +
                  " L " + x0 + "," + y0 ;
              })
              .attr('style','stroke: #000000; stroke-width: 1.5px; fill: none;')

              g.append('text')
              .attr('x', curX + 40 + 5)
              .attr('y', curY )
              .attr('font-size', '12px')
              .attr('alignment-baseline', 'hanging')
              .attr('font-weight', 'bold')
            .attr('fill', '#2c2c2c')
              .text(() => node['regex']['composition'][i]['repeat'][0])

              if(node['regex']['composition'][i]['repeat'][1] == '*'){
                g.append('text')
                  .attr('x', curX + 40 + 5)
                  .attr('y', curY + 30)
                  .attr('font-size', '20px')
                  .attr('alignment-baseline', 'hanging')
                  .attr('font-weight', 'bold')
                  .attr('fill', '#2c2c2c')
                  .text(() => node['regex']['composition'][i]['repeat'][1])
              }
              else{
                g.append('text')
                .attr('x', curX + 40 + 5)
                .attr('y', curY + 30)
                .attr('font-size', '12px')
                .attr('alignment-baseline', 'hanging')
                .attr('font-weight', 'bold')
                .attr('fill', '#2c2c2c')
                .text(() => node['regex']['composition'][i]['repeat'][1])
              }
            }

            curY = curY + 40 + 10
            eleHeight = eleHeight + 40 + 10


          }
          else if(node['regex']['composition'][i]['type'] == 'or'){
            g.append('path')
            .attr('class', 'path-'+node['regex']['composition'][i]['key'])
            .attr('d', function(){
              var x1 = curX + 15
              var y1 = curY + 2.5
              var x2 = curX + 15
              var y2 = curY + 44.5

              var qx = x1-(y2-y1)/3
              var qy = (y2+y1)/2

              return ( "M " +  x1 + " " +  y1 +
                    " Q " + qx + " " + qy + " " + x2 + " " + y2 );
            })
            .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')

            g.append('rect')
              .attr('width', '18')
              .attr('height', '42')
              .attr('transform', function(){
                var x1 = curX + 15
                var y1 = curY + 2.5
                var x2 = curX + 15
                var y2 = curY + 44.5

                var qx = x1-(y2-y1)/3 + 5
                var qy = (y2+y1)/2
                return `translate(${qx}, ${y1})`
              })
              .attr('opacity', '0')
              .on('click', function(){
                that.UPDATE_SELECTED_DOM(node['regex']['composition'][i])
                  d3.selectAll('.path-'+node['regex']['composition'][i]['key'])
                    .attr('style', 'stroke: red; stroke-width: 2px; fill: none;')
                  })

            curX = curX + 15
            eleWidth += 15

            for(let j in node['regex']['composition'][i]['composition']){
              if(j!=0){
                g.append('path')
                .attr('d', function(){
                  var x1 = curX+10
                  var y1 = curY+3
                  return ( "M " +  x1 + " " +  y1 +
                      " v " + 42);
                })
                .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
                curX += 10
                eleWidth += 5
              }
              
              if('notFlag' in node['regex']['composition'][i]['composition'][j] && node['regex']['composition'][i]['composition'][j]['notFlag']){
              g.append('path')
              .attr('d', function(){
                var x1 = curX+7
                var y1 = curY+5
            
                return ( "M " + x1 + " " + y1 +
                        "v " + 32);
              })
              .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
              g.append('circle')
              .attr('cx', curX+7)
              .attr('cy', curY+40)
              .attr('r', '1')
              .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')
            
              curX += 3
              eleWidth += 3
            }

                g.append('rect')
                  .attr('class', 'unselectable title')
                  .attr('id', 'rect'+node['regex']['composition'][i]['composition'][j]['key'])
                  .attr('x', curX+10)
                  .attr('y', curY+3)
                  .attr('width', 42)
                  .attr('height', 42)
                  .attr('style', function(){
                      let tmpKey = sysDatasetObj.getSelectedDomKey()
                      if('definition' in node['regex']['composition'][i]['composition'][j]){
                          if(node['regex']['composition'][i]['composition'][j]['definition']){
                              if(node['regex']['composition'][i]['composition'][j]['key'] === tmpKey){
                                  return ( 
                                          "stroke: red !important;" + 
                                          "fill: " + node['regex']['composition'][i]['composition'][j]['nodeColor'] + "; "+
                                          "stroke-dasharray: 0 0; " + 
                                          "stroke-width: 1;"
                                  )
                              }
                              return (
                                "stroke: #c4bbbb; !important;" + 
                                "fill: " + node['regex']['composition'][i]['composition'][j]['nodeColor'] + "; " + 
                                  "stroke-dasharray: 0 0; " + 
                                  "stroke-width: 1;"
                              )

                          }
                      }
                      if('key' in node['regex']['composition'][i]['composition'][j] && node['regex']['composition'][i]['composition'][j].key === tmpKey){
                            return ( "stroke: red !important; "+                
                              "stroke-width: 2; " + 
                              "stroke-dasharray: 4 2;" + 
                              "fill: white; ");
                      }
                      return (
                          "stroke: #c4bbbb; " + 
                          "stroke-width: 2; " + 
                          "stroke-dasharray: 4 2;" + 
                          "fill: white; "
                      )
                  })
                  .on('click', function(){
                    d3.select(this)
                    .attr('style', function(){
                        if('definition' in node['regex']['composition'][i]['composition'][j]){
                            if(node['regex']['composition'][i]['composition'][j]['definition']){
                              return (     
                                "stroke: red !important;" + 
                                "fill: " + node['regex']['composition'][i]['composition'][j]['nodeColor'] + "; "+
                                "stroke-dasharray: 0 0; " + 
                                "stroke-width: 1;"
                              )
                            }
                        }
                        return (
                              "stroke: red !important;" + 
                              "stroke-width: 2; " + 
                              "stroke-dasharray: 4 2;" + 
                              "fill: white; "
                          )
                    })
                    that.UPDATE_CONDITION_STATE(false)
                    that.UPDATE_SELECTED_DOM(node['regex']['composition'][i]['composition'][j])
                    sysDatasetObj.updateSelectedOr(node['regex']['composition'][i], j)
                  })
                if('nodeName' in node['regex']['composition'][i]['composition'][j]){
                  g.append('text')
                  .attr('class', 'new11')
                  .attr('x', curX + 31)
                  .attr('y', curY + 24)
                  .attr('fill', 'white')
                  .attr('font-size', '18px !important')
                  .attr('text-anchor', "middle")
                  .attr("alignment-baseline", "middle")
                  .attr('class', 'unselectable title')
                  .text(() =>node['regex']['composition'][i]['composition'][j]['nodeName'])
                  .on('click', function(){
                      d3.select('#rect'+node['regex']['composition'][i]['key'])
                      .attr('style', function(){
                      if('definition' in node['regex']['composition'][i]['composition'][j]){
                          if(node['regex']['composition'][i]['composition'][j]['definition']){
                            return (     
                              "stroke: red !important;" + 
                              "fill: " + node['regex']['composition'][i]['composition'][j]['nodeColor'] + "; "+
                              "stroke-dasharray: 0 0; " + 
                              "stroke-width: 1;"
                            )
                          }
                      }
                      return (
                          "stroke: red !important;" + 
                          "stroke-width: 2; " + 
                          "stroke-dasharray: 4 2;" + 
                          "fill: white; "
                      )
                  })
                    that.UPDATE_CONDITION_STATE(false)
                    that.UPDATE_SELECTED_DOM(node['regex']['composition'][i]['composition'][j])
                    sysDatasetObj.updateSelectedOr(node['regex']['composition'][i], j)
                  })
                }
                curX = curX + 52
                eleWidth += 52
                if(!(node['regex']['composition'][i]['composition'][j]['repeat'][0] == 1 && node['regex']['composition'][i]['composition'][j]['repeat'][1] == 1)){
                  g.append('text')
                  .attr('x', curX + 5)
                  .attr('y', curY + 2)
                  .attr('font-size', '15px')
                  .attr('alignment-baseline', 'hanging')
                  .text(() => node['regex']['composition'][i]['composition'][j]['repeat'][0] + '..' + node['regex']['composition'][i]['composition'][j]['repeat'][1])
                  curX = curX + 30
                  eleWidth += 30
                }
            }
            g.append('path')
              .attr('class', 'path-'+node['regex']['composition'][i]['key'])
              .attr('d', function(){
                var x1 = curX + 10
                var y1 = curY + 2.5
                var x2 = curX + 10
                var y2 = curY + 44.5

                var qx = x1+(y2-y1)/3
                var qy = (y2+y1)/2

                return ( "M " +  x1 + " " +  y1 +
                      " Q " + qx + " " + qy + " " + x2 + " " + y2 );
              })
              .attr('style','stroke: #000000; stroke-width: 2px; fill: none;')

              g.append('rect')
                .attr('width', '18')
                .attr('height', '42')
                .attr('transform', function(){
                  var x1 = curX + 10
                  var y1 = curY + 2.5
                  var x2 = curX + 10
                  var y2 = curY + 44.5

                  var qx = x1-5
                  var qy = (y2+y1)/2
                  return `translate(${qx}, ${y1})`
                })
              .attr('opacity', '0')
              .on('click', function(){
                that.UPDATE_SELECTED_DOM(node['regex']['composition'][i])
                  d3.selectAll('.path-'+node['regex']['composition'][i]['key'])
                    .attr('style', 'stroke: red; stroke-width: 2px; fill: none;')
                  })

              curX = curX + 15
              eleWidth += 15

            if(!(node['regex']['composition'][i]['repeat'][0] == 1 && node['regex']['composition'][i]['repeat'][1] == 1)){
              g.append('text')
              .attr('x', curX + 5)
              .attr('y', curY + 2)
              .attr('font-size', '15px')
              .attr('alignment-baseline', 'hanging')
              .text(() => node['regex']['composition'][i]['repeat'][0] + '..' + node['regex']['composition'][i]['repeat'][1])
              curX = curX + 30
              eleWidth += 30
            }

            node.width = 8 + eleWidth

          }

        }
        
        node.width = eleWidth + 40 + 5
        node.height = eleHeight - 5


        
      }


          // .attr("class", "connector");
      let connectors = [];
      let connectorPosition = this.getConnectorPosition(node);
      for (let position in connectorPosition) {
        let positionElement = connectorPosition[position];
        let connector = g
          .append("circle")
          .attr("cx", positionElement.x)
          .attr("cy", positionElement.y)
          .attr("r", 4)
          .attr("class", "connector");

        connector
          .on("mousedown", function () {
            d3.event.stopPropagation();
            if (node.type === "end" || that.readonly) {
              return;
            }
            that.connectingInfo.source = node;
            that.connectingInfo.sourcePosition = position;
          })
          .on("mouseup", function () {
            d3.event.stopPropagation();
            if (that.connectingInfo.source) {
              if (that.connectingInfo.source.id !== node.id) {
                // Node can't connect to itself
                let tempId = +new Date();
                let conn = {
                  source: {
                    id: that.connectingInfo.source.id,
                    position: that.connectingInfo.sourcePosition,
                  },
                  destination: {
                    id: node.id,
                    position: position,
                  },
                  id: tempId,
                  type: "pass",
                  name: "Pass",
                };
                let tmpSource = that.internalNodes.filter((item) => item.id === conn['source']['id'])[0]
                let tmpDestination = that.internalNodes.filter((item) => item.id === conn['destination']['id'])[0]
                sysDatasetObj.addEdge(tmpSource['regexIndex'], tmpDestination['regexIndex'])
                that.internalConnections.push(conn);

              }
              that.connectingInfo.source = null;
              that.connectingInfo.sourcePosition = null;
            }
          })
          .on("mouseover", function () {
            connector.classed("active", true);
          })
          .on("mouseout", function () {
            connector.classed("active", false);
          });
        connectors.push(connector);
      }
      g.on("mouseover", function () {
        connectors.forEach((conn) => conn.classed("active", true));
      }).on("mouseout", function () {
        connectors.forEach((conn) => conn.classed("active", false));
      });
    },
    getCurrentNodesEdge() {
      let points = this.currentNodes.map((node) => ({
        x: node.x,
        y: node.y,
      }));
      points.push(
        ...this.currentNodes.map((node) => ({
          x: node.x + node.width,
          y: node.y + node.height,
        }))
      );
      return getEdgeOfPoints(points);
    },
    async remove() {
      if (this.readonly) {
        return;
      }
      if (this.currentConnections.length > 0) {
        for (let conn of this.currentConnections) {
          this.removeConnection(conn);
        }
        this.currentConnections.splice(0, this.currentConnections.length);
      }
      if (this.currentNodes.length > 0) {
        for (let node of this.currentNodes) {
          this.removeNode(node);
        }
        this.currentNodes.splice(0, this.currentNodes.length);
      }
    },
    removeNode(node) {
      let connections = this.internalConnections.filter(
        (item) => item.source.id === node.id || item.destination.id === node.id
      );
      for (let connection of connections) {
        this.internalConnections.splice(
          this.internalConnections.indexOf(connection),
          1
        );
      }
      sysDatasetObj.deleteEdge(node['regexIndex'])
      this.internalNodes.splice(this.internalNodes.indexOf(node), 1);
    },
    removeConnection(conn) {
      let index = this.internalConnections.indexOf(conn);
      let tmpSource = this.internalNodes.filter((item) => item.id === conn['source']['id'])[0]
      let tmpDestination = this.internalNodes.filter((item) => item.id === conn['destination']['id'])[0]
      sysDatasetObj.deleteEdge1(tmpSource['regexIndex'], tmpDestination['regexIndex'])
      this.internalConnections.splice(index, 1);
    },
    moveCurrentNode(x, y) {
      if (this.currentNodes.length > 0 && !this.readonly) {
        for (let node of this.currentNodes) {
          node.x += x;
          node.y += y;
        }
      }
    },
    init() {
      let that = this;
      that.internalNodes.splice(0, that.internalNodes.length);
      that.internalConnections.splice(0, that.internalConnections.length);
      that.nodes.forEach((node) => {
        let newNode = Object.assign({}, node);
        newNode.width = newNode.width || 120;
        newNode.height = newNode.height || 60;
        that.internalNodes.push(newNode);
      });
      that.connections.forEach((connection) => {
        that.internalConnections.push(JSON.parse(JSON.stringify(connection)));
      });
    },
    ...mapMutations([
      'UPDATE_HOVERING_ID'
    ])
  },
  mounted() {
    let that = this;
    that.init();
    document.onkeydown = function (event) {
      switch (event.keyCode) {
        case 37:
          that.moveCurrentNode(-10, 0);
          break;
        case 38:
          that.moveCurrentNode(0, -10);
          break;
        case 39:
          that.moveCurrentNode(10, 0);
          break;
        case 40:
          that.moveCurrentNode(0, 10);
          break;
        case 27:
          that.currentNodes.splice(0, that.currentNodes.length);
          that.currentConnections.splice(0, that.currentConnections.length);
          break;
        case 65:
          if (document.activeElement === document.getElementById("chart")) {
            that.currentNodes.splice(0, that.currentNodes.length);
            that.currentConnections.splice(0, that.currentConnections.length);
            that.currentNodes.push(...that.internalNodes);
            that.currentConnections.push(...that.internalConnections);
            event.preventDefault();
          }
          break;
        // delete the selected item
        case 8:
        // case 46:
        //   that.remove();
        //   break;
        default:
          break;
      }
    };
  },
  created() {},
  computed: {
    // ...mapState([
    //   'hoveringId'
    // ]),
    hoveredConnector() {
      for (const node of this.internalNodes) {
        let connectorPosition = this.getConnectorPosition(node);
        for (let prop in connectorPosition) {
          let entry = connectorPosition[prop];
          if (
            Math.hypot(
              entry.x - this.cursorToChartOffset.x,
              entry.y - this.cursorToChartOffset.y
            ) < 10
          ) {
            return { position: prop, node: node };
          }
        }
      }
      return null;
    },
    hoveredConnection() {
      for (const line of this.lines) {
        let distance = distanceOfPointToLine(
          line.sourceX,
          line.sourceY,
          line.destinationX,
          line.destinationY,
          this.cursorToChartOffset.x,
          this.cursorToChartOffset.y
        );
        if (
          distance < 5 &&
          between(
            line.sourceX - 2,
            line.destinationX + 2,
            this.cursorToChartOffset.x
          ) &&
          between(
            line.sourceY - 2,
            line.destinationY + 2,
            this.cursorToChartOffset.y
          )
        ) {
          let connections = this.internalConnections.filter(
            (item) => item.id === line.id
          );
          return connections.length > 0 ? connections[0] : null;
        }
      }
      return null;
    },
    cursor() {
      if (this.connectingInfo.source || this.hoveredConnector) {
        return "crosshair";
      }
      if (this.hoveredConnection != null) {
        return "pointer";
      }
      return null;
    },
  },
  watch: {

    internalNodes: {
      immediate: true,
      deep: true,
      handler() {
        this.renderNodes();
        this.renderConnections();
      },
    },
    internalConnections: {
      immediate: true,
      deep: true,
      handler() {
        this.renderConnections();
      },
    },
    selectionInfo: {
      immediate: true,
      deep: true,
      handler() {
        this.renderSelection();
      },
    },
    currentNodes: {
      immediate: true,
      deep: true,
      handler() {
        this.renderNodes();
      },
    },
    currentConnections: {
      immediate: true,
      deep: true,
      handler() {
        this.renderConnections();
      },
    },
    cursorToChartOffset: {
      immediate: true,
      deep: true,
      handler() {
        if (this.selectionInfo) {
          this.renderSelection();
        }
      },
    },
    connectingInfo: {
      immediate: true,
      deep: true,
      handler() {
        this.renderConnections();
      },
    },
    nodes: {
      immediate: true,
      deep: true,
      handler() {
        this.init();
      },
    },
    connections: {
      immediate: true,
      deep: true,
      handler() {
        this.init();
      },
    },
  },
};
</script>
<style lang="less" scoped>
.query-btn{
    position: absolute;
    left: 5px;
    bottom: 5px;
    font-size: 0.8rem;
    font-weight: bolder;
    color: #808080;
    line-height: 10px;
  
}
path {
    &.highlighted {
        stroke: red;
    }
}

</style>
