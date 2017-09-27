import React from 'react';

export default class Header extends React.Component {
  render() {
    return (
      <nav className="navbar sticky-top navbar-toggleable-md navbar-light bg-faded">
        <a className="navbar-brand" href="#">MuDiMa</a>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item">
              <a className="nav-link" href="#/about">About</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#/contact">Contact</a>
            </li>
          </ul>

        </div>
      </nav>);
  }
}
