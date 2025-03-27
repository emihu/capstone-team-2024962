import React from "react";
import PropTypes from "prop-types";
import "./AirplaneCard.css";

interface AirplaneCardProps {
    id: string
    flightNumber: string
}

const AirplaneCard: React.FC<AirplaneCardProps> = ({ id, flightNumber }) => {
  return (
    <div className="tooltip-card">
      <div className="tooltip-row">
        <span className="tooltip-title">ID</span>
        <span className="vertical-line"></span>
        <span className="tooltip-value">{id}</span>
      </div>
      <div className="tooltip-row">
        <span className="tooltip-title">FLIGHT NUMBER</span>
        <span className="tooltip-value">{flightNumber}</span>
      </div>
    </div>
  );
};

export default AirplaneCard;