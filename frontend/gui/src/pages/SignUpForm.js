import React, { Component } from 'react';


class SignUpForm extends Component {
    render() {
        return (
            <div class="App">
          <div class='App__Aside'></div>
          <div class='App__Form'>
            <div class='PageSwitcher'>
              <a href='Sign_In' class='PageSwitcher__Item'>Sign In</a>
              <a href='Sign_Up' class='PageSwitcher__Item PageSwitcher__Item--Active'>Sign up</a>
            </div>
            
            <div class='FormTitle'>
          <a href='Sign_In' class='FormTitle__Link'>Sign In</a> or <a href ='Sign_Up'
          class='FormTitle__Link FormTitle__Link--Active'>Sign up</a>
        </div>

        <div class='FormCenter'>
          <form class='FormFields' onSubmit={this.handleSubmit}>
            <div class='FormField'>
              <label class='FormField__Label' htmlFor='name'>Restaurant Name</label>
              <input type='text' id='name' class='FormField__Input' 
              placeholder='Please enter the restaurant name' name='name' required/>
            </div>
            <div class='FormField'>
              <label class='FormField__Label' htmlFor='name'>City</label>
              <input type='text' id='name' class='FormField__Input' 
              placeholder='Please enter the city your restaurant is located in' name='city' required/>
            </div>
            <div class='FormField'>
              <label class='FormField__Label' htmlFor='name'>Zipcode</label>
              <input type='text' id='name' class='FormField__Input' 
              placeholder='Please enter the zipcode your restaurant is located in' name='zipcode' required/>
            </div>
            <div class='FormField'>
              <label class='FormField__Label' htmlFor='name'>Email</label>
              <input type='text' id='name' class='FormField__Input' 
              placeholder='Please enter an email' name='email' required/>
            </div>
            <div class='FormField'>
              <label class='FormField__Label' htmlFor='name'>Password</label>
              <input type='text' id='name' class='FormField__Input' 
              placeholder='Create a password' name='password' required/>
            </div>
          </form>
          Already a member? <a href="SignInForm.js">Login</a>
        </div>

          </div>
        </div>
        );
    }
}

export default SignUpForm;