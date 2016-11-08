import { arrayOf, normalize, Schema } from 'normalizr'
import 'whatwg-fetch'

const nodeSchema = new Schema('nodes', { idAttribute: 'key' })

nodeSchema.define({
  subnodes: arrayOf(nodeSchema),
})

export function normalizeData(taxonomyJson) {
  return normalize(taxonomyJson, nodeSchema)
}

function buildChild(nodes, id) {
  const node = nodes[id]
  return {
    key: id,
    translations: node.translations,
    subnodes: node.subnodes.map(childId => buildChild(nodes, childId))
  }
}

function buildTree(nodes, rootId) {
  const rootNode = nodes[rootId]
  const subnodes = rootNode.subnodes.map(id => buildChild(nodes, id))
  return {
    key: rootId,
    title: rootNode.title,
    subnodes,
    default_language: rootNode.default_language,
    languages: rootNode.languages
  }
}

export function asyncSaveTree(nodes, rootId, languages) {
  const baseUrl = $('base').attr('href')
  const viewUrl = `${baseUrl}/@@taxonomy-import`
  const hashes = window.location.href.slice(
    window.location.href.indexOf('?') + 1).split('&')
  const taxonomyParam = hashes.map(hash => hash.split('=')).find(
    param => param[0] === 'taxonomy')
  const tree = buildTree(nodes, rootId)
  return fetch(viewUrl, {
    credentials: 'include',
    method: 'post',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      languages,
      tree,
      taxonomy: taxonomyParam[1]
    })
  }).then(response => response.json())
}
