import React from 'react';
import {Link} from 'react-router-dom';

export default class StoryCard extends React.Component {
  render() {
    return (
      <div className="col-md-6">
        <Link to={"/story/" + this.props.id}>
          <div className="card card-inverse">
            <img className="card-img" src={this.props.url} alt="Card image" style={{height:300 + 'px'}}></img>
            <div className="card-img-overlay">
              <h4 className="card-title">{this.props.name}</h4>
              <p className="card-text">{this.props.count} article{this.props.count > 1 && "s"}</p>
            </div>
          </div>
        </Link>
      </div>);
    }
  }
