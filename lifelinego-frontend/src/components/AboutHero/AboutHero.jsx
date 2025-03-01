import React, { useState, useEffect, useRef } from "react";
import "./AboutHero.css";
import images from "../../assets/image";

const AboutHero = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [isback, setIsBack] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    setIsBack(true);
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true); // Set visible when in view
        } else {
          setIsVisible(false); // Reset when out of view
        }
      },
      {
        threshold: 0.1, // Trigger when 10% of the component is visible
      }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, []);
  return (
    <div
      className={`AboutHero ${isback ? "slide-in-background-about-hero" : ""}`}
      ref={ref}
      style={{ backgroundImage: `url(${images.aboutUs})` }}
    >
      {/* Toggle fade-in/out based on isVisible */}
      <div className={`AboutPara ${isVisible ? "AboutPara-fade-in" : "AboutPara-fade-out"}`}>
        <h3>LifeLineGo - Fast, Reliable, Life-Saving Rides</h3>
        <p>
          LifeLineGo is your trusted partner in emergency and non-emergency
          ambulance bookings. With just a few clicks, you can access swift,
          well-equipped ambulances, ensuring timely medical assistance when
          every second counts. Our mission is to bridge the gap between patients
          and immediate care, providing a seamless, dependable, and life-saving
          transportation service.
        </p>
      </div>
      {/* Toggle slide-in/out for image */}
    </div>
  );
};

export default AboutHero;
