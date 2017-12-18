import React from 'react';
import ScatterPlot from './ScatterPlot.jsx';
import stories from '../data/mock-stories.js'
import fuzzySearch from 'fuzzysearch'

const styles = {
  text_center: {
    textAlign: 'center'
  },
  center_div: {
    margin: 'auto'
  }
};

const xScale = () => {
    return d3.scale.pow()
        .domain([-1, 1])
        .range([20, 1200-20])
        
};

const yScale = () => {
    return d3.scale.pow()
        .domain([-1, 1])
        .range([1000 - 20, 20])
        
};

export default class Story extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      isLoading: true
    }
  }
  getTranformedData(data) {
    return data.map((article) => {
      const {x, y} = article;
      return {
        cx: xScale()(x),
        cy: yScale()(y),
        r: 4,
        payload: article
      }
    });
  }
  getSources() {
    return fetch('http://localhost/getStories?topic_id=' + this.props.match.params.id)
      .then((response) => response.json())
      .then((responseJson) => {
        this.setState({
          isLoading: false,
          data: responseJson.articles,
          searched_data: responseJson.articles,
          title: responseJson.title
        })
      })
      .catch((error) => { console.error(error); });
  }
  componentWillMount() {
    this.getSources();
  }
  onSearchChange(e) {
    const searched_phrase = (e.target.value || "").toLowerCase();
    const searched_data = this.state.data.filter((article) => {
      return (
        article['name'].toLowerCase().includes(searched_phrase)
        || article['source'].toLowerCase().includes(searched_phrase)
      )
    });
    this.setState({
      searched_data: searched_data
    });
  }
  getSearchTitlesField() {
    return (
      <div className="col-sm-8 col-lg-6" style={styles.center_div}>
        <label htmlFor="inputPassword5">Search News by Title, Source</label>
        <input type="text" className="form-control" onChange={this.onSearchChange.bind(this)} placeholder="eg. attack, The New York Times"/>
      </div>
    )
  }
  render() {
    if (this.state.isLoading) {
      return (
        <h1></h1>
      );
    }
    return (
      <div className="row" style={styles.text_center}>
        <h1 className="storyTitle">{this.state.title}</h1>
        {this.getSearchTitlesField()}
        <ScatterPlot data={this.state.searched_data}/>
      </div>
    );
  }
  // <ul>
  // {this.state.source.map(storyData => <li><a href={storyData[1]}>{storyData[0]}</a></li>)}
  // </ul>
}
