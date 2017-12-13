import React from 'react';
import {Link} from 'react-router-dom';

export default class StoryCard extends React.Component {
  render() {
    return (
      <div className="col-md-6 storyCard">
        <Link to={"/story/" + this.props.id}>
          <div className="card hover-card">
            <div className="card-img-top img-responsive" style={{background: 'url(' + this.props.url +')', backgroundSize: 'cover', backgroundPosition: 'center center', width: '100%', height: '300px', position: 'relative', zIndex: '2'}}>
            <div className="top">
              {this.props.name} <br />
              <span className="card-text num-articles">{this.props.count} article{this.props.count > 1 && "s"}</span>
            </div>
            </div>
          </div>
        </Link>
      </div>);
    }
  }
