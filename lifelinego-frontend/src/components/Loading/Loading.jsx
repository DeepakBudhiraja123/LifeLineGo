import React from 'react'
import images from '../../assets/image'
import "./Loading.css"

const Loading = () => {
  return (
    <div className="loading-container">
      <div className="rotating-border">
      </div>
      <img src={images.Loading} alt="Loading Ambulance" className="ambulance-image" />
    </div>
  )
}

export default Loading
