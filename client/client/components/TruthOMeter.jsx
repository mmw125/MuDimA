/* 
* Component to display a list of verified facts from Politifact API
* For Documentation of the API, visit : http://static.politifact.com/api/doc.html
*/
import React from 'react';
import moment from 'moment';

export default class TruthList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      item : [],
      isLoading: true
    }
  }
  getTruth() {
    return fetch('http://localhost/getTruth?n=15')
      .then((response) => response.json())
      .then((responseJson) => {
        console.log('responseJson', responseJson);
        this.setState({
          isLoading: false,
          items: responseJson
        })})
      .catch((error) => { console.error(error); });
  }
  componentDidMount() {
    this.getTruth();
  }
  getTrimmedLongText(text="") {
    if (text.length > 255) {
        return text.slice(0, 255) + "...";
    }
    return text;
  }

  getItems() {
    const {items = []} = this.state;
    let all_items = items.map((item) => {
      return (
        <div className="wrapper" key={item.statement_url}>
          <a href={'http://politifact.com' + item.statement_url} target="_blank">
            <div className="truth-img">
              <img src={item.speaker.canonical_photo} height="105" width="105" />
            </div>
            <div className="truth-info">
              <div className="truth-text">
                <h3 dangerouslySetInnerHTML={{__html: this.getTrimmedLongText(item.statement)}}></h3>
                <span className="subtext">
                  - {item.speaker.first_name + " " + item.speaker.last_name}, 
                  <span className="subsubtext">{' on ' + moment(item.statement_date, "YYYY-MM-DD").format("dddd, MMMM Do YYYY")}</span>
                </span>
              </div>
              
            </div>
            <div className="truth-img-right">
              <img src={item.ruling.canonical_ruling_graphic} height="105" width="105" />
            </div>
          </a>
        </div>
      );
    });
    return all_items;
  }
  render() {
    if (!this.state.isLoading) {
      return (
        <div>
            <div className="fact-checks" >
              Latest fact-checks
              <span className="powered_by"> - Powered by Politifact</span>
            </div>
            {this.getItems()}
        </div>
      );
    }
    return (
      <div className="truth-loading">
        <h3>Loading Truth-O-meter...</h3>
      </div>
    );
  }
}
