import React from "react";
import "./whyus.css";
import images from "../../assets/image";

const WhyUs = () => {
  return (
    <div className="whyusOver">
      <div className="whyus-container">
        <div className="left">
          <img src={images.whyUs} alt="" />
        </div>
        <div className="right">
          <div className="layer">
            <img src={images.Emergency} alt="" />
            <p>
              Our network ensures <span> round-the-clock</span> ambulance availability, even
              in <span>remote areas</span>.
            </p>
          </div>
          <div className="layer">
            <img src={images.Location} alt="" />
            <p>
              Track your ambulance in <span>real-time</span> and receive accurate arrival
              estimates for peace of mind.
            </p>
          </div>
          <div className="layer">
            <img src={images.Staff} alt="" />
            <p>
              Every ambulance is equipped with <span>professional paramedics</span> and
              <span>life-saving</span> medical equipment.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WhyUs;
