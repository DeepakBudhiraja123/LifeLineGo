import React from 'react';
import BookingDistributionChart from '../BookDistribution/BookDistribution';
import ResponseTimeChart from '../ResponseTime/ResponseTime';
import "./Statistics.css";

const Statistics = () => {
  return (
    <section className="coverage-performance">
      <h2 className="section-title">Our Coverage & Performance</h2>

      <div className="stat-block right-align">
        <div className="stat-text">
          <h3>Booking Distribution by State</h3>
          <p>
            Our ambulance booking requests are widely distributed across major states. Maharashtra and Delhi hold the highest request ratios, proving our strong presence in urban zones.
          </p>
        </div>
        <div className="stat-chart">
          <BookingDistributionChart />
        </div>
      </div>

      <div className="stat-block left-align">
        <div className="stat-chart">
          <ResponseTimeChart />
        </div>
        <div className="stat-text">
          <h3>Response Time Improvement</h3>
          <p>
            Over the past few months, our average response time has improved significantly, ensuring faster pickups and better emergency handling for our customers.
          </p>
        </div>
      </div>

    </section>
  );
};

export default Statistics;
