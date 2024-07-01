import * as constants from '../js/constants';
import * as reducers from '../js/reducers';

describe('Reducers', () => {
  describe('Tree reducer', () => {
    const { tree } = reducers;
    const initialState = {
      dirty: false,
      nodes: {
        foo: {
          key: 'foo',
          subnodes: ['bar'],
          translations: { en: 'Foo', fr: 'Toto' }
        },
        bar: {
          key: 'bar',
          subnodes: [],
          translations: { en: 'Bar', fr: 'Titi' }
        }
      }
    };
    it('should handle ADD_NODE action type', () => {
      const action = {
        type: constants.ADD_NODE,
        parentId: 'foo',
        index: 1,
        newKey: 'xyz'
      };
      const actual = tree(initialState, action);
      const expected = {
        dirty: true,
        nodes: {
          foo: {
            key: 'foo',
            subnodes: ['bar', 'xyz'],
            translations: { en: 'Foo', fr: 'Toto' }
          },
          bar: {
            key: 'bar',
            subnodes: [],
            translations: { en: 'Bar', fr: 'Titi' }
          },
          xyz: { key: 'xyz', subnodes: [], translations: {} }
        }
      };
      expect(actual).to.eql(expected);
    });

    it('should handle REMOVE_NODE action type', () => {
      const action = {
        type: constants.REMOVE_NODE,
        parentId: 'foo',
        id: 'bar',
        index: 42
      };
      const actual = tree(initialState, action);
      const expected = {
        dirty: true,
        nodes: {
          foo: {
            key: 'foo',
            subnodes: ['bar'], // TODO: FIXME?
            translations: { en: 'Foo', fr: 'Toto' }
          }
        }
      };
      expect(actual).to.eql(expected);
    });
  });
});
