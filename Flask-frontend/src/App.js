import './App.css';
import {Route, Switch, withRouter, Redirect} from 'react-router-dom';
import MainPage from './containers/MainPage/MainPage';
import Welcome from './containers/Welcome/Welcome';
import React from 'react';
import Images from './containers/Images/Images';


function App() {

  let routes = (
    <Switch>
      <Route path='/' exact component={Welcome} />
      <Route path='/main' exact component={MainPage} />
      <Route path='/outputs' exact component={Images} />
      
      <Redirect to='/' />
    </Switch>
  )

  return (
    <div className="App">
     {routes}
    </div>
  );
}

export default withRouter(App);