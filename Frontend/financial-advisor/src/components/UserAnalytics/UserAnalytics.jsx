"use client"

import React, { useEffect, useState } from 'react'
import CountUp from 'react-countup'
import UserService from '../../Service/UserService'
import {
  GaugeContainer,
  GaugeValueArc,
  GaugeReferenceArc,
  useGaugeState,
} from '@mui/x-charts/Gauge';

export default function UserAnalytics() {
  const [userCount, setUserCount] = useState(0)

  useEffect(() => {
    UserService.getUserCount()
      .then((count) => {
        setUserCount(count)
      })
      .catch((error) => console.error('Error fetching user count:', error))
  }, [])
  function GaugePointer() {
    const { valueAngle, outerRadius, cx, cy } = useGaugeState();
  
    if (valueAngle === null) {
      // No value to display
      return null;
    }
  
    const target = {
      x: cx + outerRadius * Math.sin(valueAngle),
      y: cy - outerRadius * Math.cos(valueAngle),
    };
    return (
      <g>
        <circle cx={cx} cy={cy} r={5} fill="red" />
        <path
          d={`M ${cx} ${cy} L ${target.x} ${target.y}`}
          stroke="red"
          strokeWidth={3}
        />
      </g>
    );
  }
  return (
    <div className="container mx-auto p-4">
          <h1 className="fw-bold text-center text-danger">User History</h1>
          <br></br>
      <div className="grid gap-6 md:grid-cols-2">
        <div className="border p-4 rounded-md shadow-sm">
        <div class="d-flex justify-content-around">
          <div class="p-2">
            <h2 className="text-xl font-semibold">Total Users</h2>
          <p className="text-gray-500">Current number of registered users</p>
          <h2 className="fw-bold mt-4 ">
            <CountUp end={userCount} duration={2.5} />+
          </h2></div>
        <div class="p-2">
          <GaugeContainer
           width={200}
            height={200}
            startAngle={-110}
            endAngle={110}
          value={userCount}>
          <GaugeReferenceArc />
         <GaugeValueArc />
        <GaugePointer />
        </GaugeContainer>
        </div>
        </div>
        </div>
      </div>
    </div>
  )
}
