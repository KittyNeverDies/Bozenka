import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  Label,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { Box, Typography } from "@mui/joy";
import Avatar from '@mui/joy/Avatar';

import Divider from '@mui/joy/Divider';
import Card from '@mui/joy/Card';
import Grid from '@mui/joy/Grid';





export default function TestChart({ data, displayData, }) {
  
  const CustomLegend = (props) => {
    const { payload } = props;

    return (
    <Box sx={{ 
      display: "flex", 
      flexDirection: "row", 
      justifyContent: "space-between", 
      alignItems: "flex-start",
      marginTop: 2
    }}>
      <Grid container >
        {payload.map((item, index) => (
          <Grid>
          <Box key={index} sx={{ 
            display: "flex", 
            flexDirection: "row", 
            alignItems: "center", marginBottom: 2,
            marginLeft: 2 
          }}>
          
            {displayData[item.value].icon ? 
              <Avatar size="md" color="neutral" variant="outlined">
                {displayData[item.value].icon}
              </Avatar> 
              : 
              <Box sx={{ backgroundColor: item.color, width: 10, height: 10,}} />
            }
            <Box sx={{ 
              display: "flex", 
              flexDirection: "column", 
              alignItems: "flex-start", ml: 2 ,
            }}>
              <Typography level="title-xs" sx={{lineHeight: 1.3, fontWeight: 'bold'}}>
                {displayData[item.value].title ? displayData[item.value].title : item.value}
              </Typography>
              {displayData[item.value].description && (
                <Typography level="body-xs" >
                  {displayData[item.value].description}
                </Typography>
              )}
          </Box>
        </Box>
        </Grid>
      ))}
      </Grid>
    </Box>
    );
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
      <Box sx={{ 
          backgroundColor: "background.surface", 
          padding: 2, 
          border: "1px solid",
          borderColor: 'background.level3', 
          borderRadius: "lg",
          boxShadow: 'xs' 
      }}>
        <Typography level="title-lg">{label}</Typography>
        
        <Divider sx={{ mb: 2, mt: 1 }} />
        {payload.map((item, index) => (
          <>
            <Typography key={index} startDecorator={displayData[item.name].icon ? displayData[item.name].icon : ""} level="body-xs">
              {displayData[item.name] ? displayData[item.name].shortTitle: item.name}: 
                <Typography textColor={item.color}>
                  <b>{item.value}</b>
                </Typography>
              </Typography>
            </>
          ))}
        
        </Box>
      );
    }

    return null;
  };

  return (
    <Box sx={{ width: 500, height: 300, padding: 2, paddingBottom: 5 }}>
      <LineChart width={500} height={400} data={data} style={{fontFamily: 'Inter'}}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis style={{fontSize: 12}} dataKey="name" padding={{ left: 30, right: 30 }} marginBottom={1}>
          <Label value="Dates of knowngrowth" offset={0} position="bottom" fontSize={12} />
        </XAxis>
        <YAxis style={{fontSize: 12}} /> 
        <Tooltip content={<CustomTooltip />} />
        <Legend content={<CustomLegend />} />
        <Line type="monotone" dataKey="members" stroke="#8884d8"/>
        <Line type="monotone" dataKey="views" stroke="#82ca9d" />
      </LineChart>
    </Box>
  );
}