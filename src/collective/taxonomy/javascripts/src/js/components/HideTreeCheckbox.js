import React, { PropTypes } from 'react';
import { FormattedMessage } from 'react-intl';

const HideTreeCheckbox = ({ onChange }) => (
  <div className="field">
    <input
      type="checkbox"
      id="toggle-view-tree"
      name="toggle-view-tree"
      onChange={onChange}
    />
    &nbsp;
    <label htmlFor="toggle-view-tree">
      <FormattedMessage
        id="showViewTree"
        defaultMessage="Show the taxonomy in another language to compare"
      />
    </label>
  </div>
);

HideTreeCheckbox.propTypes = {
  onChange: PropTypes.func.isRequired
};

export default HideTreeCheckbox;
