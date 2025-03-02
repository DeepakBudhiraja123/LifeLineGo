import React from "react";
import "./ServiceItem.css";

const ServiceItem = ({ icon, title, description }) => {
  return (
    <div className="service-item">
      <div className="up">
        <img src={icon} alt={`${title} Icon`} className="service-icon" />
        <h4>{title}</h4>
      </div>
      <p>{description}</p>
    </div>
  );
};

export default ServiceItem;
