

const highlight_2nodes_str = 'current two highlighted nodes';
const highlight_2nodes_str_1 = 'current two highlighted leaf nodes';
const highlight_1node_str = 'current highlighted node';

let highlight_2leaves=false;

const width = 550;
const height = 400;

function highLight2Nodes(){
    let node_i = Math.random()
    let node_j = Math.random()
    let sendInfo = {}
    sendInfo[node_i]=node_i
    sendInfo[node_j]=node_j
    return sendInfo
}

function highLight1Nodes(){
    let node_i = Math.random()
    let sendInfo = {}
    sendInfo[node_i]=node_i
    return sendInfo
}
export default{
    highlight_2nodes_str,
    highlight_2nodes_str_1,
    highlight_1node_str,
    width,
    height,
    highLight2Nodes,
    highLight1Nodes,
    highlight_2leaves,
}