import React, { useState } from "react";
import "./Airplane.css"; 
import flightImage from "../assets/Airplane.png";
import AirplaneCard from "./AirplaneCard";

interface AirplaneProps {
    flight: {
      ID: string;  
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
  var delta_RA = RA - fovCenter.RA;  // Difference from FOV center (degrees)
  if (delta_RA > 180) {
    delta_RA = -(360 - delta_RA);
  } else if (delta_RA < -180) {
    delta_RA = 360 + delta_RA;
  }
  var delta_Dec = Dec - fovCenter.Dec;  // Difference from FOV center (degrees)

  // Convert RA/Dec offsets into FOV frame coordinates
  const x = delta_RA / fovCenter.Size; // Normalize for display
  const y = delta_Dec / fovCenter.Size; // Normalize for display

  // Convert to CSS positioning
  const right = 0.5 - x / 2;
  const rightPercentage = `${right * 100}%`;

  const top = 0.5 - y / 2;
  const topPercentage = `${top * 100}%`;

  // const leftPercentage = `${(0.5 + x) * 100}%`;
  // const topPercentage = `${(0.5 - y) * 100}%`; // Invert Y-axis (CSS top-down)

  return (
    <div
      className="airplane"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        top: topPercentage,
        right: rightPercentage,
      }}
    >
      <img src={flightImage} alt={`Flight ${ID}`} className="airplane-image" style={{ transform: `rotate(${Heading}deg)` }}/>
      {isHovered && <AirplaneCard id={ID} flightNumber={FlightNumber}/>}
    </div>
  );
};

export default Airplane;
