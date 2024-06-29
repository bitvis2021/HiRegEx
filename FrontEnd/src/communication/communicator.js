import axios from 'axios'
import { simpleStringify } from '@/utils/stringify.js'

let server_address = 'http://127.0.0.1:14449'

export function getHierarchyData(hierarchicalParam, getHierarchyDataCallback) {
    console.log('hierarchicalParam', hierarchicalParam)
    let formData = {"hierarchicalParam": JSON.parse(simpleStringify(hierarchicalParam))}
    axios({
        method: 'post',
        url: server_address + '/hierarchydata',
        data: formData
    })
    .then((res) => {
        let hierarchyData = res['data']
        getHierarchyDataCallback(hierarchyData)
    })
}