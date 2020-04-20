import React from "react";
import { Route } from 'react-router-dom';

import SignUpForm from './containers/SignUpForm';
import SignInForm from './containers/SignInForm';
import SemanticUI from './containers/SemanticUI';

const BaseRouter = () => (
    <div>
        <Route path="/signin" component={SignInForm} />
        <Route path="/signup" component={SignUpForm} />
        <Route path="/SemanticUI" component={SemanticUI} />
    </div>
);


export default BaseRouter;