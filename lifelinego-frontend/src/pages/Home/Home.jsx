import React from 'react'
import Hero from "../../components/Hero/Hero"
import WhyUs from "../../components/whyus/whyus"
import "./Home.css"
import Steps from '../../components/Steps/Steps'
import Testimonials from '../../components/Testimonials/Testimonials'
import Footer from '../../components/Footer/Footer'

const Home = () => {
  return (
    <div className='HomeContainer'>
      <Hero/>
      <WhyUs />
      <Steps/>
      <Testimonials/>
      <Footer/>
    </div>
  )
}

export default Home
