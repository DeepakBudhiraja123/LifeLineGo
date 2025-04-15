import React from 'react'
import AmbulanceForm from '../../components/AmbulanceForm/AmbulanceForm'
import AvailableStates from '../../components/AvailableStates/AvailableStates'
import Statistics from '../../components/Statistics/Statistics'
import AmbulanceTypes from '../../components/AmbulanceTypes/AmbulanceTypes'

const BookAmbulance = () => {
  return (
    <div>
      <AmbulanceForm/>
      <AmbulanceTypes/>
      <AvailableStates/>
      <Statistics/>
    </div>
  )
}

export default BookAmbulance