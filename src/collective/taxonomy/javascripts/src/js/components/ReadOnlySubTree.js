import React, { PropTypes } from 'react';
import TreeView from 'react-treeview';
import { FormattedMessage } from 'react-intl';

import ReadOnlySubTreeContainer from '../containers/ReadOnlySubTree';

const ReadOnlySubTree = ({ language, subnodes, title }) => {
  const nodeLabel = title || (
    <FormattedMessage id="untranslated" defaultMessage="(Untranslated)" />
  );

  if (subnodes.length > 0) {
    return (
      <TreeView nodeLabel={nodeLabel}>
        {subnodes.map(childId => (
          <ReadOnlySubTreeContainer
            key={childId}
            id={childId}
            language={language}
          />
        ))}
      </TreeView>
    );
  }

  return <div className="info ro-node">{nodeLabel}</div>;
};

ReadOnlySubTree.propTypes = {
  language: PropTypes.string.isRequired,
  subnodes: PropTypes.array.isRequired,
  title: PropTypes.string
};

ReadOnlySubTree.defaultProps = {
  title: ''
};

export default ReadOnlySubTree;
