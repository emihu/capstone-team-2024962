import { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.css";

// component imports
import NavBar from "./components/NavBar";

function App() {
  const [data, setData] = useState<any>(null); // State to store API response
  const [formData, setFormData] = useState({
    focal_length: "",
    camera_sensor_size: "",
    barlow_reducer_factor: "",
    fov_center_ra: "",
    fov_center_dec: "",
  });

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async () => {
    try {
      console.log(formData);
      const response = await axios.post(
        "http://127.0.0.1:8080/api/flight-prediction",
        formData
      );
      setData(response.data);
      console.log(response);
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
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Focal Length</label>
            <input
              type="text"
              className="form-control"
              name="focal_length"
              value={formData.focal_length}
              onChange={handleChange}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Camera Sensor Size</label>
            <input
              type="text"
              className="form-control"
              name="camera_sensor_size"
              value={formData.camera_sensor_size}
              onChange={handleChange}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Barlow Reducer Factor</label>
            <input
              type="text"
              className="form-control"
              name="barlow_reducer_factor"
              value={formData.barlow_reducer_factor}
              onChange={handleChange}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">FOV Center (RA)</label>
            <input
              type="text"
              className="form-control"
              name="fov_center_ra"
              value={formData.fov_center_ra}
              onChange={handleChange}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">FOV Center (Dec)</label>
            <input
              type="text"
              className="form-control"
              name="fov_center_dec"
              value={formData.fov_center_dec}
              onChange={handleChange}
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>
        <p>{JSON.stringify(data, null, 2)}</p>
      </div>
    </>
  );
}

export default App;
