import React from 'react';
import StoryCard from './StoryCard.jsx'
import stories from '../data/mock-stories.js'

export default class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: true
    }
  }
  getTopics() {
    return fetch('http://localhost/getTopics')
      .then((response) => response.json())
      .then((responseJson) => {
        this.setState({
          isLoading: false,
          topics: responseJson
        })})
      .catch((error) => { console.error(error); });
  }
  componentWillMount() {
    this.getTopics();
  }
  render() {
    if (this.state.isLoading) {
      return (
        <h1>Temp</h1>
      );
    }
    return (
      <div className="row">
        <div className="col-md-12">
          {this.state.topics.map(storyData => <StoryCard url={storyData.image} name={storyData.title} id={storyData.id} count={storyData.count} {...storyData} />)}
        </div>
      </div>
      );
  }
}
