import { useState, useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import "bootstrap/dist/css/bootstrap.css";

import FlightTable from "../components/TableFlights";
import FovDisplay from "../components/FovDisplay";
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
      datetime: ""
    },
  });

  const [flightsPosition, setFlightsPosition] = useState<any[]>([]);
  const [flightData, setFlightData] = useState<any[]>([]);

  const [simulatedFlights, setSimulatedFlights] = useState<any[]>([]);
  const [newFlight, setNewFlight] = useState({
    altitude: "",
    altitudeUnit: "m",
    speed: "",
    speedUnit: "knots",
    latitude: "",
    longitude: "",
    heading: "",
  });
  const [exposureTime, setExposureTime] = useState<number>(0);
  const [fovCenterRA, setfovCenterRA] = useState<number>(0);
  const [fovCenterDec, setfovCenterDec] = useState<number>(0);
  const [counter, setCounter] = useState(0);
  const [visibleFlights, setvisibleFlights] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const flightDataType = watch("flightDataType");

  const remainingTimePercentage =
    ((exposureTime - counter) / exposureTime) * 100;

  const isFlightDataEmpty = Object.values(flightData).every(
    (arr) => arr.length === 0
  );

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCounter((prevCounter) =>
        prevCounter >= flightsPosition.length - 1 ? 0 : prevCounter + 1
      );
    }, 250);

    return () => clearInterval(intervalId);
  }, [flightsPosition]);

  useEffect(() => {
    setvisibleFlights(flightsPosition[counter] || []);
  }, [counter, flightsPosition]);

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
          simulatedFlights
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
    setIsLoading(true);
    if (formData.altitudeUnit === "ft") {
      formData.altitude = (parseFloat(formData.altitude) * 0.3048).toString();
    }
    setExposureTime(formData.exposure);
    setfovCenterRA(
      formData.fovCenterRaH * 15 +
        (formData.fovCenterRaM * 15) / 60 +
        (formData.fovCenterRaS * 15) / 3600
    );
    setfovCenterDec(formData.fovCenterDec);
    fetchFlightData(formData);
    setIsLoading(false);
  };

  const addSimulatedFlight = () => {
    if (Object.values(newFlight).some((val) => val === "")) {
      console.log(Object.values(newFlight));

      alert("Error: All fields must be filled out.");
      return;
    }

    // Check if speed is greater or equal to 0
    if (parseFloat(newFlight.speed) < 0) {
      alert("Error: Speed must be greater or equal to 0.");
      return;
    }

    // Check if latitude is within valid range (-90 to 90)
    const latitude = parseFloat(newFlight.latitude);
    if (latitude < -90 || latitude > 90) {
      alert("Error: Latitude must be between -90 and 90.");
      return;
    }

    // Check if longitude is within valid range (-180 to 180)
    const longitude = parseFloat(newFlight.longitude);
    if (longitude < -180 || longitude > 180) {
      alert("Error: Longitude must be between -180 and 180.");
      return;
    }

    // Check if heading is within valid range (0 to 360)
    const heading = parseFloat(newFlight.heading);
    if (heading < 0 || heading >= 360) {
      alert("Error: Heading must be between 0 and 360.");
      return;
    }

    const altitudeValue =
      newFlight.altitudeUnit === "ft"
        ? parseFloat(newFlight.altitude)
        : parseFloat(newFlight.altitude) * 3.28084;

    const speedValue =
      newFlight.speedUnit === "kph"
        ? parseFloat(newFlight.speed) * 0.539957
        : newFlight.speedUnit === "mph"
        ? parseFloat(newFlight.speed) * 0.868976
        : parseFloat(newFlight.speed);

    setSimulatedFlights([
      ...simulatedFlights,
      { ...newFlight, altitude: altitudeValue, speed: speedValue },
    ]);
    setNewFlight({
      altitude: "",
      altitudeUnit: "m",
      speed: "",
      speedUnit: "knots",
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
        <br></br>
        <div className="row mb-3 pt-2">
          <label className="col-md-3 form-label">Focal Length</label>
          <div className="col-md-6 d-flex align-items-center gap-2">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("focalLength", {
                min: {
                  value: 0,
                  message: "Focal length must be positive",
                },
              })}
            />
            <span className="text-muted">mm</span>
          </div>
          {errors.focalLength && (
            <div className="text-danger mt-1">{errors.focalLength.message}</div>
          )}
        </div>

        <div className="row mb-3 pt-2">
          <label className="col-md-3 form-label">
            Camera Sensor Diagonal Dimension
          </label>
          <div className="col-md-6 d-flex align-items-center gap-2">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("cameraSensorSize", {
                min: {
                  value: 0,
                  message: "Camera sensor size must be positive",
                },
              })}
            />
            <span className="text-muted">mm</span>
          </div>
          {errors.cameraSensorSize && (
            <div className="text-danger mt-1">
              {errors.cameraSensorSize.message}
            </div>
          )}
        </div>

        <div className="row mb-3 pt-2">
          <label className="col-md-3 form-label">Barlow/Reducer Factor</label>
          <div className="col-md-6 d-flex align-items-center gap-2">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("barlowReducerFactor", {
                min: {
                  value: 0,
                  message: "Barlow/reducer factor must be positive",
                },
              })}
            />
            <span className="text-muted">x</span>
          </div>
          {errors.barlowReducerFactor && (
            <div className="text-danger mt-1">
              {errors.barlowReducerFactor.message}
            </div>
          )}
        </div>

        <div className="row mb-3 pt-2">
          <label className="col-md-3 form-label">Exposure Time</label>
          <div className="col-md-6 d-flex align-items-center gap-2">
            <input
              type="number"
              step="any"
              className="form-control w-auto"
              {...register("exposure", {
                min: {
                  value: 0,
                  message: "Exposure must be positive",
                },
              })}
            />
            <span className="text-muted">secs</span>
          </div>
          {errors.exposure && (
            <div className="text-danger mt-1">{errors.exposure.message}</div>
          )}
        </div>

        <div className="row mb-3 pt-2">
          <label className="col-md-3 form-label">FOV Center - RA</label>
          <div className="col-md-6 d-flex align-items-center gap-2">
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
            <span className="text-muted pe-4">hours</span>
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
            <span className="text-muted pe-4">mins</span>
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
            <span className="text-muted pe-4">secs</span>
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

        <div className="row mb-3 pt-2">
          <label className="col-md-3 form-label">FOV Center - Dec</label>
          <div className="col-md-6 d-flex align-items-center gap-2">
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
            <span className="text-muted">deg</span>
          </div>
          {errors.fovCenterDec && (
            <div className="text-danger mt-1">
              {errors.fovCenterDec.message}
            </div>
          )}
        </div>

        <div className="row mb-3 pt-2">
          <label className="col-md-3 form-label">Latitude</label>
          <div className="col-md-6 d-flex align-items-center gap-2">
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
            <span className="text-muted">deg</span>
          </div>
          {errors.latitude && (
            <div className="text-danger mt-1">{errors.latitude.message}</div>
          )}
        </div>

        <div className="row mb-3 pt-2">
          <label className="col-md-3 form-label">Longitude</label>
          <div className="col-md-6 d-flex align-items-center gap-2">
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
            <span className="text-muted">deg</span>
          </div>
          {errors.longitude && (
            <div className="text-danger mt-1">{errors.longitude.message}</div>
          )}
        </div>

        <div className="row mb-3 pt-2">
          <label className="col-md-3 form-label">Altitude</label>
          <div className="col-md-6 d-flex align-items-center gap-2">
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
          <div className="p-4" style={{ backgroundColor: "#e6e6e6" }}>
            <div className="row mb-3 pt-2">
              <label className="col-md-3 form-label">Date and Time</label>
              <div className="col-md-6 d-flex align-items-center gap-2">
              <input
                type="datetime-local"
                className="form-control w-auto"
                {...register("datetime")}
              />
              </div>
            </div>

            <h4>Add Simulated Flight</h4>

            <div className="row mb-3 pt-2">
              <label className="col-md-3 form-label">Altitude</label>
              <div className="col-md-6 d-flex align-items-center gap-2">
                <input
                  type="number"
                  step="any"
                  className="form-control w-auto"
                  value={newFlight.altitude}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, altitude: e.target.value })
                  }
                />
                <select
                  className="form-select w-auto"
                  value={newFlight.altitudeUnit}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, altitudeUnit: e.target.value })
                  }
                >
                  <option value="m">m</option>
                  <option value="ft">ft</option>
                </select>
              </div>
            </div>

            <div className="row mb-3 pt-2">
              <label className="col-md-3 form-label">Speed</label>
              <div className="col-md-6 d-flex align-items-center gap-2">
                <input
                  type="number"
                  step="any"
                  className="form-control w-auto"
                  value={newFlight.speed}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, speed: e.target.value })
                  }
                />
                <select
                  className="form-select w-auto"
                  value={newFlight.speedUnit}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, speedUnit: e.target.value })
                  }
                >
                  <option value="knots">knots</option>
                  <option value="kph">kph</option>
                  <option value="mph">mph</option>
                </select>
              </div>
            </div>

            <div className="row mb-3 pt-2">
              <label className="col-md-3 form-label">Latitude</label>
              <div className="col-md-6 d-flex align-items-center gap-2">
                <input
                  type="number"
                  step="any"
                  className="form-control w-auto"
                  value={newFlight.latitude}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, latitude: e.target.value })
                  }
                />
                <span className="text-muted">deg</span>
              </div>
            </div>

            <div className="row mb-3 pt-2">
              <label className="col-md-3 form-label">Longitude</label>
              <div className="col-md-6 d-flex align-items-center gap-2">
                <input
                  type="number"
                  step="any"
                  className="form-control w-auto"
                  value={newFlight.longitude}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, longitude: e.target.value })
                  }
                />
                <span className="text-muted">deg</span>
              </div>
            </div>

            <div className="row mb-3 pt-2">
              <label className="col-md-3 form-label">Heading</label>
              <div className="col-md-6 d-flex align-items-center gap-2">
                <input
                  type="number"
                  step="any"
                  className="form-control w-auto"
                  value={newFlight.heading}
                  onChange={(e) =>
                    setNewFlight({ ...newFlight, heading: e.target.value })
                  }
                />
                <span className="text-muted">deg</span>
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

            <h4>Simulated Flights</h4>
            <p>*NOTE: Altitude is converted to feet and speed is converted to knots.</p>
            <div className="table-responsive">
              <table className="table table-striped table-bordered table-light">
                <thead className="thead-dark">
                  <tr>
                    <th>Flight Number</th>
                    <th>Altitude (feet)</th>
                    <th>Speed (knots)</th>
                    <th>Latitude (deg)</th>
                    <th>Longitude (deg)</th>
                    <th>Heading (deg)</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {simulatedFlights.map((flight: any, index: number) => (
                    <tr key={index}>
                      <td>{`SIM${index + 1}`}</td>
                      <td>{flight.altitude}</td>
                      <td>{flight.speed}</td>
                      <td>{flight.latitude}</td>
                      <td>{flight.longitude}</td>
                      <td>{flight.heading}</td>
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
        <div>
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </div>
      </form>
      <FlightTable data={flightData} />
      <FovDisplay
        isLoading={isLoading}
        flightData={flightData}
        isFlightDataEmpty={isFlightDataEmpty}
        fovCenterRA={fovCenterRA}
        fovCenterDec={fovCenterDec}
        visibleFlights={visibleFlights}
        currentExposureTime={exposureTime}
        remainingTimePercentage={remainingTimePercentage}
      />
    </div>
  );
}

export default FlightPredictor;
