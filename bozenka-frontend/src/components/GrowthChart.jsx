import React, { useState } from "react";
import {
    LineChart,
    Line,
    XAxis,
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
import {
    Box,
    Typography,
    useTheme,
    IconButton,
    Button,
    Grid,
    Card,
    Avatar,
    Divider
} from "@mui/joy";
import DownloadIcon from '@mui/icons-material/Download';


export default function DynamicChart({ data, displayData }) {
    const theme = useTheme();
    const [chartType, setChartType] = useState('line');
    const [hoveredDataPoint, setHoveredDataPoint] = useState(null);

    const dataKeys = Object.keys(displayData);

    // Dynamic calculations
    const averages = dataKeys.reduce((acc, key) => {
        acc[key] = data.reduce((sum, curr) => sum + curr[key], 0) / data.length;
        return acc;
    }, {});

    const colors = dataKeys.reduce((acc, key) => {
        acc[key] = displayData[key].color
        return acc;
    }, {});

    // CSV Export
    const exportData = () => {
        const headers = ["Date", ...dataKeys.map(k => displayData[k].shortTitle)];
        const csvContent = "data:text/csv;charset=utf-8,"
            + [headers.join(",")]
                .concat(data.map(row =>
                    [row.name, ...dataKeys.map(k => row[k])].join(",")
                ))
                .join("\n");

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "chart_data.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    // Custom Components
    const CustomLegend = ({ payload }) => (
        <Card variant="outlined" sx={{ p: 2, mt: 2 }}>
            <Box sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                mb: 1
            }}>
                <Typography level="title-sm" fontWeight="bold">
                    Metrics Legend
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
                {payload.map(({ value, color }, index) => (
                    <Grid xs={12} sm={6} key={value}>
                        <Box sx={{
                            display: "flex",
                            alignItems: "center",
                            gap: 2,
                            p: 1,
                            borderRadius: 'sm',
                            transition: 'all 0.2s',
                            '&:hover': { backgroundColor: 'background.level1' }
                        }}>
                            <Avatar
                                size="md"
                                variant="soft"
                            >
                                {displayData[value].icon}
                            </Avatar>
                            <Box>
                                <Typography level="title-sm">
                                    {displayData[value].shortTitle}
                                </Typography>
                                <Typography level="body-xs" color="neutral">
                                    Avg: {Math.round(averages[value])}
                                </Typography>
                            </Box>
                        </Box>
                    </Grid>
                ))}
            </Grid>
        </Card>
    );

    const CustomTooltip = ({ active, payload, label }) => {
        if (!active || !payload) return null;

        return (
            <Card variant="outlined" sx={{
                boxShadow: 'md',
                backgroundColor: 'background.surface',
                p: 2
            }}>
                <Typography level="title-sm" fontWeight="lg" mb={1}>
                    {label}
                </Typography>
                <Divider sx={{ mb: 1 }} />
                {payload.map(({ name, value, color }) => (
                    <Box
                        key={name}
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 1.5,
                            mb: 1,
                            '&:last-child': { mb: 0 }
                        }}
                    >
                        <Box sx={{ color }}>{displayData[name].icon}</Box>
                        <Box>
                            <Typography level="body-xs">
                                {displayData[name].shortTitle}
                            </Typography>
                            <Typography fontWeight="lg" sx={{ color }}>
                                {value}
                            </Typography>
                        </Box>
                    </Box>
                ))}
            </Card>
        );
    };

    // Chart Configurations
    const chartComponents = {
        line: (
            <LineChart
                data={data}
                margin={{ top: 20, right: 30, left: 20, bottom: 70 }}
                onMouseMove={(e) => setHoveredDataPoint(e?.activePayload?.[0]?.name)}
                onMouseLeave={() => setHoveredDataPoint(null)}
            >
                <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
                <XAxis
                    dataKey="name"
                    stroke={theme.palette.divider}
                    tick={{ fill: theme.palette.text.primary }}
                    style={{ fontSize: 12 }}
                />
                <YAxis
                    stroke={theme.palette.divider}
                    tick={{ fill: theme.palette.text.primary }}
                    style={{ fontSize: 12 }}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend content={<CustomLegend />} />
                {dataKeys.map(key => (
                    <ReferenceLine
                        key={key}
                        y={averages[key]}
                        stroke={colors[key]}
                        strokeDasharray="3 3"
                        label={{
                            value: `Avg ${displayData[key].shortTitle}`,
                            fill: colors[key],
                            fontSize: 12
                        }}
                    />
                ))}
                {dataKeys.map(key => (
                    <Line
                        key={key}
                        type="monotone"
                        dataKey={key}
                        stroke={colors[key]}
                        strokeWidth={2}
                        dot={{ fill: colors[key], r: 4 }}
                        activeDot={{ r: 8 }}
                        animationDuration={500}
                    />
                ))}
            </LineChart>
        ),
        bar: (
            <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
                <XAxis
                    dataKey="name"
                    stroke={theme.palette.divider}
                    tick={{ fill: theme.palette.text.primary }}
                    style={{ fontSize: 12 }}
                />
                <YAxis
                    stroke={theme.palette.divider}
                    tick={{ fill: theme.palette.text.primary }}
                    style={{ fontSize: 12 }}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend content={<CustomLegend />} />
                {dataKeys.map(key => (
                    <Bar
                        key={key}
                        dataKey={key}
                        fill={colors[key]}
                    />
                ))}
            </BarChart>
        ),
        area: (
            <AreaChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
                <XAxis
                    dataKey="name"
                    stroke={theme.palette.divider}
                    tick={{ fill: theme.palette.text.primary }}
                    style={{ fontSize: 12 }}
                />
                <YAxis
                    stroke={theme.palette.divider}
                    tick={{ fill: theme.palette.text.primary }}
                    style={{ fontSize: 12 }}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend content={<CustomLegend />} />
                {dataKeys.map(key => (
                    <Area
                        key={key}
                        type="monotone"
                        dataKey={key}
                        stroke={colors[key]}
                        fill={colors[key]}
                        fillOpacity={0.2}
                    />
                ))}
            </AreaChart>
        ),
    };

    return (
        <Box sx={{
            height: 500,
            p: 2,
            backgroundColor: 'background.surface',
            borderRadius: 'sm',
        }}>
            <Box sx={{
                mb: 2,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                <Box sx={{ display: 'flex', gap: 1 }}>
                    {Object.keys(chartComponents).map(type => (
                        <Button
                            key={type}
                            variant={chartType === type ? 'solid' : 'soft'}
                            onClick={() => setChartType(type)}
                            sx={{ textTransform: 'capitalize' }}
                        >
                            {type}
                        </Button>
                    ))}
                </Box>
            </Box>
            <ResponsiveContainer width="100%" height="90%">
                {chartComponents[chartType]}
            </ResponsiveContainer>
        </Box>
    );
}