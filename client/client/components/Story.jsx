import React from 'react';

export default class Story extends React.Component {
  render() {
    return (
      <div className="row">
        <h1>Put information here about story {this.props.match.params.id}</h1>
      </div>

      );
  }
}
