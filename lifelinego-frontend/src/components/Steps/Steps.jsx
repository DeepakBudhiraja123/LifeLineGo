import React, { useEffect, useState } from "react";
import "./Steps.css"; // Import the CSS file
import { useInView } from "react-intersection-observer";
import images from "../../assets/image";

const steps = [
  {
    icon: images.EnterLocation,
    title: "Enter Location",
    description:
      "Provide your pickup location to ensure the nearest ambulance reaches you quickly, reducing response time in emergencies.",
  },
  {
    icon: images.ChooseAmbulance,
    title: "Choose Ambulance",
    description:
      "Select the right ambulance based on your needs—basic, ICU-equipped, or neonatal care—for the best medical support.",
  },
  {
    icon: images.confirmBooking,
    title: "Confirm Booking",
    description:
      "Review and confirm your request, ensuring accurate details for a smooth and timely ambulance service.",
  },
  {
    icon: images.TrackLocation,
    title: "Track Ambulance",
    description:
      "Monitor your ambulance in real-time, track its arrival, and get driver details for a stress-free experience.",
  },
];


export default function Steps() {
  const [visible, setVisible] = useState(false);
  const [pointerClass, setPointerClass] = useState({
    block1: false,
    block2: false,
    block3: false,
    block4: false,
  });
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
        () => setPointerClass((prev) => ({ ...prev, block1: true })),
        1500
      );
      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block2: true })),
        () => setPointerClass((prev) => ({ ...prev, block2: true })),
        3000
      );
      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block3: true })),
        () => setPointerClass((prev) => ({ ...prev, block3: true })),
        4500
      );
      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block4: true })),
        () => setPointerClass((prev) => ({ ...prev, block4: true })),
        6000
      );
    }
  }, [inView]);

  return (
    <section className="how-it-works" ref={ref}>
      <div className="absoluteBlue1"></div>
      <div className="absoluteBlue2"></div>
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
          <div key={index} className={`how-it-work-step-closure ${
            pointerClass[`block${index + 1}`]
              ? ""
              : "cursor-inactive"
          }`}>
            <p className={`${
                visibleBlocks[`block${index + 1}`]
                  ? "slide-left-how-it-work"
                  : ""
              }`}>0{index+1}</p>
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
