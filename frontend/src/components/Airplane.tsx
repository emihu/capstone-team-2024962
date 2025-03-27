import React, { useState } from "react";
import "./Airplane.css"; // Use similar styles as Satellite
import flightImage from "../assets/Airplane.png"; // Flight image
import AirplaneCard from "./AirplaneCard";

// USE:
// import AirplaneProps from "./Airplane";

// // Example data from backend
// const flightsData = [
//   { ID: "F123", RA: 120.5, Dec: 45.2 },
//   { ID: "F456", RA: 115.3, Dec: 50.1 },
// ];

// const fovCenter = { RA: 118.0, Dec: 48.0 };

// {flightsData.map((flight) => (
//   <Flight key={flight.ID} flight={flight} fovCenter={fovCenter} />
// ))}

interface AirplaneProps {
    flight: {
      ID: string;  // Flight ID (can be a string or number)
      FlightNumber: string
      RA: number;  // Right Ascension in degrees
      Dec: number; // Declination in degrees
      Heading: number;
    };
    fovCenter: {
      RA: number;  // FOV Center Right Ascension
      Dec: number; // FOV Center Declination
      Size: number;
    };
}

const Airplane: React.FC<AirplaneProps> = ({ flight, fovCenter }) => {
  const { ID, FlightNumber, RA, Dec, Heading } = flight;
  const [isHovered, setIsHovered] = useState(false);

  // Compute relative position in FOV
  const delta_RA = RA - fovCenter.RA;  // Difference from FOV center (degrees)
  const delta_Dec = Dec - fovCenter.Dec;  // Difference from FOV center (degrees)

  // Convert RA/Dec offsets into FOV frame coordinates
  const x = delta_RA / fovCenter.Size; // Normalize for display
  const y = delta_Dec / fovCenter.Size; // Normalize for display

  // Convert to CSS positioning
  const right = 0.5 - x / 2;
  const rightPercentage = `${right * 100}%`;

  const top = 0.5 - y / 2;
  const topPercentage = `${top * 100}%`;

  return (
    <div
      className="airplane"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        position: "absolute",
        top: topPercentage,
        right: rightPercentage,
        transform: "translate(50%, -50%)"
      }}
    >
      <img src={flightImage} alt={`Flight ${ID}`} className="airplane-image" style={{ transform: `rotate(${Heading}deg)` }}/>
      {isHovered && <AirplaneCard id={ID} flightNumber={FlightNumber}/>}
    </div>
  );
};

export default Airplane;
