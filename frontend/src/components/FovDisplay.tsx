import React from "react";
import { Col, Row, Alert } from "react-bootstrap";
import FlightPath from "./FlightPath";

const FovDisplay = ({
  isLoading,
  errorMessage,
  flightData,
  isSatelliteDataEmpty,
  counter,
  visibleSatellites,
  currentExposureTime,
  remainingTimePercentage,
}) => {
  return (
    <Col className="mx-auto text-center">
      <Row>
        <div className="fov-title">Your Field of View</div>
      </Row>
      <div className="fov-frame">
        {/* Loading Message */}
        {isLoading && (
          <Row className="message-box mt-3">
            <Alert variant="info" className="message">
              Scanning the sky...
            </Alert>
          </Row>
        )}
        {/* Error Message */}
        {errorMessage && (
          <Row className="message-box mt-3">
            <Alert variant="danger" className="message">
              {errorMessage}
            </Alert>
          </Row>
        )}
        {/* Render satellites and their future positions */}
        {!errorMessage &&
          !isLoading &&
          Object.values(flightData).map((satelliteDataForSecond, index) => {
            if (isSatelliteDataEmpty) {
              return (
                <Row className="message-box mt-3" key={`empty-${index}`}>
                  <Alert variant="info" className="message">
                    No Satellite Interference Found.
                  </Alert>
                </Row>
              );
            }

            return satelliteDataForSecond.map((satellite) => {
              const { sid, delta_radius, delta_theta } = satellite;

              let dotColor = "blue-dot";
              if (index === 0) dotColor = "green-dot";
              else if (index === satelliteDataForSecond.length - 2) dotColor = "red-dot";

              if (index >= counter) {
                // Calculate future position
                const x = delta_radius * Math.sin(delta_theta * (Math.PI / 180));
                const y = delta_radius * Math.cos(delta_theta * (Math.PI / 180));
                const right = 0.5 - x / 2 - 0.07;
                const top = 0.5 - y / 2 - 0.07;

                const rightPercentage = `${right * 100 + 7}%`;
                const topPercentage = `${top * 100 + 7}%`;

                // Render red dot for future position only if the satellite is visible
                if (visibleSatellites.some((visibleSatellite) => visibleSatellite.sid === sid)) {
                  return (
                    <div
                      key={sid}
                      className={dotColor}
                      style={{
                        position: "absolute",
                        right: rightPercentage,
                        top: topPercentage,
                      }}
                    />
                  );
                }
              }
              return null;
            });
          })}
        {/* Render currently visible satellites */}
        {!errorMessage &&
          !isLoading &&
          visibleSatellites.map((satellite, index) => (
            <Satellite key={index} satellite={satellite} />
          ))}
      </div>
      {/* Exposure time pill */}
      {!errorMessage && !isLoading && (
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
