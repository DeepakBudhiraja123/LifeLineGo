import React, { useEffect, useState } from "react";
import "./whyus.css";
import images from "../../assets/image";
import { Link } from "react-router-dom";
import { useInView } from "react-intersection-observer";

const WhyUs = () => {
  const [ref, inView] = useInView({
    threshold: 0.1, // Start animation when 10% of the section is in view
  });

  const [visibleBlocks, setVisibleBlocks] = useState({
    block1: false,
    block2: false,
    block3: false,
    block4: false,
  });

  useEffect(() => {
    if (inView) {
      setVisibleBlocks({
        block1: false,
        block2: false,
        block3: false,
        block4: false,
      });

      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block1: true })),
        800
      );
      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block3: true })),
        1600
      );
      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block2: true })),
        2400
      );
      setTimeout(
        () => setVisibleBlocks((prev) => ({ ...prev, block4: true })),
        3200
      );
    }
  }, [inView]);
  useEffect(() => {
    if (!inView) {
      setVisibleBlocks({
        block1: false,
        block2: false,
        block3: false,
        block4: false,
      });
    }
  }, [inView]);

  return (
    <div className="whyus-container" ref={ref}>
      <div className="left">
        <h6>
          <span>/</span>Why LifeLineGo?
        </h6>
        <h2>The LifeLineGo Difference</h2>
        <p>
          At our core, we prioritize your safety and well-being. Our 24/7
          ambulance network, real-time tracking, and expert medical staff ensure
          you receive swift, reliable, and life-saving care when it matters
          most. Trust us to be there for you—anytime, anywhere.
        </p>
        <div className="facilities">
          <Link to="/" className="facility">
            Call Now
          </Link>
          <Link to="/" className="facility">
            Book Now
          </Link>
        </div>
      </div>
      <div className="right">
        <div className="right-left">
          <div
            className={`block block1 ${
              visibleBlocks.block1 ? "slide-top" : ""
            }`}
          >
            <img src={images.AmbulanceDispatch} alt="" />
            <div className="block-text">
              <h3>Rapid Dispatch</h3>
              <p>
                Get the nearest ambulance in minutes with real-time GPS
                tracking.
              </p>
            </div>
          </div>
          <div className="right-seperator"></div>
          <div
            className={`block block2 ${
              visibleBlocks.block2 ? "slide-top" : ""
            }`}
          >
            <img src={images.Emergency} alt="" />
            <div className="block-text">
              <h3>24/7 Availability</h3>
              <p>
                Our network ensures round-the-clock ambulance availability, even
                in remote areas.
              </p>
            </div>
          </div>
        </div>
        <div className="seperator"></div>
        <div className="right-right">
          <div
            className={`block block3 ${
              visibleBlocks.block3 ? "slide-top" : ""
            }`}
          >
            <img src={images.Location} alt="" />
            <div className="block-text">
              <h3>Live Tracking</h3>
              <p>
                Track your ambulance in real-time and receive accurate arrival
                estimates for peace of mind.
              </p>
            </div>
          </div>
          <div className="right-seperator"></div>
          <div
            className={`block block4 ${
              visibleBlocks.block4 ? "slide-top" : ""
            }`}
          >
            <img src={images.Staff} alt="" />
            <div className="block-text">
              <h3>Expert Care</h3>
              <p>
                Every ambulance is equipped with professional paramedics and
                life-saving medical equipment.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WhyUs;
