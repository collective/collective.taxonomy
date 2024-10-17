import * as constants from './constants';
import { asyncSaveTree } from './api';

export function addNode(parentId, index, newKey) {
  return { type: constants.ADD_NODE, parentId, index, newKey };
}

export function removeNode(parentId, id, index) {
  return { type: constants.REMOVE_NODE, parentId, id, index };
}

export function moveDown(parentId, id, index) {
  return { type: constants.MOVE_DOWN, parentId, id, index };
}

export function moveUp(parentId, id, index) {
  return { type: constants.MOVE_UP, parentId, id, index };
}

export function editTranslation(id, language, value) {
  return { type: constants.EDIT_TRANSLATION, id, language, value };
}

export function editIdentifier(id, index, parentId, language, value) {
  return {
    type: constants.EDIT_IDENTIFIER,
    id,
    index,
    parentId,
    language,
    value
  };
}

export function saveTreeWithData(nodes, rootId, languages) {
  // post tree to plone view
  return {
    type: constants.SAVE_TREE,
    payload: asyncSaveTree(nodes, rootId, languages)
  };
}

export function saveTree() {
  return (dispatch, getState) => {
    const { languages, rootId, tree } = getState();
    const languagesKeys = Object.keys(languages);
    dispatch(saveTreeWithData(tree.nodes, rootId, languagesKeys));
  };
}

export function selectLanguage(value) {
  return {
    type: constants.SELECT_LANGUAGE,
    value
  };
}
