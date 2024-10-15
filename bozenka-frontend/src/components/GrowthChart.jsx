
import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const data = [
  {
    name: "03.09",
    views: 4000,
    members: 2400,
    amt: 2400,
  },
  {
    name: "04.09",
    views: 3000,
    members: 1398,
    amt: 2210,
  },
  {
    name: "05.09",
    views: 2000,
    members: 9800,
    amt: 2290,
  },
  {
    name: "06.09",
    views: 2780,
    members: 3908,
    amt: 2000,
  },
  {
    name: "07.09",
    views: 1890,
    members: 4800,
    amt: 2181,
  },
  {
    name: "08.09",
    views: 2390,
    members: 3800,
    amt: 2500,
  },
  {
    name: "09.09",
    views: 3490,
    members: 4300,
    amt: 2100,
  },
];

export default function TestChart() {
  return (
    <LineChart width={500} height={300} data={data} style={{fontFamily: 'Inter'}}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" padding={{ left: 30, right: 30 }} />
      
      <YAxis />
      <Tooltip />
      <Legend />
      <Line
        type="monotone"
        dataKey="members"
        stroke="#8884d8"
        activeDot={{ r: 8 }}
      />
      <Line type="monotone" dataKey="views" stroke="#82ca9d" />
    </LineChart>
  );
}