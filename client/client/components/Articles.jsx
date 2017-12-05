import React from 'react';
import Pagination from 'react-js-pagination';

class Article extends React.Component {
  render() {
    return (
      <div className="col-md-6">
        <a href={this.props.url}>
          <div className="card card-inverse">
            <img className="card-img" src={this.props.image} alt="Card image" style={{height:300 + 'px'}}></img>
            <div className="card-img-overlay">
              <h4 className="card-title">{this.props.name}</h4>
              <p className="card-text">{this.props.source}</p>
            </div>
          </div>
        </a>
      </div>);
    }
  }

export default class Articles extends React.Component {
  render() {
    return (
      <div className="row">
        {this.props.articles.map(storyData => <Article key={storyData.link} image={storyData.image} name={storyData.title} url={storyData.link} source={storyData.source} {...storyData} />)}
      </div>
      );
  }
}
