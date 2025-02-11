import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, X, Home, PhoneCall, Info, Ambulance } from "lucide-react";
import "./Navbar.css";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="nav-container">
        <button className="nav-toggle" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
        <Link to="/" className="nav-logo">
          🚑 Life Line Go
        </Link>

        <ul className={`nav-links ${isOpen ? "open" : ""}`}>
          <li>
            <Link to="/" onClick={() => setIsOpen(false)}>
              <Home size={18} /> Home
            </Link>
          </li>
          <li>
            <Link to="/book-ambulance" onClick={() => setIsOpen(false)}>
              <Ambulance size={18} /> Book Ambulance
            </Link>
          </li>
          <li>
            <Link to="/about" onClick={() => setIsOpen(false)}>
              <Info size={18} /> About Us
            </Link>
          </li>
          <li>
            <Link to="/contact" onClick={() => setIsOpen(false)}>
              <PhoneCall size={18} /> Contact
            </Link>
          </li>
        </ul>

        <Link to="/emergency" className="emergency-btn">
          🚨 Emergency Call
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
