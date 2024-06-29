import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  	displayMode: 'vis',
    selectedDom: {
      repeat:[1 ,1]
    },
    selectedDomKey: -1,
    reTreeDataState: 0,
    nodeDefinitionState: 0,
    nodeDefinitionState2: 0,
    selectedListNode: null,
    regexCommitState: 0,
    selectedRepeatDom: null,
    selectedRepeatDomState: 0,
    lastDom: null,
    regexList: [],
    regexListState: 0,
    attributeList: {'depth':'number', 'height': 'number','degree':'number'},
    selectedPartState: 0,
    regexViewState: false,
    visViewState: 0,
    curRegexIndex: 0,
    reViewDataState: 0, 
    treeViewState: 0,
    nodeListState: 0,
    connectionState: 0,
    curConnectionNode: null,
    regexContentState: 0,

    visTreeDataState: 0,
    queryType: 0,
    queryStateIndex: 0,
    queryIndex: 0,
    queryStateRegex: 0,
    queryPage: 0,
    queryStatePage: 0,
    queryCoding: '',
    queryStateCoding: 0,

    overviewPanelState: 0,
    visPanelState: 0,
    treeListState: 0,
    regPanelState: 0,
    conditionState: true,
    repeatState: false,

  },
  mutations: {
    ['UPDATE_DISPLAY_MODE'] (state, displayMode) {
      state.displayMode = displayMode
    },
    ['UPDATE_SELECTED_DOM'] (state, selectedDom) {
      //console.log('================UPDATE_SELECTED_DOM================', selectedDom['type'], selectedDom['parent']['type'])
      
      state.selectedDom = selectedDom
      if ((selectedDom != null) && (typeof(selectedDom.key) !== 'undefined')) {
        state.selectedDomKey = selectedDom.key
      }
    },
    ['GET_SELECTEDKEY'](state){
      return state.selectedDomKey
    },
    ['UPDATE_RETREE_DATA_STATE'] (state) {
      console.log('UPDATE_RETREE_DATA_STATE')
      state.reTreeDataState = (state.reTreeDataState + 1) % 2
    },
    ['UPDATE_NODE_DEFINITION_STATE'] (state){
      state.nodeDefinitionState = (state.nodeDefinitionState + 1) % 2
    },
    ['UPDATE_SELECTED_LIST_DOM'] (state, selectedNode){
      state.selectedListNode = selectedNode
    },
    ['UPDATE_NODE_DEFINITION_STATE2'] (state){
      state.nodeDefinitionState2 = (state.nodeDefinitionState2 + 1)%2
    },
    ['UPDATE_REGEX_COMMIT_STATE'] (state){
      state.regexCommitState = (state.regexCommitState + 1) % 2
    },
    ['RESET_DOM_KEY_STATE'] (state){
      state.selectedDomKey = -1
      state.selectedDom = null
    },
    ['UPDATE_REPEAT_DOM'](state, curRepeatDom) {
      state.selectedRepeatDom = curRepeatDom
      state.selectedRepeatDomState = (state.selectedRepeatDomState + 1) % 2
    },
    ['UPDATE_LAST_DOM'](state, lastDom){
      state.lastDom = lastDom
    },
    ['ADD_REGEX_LIST'](state, regex){
      if(!('regexIndex' in regex)){
        regex['regexIndex'] = state.regexList.length
        state.regexList.push(regex)
      }
      state.regexListState = (state.regexListState + 1) % 2
    },
    ['UPDATE_CURRENT_REGEX'](state, regexIndex){
      state.curRegexIndex = regexIndex
    },
    ['DELETE_REGEX_LIST'](state, regex){
      state.regexList.splice(regex['regexIndex'],1)
    },
    ['UPDATE_ATTRIBUTE_LIST_NUMBER'](state, key){
      state.attributeList[key] = 'number'
    },
    ['UPDATE_ATTRIBUTE_LIST_STRING'](state, key){
      state.attributeList[key] = 'string'
    },
    ['UPDATE_ATTRIBUTE_LIST_BOOLEAN'](state, key){
      state.attributeList[key] = 'boolean'
    },
    ['UPDATE_SELECTED_PART'](state){
      state.selectedPartState = (state.selectedPartState + 1) % 2
    },
    ['UPDATE_HOVERING_ID'] (state, hoveringId) {
      state.hoveringId = hoveringId
    },
    ['SHOW_REVIEW'] (state){
      state.regexViewState = true
    },
    ['UN_SHOW_REVIEW'] (state){
      state.regexViewState = false
    },
    ['UPDATE_VISVIEW'] (state){
      state.visViewState = (state.visViewState + 1) % 2
    },
    ['UPDATE_REVIEW_DATA'] (state){
      state.reViewDataState = (state.reViewDataState+1)%2
    },
    ['UPDATE_TREEVIEW'] (state){
      state.treeViewState = (state.treeViewState + 1)%2
    },
    ['UPDATE_NODE_LIST'] (state){
      state.nodeListState = (state.nodeListState + 1)%2
    },
    ['UPDATE_CONNECTION'] (state, index){
      state.curConnectionNode = index
      state.connectionState = (state.connectionState + 1)%2
    },
    ['UPDATE_REGEX_CONTENT'](state){
      state.regexContentState = (state.regexContentState + 1)%2
    },

    ['UPDATE_VIS_TREE'](state){
      state.visTreeDataState = (state.visTreeDataState + 1)%2
    },
    ['DATA_QUERY_INDEX'](state, index){
      state.queryIndex = index
      state.queryStateIndex = (state.queryStateIndex + 1)%2
    },
    ['DATA_QUERY_REGEX'](state){
      state.queryStateRegex = (state.queryStateRegex + 1)%2
    },
    ['DATA_QUERY_PAGE'](state, index){
      state.queryPage = index
      state.queryStatePage = (state.queryStatePage + 1)%2
    },
    ['DATA_QUERY_CODING'](state, reg_coding){
      state.queryCoding = reg_coding
      state.queryStateCoding = (state.queryStateCoding + 1) % 2
    },
    
    ['UPDATE_VIS_PANEL'](state){
      state.visPanelState = (state.visPanelState + 1)%2
    },
    ['UPDATE_TREE_LIST'](state){
      state.treeListState = (state.treeListState + 1)%2
    },
    ['UPDATE_REG_PANEL'](state){
      state.regPanelState = (state.regPanelState + 1)%2
    },
    ['UPDATE_CONDITION_STATE'](state, flag){
      state.conditionState = flag
    },
    ['UPDATE_REPEAT_STATE'](state, flag){
      state.repeatState = flag
    }


  },
  actions: {

  }
})
