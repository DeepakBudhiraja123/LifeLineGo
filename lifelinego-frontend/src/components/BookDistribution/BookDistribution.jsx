import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const BookingDistributionChart = () => {
  const data = [
    { name: 'Maharashtra', value: 32 },
    { name: 'Delhi', value: 28 },
    { name: 'Karnataka', value: 12 },
    { name: 'Punjab', value: 8 },
    { name: 'Others', value: 10 },
  ];

  const COLORS = ['#ff4d4d', '#0099cc', '#ffcc00', '#66cc66', '#e6e6e6'];

  return (
    <div style={{ textAlign: 'center', marginTop: '40px' }}>
      <h2>📦 Booking Distribution Overview</h2>
      <ResponsiveContainer width="100%" height={350}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={120}
            fill="#8884d8"
            label
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend
            layout="horizontal"
            verticalAlign="bottom"
            align="center"
            wrapperStyle={{
              paddingTop: '20px',
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BookingDistributionChart;
