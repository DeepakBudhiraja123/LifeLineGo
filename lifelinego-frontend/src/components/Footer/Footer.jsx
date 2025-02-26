import React from "react";
import "./Footer.css";
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from "react-icons/fa";
import { FaArrowRight } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const Footer = () => {
  const navigate = useNavigate();
    const handleNavigate = () => {
    navigate("/contact"); // Contact page par navigate karega
  };
  return (
    <footer className="footer-container">
      <div className="footer-1">
        <h4>
          HEARD <br />
          ENOUGH?&#8594;
        </h4>
        <h1>Contact us</h1>
        <div onClick={handleNavigate}>
          <FaArrowRight className="arrow" />
        </div>
      </div>
      <div className="footer-2">
        <div className="footerBlock footerBlock1">
          LifelineGo - Caring Beyond Boundaries
        </div>
        <div className="footerBlock footerBlock2">
          <p>INDIA</p>
          <p>
            <span>lifelinego@wecare.gov.in </span>
            <br />
            +44 20 7878 5265 <br />
            Unit - 5, S.A.S Nagar, Mohali <br />
            Sector - 60 Punjab, India 160059
          </p>
          <p>
            <span>SEE ON MAP&#8599; </span>
          </p>
        </div>
        <div className="footerBlock footerBlock3">
          <p>LONDON</p>
          <p>
            <span>lifelinego@wecare.londongov.in </span>
            <br />
            +54 11 6799 7949
            <br />
            Cabildo 1458 1st floor <br />
            70 Wapping Wall, London
          </p>
          <p>
            <span>SEE ON MAP&#8599; </span>
          </p>
        </div>
        <div className="footerBlock footerBlock4">
            <p>Need instant medical updates? Stay prepared with us!</p>
            <p> <span>SIGN UP FOR FREE <FaArrowRight/></span></p>
            <p>FOLLOW US</p>
            <ul>
                <li><FaFacebook/></li>
                <li><FaTwitter/></li>
                <li><FaLinkedin/></li>
                <li><FaInstagram/></li>
            </ul>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
