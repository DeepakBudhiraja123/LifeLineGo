import React from 'react'
import Hero from "../../components/Hero/Hero"
import WhyUs from "../../components/whyus/whyus"
import "./Home.css"
import Steps from '../../components/Steps/Steps'
import AvailableStates from '../../components/AvailableStates/AvailableStates'

const Home = () => {
  return (
    <div className='HomeContainer'>
      <Hero/>
      <WhyUs />
      <Steps/>
      <AvailableStates/>
    </div>
  )
}

export default Home
