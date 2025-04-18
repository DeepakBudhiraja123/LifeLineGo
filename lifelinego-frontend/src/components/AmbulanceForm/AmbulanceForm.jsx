import { useState } from "react";
import {
  FaAmbulance,
  FaMapMarkerAlt,
  FaClock,
  FaPhoneAlt,
} from "react-icons/fa";
import "./AmbulanceForm.css"; // Updated CSS
import images from "../../assets/image";

const AmbulanceForm = ({ openCallModal }) => {
  const [pickup, setPickup] = useState("");
  const [destination, setDestination] = useState("");
  const [ambulanceType, setAmbulanceType] = useState("BLS");

  const handleBooking = () => {
    alert(
      `🚑 Ambulance Booked!\nPickup: ${pickup}\nDestination: ${destination}\nType: ${ambulanceType}`
    );
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <div className="ambulance-container">
        <h2 className="ambulance-title">
          <FaAmbulance /> Book an Ambulance
        </h2>

        <div className="input-group">
          <FaMapMarkerAlt className="icon" />
          <input
            type="text"
            placeholder="Pickup Location"
            value={pickup}
            onChange={(e) => setPickup(e.target.value)}
          />
        </div>

        <div className="input-group">
          <FaMapMarkerAlt className="icon" />
          <input
            type="text"
            placeholder="Destination"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
          />
        </div>

        <div className="dropdown-group">
          <label>Select Ambulance Type:</label>
          <select
            className="dropdown"
            value={ambulanceType}
            onChange={(e) => setAmbulanceType(e.target.value)}
          >
            <option value="BLS">🚑 Basic Life Support (BLS)</option>
            <option value="ALS">💉 Advanced Life Support (ALS)</option>
            <option value="Neonatal">👶 Neonatal Ambulance</option>
          </select>
        </div>

        <button className="book-btn" onClick={handleBooking}>
          🚨 Book Now
        </button>

        <div className="info-row">
          <p className="arrival-info">
            <FaClock /> Estimated Arrival: 10 mins
          </p>
          <button
            className="emergency-btn"
            onClick={() => {
              console.log("Call Emergency button clicked");
              openCallModal(); // This should open the modal
            }}
          >
            <FaPhoneAlt /> Call Emergency
          </button>
        </div>
      </div>
      <img
        src={images.BookAmbulance}
        alt="Ambulance Illustration"
        style={{ width: "40%", borderRadius: "20px", paddingRight: "100px" }}
      />
    </div>
  );
};

export default AmbulanceForm;
