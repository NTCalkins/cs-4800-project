import React, { Component } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import SignUpForm from './pages/SignUpForm';
import SignInForm from './pages/SignInForm';
import SemanticUI from './containers/SemanticUI';


import CustomLayout from './containers/Layout';

import {BrowserRouter as Router, Link} from 'react-router-dom';
import Route from 'react-router-dom/Route';

class App extends Component {
  render() {
    return (
    <Router>
    <ul>
    <Link to="/">Home</Link>
    <Link to="/about">About</Link>
    </ul>
    <Route path="/" exact strict render={
      () => {
        return (<SemanticUI/>);
      }
    }/>
    <Route path="/about" exact strict render={
      () => {
        return (<SignUpForm/>);
      }
    }/>
    </Router>
    );
  }
}

export default App;