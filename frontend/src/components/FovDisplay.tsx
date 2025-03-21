import React from "react";
import { Col, Row, Alert } from "react-bootstrap";
import Airplane from "./Airplane";
import "./FovDisplay.css";

interface FovDisplayProps {
  isLoading: boolean;
  flightData: any; // Replace 'any' with the appropriate type
  isFlightDataEmpty: boolean;
  fovCenterRA: number;
  fovCenterDec: number;
  visibleFlights: any; // Replace 'any' with the appropriate type
  currentExposureTime: number;
  remainingTimePercentage: number;
}

const FovDisplay: React.FC<FovDisplayProps> = ({
  isLoading,
  flightData,
  isFlightDataEmpty,
  fovCenterRA,
  fovCenterDec,
  visibleFlights,
  currentExposureTime,
  remainingTimePercentage,
}) => {
  return (
    <div className="container">
      <div className="fov-title">Field of View</div>
      <div className="fov-frame">
        {isLoading && (
          <Row className="message-box mt-3">
            <Alert variant="info" className="message">
              Scanning the sky...
            </Alert>
          </Row>
        )}
        {!isLoading &&
          Object.values(flightData).map((satelliteDataForSecond, index) => {
            if (isFlightDataEmpty) {
              return (
                <Row className="message-box mt-3" key={`empty-${index}`}>
                  <Alert variant="info" className="message">
                    No airplane interference found.
                  </Alert>
                </Row>
              );
            }
            return null;
          })}
        {/* Render currently visible satellites */}
        {!isLoading &&
          visibleFlights.map((flight: any, index: number) => (
            <Airplane
              key={index}
              flight={flight}
              fovCenter={{ RA: fovCenterRA, Dec: fovCenterDec }}
            />
          ))}
      </div>
      {/* Exposure time pill */}
      {!isLoading && (
        <>
        <div className="pill-title">Next {currentExposureTime} seconds</div>
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
