import React, { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  Label,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  BarChart,
  Bar,
  AreaChart,
  Area,
} from "recharts";
import { Box, Typography, useTheme, IconButton, Button } from "@mui/joy";
import Avatar from '@mui/joy/Avatar';
import Divider from '@mui/joy/Divider';
import Card from '@mui/joy/Card';
import Grid from '@mui/joy/Grid';
import DownloadIcon from '@mui/icons-material/Download';
import { CSVLink } from 'react-csv';

export default function TestChart({ data, displayData }) {
  const theme = useTheme();
  const [chartType, setChartType] = useState('line');
  const [hoveredDataPoint, setHoveredDataPoint] = useState(null);

  const colors = {
    members: theme.palette.primary[500],
    views: theme.palette.success[500]
  };

  const averages = {
    members: data.reduce((acc, curr) => acc + curr.members, 0) / data.length,
    views: data.reduce((acc, curr) => acc + curr.views, 0) / data.length
  };

  const exportData = () => {
    const csvContent = "data:text/csv;charset=utf-8," 
      + ["Date,Members,Views"]
        .concat(data.map(row => `${row.name},${row.members},${row.views}`))
        .join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "chart_data.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const CustomLegend = (props) => {
    const { payload } = props;

    return (
      <Card variant="outlined" sx={{ p: 2, mt: 2 }}>
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <Typography level="title-sm" 
          sx={{fontWeight: 'bold'}}>
            Chart Legend
          </Typography>
          <IconButton 
            variant="soft"
            color="neutral"
            onClick={exportData}
            title="Export data"
          >
            <DownloadIcon />
          </IconButton>
        </Box>
        <Grid container spacing={2}>
          {payload.map((item, index) => (
            <Grid xs={12} sm={6} key={index}>
              <Box sx={{ 
                display: "flex", 
                alignItems: "center",
                gap: 2,
                transition: 'all 0.2s ease',
                '&:hover': {
                  bgcolor: 'background.level1',
                  borderRadius: 'sm'
                },
                p: 1
              }}>
                <Avatar 
                  size="md" 
                  color={item.value === 'members' ? 'primary' : 'success'}
                  variant="soft"
                >
                  {displayData[item.value].icon}
                </Avatar>
                <Box>
                  <Typography level="title-sm">
                    {displayData[item.value].shortTitle}
                  </Typography>
                  <Typography level="body-xs" color="neutral">
                    Avg: {Math.round(averages[item.value])}
                  </Typography>
                </Box>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Card>
    );
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <Card variant="outlined" size='xs' sx={{ 
        
          boxShadow: 'sm',
        }}>
          <Typography level="title-sm" sx={{ mb: 1, fontWeight: 'bold' }}>
            {label}
          </Typography>
          <Box sx={{ mt: 1 }}>
            {payload.map((item, index) => (
              <Box 
                key={index} 
                sx={{ 
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1,
                  mt: 1,
                  borderRadius: 'sm'
                }}
              >
                {displayData[item.name].icon}
                <Box>
                  <Typography level="body-xs">
                    {displayData[item.name].shortTitle}
                  </Typography>
                  <Typography 
                    level="title-sm"
                    sx={{ color: colors[item.name] }}
                  >
                    {item.value}
                  </Typography>
                </Box>
              </Box>
            ))}
          </Box>
        </Card>
      );
    }
    return null;
  };

  const chartTypes = {
    line: (
      <LineChart 
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 70 }}
        onMouseMove={(e) => {
          if (e && e.activePayload) {
            setHoveredDataPoint(e.activePayload[0].name);
          }
        }}
        onMouseLeave={() => setHoveredDataPoint(null)}
      >
        <CartesianGrid 
          strokeDasharray="3 3"
          stroke={theme.palette.divider}
        />
        <XAxis 
          dataKey="name"
          tick={{ fill: theme.palette.text.primary }}
          stroke={theme.palette.divider}
          style={{fontSize: 10}}
        />
        <YAxis
          
          tick={{ fill: theme.palette.text.primary }}
          stroke={theme.palette.divider}
          style={{fontSize: 10}}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend content={<CustomLegend />} />
        <ReferenceLine 
          y={averages.members}
          stroke={colors.members}
          strokeDasharray="3 3"
          label={{ 
            value: 'Avg Members',
            fill: colors.members,
            fontSize: 12
          }}
        />
        <ReferenceLine 
          y={averages.views}
          stroke={colors.views}
          strokeDasharray="3 3"
          label={{ 
            value: 'Avg Views',
            fill: colors.views,
            fontSize: 12
          }}
        />
        <Line
          type="monotone"
          dataKey="members"
          stroke={colors.members}
          strokeWidth={2}
          dot={{ fill: colors.members, r: 4 }}
          activeDot={{ r: 8 }}
          animationDuration={1500}
        />
        <Line
          type="monotone"
          dataKey="views"
          stroke={colors.views}
          strokeWidth={2}
          dot={{ fill: colors.views, r: 4 }}
          activeDot={{ r: 8 }}
          animationDuration={1500}
        />
      </LineChart>
    ),
    bar: (
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" 
        tick={{ fill: theme.palette.text.primary }}
        stroke={theme.palette.divider} style={{fontSize: 12}} />
        <YAxis 
        tick={{ fill: theme.palette.text.primary }}
        stroke={theme.palette.divider} style={{fontSize: 12}}  />
        <Tooltip content={<CustomTooltip />} />
        <Legend content={<CustomLegend />} />
        <Bar
          dataKey="views"
          fill="#8884d8"
        />
        <Bar
          dataKey="members"
          fill="#82ca9d"
        />
      </BarChart>
    ),
    area: (
      <AreaChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
                  tick={{ fill: theme.palette.text.primary }}
                  stroke={theme.palette.divider} 
          style={{fontSize: 12}} dataKey="name" />
        <YAxis 
                  tick={{ fill: theme.palette.text.primary }}
                  stroke={theme.palette.divider} 
          style={{fontSize: 12}} />
        <Tooltip content={<CustomTooltip />} />
        <Legend content={<CustomLegend />} />
        <Area
          type="monotone"
          dataKey="views"
          stackId="1"
          stroke="#8884d8"
          fill="#8884d8"
        />
        <Area
          type="monotone"
          dataKey="members"
          stackId="1"
          stroke="#82ca9d"
          fill="#82ca9d"
        />
      </AreaChart>
    ),
  };

  return (
    <Box sx={{ 
      width: '90%',
      height: 500,
      p: 2
    }}>
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          {Object.keys(chartTypes).map((type) => (
            <Button
              key={type}
              variant={chartType === type ? 'solid' : 'soft'}
              onClick={() => setChartType(type)}
              aria-label={`Switch to ${type} chart`}
            >
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </Button>
          ))}
        </Box>
      </Box>
      <ResponsiveContainer>
        {chartTypes[chartType]}
      </ResponsiveContainer>
    </Box>
  );
}