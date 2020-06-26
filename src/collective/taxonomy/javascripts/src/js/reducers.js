/* eslint no-unused-vars:[2, {"args": "none"}] */
import update from 'react-addons-update';
import { combineReducers } from 'redux';

import {
  ADD_NODE,
  REMOVE_NODE,
  MOVE_DOWN,
  MOVE_UP,
  EDIT_TRANSLATION,
  SAVE_TREE_PENDING,
  SAVE_TREE_FULFILLED,
  SAVE_TREE_REJECTED,
  SELECT_LANGUAGE
} from './constants';

function addNode(nodes, parentId, newKey) {
  const newNodes = update(nodes, {
    // add new item to nodes
    $merge: {
      [newKey]: {
        key: newKey,
        subnodes: [],
        translations: {}
      }
    },

    [parentId]: { subnodes: { $push: [newKey] } }
  });

  return newNodes;
}

function removeNode(nodes, action) {
  // remove item from parents' subnodes
  const newNodes = update(nodes, {
    [action.parentId]: { subnodes: { $splice: [[action.index, 1]] } }
  });

  // remove from nodes
  delete newNodes[action.id];

  // action.parentId
  return newNodes;
}

function moveDown(nodes, action) {
  const swapped = nodes[action.parentId].subnodes
    .slice(action.index, action.index + 2)
    .reverse();

  return update(nodes, {
    [action.parentId]: {
      subnodes: { $splice: [[].concat([action.index, 2], swapped)] }
    }
  });
}

function moveUp(nodes, action) {
  if (action.index == 0) return nodes;
  const swapped = nodes[action.parentId].subnodes
    .slice(action.index - 1, action.index + 1)
    .reverse();

  return update(nodes, {
    [action.parentId]: {
      subnodes: { $splice: [[].concat([action.index - 1, 2], swapped)] }
    }
  });
}

export function tree(state = { nodes: {}, dirty: false }, action) {
  switch (action.type) {
    case ADD_NODE:
      return {
        dirty: true,
        nodes: addNode(state.nodes, action.parentId, action.newKey)
      };
    case REMOVE_NODE:
      return {
        dirty: true,
        nodes: removeNode(state.nodes, action)
      };
    case MOVE_DOWN:
      return {
        dirty: true,
        nodes: moveDown(state.nodes, action)
      };
    case MOVE_UP:
      return {
        dirty: true,
        nodes: moveUp(state.nodes, action)
      };
    case EDIT_TRANSLATION: {
      const language = action.language;
      return {
        dirty: true,
        nodes: update(state.nodes, {
          [action.id]: { translations: { [language]: { $set: action.value } } }
        })
      };
    }
    case SAVE_TREE_FULFILLED:
      return {
        ...state,
        dirty: false
      };
    default:
      return state;
  }
}

export function rootId(state = 'root', action) {
  return state;
}

export function defaultLanguage(state = 'en', action) {
  return state;
}

export function selectedLanguage(state = 'en', action) {
  switch (action.type) {
    case SELECT_LANGUAGE:
      return action.value;
    default:
      return state;
  }
}

export function languages(state = { en: 'English' }, action) {
  return state;
}

const defaultState = { isPending: false, status: '', message: '' };

export function saveTree(state = defaultState, action) {
  switch (action.type) {
    case SAVE_TREE_PENDING:
      return {
        isPending: true,
        status: '',
        message: ''
      };
    case SAVE_TREE_FULFILLED:
      return {
        isPending: false,
        status: action.payload.status,
        message: action.payload.message
      };
    case SAVE_TREE_REJECTED:
      return state;
    default:
      return state;
  }
}

export default combineReducers({
  defaultLanguage,
  languages,
  rootId,
  saveTree,
  selectedLanguage,
  tree
});
