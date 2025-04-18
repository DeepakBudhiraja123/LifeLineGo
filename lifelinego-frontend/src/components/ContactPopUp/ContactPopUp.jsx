import React, { useEffect, useState } from "react";
import "./ContactPopUp.css";

const ContactPopUp = ({ isOpen, onClose }) => {
  const [scrollPosition, setScrollPosition] = useState(0);

  useEffect(() => {
    if (isOpen) {
      // Capture scroll position when modal opens
      setScrollPosition(window.scrollY);
    }

    const handleScroll = () => {
      setScrollPosition(window.scrollY); // Update scroll position as user scrolls
    };

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll); // Clean up on component unmount
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-cover" style={{ top: `${scrollPosition}px` }}>
      <div className="modal-content" >
        <h2>Contact Our Team</h2>
        <p>📞 +91-62805-10673</p>
        <div className="buttonsContact">
        <a href="tel:+916280510673" className="call-button">
          Call Now
        </a>
        <button onClick={onClose} className="close-button">
          Close
        </button>
        </div>
      </div>
    </div>
    </div>
  );
};

export default ContactPopUp;
