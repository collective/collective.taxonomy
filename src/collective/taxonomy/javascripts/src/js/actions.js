import { asyncSaveTree } from './api'

/*
 * action types
 */

export const ADD_NODE = 'ADD_NODE'
export const REMOVE_NODE = 'REMOVE_NODE'
export const EDIT_TRANSLATION = 'EDIT_TRANSLATION'
export const SAVE_TREE_PENDING = 'SAVE_TREE_PENDING'
export const SAVE_TREE_FULFILLED = 'SAVE_TREE_FULFILLED'
export const SAVE_TREE_REJECTED = 'SAVE_TREE_REJECTED'

/*
 * action creators
 */

export function addNode(parentId, index, newKey, languages) {
  return { type: ADD_NODE, parentId, index, newKey, languages }
}

export function removeNode(parentId, id, index) {
  return { type: REMOVE_NODE, parentId, id, index }
}

export function editTranslation(id, language, value) {
  return { type: EDIT_TRANSLATION, id, language, value }
}

export function saveTree(nodes, rootId) {
  // post tree to plone view
  return {
    types: [
      SAVE_TREE_PENDING,
      SAVE_TREE_FULFILLED,
      SAVE_TREE_REJECTED
    ],
    payload: {
      data: { nodes: nodes, rootId: rootId },
      promise: asyncSaveTree(nodes, rootId)
    }
  }
}
