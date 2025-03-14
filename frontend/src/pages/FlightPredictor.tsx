import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import "bootstrap/dist/css/bootstrap.css";

import FlightTable from "../components/TableFlights";
import "./FlightPredictor.css";

function FlightPredictor() {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    watch,
  } = useForm({
    defaultValues: {
      focalLength: "",
      cameraSensorSize: "",
      barlowReducerFactor: "",
      exposure: "",
      fovCenterRaH: "",
      fovCenterRaM: "",
      fovCenterRaS: "",
      fovCenterDec: "",
      latitude: "",
      longitude: "",
      altitude: "",
      altitudeUnit: "m",
      flightDataType: "live",
    },
  });

  const [flightsPosition, setFlightsPosition] = useState<any[]>([]);
  const [flightData, setFlightData] = useState<any[]>([]);

  const [simulatedFlights, setSimulatedFlights] = useState<any[]>([]);
  const [simulatedFlightAltitudeUnit, setSimulatedFlightAltitudeUnit] =
    useState("ft");
  const [simulatedFlightSpeedUnit, setSimulatedFlightSpeedUnit] =
    useState("knots");
  const [newFlight, setNewFlight] = useState({
    altitude: "",
    speed: "",
    latitude: "",
    longitude: "",
    heading: "",
  });

  const flightDataType = watch("flightDataType");

  const fetchFlightData = async (formData: any) => {
    if (flightDataType === "simulated" && simulatedFlights.length === 0) {
      alert("Error: Please add at least one simulated flight.");
      return;
    }
  
    try {
      console.log("Fetching flight data...", formData);
      const response = await axios.post(
        "http://127.0.0.1:5000/api/flight-prediction",
        {
          ...formData,
          simulatedFlights,
        }
      );
  
      // Extract the returned data
      const { flights_position, flight_data } = response.data;
  
      // Set the state variables
      setFlightsPosition(flights_position);
      setFlightData(flight_data);
      
    } catch (error) {
      console.error("Error fetching flight data:", error);
    }
  };

  const onSubmit = (formData: any) => {
    if (formData.altitudeUnit === "ft") {
      formData.altitude = (parseFloat(formData.altitude) * 0.3048).toString();
    }
    fetchFlightData(formData);
  };

  const addSimulatedFlight = () => {
    if (Object.values(newFlight).some((val) => val === "")) {
      alert("Error: All fields must be filled out.");
      return;
    }

    const altitudeValue =
      simulatedFlightAltitudeUnit === "ft"
        ? parseFloat(newFlight.altitude)
        : parseFloat(newFlight.altitude) * 3.28084;

    const speedValue =
      simulatedFlightSpeedUnit === "kph"
        ? parseFloat(newFlight.speed) * 0.539957
        : simulatedFlightSpeedUnit === "mph"
        ? parseFloat(newFlight.speed) * 0.868976
        : parseFloat(newFlight.speed);

    setSimulatedFlights([
      ...simulatedFlights,
      { ...newFlight, altitude: altitudeValue, speed: speedValue },
    ]);
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

  return (
    <div className="container">
      <h1>Flight Predictor</h1>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="mb-3 pt-2">
          <label className="form-label">Focal Length</label>
          <div className="d-flex align-items-center">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("focalLength")}
            />
            <span className="ms-2 text-muted">mm</span>
          </div>
        </div>

        <div className="mb-3 pt-2">
          <label className="form-label">Camera Sensor Diagonal Dimension</label>
          <div className="d-flex align-items-center">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("cameraSensorSize")}
            />
            <span className="ms-2 text-muted">mm</span>
          </div>
        </div>

        <div className="mb-3 pt-2">
          <label className="form-label">Barlow/Reducer Factor</label>
          <div className="d-flex align-items-center">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("barlowReducerFactor")}
            />
            <span className="ms-2 text-muted">x</span>
          </div>
        </div>

        <div className="mb-3 pt-2">
          <label className="form-label">Exposure Time</label>
          <div className="d-flex align-items-center">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("exposure")}
            />
            <span className="ms-2 text-muted">secs</span>
          </div>
        </div>

        <div className="mb-3">
          <label className="form-label">FOV Center - RA</label>
          <div className="d-flex align-items-center">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("fovCenterRaH", {
                min: {
                  value: 0,
                  message: "Hour must be greater than or equal to 0",
                },
                max: {
                  value: 23,
                  message: "Hour must be less than or equal to 23",
                },
              })}
            />
            <span className="ms-2 text-muted pe-4">hours</span>
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("fovCenterRaM", {
                min: {
                  value: 0,
                  message: "Minute must be greater than or equal to 0",
                },
                max: {
                  value: 59,
                  message: "Minute must be less than or equal to 59",
                },
              })}
            />
            <span className="ms-2 text-muted pe-4">mins</span>
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("fovCenterRaS", {
                min: {
                  value: 0,
                  message: "Second must be greater than or equal to 0",
                },
                max: {
                  value: 59,
                  message: "Second must be less than or equal to 59",
                },
              })}
            />
            <span className="ms-2 text-muted pe-4">secs</span>
          </div>
          {errors.fovCenterRaH && (
            <div className="text-danger mt-1">
              {errors.fovCenterRaH.message}
            </div>
          )}
          {errors.fovCenterRaM && (
            <div className="text-danger mt-1">
              {errors.fovCenterRaM.message}
            </div>
          )}
          {errors.fovCenterRaS && (
            <div className="text-danger mt-1">
              {errors.fovCenterRaS.message}
            </div>
          )}
        </div>

        <div className="mb-3 pt-2">
          <label className="form-label">FOV Center - Dec</label>
          <div className="d-flex align-items-center">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("fovCenterDec", {
                min: {
                  value: -90,
                  message: "Declination must be greater than or equal to -90",
                },
                max: {
                  value: 90,
                  message: "Declination must be less than or equal to 90",
                },
              })}
            />
            <span className="ms-2 text-muted">deg</span>
          </div>
          {errors.fovCenterDec && (
            <div className="text-danger mt-1">
              {errors.fovCenterDec.message}
            </div>
          )}
        </div>

        <div className="mb-3 pt-2">
          <label className="form-label">Latitude</label>
          <div className="d-flex align-items-center">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("latitude", {
                min: {
                  value: -90,
                  message: "Latitude must be greater than or equal to -90",
                },
                max: {
                  value: 90,
                  message: "Latitude must be less than or equal to 90",
                },
              })}
            />
            <span className="ms-2 text-muted">deg</span>
          </div>
          {errors.latitude && (
            <div className="text-danger mt-1">{errors.latitude.message}</div>
          )}
        </div>

        <div className="mb-3 pt-2">
          <label className="form-label">Longitude</label>
          <div className="d-flex align-items-center">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("longitude", {
                min: {
                  value: -180,
                  message: "Longitude must be greater than or equal to -180",
                },
                max: {
                  value: 180,
                  message: "Longitude must be less than or equal to 180",
                },
              })}
            />
            <span className="ms-2 text-muted">deg</span>
          </div>
          {errors.longitude && (
            <div className="text-danger mt-1">{errors.longitude.message}</div>
          )}
        </div>

        <div className="mb-3 pt-2">
          <label className="form-label">Altitude</label>
          <div className="d-flex align-items-center">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("altitude")}
            />
            <select
              className="form-select w-auto"
              {...register("altitudeUnit")}
            >
              <option value="m">m</option>
              <option value="ft">ft</option>
            </select>
          </div>
        </div>

        <div className="mb-3">
          <label className="form-label">Select Flight Data Source</label>
          <div className="form-check">
            <input
              type="radio"
              className="form-check-input"
              value="live"
              {...register("flightDataType")}
            />
            <label className="form-check-label">Live Data</label>
          </div>
          <div className="form-check">
            <input
              type="radio"
              className="form-check-input"
              value="simulated"
              {...register("flightDataType")}
            />
            <label className="form-check-label">Simulated Data</label>
          </div>
        </div>

        {flightDataType === "simulated" && (
          <>
            <h3>Add Simulated Flight</h3>
            <div className="mb-3">
              <label className="form-label">Altitude</label>
              <div className="d-flex align-items-center">
                <input
                  type="number"
                  step="any"
                  className="form-control w-auto"
                  value={newFlight.altitude}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, altitude: e.target.value })
                  }
                />
                <span className="ms-2 text-muted">m</span>
              </div>
            </div>

            <div className="mb-3">
              <label className="form-label">Speed</label>
              <div className="d-flex align-items-center">
                <input
                  type="number"
                  step="any"
                  className="form-control w-auto"
                  value={newFlight.speed}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, speed: e.target.value })
                  }
                />
                <span className="ms-2 text-muted">kmh</span>
              </div>
            </div>

            <div className="mb-3">
              <label className="form-label">Latitude</label>
              <div className="d-flex align-items-center">
                <input
                  type="number"
                  step="any"
                  className="form-control w-auto"
                  value={newFlight.latitude}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, latitude: e.target.value })
                  }
                />
                <span className="ms-2 text-muted">deg</span>
              </div>
            </div>

            <div className="mb-3">
              <label className="form-label">Longitude</label>
              <div className="d-flex align-items-center">
                <input
                  type="number"
                  step="any"
                  className="form-control w-auto"
                  value={newFlight.longitude}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, longitude: e.target.value })
                  }
                />
                <span className="ms-2 text-muted">deg</span>
              </div>
            </div>

            <div className="mb-3">
              <label className="form-label">Heading</label>
              <div className="d-flex align-items-center">
                <input
                  type="number"
                  step="any"
                  className="form-control w-auto"
                  value={newFlight.heading}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, heading: e.target.value })
                  }
                />
                <span className="ms-2 text-muted">deg</span>
              </div>
            </div>

            <div>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={addSimulatedFlight}
              >
                Add Flight
              </button>
            </div>
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
          </>
        )}
        <div>
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </div>
      </form>
      <FlightTable data={flightData} />
    </div>
  );
}

export default FlightPredictor;
