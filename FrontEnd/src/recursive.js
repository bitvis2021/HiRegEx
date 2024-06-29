
function recursive1(data, str_to_value='value'){
    let ans = {};
    ans['name'] = data.name
    if(data.children && data.children.length){
      ans['children'] = [];
      for(let index = 0; index < data.children.length; index++){
        let element = data.children[index];
        let ans1 = recursive1(element,str_to_value);
        ans["children"].push(ans1);
      }
    }
    else{
      if(data[str_to_value])
      {
        ans["value"] = parseInt(data[str_to_value]);
      }
      else{
        ans["value"] = 5;
      }
    }
    return ans;
}

function recursive(data, str_to_value='value'){
  let tmp = recursive1(eval(data), str_to_value);
  let root = function(data){
    let i = 0;
    return d3.hierarchy(data).eachBefore(d=>{d.index = i++; d.data.name = d.data.name + d.index;});
  }; 
  root(tmp);
  return tmp
}

export default{
    install: function(Vue){
      Vue.prototype.recursive = (param1,param2) =>recursive(param1,param2)
    }
}