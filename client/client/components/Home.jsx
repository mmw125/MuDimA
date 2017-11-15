import React from 'react';
import StoryCard from './StoryCard.jsx'
import stories from '../data/mock-stories.js'
// import ReactPaginate from 'react-paginate';
import Pagination from 'react-js-pagination';
export default class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: true,
      activePage: 1,
      total_items: false
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
          total_items: responseJson[0] ? responseJson[0]['total_items'] : 0
        })
      })
      .catch((error) => { console.error(error); });
  }
  componentWillReceiveProps(nextProps) {
    let {page_number=1} = nextProps.match.params;
    page_number = page_number != '' ? parseInt(page_number) : 1;
    console.log('componentWillReceiveProps1', page_number);
    this.setState({
      activePage: page_number
    }, () => {
      this.getTopics(page_number);
    });
  }
  componentDidMount() {
    let {page_number=1} = this.props.match.params;
    page_number = page_number != '' ? parseInt(page_number) : 1;
    console.log('componentDidMount', page_number);
    this.setState({
      activePage: page_number
    }, () => {
      this.getTopics(page_number);
    });
  }
  handlePageClick(page_number) {
    this.setState({
      activePage: page_number
    }, () => {
      this.props.history.push('/'+page_number);
    });
  }
  getPagination() {
    return (
      <div className="pagination-container">
        <Pagination
          activePage={this.state.activePage}
          itemsCountPerPage={10}
          totalItemsCount={this.state.total_items}
          onChange={(e) => this.handlePageClick(e)}
          activeClass="active"
          innerClass="pagination"
          activeLinkClass="page-link"
          itemClass="page-item"
          linkClass="page-link"
        />
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
        {this.state.total_items && this.getPagination()}
      </div>
      );
  }
}
