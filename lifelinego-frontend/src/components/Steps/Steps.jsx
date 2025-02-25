import React, { useEffect, useState } from "react";
import "./Steps.css"; // Import the CSS file
import { useInView } from "react-intersection-observer";
import images from "../../assets/image";

const steps = [
  {
    icon: images.EnterLocation,
    title: "Enter Location",
    description:
      "Provide your pickup location for quick access. This ensures the nearest available ambulance can reach you without delays, reducing response time during critical emergencies.",
  },
  {
    icon: images.ChooseAmbulance,
    title: "Choose Ambulance",
    description:
      "Select the type of ambulance service you need based on the emergency. Whether it's a basic life support ambulance, an advanced ICU-equipped vehicle, or a neonatal care unit, choose the right option for the best care.",
  },
  {
    icon: images.confirmBooking,
    title: "Confirm Booking",
    description:
      "Review all the details before confirming your ambulance request. Ensure accuracy in pickup location, ambulance type, and estimated arrival time to avoid any last-minute confusion.",
  },
  {
    icon: images.TrackLocation,
    title: "Track Ambulance",
    description:
      "Monitor your ambulance in real-time on the map. Stay updated on its estimated arrival time, route, and driver details for a seamless and stress-free emergency response.",
  },
];

export default function Steps() {
  const [visible, setVisible] = useState(false);
  const [ref, inView] = useInView({
    threshold: 0.4,
  });
  const [visibleBlocks, setVisibleBlocks] = useState({
    block1: false,
    block2: false,
    block3: false,
    block4: false,
  });

  useEffect(() => {
    if (inView) {
      setVisible(true);
    }
  }, [inView]);

  useEffect(() => {
    if (inView) {
      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block1: true })),
        1500
      );
      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block2: true })),
        3000
      );
      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block3: true })),
        4500
      );
      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block4: true })),
        6000
      );
    }
  }, [inView]);

  return (
    <section className="how-it-works" ref={ref}>
      <div className="how-it-works-heading">
        <h2 className={`${visible ? "slide-in-left-how-it-works" : ""}`}>
          <span>/</span>How Can
          <br />
          LifeLineGo Help?
        </h2>
      </div>
      <div className="description-how-it-works">
        <p className={`${visible ? "slide-in-bottom-how-it-works" : ""}`}>
          Medical emergencies demand speed and efficiency, and LifelineGo
          ensures you get help without delays. Enter your location, select the
          right ambulance, confirm your booking, and track your ride in
          real-time. Stay prepared, stay safe—lifesaving help is just a few taps
          away!
        </p>
      </div>
      <div className="how-it-works-steps">
        {steps.map((step, index) => (
          <div key={index} className="how-it-work-step-closure">
            <div
              className={`how-it-work-step ${
                visibleBlocks[`block${index + 1}`]
                  ? "slide-left-how-it-work"
                  : ""
              }`}
            >
              <img src={step.icon} alt={step.title} className="step-image" />
              <h3 className="step-title">{step.title}</h3>
            </div>
            <div className="how-it-work-step-desc">{step.description}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
