import React, { useEffect, useState } from "react";
import "./OurMission.css";
import images from "../../assets/image";
import { IoMdArrowDropup } from "react-icons/io";
import { useInView } from "react-intersection-observer";

const OurMission = () => {
  const [visible, setVisible] = useState(false);
  const [visibleText, setVisibleText] = useState(false);
  const [visibleBlock, setVisibleBlock] = useState(false);

  const [ref, inView] = useInView({
    threshold: 0.4,
  });
  useEffect(() => {
    if (inView) {
      setVisible(true);
      setTimeout(() => setVisibleBlock(true), 1000);
      setTimeout(() => setVisibleText(true), 1000);
    }
  }, [inView]);
  return (
    <div
      className={`encloseMission ${visible ? "AppearMission" : ""}`}
      ref={ref}
    >
      <div className="mission-container">
        <div className="leftMission">
          <img src={images.ourVision} alt="" />
        </div>
        <div className="posAbsoluteMission">
          <div className="upAbsoluteMission">
            <div className="AbsoluteAbsolute">
              <IoMdArrowDropup className="iconAbsolute" />
            </div>
            <h4>150</h4>
          </div>
          <div
            className={`downAbsoluteMission`}
          >
            <p className={`${
              visibleBlock ? "slide-in-bottom-mission-block" : ""
            }`}>Swift response, superior care, a safer tomorrow.</p>
          </div>
        </div>
        <div className="outlinePosAbsoluteMission">
          <div className="leftOutline"></div>
          <div className="rightOutline"></div>
        </div>
        <div className="rightMission">
          <h2 className={`${visibleText ? "slide-in-left-mission" : ""}`}>
            Our Vision
          </h2>
          <p className={`${visibleText ? "slide-in-left-mission" : ""}`}>
            We strive to make emergency medical response accessible to all,
            anytime, anywhere. Through technology and network expansion, we aim
            to reduce response times and improve urgent care quality.
          </p>
        </div>
      </div>
    </div>
  );
};

export default OurMission;
