import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import FlightPredictor from "./pages/FlightPredictor";
import About from "./pages/About";
import HowToUse from "./pages/HowToUse";

function App() {
  return (
    <Router>
      <div>
        <NavBar />
        <Routes>
          <Route path="/" element={<FlightPredictor />} />
          <Route path="/about" element={<About />} />
          <Route path="/how-to-use" element={<HowToUse />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
