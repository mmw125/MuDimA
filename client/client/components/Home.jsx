import React from 'react';
import StoryCard from './StoryCard.jsx'
import ReactPaginate from 'react-paginate';

export default class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: true,
            page: 0,
        }
    }

    getTopics() {
        return fetch('http://localhost/getTopics?p=' + this.state.page)
            .then((response) => response.json())
            .then((responseJson) => {
                this.setState({
                    isLoading: false,
                    topics: responseJson,
                    pageCount: 10,
                    page: this.state.page,
                })
            })
            .catch((error) => {
                console.error(error);
            });
    }

    componentWillMount() {
        this.getTopics();
    }

    handlePageClick(data) {
        console.log(this);
        this.setState({
            isLoading: true,
            page: data.selected,
        }, () => this.getTopics());
    }

    render() {
        if (this.state.isLoading) {
            return (
                <h1></h1>
            );
        }
        return (
            <div>
                <div className="row">
                    {this.state.topics.map(storyData => <StoryCard key={storyData.id} url={storyData.image}
                                                                   name={storyData.title} id={storyData.id}
                                                                   count={storyData.count} {...storyData} />)}
                </div>
                <ReactPaginate previousLabel={"previous"}
                       nextLabel={"next"}
                       breakLabel={<a href="">...</a>}
                       breakClassName={"break-me"}
                       pageCount={this.state.pageCount}
                       marginPagesDisplayed={2}
                       pageRangeDisplayed={5}
                       onPageChange={(pageNumber) => {
                                   console.log(pageNumber);
                                   this.setState({isLoading: true, page: pageNumber,});
                                   this.getTopics();
                               }}
                       containerClassName={"pagination"}
                       subContainerClassName={"pages pagination"}
                       activeClassName={"active"} />
            </div>
        );
    }
}
