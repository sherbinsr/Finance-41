import React, { useEffect, useState } from 'react';
import UserService from '../Service/UserService'; 
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const UserAnalytics = () => {
  const [userCount, setUserCount] = useState(0);
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: []
  });

  useEffect(() => {
    UserService.getUserCount()
      .then((count) => {
        setUserCount(count);
        console.log("User count: ", count);
        generateChartData(count);
      })
      .catch((error) => console.error("Error fetching user count:", error));
  }, []);

  const generateChartData = (count) => {
    setChartData({
      labels: ['Users'],
      datasets: [
        {
          label: 'User Activity Count',
          data: [count],
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    });
  };

  return (
    <div>
      <h2>Total Users: {userCount}</h2>
      {/* Render Line chart only when chartData is available */}
      {chartData && chartData.datasets.length > 0 && (
        <Line data={chartData} />
      )}
    </div>
  );
};

export default UserAnalytics;
