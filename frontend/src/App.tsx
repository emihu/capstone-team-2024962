import { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.css";

// component imports
import NavBar from "./components/NavBar";

function App() {
  const [data, setData] = useState("");
  const [focalLength, setFL] = useState("");
  const [cameraSensorSize, setCSS] = useState("");
  const [barlowReducerFactor, setBRF] = useState("");
  const [fovCenterRa, setFCR] = useState("");
  const [fovCenterDec, setFCD] = useState("");

  const handleSubmit = (event: any) => {
    event.preventDefault();
    try {
      const formData = {
        focalLength,
        cameraSensorSize,
        barlowReducerFactor,
        fovCenterRa,
        fovCenterDec,
      };
      console.log(formData);
      axios
        .post(`http://127.0.0.1:5000/api/flight-prediction`, formData)
        .then((response) => {
          const responseData = response.data;
          console.log(responseData);
          setData(responseData);
        })
        .catch((error) => {
          console.error("There was an error", error);
        });
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
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Focal Length</label>
            <input
              type="number"
              className="form-control"
              name="focal_length"
              value={focalLength}
              onChange={(e) => setFL(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Camera Sensor Size</label>
            <input
              type="number"
              className="form-control"
              name="camera_sensor_size"
              value={cameraSensorSize}
              onChange={(e) => setCSS(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Barlow Reducer Factor</label>
            <input
              type="number"
              className="form-control"
              name="barlow_reducer_factor"
              value={barlowReducerFactor}
              onChange={(e) => setBRF(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">FOV Center (RA)</label>
            <input
              type="text"
              className="form-control"
              name="fov_center_ra"
              value={fovCenterRa}
              onChange={(e) => setFCR(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">FOV Center (Dec)</label>
            <input
              type="text"
              className="form-control"
              name="fov_center_dec"
              value={fovCenterDec}
              onChange={(e) => setFCD(e.target.value)}
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>
        {data === "" ? null : data.length === 0 ? (
          <p>No flights found</p>
        ) : (
          <pre>{JSON.stringify(data, null, 2)}</pre>
        )}
      </div>
    </>
  );
}

export default App;
