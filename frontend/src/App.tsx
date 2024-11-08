import { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.css";

// component imports
import NavBar from "./components/NavBar";

function App() {
  const [data, setData] = useState<any>(null); // State to store API response

  const handleSubmit = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8080/api/flight-prediction"
      );
      setData(response.data);
      console.log("Success");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      <div>
        <NavBar />
      </div>
      <div className="container">
        <h1>Flight Prediction</h1>
        <form>
          <div className="mb-3">
            <label className="form-label">Focal Length</label>
            <input
              type="email"
              className="form-control"
              id="exampleInputEmail1"
              aria-describedby="emailHelp"
            ></input>
          </div>
          <div className="mb-3">
            <label className="form-label">Camera Sensor Size</label>
            <input
              type="password"
              className="form-control"
              id="exampleInputPassword1"
            ></input>
          </div>
          <div className="mb-3">
            <label className="form-label">Barlow Reducer Facter</label>
            <input
              type="password"
              className="form-control"
              id="exampleInputPassword1"
            ></input>
          </div>
          <div className="mb-3">
            <label className="form-label">FOV Center (RA)</label>
            <input
              type="password"
              className="form-control"
              id="exampleInputPassword1"
            ></input>
          </div>
          <div className="mb-3">
            <label className="form-label">FOV Center (Dec)</label>
            <input
              type="password"
              className="form-control"
              id="exampleInputPassword1"
            ></input>
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            onClick={handleSubmit}
          >
            Submit
          </button>
        </form>
        <p>{JSON.stringify(data, null, 2)}</p>
      </div>
    </>
  );
}

export default App;
