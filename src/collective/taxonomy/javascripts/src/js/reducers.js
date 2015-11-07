/* eslint no-unused-vars:[2, {"args": "none"}] */
import update from 'react-addons-update'

import {
  ADD_NODE,
  REMOVE_NODE,
  EDIT_TRANSLATION,
  SAVE_TREE_PENDING,
  SAVE_TREE_FULFILLED,
  SAVE_TREE_REJECTED } from './actions'


function addNode(nodes, parentId, newKey, nodeLanguages) {
  let emptyTranslations = {}  // eslint-disable-line prefer-const
  nodeLanguages.forEach(value => emptyTranslations[value] = '??????')
  const newNodes = update(
    nodes, {
      // add new item to nodes
      $merge: { [newKey]: {
        key: newKey,
        subnodes: [],
        translations: emptyTranslations,
      } },

      [parentId]: { subnodes: { $push: [newKey] } }
    })

  return newNodes
}

function removeNode(nodes, action) {
  // remove item from parents' subnodes
  const newNodes = update(
    nodes, {
      [action.parentId]: { subnodes: { $splice: [[action.index, 1]] } },
    })

  // remove from nodes
  delete newNodes[action.id]

  // action.parentId
  return newNodes
}

export function tree(state = { nodes: {}, dirty: false }, action) {
  switch (action.type) {
  case ADD_NODE:
    return {
      dirty: true,
      nodes: addNode(state.nodes, action.parentId, action.newKey, action.languages)
    }
  case REMOVE_NODE:
    return {
      dirty: true,
      nodes: removeNode(state.nodes, action)
    }
  case EDIT_TRANSLATION:
    const language = action.language
    return {
      dirty: true,
      nodes: update(
        state.nodes, {
          [action.id]: { translations: { [language]: { $set: action.value } } },
        })
    }
  case SAVE_TREE_FULFILLED:
    return {
      dirty: false,
      nodes: state.nodes
    }
  default:
    return state
  }
}

export function rootId(state = 'root', action) {
  return state
}

export function defaultLanguage(state = 'en', action) {
  return state
}

export function languages(state = ['en'], action) {
  return state
}

const defaultState = { isPending: false, status: '', message: '' }

export function saveTree(state = defaultState, action) {
  switch (action.type) {
  case SAVE_TREE_PENDING:
    return {
      isPending: true,
      status: '',
      message: ''
    }
  case SAVE_TREE_FULFILLED:
    return {
      isPending: false,
      status: action.payload.status,
      message: action.payload.message
    }
  case SAVE_TREE_REJECTED:
    return state
  default:
    return state
  }
}
