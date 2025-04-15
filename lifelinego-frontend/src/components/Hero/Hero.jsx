import React, { useEffect, useState } from "react";
import "./Hero.css";
import images from "../../assets/image";
import {useNavigate} from "react-router-dom"; 

const words = ["HEALTH", "SAFETY", "FUTURE"];

const Hero = () => {
  
  const navigate = useNavigate();

  const [wordIndex, setWordIndex] = useState(0);
  const [displayText, setDisplayText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);
  const [letterIndex, setLetterIndex] = useState(0);
  const [backgroundImage, setBackgroundImage] = useState("");
  const [bgOpacity, setBgOpacity] = useState(0);

  useEffect(() => {
    const currentWord = words[wordIndex];

    const updateText = () => {
      if (!isDeleting && letterIndex < currentWord.length) {
        setDisplayText(currentWord.substring(0, letterIndex + 1));
        setLetterIndex(letterIndex + 1);
      } else if (isDeleting && letterIndex > 0) {
        setDisplayText(currentWord.substring(0, letterIndex - 1));
        setLetterIndex(letterIndex - 1);
      } else {
        setTimeout(() => {
          setIsDeleting(!isDeleting);
          if (!isDeleting) {
            setWordIndex((prevIndex) => (prevIndex + 1) % words.length);
            setLetterIndex(0);
          }
        }, 1000);
      }
    };

    const typingSpeed = isDeleting ? 100 : 200;
    const timeout = setTimeout(updateText, typingSpeed);

    return () => clearTimeout(timeout);
  }, [letterIndex, isDeleting, wordIndex]);

  // Handle hover effect with smooth transition
  const handleMouseEnter = (image) => {
    setBgOpacity(0); // First fade out
    setTimeout(() => {
      setBackgroundImage(image); // Change background after fade out
      setBgOpacity(1); // Then fade in smoothly
    }, 300); // Delay should match fade-out duration
  };

  const handleMouseLeave = () => {
    setBgOpacity(0); // Fade out effect
  };

  const handleOnClick = ()=>{
    navigate("/book-ambulance")
  }
  return (
    <div className="hero-container">
      {/* Background Overlay with Smooth Transition */}
      <div
        className="background-overlay"
        style={{
          backgroundImage: backgroundImage ? `url(${backgroundImage})` : "none",
          backgroundSize: "cover",  
          backgroundPosition: "center",
          transition: "opacity 0.5s ease-in-out",
          opacity: bgOpacity,
        }}
      ></div>

      <div className="home-page">
        <div className="left-home">
          <h2>
            WE CARE ABOUT <br />
            YOUR <span className="changing-word">{displayText}</span>
          </h2>
          <p>
            In emergencies, every second counts. LifelineGo ensures fast,
            reliable ambulance services, connecting you to life-saving care with
            just a tap—quick, efficient, and always ready.
          </p>
          <button className="left-home-btn" onClick={handleOnClick}>
            <svg>
              <rect x="0" y="0" fill="none" width="100%" height="100%" />
            </svg>
            Book Now
          </button>
        </div>
        <div className="right-home">
          <img
            src={images.hero1}
            alt=""
            className="home-image home-image1"
            onMouseEnter={() => handleMouseEnter(images.hero1)}
            onMouseLeave={handleMouseLeave}
          />
          <img
            src={images.hero2}
            alt=""
            className="home-image home-image2"
            onMouseEnter={() => handleMouseEnter(images.hero2)}
            onMouseLeave={handleMouseLeave}
          />
          <img
            src={images.hero3}
            alt=""
            className="home-image home-image3"
            onMouseEnter={() => handleMouseEnter(images.hero3)}
            onMouseLeave={handleMouseLeave}
          />
        </div>
      </div>
    </div>
  );
};

export default Hero;
