import React from 'react';
import Header from './Header.jsx';
import Content from './Content.jsx';


const divStyle= {
  height: 100,
  width: 100,
  backgroundColor: "blue"
}
export default class App extends React.Component {
  render() {
    return (
      <div className="background">
        <Header />
          <div className="container-fluid">
             <Content />
        </div>
     </div>

    );
  }
}
