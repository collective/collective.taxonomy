import React, { Component, PropTypes } from 'react';

import Tree from '../containers/Tree';
import LanguageSelector from '../containers/LanguageSelector';

class TaxonomyTree extends Component {
  static propTypes = {
    defaultLanguage: PropTypes.string.isRequired,
    editable: PropTypes.bool
  };

  static defaultProps = {
    editable: true
  };

  constructor({ defaultLanguage }) {
    super();
    this.state = {
      hidden: false,
      language: defaultLanguage
    };
    this.handleSelectLanguage = this.handleSelectLanguage.bind(this);
  }

  handleSelectLanguage(e) {
    this.setState({
      language: e.target.value
    });
  }

  render() {
    const { editable } = this.props;
    return (
      <div className="taxonomy-tree">
        <LanguageSelector
          onChange={this.handleSelectLanguage}
          selectedLanguage={this.state.language}
        />
        <Tree language={this.state.language} editable={editable} />
      </div>
    );
  }
}

export default TaxonomyTree;
