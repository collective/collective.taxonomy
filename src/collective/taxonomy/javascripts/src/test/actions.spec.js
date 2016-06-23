import * as actions from '../js/actions'
import * as constants from '../js/constants'

describe('Action creators', () => {
  describe('addNode action creator', () => {
    it('should create an action to add a node', () => {
      const { addNode } = actions
      const actual = addNode('foo', 1, 'xyz')
      const expected = {
        type: constants.ADD_NODE,
        parentId: 'foo',
        index: 1,
        newKey: 'xyz',
      }
      expect(actual).to.eql(expected)
    })
  })

  describe('removeNode action creator', () => {
    const { removeNode } = actions
    it('should create an action to remove a node', () => {
      const actual = removeNode('foo', 'bar', 42)
      const expected = {
        type: constants.REMOVE_NODE,
        parentId: 'foo',
        id: 'bar',
        index: 42,
      }
      expect(actual).to.eql(expected)
    })
  })

  describe('editTranslation action creator', () => {
    const { editTranslation } = actions
    it('should create an action to edit a translation', () => {
      const actual = editTranslation('foo', 'fr', 'Lorem ipsum')
      const expected = {
        type: constants.EDIT_TRANSLATION,
        id: 'foo',
        language: 'fr',
        value: 'Lorem ipsum'
      }
      expect(actual).to.eql(expected)
    })
  })
})
