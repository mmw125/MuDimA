// unfinished/src/components/scatter-plot.jsx
import React        from 'react';
import DataCircles  from './DataCircles.jsx';


export default class ScatterPlot extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      scales : {
        xScale: this.props.data[0],
        yScale: this.props.data[1]
      }
    }

  }
  handleMouseHover(e) {
    const d = {
      x: e.target.getAttribute('cx'),
      y: e.target.getAttribute('cy')
    }
    d3.select(e.target).attr({fill: "orange"});

    d3.select(this.refs.scatterPlot).append("text").attr({
               id: "t" + d.x + "-" + d.y,  // Create an id for text so we can select it later for removing on mouseout
                x: function() { return d.x - 30; },
                y: function() { return d.y - 15; }
            })
            .text(function() {
              return [d.x, d.y];  // Value of the text
            });
  }
  handleMouseOut(e) {
    const d = {
      x: e.target.getAttribute('cx'),
      y: e.target.getAttribute('cy')
    }
    d3.select(e.target).attr({fill: "black"});
    d3.select("#t" + d.x + "-" + d.y).remove();
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
      <svg ref="scatterPlot" width={this.props.width} height={this.props.height}>
        <g>{ this.props.data.map(this.renderCircles(this.props)) }</g>
      </svg>
    );
  }
}
