import chai from 'chai';
// import chaiImmutable from 'chai-immutable'
import equalJSX from 'chai-equal-jsx';
// import spies from 'chai-spies'

// chai.use(chaiImmutable)
chai.use(equalJSX);
// chai.use(spies)

global.__DEV__ = true; /* eslint no-underscore-dangle: 0 */
global.expect = chai.expect;
// global.spy = chai.spy
