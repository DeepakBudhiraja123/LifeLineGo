import React from "react";
import "./Services.css";
import ServiceItem from "../ServiceItem/ServiceItem";
import images from "../../assets/image";

const services = [
  {
    icon: images.Emergency,
    title: "Emergency Ambulance",
    description:
      "Our 24/7 emergency ambulance service ensures rapid response and safe transportation to the nearest hospital in critical situations.",
  },
  {
    icon: images.ICUService,
    title: "ICU Ambulance",
    description:
      "Equipped with advanced life support systems, our ICU ambulances provide critical care transportation for patients requiring intensive monitoring.",
  },
  {
    icon: images.AirAmbulance,
    title: "Air Ambulance",
    description:
      "For long-distance medical emergencies, our air ambulance service offers swift and safe patient transport with specialized medical personnel.",
  },
  {
    icon: images.nonEmergency,
    title: "Non-Emergency Transport",
    description:
      "We provide comfortable and reliable transportation for non-emergency medical visits, including check-ups and routine hospital appointments.",
  },
];

const Services = () => {
  return (
    <div className="services">
      <h2>Our Services</h2>
      <div className="services-wrapper">
        <div className="render">
          {services.slice(0, 2).map((service, index) => (
            <ServiceItem key={index} {...service} />
          ))}
        </div>
        <div className="doctor-image">
          <img src={images.ServicesDoctor} alt="Doctor" />
        </div>
        <div className="render">
          {services.slice(2).map((service, index) => (
            <ServiceItem key={index} {...service} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Services;
