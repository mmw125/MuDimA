import React from 'react';

export default class StoryCard extends React.Component {
  render() {
    return (
      <a href="/#/story/122">
      <div className="card card-inverse">
        <img className="card-img" src="http://www.cooperindustries.com/content/dam/public/safety/notification/products/Mass%20Notification%20Systems/Spotlight/MNS_WideArea_Spotlight3.jpg" alt="Card image"></img>
        <div className="card-img-overlay">
          <h4 className="card-title">{this.props.name}</h4>
        </div>
      </div>
    </a>);
    }
  }
