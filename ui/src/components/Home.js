import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="container">
      <h1>Welcome to the GPT-2 Fine-Tuning and Text Generation App</h1>
      <p>Use the navigation bar to fine-tune a model or to run the model.</p>
      <nav>
        <ul>
          <li><Link to="/finetune">Fine-Tune Model</Link></li>
          <li><Link to="/run">Run Model</Link></li>
        </ul>
      </nav>
    </div>
  );
}

export default Home;
