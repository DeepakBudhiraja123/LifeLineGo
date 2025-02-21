import React from 'react'
import Hero from "../../components/Hero/Hero"
import WhyUs from "../../components/whyus/whyus"
import "./Home.css"

const Home = () => {
  return (
    <div className='HomeContainer'>
      <Hero/>
      <WhyUs />
    </div>
  )
}

export default Home
