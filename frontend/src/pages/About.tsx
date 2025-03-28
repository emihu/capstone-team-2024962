import { Container, Row, Col, Card } from "react-bootstrap";
import { FaEnvelope, FaPlane, FaMapMarkedAlt, FaGlobe } from "react-icons/fa";
import "./About.css";

function About() {
  return (
    <Container fluid className="mt-5 mb-5">
      <Row className="justify-content-center">
        <Col md={8}>
          <Card className="p-4 shadow-sm border-0 bg-light">
            <h2 className="text-center mb-4 navy">About ClearSkies</h2>
            <p className="text-muted text-center">
              Predict and prevent aircraft light trail interference in
              astrophotography.
            </p>

            <p>
              Welcome to ClearSkies, a flight prediction tool! This platform is
              designed to help you analyze and visualize flight paths that may
              interfere with your telescope's fields of view (FOV). Whether
              you're an astronomer, scientist, or astrophotography enthusiast,
              ClearSkies provides accurate real-time flight analysis to prevent
              aircraft light trails from impacting the quality of your images.
            </p>
            <h4 className="mt-4 navy">
              <FaGlobe className="me-2 navy" /> Our Mission
            </h4>
            <p>
              Our goal is to provide a software solution that predicts when an
              aircraft will cross a telescope’s field of view and its duration,
              and warns the user against capturing an image during this
              interval. We have accomplished this by leveraging real-time data
              and predictive modeling to help users make informed decisions and
              minimize aircraft light trail interference in astrophotography.
            </p>

            <h4 className="mt-4 navy">
              <FaPlane className="me-2 navy" /> Why ClearSkies?
            </h4>
            <p>
              The idea for ClearSkies was born out of the need to eliminate
              aircraft light trail interferences that contaminate and degrade
              the quality of astronomical images. This has become a growing
              concern as global air traffic increased by ~120% from 2020 to
              2023, and is predicted to continue to rise in the future.
              Furthermore, existing methods lower productivity and destroy fine
              detail in images with a low signal to noise ratio. ClearSkies
              fills this gap by using real-time flight predictions to provide a
              preventative solution that addresses the issue of aircraft light
              trail contamination.
            </p>

            <h4 className="mt-4 navy">
              <FaMapMarkedAlt className="me-2 navy" /> Key Features
            </h4>
            <ul>
              <li>Define your telescope's FOV and observer parameters.</li>
              <li>Track real-time flight paths on an interactive map.</li>
              <li>
                View flight details, including intersection times with the
                telescope's FOV.
              </li>
              <li>Simulate flight paths for testing and demos.</li>
            </ul>

            <h4 className="mt-4 navy">
              <FaEnvelope className="me-2 navy" /> Contact Us
            </h4>
            <p>
              Have questions or suggestions? Reach out to us at{" "}
              <a href="mailto:emilyy.hu@mail.utoronto.ca">
                emilyy.hu@mail.utoronto.ca
              </a>
              ,{" "}
              <a href="mailto:l.fan@mail.utoronto.ca">l.fan@mail.utoronto.ca</a>
              , and{" "}
              <a href="mailto:andrewchapman.leung@mail.utoronto.ca">
                andrewchapman.leung@mail.utoronto.ca
              </a>
              .
            </p>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default About;
