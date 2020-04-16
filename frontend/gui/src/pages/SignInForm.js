import React, { Component } from 'react';


class SignInForm extends Component {
    render() {
        return (
            <div className="App">
          <div className='App__Aside'></div>
          <div className='App__Form'>
            <div className='PageSwitcher'>
              <a href='Sign_In' className='PageSwitcher__Item'>Sign In</a>
              <a href='Sign_Up' className='PageSwitcher__Item PageSwitcher__Item--Active'>Sign up</a>
            </div>
            
            <div className='FormTitle'>
          <a href='Sign_In' className='FormTitle__Link'>Sign In</a> or <a href ='Sign_Up'
          className='FormTitle__Link FormTitle__Link--Active'>Sign up</a>
        </div>

        <div className='FormCenter'>
          <form className='FormFields' onSubmit={this.handleSubmit}>
            <div className='FormField'>
              <label className='FormField__Label' htmlFor='name'>Restaurant Name</label>
              <input type='text' id='name' className='FormField__Input' 
              placeholder='Please enter the restaurant name' name='name' required/>
            </div>
            <div className='FormField'>
              <label className='FormField__Label' htmlFor='name'>City</label>
              <input type='text' id='name' className='FormField__Input' 
              placeholder='Please enter the city your restaurant is located in' name='city' required/>
            </div>
            <div className='FormField'>
              <label className='FormField__Label' htmlFor='name'>Zipcode</label>
              <input type='text' id='name' className='FormField__Input' 
              placeholder='Please enter the zipcode your restaurant is located in' name='zipcode' required/>
            </div>
          </form>
          Already a member? <a href="Sign_In">Login</a>
        </div>

          </div>
        </div>
        );
    }
}

export default SignInForm;