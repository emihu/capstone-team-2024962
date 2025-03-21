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
    <Col className="mx-auto text-center">
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
            // return satelliteDataForSecond.map((satellite) => {
            //   const { sid, delta_radius, delta_theta } = satellite;

            //   let dotColor = "blue-dot";
            //   if (index === 0) dotColor = "green-dot";
            //   else if (index === satelliteDataForSecond.length - 2) dotColor = "red-dot";

            //   if (index >= counter) {
            //     // Calculate future position
            //     const x = delta_radius * Math.sin(delta_theta * (Math.PI / 180));
            //     const y = delta_radius * Math.cos(delta_theta * (Math.PI / 180));
            //     const right = 0.5 - x / 2 - 0.07;
            //     const top = 0.5 - y / 2 - 0.07;

            //     const rightPercentage = `${right * 100 + 7}%`;
            //     const topPercentage = `${top * 100 + 7}%`;

            //     // Render red dot for future position only if the satellite is visible
            //     if (visibleFlights.some((visibleFlights) => visibleFlights.sid === sid)) {
            //       return (
            //         <div
            //           key={sid}
            //           className={dotColor}
            //           style={{
            //             position: "absolute",
            //             right: rightPercentage,
            //             top: topPercentage,
            //           }}
            //         />
            //       );
            //     }
            //   }
            //   return null;
            // });
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
        <div>
          <Row>
            <div className="pill-title">Next {currentExposureTime} seconds</div>
          </Row>
          <div className="col exposure-pill-container">
            <div
              className="exposure-pill"
              style={{ width: `${remainingTimePercentage}%` }}
            ></div>
          </div>
        </div>
      )}
    </Col>
  );
};

export default FovDisplay;
