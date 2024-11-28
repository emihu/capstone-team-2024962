import { useState, useEffect, useRef } from "react";
import "./FlightPredictor.css";
import axios from "axios";

// external library imports
import "leaflet/dist/leaflet.css";
import "bootstrap/dist/css/bootstrap.css";

// component imports
import MapFlights from "../components/MapFlights";

function FlightPredictor() {
  const [data, setData] = useState<any[]>([]);
  const [isUpdating, setIsUpdating] = useState(false);
  const [fovBorder, setFovBorder] = useState({
    lat: 0,
    lon: 0,
    radius: 0,
  });
  const [focalLength, setFL] = useState("");
  const [cameraSensorSize, setCSS] = useState("");
  const [barlowReducerFactor, setBRF] = useState("");
  const [exposure, setE] = useState("");
  const [fovCenterRaH, setFCRH] = useState("");
  const [fovCenterRaM, setFCRM] = useState("");
  const [fovCenterRaS, setFCRS] = useState("");
  const [fovCenterDec, setFCD] = useState("");

  const fetchFlightData = async () => {
    try {
      setFL(focalLength);
      setCSS(cameraSensorSize);
      setBRF(barlowReducerFactor);
      setE(exposure);
      setFCRH(fovCenterRaH);
      setFCRM(fovCenterRaM);
      setFCRS(fovCenterRaS);
      setFCD(fovCenterDec);
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
      console.log("Fetching flight data...", formData);
      axios
        .post(`http://127.0.0.1:5000/api/flight-prediction`, formData)
        .then((response) => {
          const { flight_info, fov_border } = response.data;
          console.log(flight_info);
          console.log(fov_border);
          setData(flight_info);
          setFovBorder(fov_border);
        })
        .catch((error) => {
          console.error("There was an error", error);
        });
    } catch (error) {
      console.error("Error fetching flight data:", error);
    }
  };

  //   const handleSubmit = (event: any) => {
  //     event.preventDefault();
  //     fetchFlightData();
  //     setIsUpdating(true); // Start periodic updates after submission
  //   };
  const handleSubmit = (event: any) => {
    setIsUpdating(false);
    event.preventDefault();

    // Update state variables explicitly (if needed)
    setFL(focalLength); // Ensures the most current value is set
    setCSS(cameraSensorSize);
    setBRF(barlowReducerFactor);
    setE(exposure);
    setFCRH(fovCenterRaH);
    setFCRM(fovCenterRaM);
    setFCRS(fovCenterRaS);
    setFCD(fovCenterDec);

    // Call API with the current state values
    fetchFlightData();
    setIsUpdating(true); // Start periodic updates
  };

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    if (isUpdating) {
      interval = setInterval(() => {
        fetchFlightData();
      }, 10000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isUpdating]);

  return (
    <>
      <div className="container">
        <h1>Flight Predictor</h1>
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
              <span className="form-text">deg</span>
            </div>
          </div>

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
                    <th>Heading (deg)</th>
                    <th>Latitude (deg)</th>
                    <th>Longitude (deg)</th>
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
            <MapFlights data={data} fovBorder={fovBorder} />
          </div>
        )}
      </div>
    </>
  );
}

export default FlightPredictor;
