import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import './App.css';
import Home from './components/Home';
import FineTune from './components/FineTune';
import RunModel from './components/RunModel';

function App() {
  return (
    <Router>
      <div className="container">
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/finetune">Fine-Tune Model</Link></li>
            <li><Link to="/run">Run Model</Link></li>
          </ul>
        </nav>
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/finetune" component={FineTune} />
          <Route path="/run" component={RunModel} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
