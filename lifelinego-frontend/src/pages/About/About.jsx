import React from 'react'
import Testimonials from '../../components/Testimonials/Testimonials'
import AboutHero from '../../components/AboutHero/AboutHero'
import Services from '../../components/Services/Services'
import OurMission from '../../components/OurMission/OurMission'

const About = () => {
  return (
    <div>
      <AboutHero/>
      <OurMission/>
      <Services/>
      <Testimonials/>
    </div>
  )
}

export default About
