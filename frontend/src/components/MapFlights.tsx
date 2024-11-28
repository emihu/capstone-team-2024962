import React, { useEffect } from "react";
import L from "leaflet";

interface MapFlightsProps {
  data: any[];
  fovBorder: { lat: number; lon: number; radius: number };
}

function MapFlights({ data, fovBorder }: MapFlightsProps) {
  useEffect(() => {
    // Initialize the map
    const map = L.map("map").setView([data[0].latitude, data[0].longitude], 6); // Default center and zoom

    // Add a tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    // Add markers for each flight
    data.forEach((flight) => {
      L.marker([flight.latitude, flight.longitude])
        .addTo(map)
        .bindPopup(
          `<strong>Flight Number:</strong> ${flight.flight_number}<br><strong>Altitude:</strong> ${flight.altitude} ft<br><strong>Speed:</strong> ${flight.speed} knots`
        );
    });

    // Add non-filled circle around the flight's coordinates
    const radiusInMeters = Math.abs(fovBorder.radius);
    L.circle([fovBorder.lat, fovBorder.lon], {
      color: "blue", // Border color
      fillColor: "transparent", // No fill
      fillOpacity: 0, // Ensure no fill
      radius: radiusInMeters * 1.1, // Radius in meters
    }).addTo(map);

    return () => {
      map.remove();
    };
  }, [data]);

  return <div id="map" style={{ height: "500px", width: "100%" }} />;
}

export default MapFlights;
