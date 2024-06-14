import {
  BrowserRouter,
  Route,
  Routes
} from 'react-router-dom';

import NavBar from "./components/NavBar";
import Dashboard from './pages/Dashboard';
import Home from "./pages/Home";


function App() {

  return (
    <>
      <BrowserRouter>
        <div id="app-holder">
          <NavBar />

          <div className="container">
            <Routes>
              <Route exact path="/" element={<Home />} />
              <Route exact path="/dashboard" element={<Dashboard />} />
            </Routes>
          </div>

        </div>
      </BrowserRouter>
    </>
  );

}

export default App;
