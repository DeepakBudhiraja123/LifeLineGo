import React, { useState, useEffect } from "react";
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
    default: "/Default.png",
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

  // 💡 Preload all images once
  useEffect(() => {
    Object.values(stateMaps).forEach(src => {
      const img = new Image();
      img.src = src;
    });
  }, []);

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
        {/* Default Map Layer */}
        <div
          className="india-map default"
          style={{
            backgroundImage: `url(${stateMaps.default})`,
          }}
        ></div>

        {/* Hovered State Map Layer */}
        <div
          className={`india-map hovered ${hoveredState ? "show" : ""}`}
          style={{
            backgroundImage: hoveredState ? `url(${stateMaps[hoveredState]})` : "none",
          }}
        ></div>
      </div>
    </div>
  );
};

export default AvailableStates;
