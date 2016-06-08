import * as constants from './constants'
import { asyncSaveTree } from './api'

export function addNode(parentId, index, newKey, languages) {
  return { type: constants.ADD_NODE, parentId, index, newKey, languages }
}

export function removeNode(parentId, id, index) {
  return { type: constants.REMOVE_NODE, parentId, id, index }
}

export function editTranslation(id, language, value) {
  return { type: constants.EDIT_TRANSLATION, id, language, value }
}

export function saveTree(nodes, rootId) {
  // post tree to plone view
  return {
    types: [
      constants.SAVE_TREE_PENDING,
      constants.SAVE_TREE_FULFILLED,
      constants.SAVE_TREE_REJECTED
    ],
    payload: {
      data: { nodes, rootId },
      promise: asyncSaveTree(nodes, rootId)
    }
  }
}
