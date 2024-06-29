import * as d3 from 'd3';
import {roundTo20} from '../../utils/math';

function render(g, node, isSelected, excludeShownAttrArray) {
  node.width = node.width || 120;
  node.height = node.height || 60;
  let borderWidth = isSelected ? '2.5px' : '1px';
  let textList = []

    let body = g.append('rect')
      .attr('class', function(d, i) {
        let classList = ['body', 'node-body']
        if (isSelected) {
          classList.push('selected')
        }
        return classList.join(' ')
      })
      .attr('x', node.x)
      .attr('y', node.y)

      .attr('width', node.width + 'px')
      .attr('height', node.height + 'px')


  let bodyTextY;
  let bodyTextX;
 
  bodyTextY = node.y + 25 + roundTo20(node.height - 20) / 2;

  
}

export default render;