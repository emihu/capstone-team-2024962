import React from "react";

function HowToUse() {
  return (
    <div className="container mt-4">
      <h1>How to Use the Flight Predictor</h1>
      <p>
        The Flight Predictor tool is designed to help you identify potential
        flight interferences with your field of view (FOV). Follow these simple
        steps to get started:
      </p>
      <h2>Step 1: Enter Your Parameters</h2>
      <p>Use the input fields to provide details about your setup:</p>
      <ul>
        <li>
          <strong>Focal Length:</strong> The focal length of your telescope or
          camera lens in millimeters.
        </li>
        <li>
          <strong>Camera Sensor Size:</strong> The size of your camera sensor in
          millimeters.
        </li>
        <li>
          <strong>Barlow/Reducer Factor:</strong> Any magnification or reduction
          factor applied by additional optics.
        </li>
        <li>
          <strong>Exposure Time:</strong> The duration of your observation in
          seconds.
        </li>
        <li>
          <strong>FOV Center (RA/Dec):</strong> The right ascension (RA) and
          declination (Dec) of the center of your FOV.
        </li>
      </ul>

      <h2>Step 2: Submit the Data</h2>
      <p>
        Click the <strong>Submit</strong> button to process your input and
        predict flight interferences. The application will calculate the field
        of view and display relevant flight paths within your defined area.
      </p>

      <h2>Step 3: View the Results</h2>
      <p>The results will include:</p>
      <ul>
        <li>
          A table displaying flight information, such as altitude, speed, and
          coordinates.
        </li>
        <li>An interactive map plotting flight paths and your FOV boundary.</li>
      </ul>

      <h2>Step 4: Customize the FOV</h2>
      <p>
        Use the map to explore and visualize the field of view. You can adjust
        the input parameters and resubmit to refine the results.
      </p>

      <h2>Tips</h2>
      <ul>
        <li>Ensure all input values are accurate for the best results.</li>
        <li>
          Use the interactive map to better understand flight positions and
          movements.
        </li>
        <li>
          Contact support if you encounter any issues or have additional feature
          requests.
        </li>
      </ul>
    </div>
  );
}

export default HowToUse;
