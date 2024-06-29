export async function loadHierarchicalData (fileName, callBackFunc) {
    //  load the hierarchical data
    console.log('fileName', fileName)
    var path = require("path")
    var fs = require("fs")
    var data =  await d3.json(fileName)
                        .then (function(data){
                            callBackFunc(data)
                        })
    return data
}