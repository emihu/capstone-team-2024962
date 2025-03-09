import React from "react";
import MapFlights from "./MapFlights"; // Adjust the import path as needed

interface Flight {
  flight_number: string;
  altitude: number;
  heading: number;
  latitude: number;
  longitude: number;
  speed: number;
}

interface TableFlightsProps {
  data: Flight[];
}

const TableFlights: React.FC<TableFlightsProps> = ({ data }) => {
  return (
    <>
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
                {data.map((flight, index) => (
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
        </div>
      )}
    </>
  );
};

export default TableFlights;
