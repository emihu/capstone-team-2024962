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
  const [flightDataType, setFlightDataType] = useState("live"); // 'live' or 'simulated'
  const [simulatedFlights, setSimulatedFlights] = useState<any[]>([]); // Manage simulated flights
  const [newFlight, setNewFlight] = useState({
    altitude: "",
    speed: "",
    latitude: "",
    longitude: "",
    heading: "",
  });

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
        flightDataType,
        simulatedFlights,
      };

      if (simulatedFlights.length === 0 && flightDataType === "simulated") {
        alert(
          "Error: please add at least one simulated flight when using simulated flight data."
        );
        return;
      }
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

  const addSimulatedFlight = () => {
    const { altitude, speed, latitude, longitude, heading } = newFlight;

    // Error checking
    if (!altitude || !speed || !latitude || !longitude || !heading) {
      alert(
        "Error: simulated flight not added. All fields must be filled out."
      );
      return;
    }

    const altitudeValue = parseFloat(altitude);
    const speedValue = parseFloat(speed);
    const latitudeValue = parseFloat(latitude);
    const longitudeValue = parseFloat(longitude);
    const headingValue = parseFloat(heading);

    if (altitudeValue < 0) {
      alert(
        "Error: simulated flight not added. Altitude must be a positive number."
      );
      return;
    }

    if (speedValue < 0) {
      alert(
        "Error: simulated flight not added. Speed must be a positive number."
      );
      return;
    }

    if (latitudeValue < -90 || latitudeValue > 90) {
      alert(
        "Error: simulated flight not added. Latitude must be between -90 and 90 degrees."
      );
      return;
    }

    if (longitudeValue < -180 || longitudeValue > 180) {
      alert(
        "Error: simulated flight not added. Longitude must be between -180 and 180 degrees."
      );
      return;
    }

    if (headingValue < 0 || headingValue >= 360) {
      alert(
        "Error: simulated flight not added. Heading must be between 0 and 360 degrees."
      );
      return;
    }

    setSimulatedFlights([...simulatedFlights, { ...newFlight }]);
    setNewFlight({
      altitude: "",
      speed: "",
      latitude: "",
      longitude: "",
      heading: "",
    });
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
              <label className="form-label">Camera Sensor Diagonal Dimension</label>
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
              <label className="form-label">Exposure Time</label>
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

          <div className="row g-3 align-items-center input-field">
            <div className="col-sm-2">
              <label className="form-label">Latitude</label>
            </div>
            <div className="col-auto">
              <input
                type="text"
                className="form-control"
                name="latitude"
              />
            </div>
            <div className="col-auto">
              <span className="form-text">deg</span>
            </div>
          </div>

          <div className="row g-3 align-items-center input-field">
            <div className="col-sm-2">
              <label className="form-label">Longitude</label>
            </div>
            <div className="col-auto">
              <input
                type="text"
                className="form-control"
                name="longitude"
              />
            </div>
            <div className="col-auto">
              <span className="form-text">deg</span>
            </div>
          </div>

          <div className="row g-3 align-items-center input-field">
            <div className="col-sm-2">
              <label className="form-label">Altitude</label>
            </div>
            <div className="col-auto">
              <input
                type="text"
                className="form-control"
                name="longitude"
              />
            </div>
            <div className="col-auto">
              <span className="form-text">m above sea level</span>
            </div>
          </div>

          <div className="mb-3 input-field">
            <label className="form-label">Select Flight Data Source</label>
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
                    onChange={(e) =>
                      handleFlightInputChange("altitude", e.target.value)
                    }
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
                    onChange={(e) =>
                      handleFlightInputChange("speed", e.target.value)
                    }
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
                    onChange={(e) =>
                      handleFlightInputChange("latitude", e.target.value)
                    }
                  />
                </div>
                <div className="col-auto">
                  <span className="form-text">deg</span>
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
                    onChange={(e) =>
                      handleFlightInputChange("longitude", e.target.value)
                    }
                  />
                </div>
                <div className="col-auto">
                  <span className="form-text">deg</span>
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
                    onChange={(e) =>
                      handleFlightInputChange("heading", e.target.value)
                    }
                  />
                </div>
                <div className="col-auto">
                  <span className="form-text">deg</span>
                </div>
              </div>

              <button
                type="button"
                className="btn btn-secondary mb-3"
                onClick={addSimulatedFlight}
              >
                Add Flight
              </button>

              <h3>Simulated Flights</h3>
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
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {simulatedFlights.map((flight: any, index: number) => (
                      <tr key={index}>
                        <td>{`SIM${index + 1}`}</td>
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
