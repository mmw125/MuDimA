import React from 'react';
import StoryCard from './StoryCard.jsx'
import stories from '../data/mock-stories.js'
import ReactPaginate from 'react-paginate';

export default class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: true
    }
  }
  getTopics(page_number, callback) {
    page_number = page_number ? parseInt(page_number) - 1 : parseInt(page_number);
    return fetch('http://localhost/getTopics?p='+page_number)
      .then((response) => response.json())
      .then((responseJson) => {
        this.setState({
          isLoading: false,
          topics: responseJson,
          all_pages_count: responseJson[0] ? responseJson[0]['page_count'] : 1
        }, () => {
          if (callback) {
            console.log('calling');
            callback();
          }
        })
      })
      .catch((error) => { console.error(error); });
  }
  componentWillReceiveProps(nextProps) {
    const {page_number=0} = nextProps.match.params;
    this.getTopics(page_number);
  }
  componentDidMount() {
    const {page_number=0} = this.props.match.params;
    this.getTopics(page_number);
  }
  handlePageClick(e) {
    let callback = () => {
      let page_id = parseInt(e.selected);
      if (page_id) {
        this.props.history.push('/' + (page_id + 1));
      } else {
        this.props.history.replace('/' + (page_id + 1));
      }
    }
    this.getTopics(e.selected, callback);
  }
  getPagination() {
    return (
      <div className="pagination-container">
        <ReactPaginate previousLabel={"previous"}
          initialPage={0}
          nextLabel={"next"}
          breakLabel={<a href="" className="page-link">...</a>}
          pageClassName="page-item"
          breakClassName="page-item"
          previousClassName="page-item"
          nextClassName="page-item"
          pageLinkClassName="page-link"
          nextLinkClassName="page-link"
          previousLinkClassName="page-link"
          pageCount={this.state['all_pages_count']}
          marginPagesDisplayed={2}
          pageRangeDisplayed={5}
          onPageChange={(e) => this.handlePageClick(e)}
          containerClassName={"pagination"}
          subContainerClassName={"pages pagination"}
          activeClassName={"active"} />
      </div>
    );
  }
  render() {
    if (this.state.isLoading) {
      return (
        <h1></h1>
      );
    }
    return (
      <div className="row">
        {this.state.topics.map(storyData => <StoryCard key={storyData.id} url={storyData.image} name={storyData.title} id={storyData.id} count={storyData.count} {...storyData} />)}
        {this.getPagination()}
      </div>
      );
  }
}
