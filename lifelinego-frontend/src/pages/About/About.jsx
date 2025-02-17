import React, { useState, useEffect, useRef } from "react";
import "./About.css";
import images from "../../assets/image";

const About = () => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true); // Show animation when in view
        } else {
          setIsVisible(false); // Hide when out of view
        }
      },
      { threshold: 0.2 } // Trigger when 20% of the element is visible
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
    <section className="about" ref={ref}>
      <div className="lifeline-content">
        {/* Left Div - Slide from Left */}
        <div className={`left ${isVisible ? "slide-in-left" : "slide-out-left"}`}>
          <h2>
            What is <span>LifelineGo?</span>
          </h2>
          <p>
            <span>LifelineGo</span> is a fast and reliable ambulance booking
            service that ensures quick medical assistance at your fingertips.
            Whether it’s an emergency or a planned transport, we connect you to
            trusted hospitals and medical professionals instantly.
          </p>
        </div>

        {/* Right Div - Slide from Right */}
        <div className={`right ${isVisible ? "slide-in-right" : "slide-out-right"}`}>
          <img src={images.firstAid} alt="" />
        </div>
      </div>
    </section>
  );
};

export default About;
