// unfinished/src/components/data-circles.jsx
import React from 'react';

export default class DataCircles extends React.Component {
  constructor(props) {
    super(props);
  }
  handleMouseHover(e) {
    d3.select(e.target).attr({fill: "orange"});
  }
  handleMouseOut(e) {
    d3.select(e.target).attr({fill: "black"});
  }
  renderCircles() {
    return (coords, index) => {
      console.log(coords);
      console.log(index);
      const circleProps = {
        cx: coords[0],
        cy: coords[1],
        r: 10,
        key: index
      };
      return <circle onMouseOut={this.handleMouseOut.bind(this)} onMouseOver={this.handleMouseHover.bind(this)} {...circleProps} />;
    };
  }
  render() {
      return (
        <g>{ this.props.data.map(this.renderCircles(this.props)) }</g>
      );
    }
}
