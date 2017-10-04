import React, { Component } from 'react';
import Home from './Home.jsx'
import About from './About.jsx'
import Contact from './Contact.jsx'
import Story from './Story.jsx'

import { HashRouter, Route } from 'react-router-dom'

export default class Content extends React.Component {
  
  render() {
    return (
      <div className="container-fluid">
        <HashRouter>
          <div className="container foreground">
            <Route exact path='/' component={Home} />
            <Route path='/contact' component={Contact} />
            <Route path='/about' component={About} />
            <Route path='/story/:id' component={Story} />
          </div>
        </HashRouter>
      </div>
  );
  }
}
