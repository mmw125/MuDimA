import React from 'react';

export default class Story extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: true
    }
  }
  getSources() {
    console.log(this.props.match.params.id);
    return fetch('http://localhost/getStories?topic_id=' + this.props.match.params.id)
      .then((response) => response.json())
      .then((responseJson) => {
        console.log(responseJson);
        this.setState({
          isLoading: false,
          source: responseJson.articles,
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
          <h1>{this.state.title}</h1>
        <ul>
        {this.state.source.map(storyData => <li><a href={storyData[1]}>{storyData[0]}</a></li>)}
        </ul>
      </div>

      );
  }
}
