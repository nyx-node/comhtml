import React from "react";
import ReactDOM from "react-dom"
import FormApp from "./components/formApp";
import ToolBar from "./components/toolBar";
import '/../static/css/toolbar.scss'
import {BrowserRouter as Router , Switch, Route} from 'react-router-dom';
import $ from 'jquery';

function Index() {
  return(
    <Router>
      <Switch>
      <Route path="/" exact component={FormApp} />
      <Route path="/error" component={FormApp} />
      <Route path="/results" component={ToolBar} />
      </Switch>

    </Router>);
}
ReactDOM.render(<Index />,document.getElementById('root'));
