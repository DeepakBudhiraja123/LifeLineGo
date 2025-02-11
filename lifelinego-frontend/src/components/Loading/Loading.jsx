import React, { useEffect, useState } from 'react'
import images from '../../assets/image'
import "./Loading.css"

const Loading = () => {
  const [pluses, setPluses] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      setPluses((prevPluses) => [
        ...prevPluses,
        {
          id: Math.random(), // Unique ID
          left: Math.random() * 100, // Random horizontal position
        },
      ]);

      // Remove old `+` signs after they exit
      setTimeout(() => {
        setPluses((prevPluses) => prevPluses.slice(1));
      }, 4000);
    }, 600); // New `+` every 600ms

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="loading-container">
      <div className="rotating-border">
      </div>
      {pluses.map((plus) => (
        <h1
          key={plus.id}
          className="falling-plus"
          style={{ left: `${plus.left}%` }}
        >
          +
        </h1>
      ))}
      <img src={images.Loading} alt="Loading Ambulance" className="ambulance-image" />
    </div>
  )
}

export default Loading
