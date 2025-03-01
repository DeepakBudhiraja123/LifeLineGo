import React, { useState } from "react";
import "./Testimonials.css";
import images from "../../assets/image";
import { RiDoubleQuotesR } from "react-icons/ri";
import { FaArrowLeftLong } from "react-icons/fa6";
import { FaArrowRightLong } from "react-icons/fa6";

const Testimonials = () => {
  const [index, setIndex] = useState(0);
  const [fade, setFade] = useState(false);
  const testimonials = [
    {
      heading: "Life-Saving Response Time",
      name: "Emily Davis",
      role: "Senior Designer at Design Studio",
      testimonial:
        "The ambulance arrived within minutes, and the staff was extremely professional. A lifesaving service indeed! From the moment I made the call, they provided real-time updates on the ambulance's location. The paramedics were calm, well-trained, and ensured that my loved one received immediate medical attention on the way to the hospital. Their swift response made all the difference!",
      image: images.Testimonials1,
    },
    {
      heading: "Seamless Booking Process",
      name: "Michael Johnson",
      role: "Project Manager at TechCorp",
      testimonial:
        "I was able to book an ambulance for my father seamlessly. The response time and care provided were excellent! The website's user-friendly interface made the entire process quick and easy. Within moments of my request, I received confirmation along with estimated arrival time. The paramedics handled my father with great care and professionalism, ensuring his comfort and safety throughout the journey.",
      image: images.Testimonials2,
    },
    {
      heading: "Reliable and Efficient Service",
      name: "Samantha William",
      role: "Marketing Lead at Creative Agency",
      testimonial:
        "Fast, reliable, and efficient! I highly recommend this ambulance service to anyone in need of urgent medical care. The entire experience was stress-free, and their dedication to providing quality emergency response was evident. The staff reassured us during the ride and provided basic medical support before we reached the hospital. Knowing such a dependable service is available gives me peace of mind.",
      image: images.Testimonials3,
    },
    {
      heading: "Hassle-Free and Timely Assistance",
      name: "David Wilson",
      role: "Software Engineer at HealthTech",
      testimonial:
        "Booking an ambulance through this website was a hassle-free experience. The team ensured timely assistance and comfort. From the moment the ambulance arrived, the medical staff took charge with professionalism and efficiency. They kept monitoring vital signs and made sure we reached the hospital safely. Their kindness and expertise truly made a difference in a stressful situation.",
      image: images.Testimonials4,
    },
  ];
  const handleLeft = () => {
    if (index > 0) {
      setFade(true); // Trigger fade out
      setTimeout(() => {
        setIndex((prevIndex) => prevIndex - 1); // Change the index
        setTimeout(() => {
          setFade(false); // Trigger fade in after new content loads
        }, 300); // Adjust timing for a smoother transition
      }, 300); // Delay for the fade-out effect
    }
  };

  const handleRight = () => {
    if (index < testimonials.length - 1) {
      setFade(true); // Trigger fade out
      setTimeout(() => {
        setIndex((prevIndex) => prevIndex + 1); // Change the index
        setTimeout(() => {
          setFade(false); // Trigger fade in after new content loads
        }, 300); // Adjust timing for a smoother transition
      }, 300); // Delay for the fade-out effect
    }
  };
  return (
    <div className="testimonials-container">
      <div className="absoluteTestimonials"></div>
      <div className={`testimonials-body ${fade ? "fade-body" : ""}`}>
        <h2>
          What Our Customers <br /> Are Saying
        </h2>
        <div className="testimonials-body-flex">
          <div className="left-testimonials-body">
            <div className="review-icon">
              <RiDoubleQuotesR />
            </div>
            <img src={testimonials[index].image} alt="" />
            <div className="options-review">
              <div
                className={`arrow-left ${index == 0 ? "disabled-class" : ""}`}
                onClick={handleLeft}
              >
                <FaArrowLeftLong />
              </div>
              <div
                className={`arrow-right ${index == 3 ? "disabled-class" : ""}`}
                onClick={handleRight}
              >
                <FaArrowRightLong />
              </div>
            </div>
          </div>
          <div className="right-testimonials-body">
            <h6>{testimonials[index].heading}</h6>
            <p>{testimonials[index].testimonial}</p>
            <div className="publisher">
              <h3>{testimonials[index].name}</h3>
              <h4>{testimonials[index].role}</h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Testimonials;
