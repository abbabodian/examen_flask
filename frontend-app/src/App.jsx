import React from 'react';
import './styles/main.css';
import ExampleComponent from './components/ExampleComponent';

const App = () => {
    return (
        <div className="App">
            <h1>Welcome to the Frontend App</h1>
            <ExampleComponent />
        </div>
    );
};

export default App;