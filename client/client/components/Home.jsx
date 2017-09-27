import React from 'react';
import StoryCard from './StoryCard.jsx'
import stories from '../data/mock-stories.js'

export default class Home extends React.Component {
  render() {
    return (
      <div className="row">
        <div className="col-md-12">
          {stories.map(storyData => <StoryCard name={storyData.name} {...storyData} />)}
        </div>
      </div>
      );
  }
}
