import { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

// external library imports
import "leaflet/dist/leaflet.css";
import "bootstrap/dist/css/bootstrap.css";

// component imports
import NavBar from "./components/NavBar";
import MapFlights from "./components/MapFlights";

function App() {
  const [data, setData] = useState<any[]>([]);
  const [focalLength, setFL] = useState("");
  const [cameraSensorSize, setCSS] = useState("");
  const [barlowReducerFactor, setBRF] = useState("");
  const [exposure, setE] = useState("");
  const [fovCenterRaH, setFCRH] = useState("");
  const [fovCenterRaM, setFCRM] = useState("");
  const [fovCenterRaS, setFCRS] = useState("");
  const [fovCenterDec, setFCD] = useState("");
  const [flightDataType, setFlightDataType] = useState("live"); // 'live' or 'simulated'
  const [simulatedFlights, setSimulatedFlights] = useState<any[]>([]); // Manage simulated flights
  const [newFlight, setNewFlight] = useState({
    altitude: "",
    speed: "",
    latitude: "",
    longitude: "",
    heading: "",
  });

  const handleSubmit = (event: any) => {
    event.preventDefault();
    try {
      const formData = {
        focalLength,
        cameraSensorSize,
        barlowReducerFactor,
        exposure,
        fovCenterRaH,
        fovCenterRaM,
        fovCenterRaS,
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

  const addSimulatedFlight = () => {
    setSimulatedFlights([...simulatedFlights, { ...newFlight }]);
    setNewFlight({ altitude: "", speed: "", latitude: "", longitude: "", heading: "" });
  };

  const removeSimulatedFlight = (index: number) => {
    const updatedFlights = simulatedFlights.filter((_, i) => i !== index);
    setSimulatedFlights(updatedFlights);
  };

  const handleFlightInputChange = (field: string, value: string) => {
    setNewFlight({ ...newFlight, [field]: value });
  };

  return (
    <>
      <div>
        <NavBar />
      </div>
      <div className="container">
        <h1>Flight Prediction</h1>
        <form onSubmit={handleSubmit}>
          <div className="row g-3 align-items-center input-field">
            <div className="col-sm-2">
              <label className="form-label">Focal Length</label>
            </div>
            <div className="col-auto">
              <input
                type="number"
                className="form-control"
                name="focal_length"
                value={focalLength}
                onChange={(e) => setFL(e.target.value)}
              />
            </div>
            <div className="col-auto">
              <span className="form-text">mm</span>
            </div>
          </div>

          <div className="row g-3 align-items-center input-field">
            <div className="col-sm-2">
              <label className="form-label">Camera Sensor Size</label>
            </div>
            <div className="col-auto">
              <input
                type="number"
                className="form-control"
                name="camera_sensor_size"
                value={cameraSensorSize}
                onChange={(e) => setCSS(e.target.value)}
              />
            </div>
            <div className="col-auto">
              <span className="form-text">mm</span>
            </div>
          </div>

          <div className="row g-3 align-items-center input-field">
            <div className="col-sm-2">
              <label className="form-label">Barlow/Reducer Factor</label>
            </div>
            <div className="col-auto">
              <input
                type="number"
                className="col-sm-10 form-control"
                name="barlow_reducer_factor"
                value={barlowReducerFactor}
                onChange={(e) => setBRF(e.target.value)}
              />
            </div>
            <div className="col-auto">
              <span className="form-text">x</span>
            </div>
          </div>

          <div className="row g-3 align-items-center input-field">
            <div className="col-sm-2">
              <label className="form-label">Exposure</label>
            </div>
            <div className="col-auto">
              <input
                type="text"
                className="form-control"
                name="exposure"
                value={exposure}
                onChange={(e) => setE(e.target.value)}
              />
            </div>
            <div className="col-auto">
              <span className="form-text">secs</span>
            </div>
          </div>

          <div className="row g-3 align-items-center input-field">
            <div className="col-sm-2">
              <label className="form-label">FOV Center - RA</label>
            </div>
            <div className="col-sm-1">
              <input
                type="text"
                className="form-control"
                name="fov_center_ra_h"
                value={fovCenterRaH}
                onChange={(e) => setFCRH(e.target.value)}
              />
            </div>
            <div className="col-auto">
              <span className="form-text">hours</span>
            </div>
            <div className="col-sm-1">
              <input
                type="text"
                className="form-control"
                name="fov_center_ra_m"
                value={fovCenterRaM}
                onChange={(e) => setFCRM(e.target.value)}
              />
            </div>
            <div className="col-auto">
              <span className="form-text">mins</span>
            </div>
            <div className="col-sm-1">
              <input
                type="text"
                className="form-control"
                name="fov_center_ra_s"
                value={fovCenterRaS}
                onChange={(e) => setFCRS(e.target.value)}
              />
            </div>
            <div className="col-auto">
              <span className="form-text">secs</span>
            </div>
          </div>

          <div className="row g-3 align-items-center input-field">
            <div className="col-sm-2">
              <label className="form-label">FOV Center - Dec</label>
            </div>
            <div className="col-auto">
              <input
                type="text"
                className="form-control"
                name="fov_center_dec"
                value={fovCenterDec}
                onChange={(e) => setFCD(e.target.value)}
              />
            </div>
            <div className="col-auto">
              <span className="form-text">&deg;</span>
            </div>
          </div>

          <div className="mb-3 input-field">
            <label className="form-label">Select Flight Data Source:</label>
            <div className="form-check">
              <input
                type="radio"
                className="form-check-input"
                id="liveData"
                name="dataType"
                value="live"
                checked={flightDataType === "live"}
                onChange={(e) => setFlightDataType(e.target.value)}
              />
              <label className="form-check-label" htmlFor="liveData">
                Live Data
              </label>
            </div>
            <div className="form-check">
              <input
                type="radio"
                className="form-check-input"
                id="simulatedData"
                name="dataType"
                value="simulated"
                checked={flightDataType === "simulated"}
                onChange={(e) => setFlightDataType(e.target.value)}
              />
              <label className="form-check-label" htmlFor="simulatedData">
                Simulated Data
              </label>
            </div>
          </div>

          {flightDataType === "simulated" && (
            <div>
              <h3>Add Simulated Flight</h3>
              <div className="row g-3 align-items-center mb-3">
                <div className="col-sm-2">
                  <label className="form-label">Altitude</label>
                </div>
                <div className="col-auto">
                  <input
                    type="number"
                    className="form-control"
                    value={newFlight.altitude}
                    onChange={(e) => handleFlightInputChange("altitude", e.target.value)}
                  />
                </div>
                <div className="col-auto">
                  <span className="form-text">feet</span>
                </div>
              </div>

              <div className="row g-3 align-items-center mb-3">
                <div className="col-sm-2">
                  <label className="form-label">Speed</label>
                </div>
                <div className="col-auto">
                  <input
                    type="number"
                    className="form-control"
                    value={newFlight.speed}
                    onChange={(e) => handleFlightInputChange("speed", e.target.value)}
                  />
                </div>
                <div className="col-auto">
                  <span className="form-text">knots</span>
                </div>
              </div>

              <div className="row g-3 align-items-center mb-3">
                <div className="col-sm-2">
                  <label className="form-label">Latitude</label>
                </div>
                <div className="col-auto">
                  <input
                    type="number"
                    className="form-control"
                    value={newFlight.latitude}
                    onChange={(e) => handleFlightInputChange("latitude", e.target.value)}
                  />
                </div>
                <div className="col-auto">
                  <span className="form-text">&deg;</span>
                </div>
              </div>

              <div className="row g-3 align-items-center mb-3">
                <div className="col-sm-2">
                  <label className="form-label">Longitude</label>
                </div>
                <div className="col-auto">
                  <input
                    type="number"
                    className="form-control"
                    value={newFlight.longitude}
                    onChange={(e) => handleFlightInputChange("longitude", e.target.value)}
                  />
                </div>
                <div className="col-auto">
                  <span className="form-text">&deg;</span>
                </div>
              </div>

              <div className="row g-3 align-items-center mb-3">
                <div className="col-sm-2">
                  <label className="form-label">Heading</label>
                </div>
                <div className="col-auto">
                  <input
                    type="number"
                    className="form-control"
                    value={newFlight.heading}
                    onChange={(e) => handleFlightInputChange("heading", e.target.value)}
                  />
                </div>
                <div className="col-auto">
                  <span className="form-text">&deg;</span>
                </div>
              </div>

              <button type="button" className="btn btn-secondary mb-3" onClick={addSimulatedFlight}>
                Add Flight
              </button>

              <h3>Simulated Flights</h3>
              <div className="table-responsive">
                <table className="table table-striped table-bordered table-light">
                  <thead className="thead-dark">
                    <tr>
                      <th>Flight Number</th>
                      <th>Altitude (feet)</th>
                      <th>Heading (degrees)</th>
                      <th>Latitude</th>
                      <th>Longitude</th>
                      <th>Speed (knots)</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {simulatedFlights.map((flight: any, index: number) => (
                      <tr key={index}>
                        <td>{`SIM${index+1}`}</td>
                        <td>{flight.altitude}</td>
                        <td>{flight.heading}</td>
                        <td>{flight.latitude}</td>
                        <td>{flight.longitude}</td>
                        <td>{flight.speed}</td>
                        <td>
                          <button
                            type="button"
                            className="btn btn-danger btn-sm"
                            onClick={() => removeSimulatedFlight(index)}
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}


          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>
        {data.length === 0 ? (
          <p>No flights found</p>
        ) : (
          <div>
            <div className="table-responsive">
              <table className="table table-striped table-bordered table-light">
                <thead className="thead-dark">
                  <tr>
                    <th>Flight Number</th>
                    <th>Altitude (feet)</th>
                    <th>Heading (degrees)</th>
                    <th>Latitude</th>
                    <th>Longitude</th>
                    <th>Speed (knots)</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((flight: any, index: number) => (
                    <tr key={index}>
                      <td>{flight.flight_number}</td>
                      <td>{flight.altitude}</td>
                      <td>{flight.heading}</td>
                      <td>{flight.latitude}</td>
                      <td>{flight.longitude}</td>
                      <td>{flight.speed}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <MapFlights data={data} />
          </div>
        )}
      </div>
    </>
  );
}

export default App;
