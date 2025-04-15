import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ResponseTimeChart = () => {
  const data = [
    { month: 'Nov', responseTime: 18 },
    { month: 'Dec', responseTime: 16 },
    { month: 'Jan', responseTime: 14 },
    { month: 'Feb', responseTime: 12 },
    { month: 'Mar', responseTime: 11 },
    { month: 'Apr', responseTime: 9 },
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="responseTime"
          stroke="#007bff"
          activeDot={{ r: 8 }}
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default ResponseTimeChart;
