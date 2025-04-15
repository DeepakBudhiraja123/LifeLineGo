import React from 'react'
import AmbulanceForm from '../../components/AmbulanceForm/AmbulanceForm'
import AvailableStates from '../../components/AvailableStates/AvailableStates'
import Statistics from '../../components/Statistics/Statistics'

const BookAmbulance = () => {
  return (
    <div>
      <AmbulanceForm/>
      <AvailableStates/>
      <Statistics/>
    </div>
  )
}

export default BookAmbulance