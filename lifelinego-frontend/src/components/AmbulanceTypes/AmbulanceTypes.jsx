import React from "react";
import "./AmbulanceTypes.css"; // CSS is next
import images from "../../assets/image.js";

const AmbulanceTypes = () => {
  const types = [
    {
      title: "BLS Ambulance",
      description:
        "Basic Life Support for non-critical patients. Equipped with oxygen, basic first aid and stretcher facilities.",
      icon: images.BLS, // use icon size images here
    },
    {
      title: "ALS Ambulance",
      description:
        "Advanced Life Support ambulances for critical care. Includes ventilators, defibrillators, and trained paramedics.",
      icon: images.ALS,
    },
    {
      title: "Neonatal Ambulance",
      description:
        "Specially designed for newborns and infants. Equipped with neonatal incubator and monitoring systems.",
      icon: images.Neonatal,
    },
  ];

  return (
    <section className="ambulance-flip-section">
    <h2>Our Ambulance Fleet</h2>
    <div className="ambulance-flip-grid">
      {types.map((type, index) => (
        <div className="flip-card" key={index}>
          <div className="flip-card-inner">
            <div className="flip-card-front">
              <img src={type.icon} alt={type.name} />
              <h3>{type.title}</h3>
            </div>
            <div className="flip-card-back">
              <p>{type.description}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  </section>
  );
};

export default AmbulanceTypes;
