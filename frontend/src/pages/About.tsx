import React from "react";

function About() {
  return (
    <div className="container mt-4">
      <h1>About</h1>
      <p>
        Welcome to SkyClear, a flight prediction tool! This platform is designed
        to help you analyze and visualize flight paths that may interfere with
        specific fields of view (FOV) for telescopic observations or other
        activities.
      </p>
      <h2>Features</h2>
      <ul>
        <li>
          Input parameters such as focal length, camera sensor size, and more to
          define your FOV.
        </li>
        <li>Visualize flight data on an interactive map.</li>
        <li>Display flight details, including altitude, speed, and heading.</li>
        <li>Customize the FOV's radius and center coordinates.</li>
      </ul>
      <h2>Our Mission</h2>
      <p>
        Our goal is to provide an intuitive tool for users to assess potential
        flight interferences with their observation fields. Whether you're an
        astronomer, scientist, or aviation enthusiast, this platform offers
        accurate and real-time flight analysis.
      </p>
      <h2>Contact Us</h2>
      <p>
        Have questions or suggestions? Reach out to us at{" "}
        <a href="mailto:emilyy.hu@mail.utoronto.ca">
          emilyy.hu@mail.utoronto.ca
        </a>
        .
      </p>
    </div>
  );
}

export default About;
