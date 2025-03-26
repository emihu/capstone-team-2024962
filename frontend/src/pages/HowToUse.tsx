import { Container, Row, Col, Card } from "react-bootstrap";
import "./HowToUse.css";

function HowToUse() {
  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={8}>
          <Card className="p-4 shadow-sm border-0 bg-light">
            <h2 className="text-center mb-4 navy">How to Use</h2>

            <h4 className="mt-4 navy">
              Step 1: Enter your parameters
            </h4>
            <p>Provide details about your telescope and observation setup:</p>
            <ul>
              <li><strong>Focal Length:</strong> Telescope or camera lens focal length [mm].</li>
              <li><strong>Camera Sensor Size:</strong> Sensor dimensions [mm].</li>
              <li><strong>Barlow/Reducer Factor:</strong> Magnification or reduction factor applied.</li>
              <li><strong>Exposure Time:</strong> Duration of your observation [seconds].</li>
              <li><strong>FOV Center RA:</strong> Right Ascension (RA) of your telescope's field of view (FOV) center [hours, minutes, seconds].</li>
              <li><strong>FOV Center Dec:</strong> Declination (Dec) of your telescope's FOV center [degrees].</li>
              <li><strong>Latitude:</strong> Latitude of the observer [degrees].</li>
              <li><strong>Longitude:</strong> Longitude of the observer [degrees].</li>
              <li><strong>Altitude:</strong> Altitude of the observer [degrees].</li>
            </ul>
            <p>Note: values can be in decimal format.</p>

            <h4 className="mt-4 navy">
              Step 2: Choose between live and simulated data
            </h4>
            <p>
              Select either <strong>Live Data</strong> or <strong>Simulated Data</strong> as the flight data source.
              Live data will use real-time flight data from the FlightRadar24 API. 
              While, simulated data will allow you to manually input flight data including its altitiude, speed, latitude, longitude, and heading.
              Multiple simulated flights are supported and you can delete any unwanted flights.
            </p>

            <h4 className="mt-4 navy">
              Step 3: Submit your data
            </h4>
            <p>
              Click the <strong>Submit</strong> button to process your input. SkyClear will analyze real-time flight 
              data or use the customized simulated flight data to identify potential interferences.
            </p>

            <h4 className="mt-4 navy">
              Step 4: View the results
            </h4>
            <p>Information on any flight path intersections with the telescope's FOV will be displayed in the following formats:</p>
            <ul>
              <li>A table displaying flight details (altitude, speed, heading, intersection time, etc).</li>
              <li>A visualization plotting any flight path intersections within your telescope's FOV over the next exposure period.</li>
            </ul>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default HowToUse;
