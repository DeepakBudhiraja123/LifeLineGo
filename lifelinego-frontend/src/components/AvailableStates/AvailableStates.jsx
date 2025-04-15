import React, { useState } from "react";
import "./AvailableStates.css";

const AvailableStates = () => {
  const [hoveredState, setHoveredState] = useState(null);

  const states = [
    { name: "Maharashtra", id: "maharashtra" },
    { name: "Delhi", id: "delhi" },
    { name: "Karnataka", id: "karnataka" },
    { name: "Tamil Nadu", id: "tamilnadu" },
    { name: "Uttar Pradesh", id: "uttarpradesh" },
    { name: "Gujarat", id: "gujarat" },
    { name: "West Bengal", id: "westbengal" },
    { name: "Rajasthan", id: "rajasthan" },
    { name: "Punjab", id: "punjab" },
    { name: "Haryana", id: "haryana" },
    { name: "Madhya Pradesh", id: "madhyapradesh" },
    { name: "Odisha", id: "odisha" },
    { name: "Assam", id: "assam" },
    { name: "Kerala", id: "kerala" },
  ];

  const stateMaps = {
    default: "/Default.png",  // Default map with all states in blue
    maharashtra: "/Maharashtra.png",
    delhi: "/Delhi.png",
    karnataka: "/Karnataka.png",
    tamilnadu: "/TamilNadu.png",
    uttarpradesh: "/UP.png",
    gujarat: "/Gujarat.png",
    westbengal: "/WestBengal.png",
    rajasthan: "/Rajasthan.png",
    punjab: "/Punjab.png",
    haryana: "/Haryana.png",
    madhyapradesh: "/MP.png",
    odisha: "/Odisha.png",
    assam: "/Assam.png",
    kerala: "/Kerala.png",
  };

  return (
    <div className="available-states-container">
      <div className="states-list">
        <h2>We Are Expanding Across India</h2>
        <p>Our ambulance services are currently available in the following states:</p>
        <ul>
          {states.map((state, index) => (
            <li
              key={index}
              onMouseEnter={() => setHoveredState(state.id)}
              onMouseLeave={() => setHoveredState(null)}
              className="state-item"
            >
              {state.name}
            </li>
          ))}
        </ul>
      </div>

      <div className="states-map">
        <div
          className="india-map"
          style={{
            backgroundImage: `url(${hoveredState ? stateMaps[hoveredState] : stateMaps.default})`,
            backgroundSize: "cover",
            height: "600px", // Adjust map size
            opacity: hoveredState ? 1 : 1, // Fade out default map when a state is hovered
          }}
        ></div>
      </div>
    </div>
  );
};

export default AvailableStates;
