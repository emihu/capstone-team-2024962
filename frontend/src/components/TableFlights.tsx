import React from "react";

interface Flight {
  id: number;
  flight_number: string;
  altitude: number;
  heading: number;
  latitude: number;
  longitude: number;
  speed: number;
  entry: string;
  exit: string;
}

interface TableFlightsProps {
  data: Flight[];
}

const TableFlights: React.FC<TableFlightsProps> = ({ data }) => {
  return (
    <>
      {data.length === 0 ? (
        <br></br>
      ) : (
        <div>
          <div className="table-responsive">
            <table className="table table-striped table-bordered table-light">
              <thead className="thead-dark">
                <tr>
                  <th>ID</th>
                  <th>Flight Number</th>
                  <th>Altitude (feet)</th>
                  <th>Heading (deg)</th>
                  <th>Latitude (deg)</th>
                  <th>Longitude (deg)</th>
                  <th>Speed (knots)</th>
                  <th>FOV Entry Time</th>
                  <th>FOV Exit Time</th>
                </tr>
              </thead>
              <tbody>
                {data.map((flight, index) => (
                  <tr key={index}>
                    <td>{flight.id}</td>
                    <td>{flight.flight_number}</td>
                    <td>{flight.altitude}</td>
                    <td>{flight.heading}</td>
                    <td>{flight.latitude}</td>
                    <td>{flight.longitude}</td>
                    <td>{flight.speed}</td>
                    <td>{flight.entry}</td>
                    <td>{flight.exit}</td>
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
