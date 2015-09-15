import normalizr from 'normalizr'
import 'whatwg-fetch'


const Schema = normalizr.Schema
const arrayOf = normalizr.arrayOf

const nodeSchema = new Schema('nodes', { idAttribute: 'key' })

nodeSchema.define({
  children: arrayOf(nodeSchema),
})

export function normalizeData(taxonomyJson) {
  return normalizr.normalize(taxonomyJson, nodeSchema)
}

function buildChild(nodes, id) {
  const node = nodes[id]
  return {
    key: id,
    translations: node.translations,
    children: node.children.map(childId => buildChild(nodes, childId))
  }
}

function buildTree(nodes, rootId) {
  const rootNode = nodes[rootId]
  const children = rootNode.children.map(id => buildChild(nodes, id))
  return {
    key: rootId,
    title: rootNode.title,
    children: children,
    default_language: rootNode.default_language,
    languages: rootNode.languages
  }
}

export function asyncSaveTree(nodes, rootId) {
  const viewUrl = $('base').attr('href') + '/@@taxonomy-import'
  const hashes = window.location.href.slice(
    window.location.href.indexOf('?') + 1).split('&')
  const taxonomyParam = hashes.map(hash => hash.split('=')).find(
    param => param[0] === 'taxonomy')
  const tree = buildTree(nodes, rootId)
  return fetch(viewUrl, {
    credentials: 'include',
    method: 'post',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      tree: tree,
      taxonomy: taxonomyParam[1]
    })
  }).then(response => response.json())
}
