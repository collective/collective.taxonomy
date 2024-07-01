import React, { Component, PropTypes } from 'react';

import Tree from '../containers/Tree';
import LanguageSelector from '../containers/LanguageSelector';

class TaxonomyTree extends Component {
  static propTypes = {
    duplicatedNode: PropTypes.string.isRequired,
    defaultLanguage: PropTypes.string.isRequired,
    editable: PropTypes.bool
  };

  static defaultProps = {
    editable: true,
    duplicatedNode: ''
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
    const { duplicatedNode } = this.props;
    return (
      <div className="taxonomy-tree">
        <LanguageSelector
          onChange={this.handleSelectLanguage}
          selectedLanguage={this.state.language}
        />
        <Tree
          language={this.state.language}
          editable={editable}
          duplicatedNode={duplicatedNode}
        />
      </div>
    );
  }
}

export default TaxonomyTree;
