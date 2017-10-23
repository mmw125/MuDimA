// unfinished/src/components/scatter-plot.jsx
import React        from 'react';
import d3           from 'd3';
import d3Scale      from 'd3-scale'
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
    d3.select(e.target).attr({fill: "orange"});
  }
  handleMouseOut(e) {
    d3.select(e.target).attr({fill: "black"});
  }
  render() {
  return (
      <svg width={this.props.width} height={this.props.height}>
        <DataCircles {...this.props} {...this.state.scales} />
      </svg>
    );
  }
}
