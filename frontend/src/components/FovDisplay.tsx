import React from "react";
import { Row, Alert } from "react-bootstrap";
import Airplane from "./Airplane";
import Stars from "./Stars";
import "./FovDisplay.css";

interface FovDisplayProps {
  isLoading: boolean;
  flightData: any; // Replace 'any' with the appropriate type
  isFlightDataEmpty: boolean;
  fovCenterRA: number;
  fovCenterDec: number;
  fovSize: number;
  visibleFlights: any; // Replace 'any' with the appropriate type
  currentExposureTime: number;
  elapsedTime: number;
  remainingTimePercentage: number;
}

const FovDisplay: React.FC<FovDisplayProps> = ({
  isLoading,
  isFlightDataEmpty,
  fovCenterRA,
  fovCenterDec,
  fovSize,
  visibleFlights,
  elapsedTime,
  remainingTimePercentage,
}) => {
  return (
    <div className="container">
      <div className="fov-title">Field of View</div>
      <div className="fov-frame">
        <Stars numberOfStars={60} />
        {isLoading && (
          <Row className="message-box mt-3">
            <Alert variant="info" className="message">
              Scanning the sky...
            </Alert>
          </Row>
        )}
        {!isLoading && isFlightDataEmpty && (
          <Row className="message-box mt-3">
            <Alert variant="light" className="message">
              No airplane interference found.
            </Alert>
          </Row>
        )}
        {!isLoading &&
          visibleFlights.map((flight: any, index: number) => (
            <Airplane
              key={index}
              flight={flight}
              fovCenter={{ RA: fovCenterRA, Dec: fovCenterDec, Size: fovSize }}
            />
          ))}
      </div>
      {/* Exposure time pill */}
      {!isLoading && (
        <>
          <div className="pill-title">Time elapsed: {elapsedTime} seconds</div>
          <div className="exposure-pill-container">
            <div
              className="exposure-pill"
              style={{ width: `${remainingTimePercentage}%` }}
            ></div>
          </div>
        </>
      )}
    </div>
  );
};

export default FovDisplay;
