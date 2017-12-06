import React from 'react';
import Pagination from 'react-js-pagination';

class Article extends React.Component {
    render() {
        return (
            <div className="row vertical-align">
                <div className="col-md-4">
                    <a href={this.props.url}>
                        <div className="card card-inverse">
                            <img className="card-img" src={this.props.image} alt="Card image"
                                 style={{height: 200 + 'px'}}></img>
                        </div>
                    </a>
                </div>
                <div className="col-sm-8">
                    <h4>{this.props.name}</h4>
                    <h6>{this.props.source}</h6>
                </div>

            </div>
        );
    }
}

export default class Articles extends React.Component {
    render() {
        return (
            <div className="row">
                {this.props.articles.map(storyData => <Article key={storyData.link} image={storyData.image}
                                                               name={storyData.title} url={storyData.link}
                                                               source={storyData.source} {...storyData} />)}
            </div>
        );
    }
}
