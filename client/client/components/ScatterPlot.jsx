// unfinished/src/components/scatter-plot.jsx
import React        from 'react';

// Returns the largest X coordinate from the data set
const xMax   = (data)  => d3.max(data, (d) => d[0]);

// Returns the highest Y coordinate from the data set
const yMax   = (data)  => d3.max(data, (d) => d[1]);

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
      name: e.target.getAttribute('name'),
      link: e.target.getAttribute('link'),
      x: e.target.getAttribute('cx'),
      y: e.target.getAttribute('cy')
    }
    d3.select(e.target).attr({fill: "orange"});

    d3.select(this.refs.scatterPlot).append("text").attr({
               id: "t" + "hi",  // Create an id for text so we can select it later for removing on mouseout
                x: function() { return d.x - 30; },
                y: function() { return d.y - 15; }
            })
            .text(function() {
              return [d.name, d.link];  // Value of the text
            });
  }
  handleMouseOut(e) {
    const d = {
      x: e.target.getAttribute('cx'),
      y: e.target.getAttribute('cy')
    }
    d3.select(e.target).attr({fill: "black"});
    d3.select("#t" + "hi").remove();
  }
  handleMouseClick(e) {
    window.open(e.target.getAttribute('href'), '_blank');
  }
  xScale() {
    return d3.scale.pow()
      .domain([-1, 1])
      .range([this.props.padding, this.props.width - this.props.padding])
      .exponent(2);
  };
  yScale() {
    return d3.scale.pow()
      .domain([-1, 1])
      .range([this.props.height - this.props.padding, this.props.padding])
      .exponent(2);
  };
  renderCircles() {
    return (story, index) => {
      const coords = [story['x'], story['y']]
      console.log(coords);
      console.log(index);
      const circleProps = {
        href: story['link'],
        name: story['name'],
        cx: this.xScale()(coords[0]),
        cy: this.yScale()(coords[1]),
        r: 10,
        key: index
      };
      return <circle href={circleProps.link} onMouseOut={this.handleMouseOut.bind(this)} onMouseOver={this.handleMouseHover.bind(this)} onClick={this.handleMouseClick.bind(this)} {...circleProps} />;
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
