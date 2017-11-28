import React from 'react';
import ScatterPlot from './ScatterPlot.jsx';
import stories from '../data/mock-stories.js'
import ScatterPlotR from './ScatterPlotRecharts.jsx';
const styles = {
  width   : 1080,
  height  : 1000,
  padding : 30,
};

// The number of data points for the chart.
const numDataPoints = 50;

// A function that returns a random number from 0 to 1000
const randomNum     = () => Math.floor(Math.random() * 1000);

// A function that creates an array of 50 elements of (x, y) coordinates.
const randomDataSet = () => {
  return Array.apply(null, {length: numDataPoints}).map(() => [randomNum(), randomNum()]);
}

export default class Story extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      isLoading: true
    }
  }

  getSources() {
    return fetch('http://localhost/getStories?topic_id=' + this.props.match.params.id)
      .then((response) => response.json())
      .then((responseJson) => {
        this.setState({
          isLoading: false,
          source: responseJson.articles,
          data: responseJson.articles,
          title: responseJson.title
        })})
      .catch((error) => { console.error(error); });
  }
  componentWillMount() {
    this.getSources();
  }
  render() {
    if (this.state.isLoading) {
      return (
        <h1></h1>
      );
    }
    return (
      <div className="row">
        <h1 style={{marginTop: '1em'}}>{this.state.title}</h1>
        <ScatterPlotR data={this.state.data}/>
      </div>
    );
  }
  // <ul>
  // {this.state.source.map(storyData => <li><a href={storyData[1]}>{storyData[0]}</a></li>)}
  // </ul>
}
