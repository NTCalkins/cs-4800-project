import React, { Component } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import SignUpForm from './pages/SignUpForm'
import SignInForm from './pages/SignInForm'

import CustomLayout from './containers/Layout';

class App extends Component {
  render() {
    return (
      <div>
        <SignInForm />
      </div>
    );
  }
}

export default App;