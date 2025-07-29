// React related components
import * as React from 'react';
import { useState, useEffect, useMemo } from 'react';

// Some React Router magic
import { Outlet, Link, useLocation } from 'react-router-dom';

// Some MUI magic
import useMediaQuery from '@mui/material/useMediaQuery';

// MUI Joy UI controls
import CircularProgress from '@mui/joy/CircularProgress';
import {FormControl, FormLabel, FormHelperText, List, ListItem, ListSubheader} from '@mui/joy';
import Snackbar from '@mui/joy/Snackbar';
import Card from '@mui/joy/Card';
import Input from '@mui/joy/Input';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import Stack from '@mui/joy/Stack';
import Avatar from '@mui/joy/Avatar';
import Grid from '@mui/joy/Grid';
import Button from '@mui/joy/Button';
import Divider from '@mui/joy/Divider';
import Tabs from '@mui/joy/Tabs';
import TabList from '@mui/joy/TabList';
import Tab, { tabClasses } from '@mui/joy/Tab';
import TabPanel from '@mui/joy/TabPanel';
import Accordion, { accordionClasses } from '@mui/joy/Accordion';
import AccordionDetails from '@mui/joy/AccordionDetails';
import AccordionGroup from '@mui/joy/AccordionGroup'; 
import AccordionSummary from '@mui/joy/AccordionSummary';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import Chip from '@mui/joy/Chip';
import ListItemContent from '@mui/joy/ListItemContent';
import IconButton from '@mui/joy/IconButton';
import Sheet from '@mui/joy/Sheet';
import ListItemButton from '@mui/joy/ListItemButton';
import Breadcrumbs from '@mui/joy/Breadcrumbs';
import RadioGroup from '@mui/joy/RadioGroup';
import Radio from '@mui/joy/Radio';
import Checkbox from '@mui/joy/Checkbox';
import Textarea from '@mui/joy/Textarea';

// Our own controls
import DynamicChart from 'src/components/GrowthChart';
import NotificationCenter from 'src/components/NotificationCenter';
import ColorModeToggle from 'src/components/ColorModeToggle';


// MUI material theme icons
import SearchIcon from '@mui/icons-material/SearchRounded';
import PersonIcon from '@mui/icons-material/Person';
import CalendarMonthRoundedIcon from '@mui/icons-material/CalendarMonthRounded';
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import HandymanRoundedIcon from '@mui/icons-material/HandymanRounded';
import TrendingUpRoundedIcon from '@mui/icons-material/TrendingUpRounded';
import VisibilityRoundedIcon from '@mui/icons-material/VisibilityRounded';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import PeopleRoundedIcon from '@mui/icons-material/PeopleRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import NotificationsRoundedIcon from '@mui/icons-material/NotificationsRounded';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';
import LinkIcon from '@mui/icons-material/Link';
import AlternateEmailRoundedIcon from '@mui/icons-material/AlternateEmailRounded';
import EditIcon from '@mui/icons-material/Edit';
import SecurityIcon from '@mui/icons-material/SecurityRounded';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import DnsRoundedIcon from '@mui/icons-material/DnsRounded';
import QueryStatsRoundedIcon from '@mui/icons-material/QueryStatsRounded';
import MailRoundedIcon from '@mui/icons-material/MailRounded';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import EditRoundedIcon from '@mui/icons-material/EditRounded';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DescriptionRoundedIcon from '@mui/icons-material/DescriptionRounded';
import BadgeRoundedIcon from '@mui/icons-material/BadgeRounded';
import AccessibilityNewRoundedIcon from '@mui/icons-material/AccessibilityNewRounded';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

// Authorization
import { useAuth } from 'src/api/contexts/AuthContext.jsx';
import { useApi } from 'src/api/hooks/useApi.js';
import BaseClientAPI from 'src/api/BaseClientAPI.js';
import ErrorOutlinedIcon from "@mui/icons-material/ErrorOutlined";


  
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



const displayData = {
  members: {
    title: "Total members of communities",
    shortTitle: "Number of members",
    description: "Total number of communities members.",
    icon: <PeopleRoundedIcon/>,
    color: '#85ccff',
  },
  views: {
    title: "Views of the posts from all communities at this date.",
    shortTitle: "Views of the posts",
    description: "Total growth of number of views on posts at this date.",
    icon: <VisibilityRoundedIcon/>,
      color: "#4b45d7"
  }

}



/**
* React component for the dashboard layout.
* @returns {JSX.Element} - The rendered component.
*/
export function DashboardLayout(){

  const location = useLocation();

  const api = useApi();
  const [accountInfo, setAccountInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: ''
  });

  useEffect(() => {
    let isMounted = true;
    const fetchData = async () => {
      if (isMounted && !accountInfo) {
        try {
          const info = await api.getAccountInfo();
          if (isMounted) {
            setAccountInfo(info);
          }
        } catch (error) {
          console.error('Failed to fetch account info:', error);
          setSnackbar({
            open: true,
            message: `Failed to fetch account info. Please try again later. ${error.message}`
          });
        } finally {
          if (isMounted) {
            setLoading(false);
          }
        }
      }
    }
    fetchData();
    return () => {
      isMounted = false;
    };
  }, [api, accountInfo]);

  const handleSnackbarClose = () => {
    setSnackbar({
      ...snackbar,
      open: false
    });
  };




  // Buttons for the dashboard, made to speed up the editing buttons list &
  // localization in future.
  const buttons = {
    'Communities': [
        {
          head: 'Manage communities', 
          description: 'Manage your communities, add administrators, create posts, etc.', 
          destination: 'communities',
          icon: <HandymanRoundedIcon />
        },
        {
          head: 'Community building',
          description: 'Create or import your own social home or club by interests.',
          destination: 'build',
          icon: <AddRoundedIcon />
        },
      ],
      "Account": [
        {
          head: 'Manage account', 
          description: 'Manage your security, privacy of your account. Change avatar or name.', 
          destination: 'account',
          icon: <SettingsRoundedIcon />
        },
      ]
  };


    // Get current route path
    const currentPath = location.pathname.split('/').pop();

    // Authorization
    const {logout} = useAuth();




    // Active item styles
    const activeItemStyles = {
      borderLeft: '2px solid',
      '&:hover': {
        backgroundColor: 'primary.softHoverBg',
      },
      '& .MuiListItemDecorator-root': {
        color: 'primary.main',
      },
      '& .MuiTypography-root': {
        color: 'primary.main',
        fontWeight: 600,
      }
    };
  
    // Common button styles
    const buttonStyles = {
      transition: 'all 0.2s ease',
      my: 0.4,
      '&.Mui-selected': activeItemStyles
    };


  // Using MUI's useMediaQuery to check, if screen is mobile.
  const isMobile = useMediaQuery('@media (max-width:1000px)'); 

  return(
    <>
    <Box sx={{ display: 'flex', height: '100%',
      '@media (max-width:1000px)': {
        height: '100%'
      }}}>
    {(!isMobile) && (
      <Sheet
          sx={{
            width: 300,
            minWidth: 300,
            p: 2,
            borderRight: '1px solid',
            borderColor: 'divider',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
        <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 2, p: 1}}>
        {loading ? (
                  <CircularProgress size="sm" />
                ) : (
              <>
              {accountInfo.image ? <Avatar src={`${import.meta.env.REACT_APP_API_URL || 'http://localhost:8000'}${accountInfo.image}`}/> : <Avatar>{accountInfo?.display_name?.[0] || accountInfo?.username?.[0] || 'user'}</Avatar>}
               <Box>
                  <>
                    <Typography level="h5" element="h5" fontWeight='bold'>
                      Welcome, {accountInfo?.display_name || accountInfo?.username || 'user'}
                    </Typography>
                    <Typography color='neutral' level="body-xs">
                      {accountInfo?.email}
                    </Typography>     
                    <Typography level="body-xs">
                      Have a nice day!
                    </Typography>
                  </>
              </Box></>)}
        </Box>
        <Box sx={{px: 0.8}}>
        <List
              size="sm"
              sx={{
                '--ListItem-radius': '8px',
                '--ListItemDecorator-size': '32px',
              }}
            >            <Link to="" style={{ textDecoration: 'none' }}>
            <ListItem>
              <ListItemButton 
                selected={currentPath === '' || currentPath === 'dashboard'}
                sx={buttonStyles}
              >
                <ListItemDecorator>
                  <HomeRoundedIcon />
                </ListItemDecorator>
                <ListItemContent>
                  <Typography level='title-xs'>Home</Typography>
                  <Typography level='body-xs'>Overview of your Dashboard</Typography>
                </ListItemContent>
              </ListItemButton>
            </ListItem>
          </Link>


          {Object.entries(buttons).map(([section, items]) => (
              <ListItem nested key={section}>
                <ListSubheader>{section}</ListSubheader>
                <List>
                  {items.map((item) => (
                    <Link 
                      key={item.destination}
                      to={item.destination}
                      style={{ textDecoration: 'none' }}
                    >
                      <ListItem>
                        <ListItemButton
                          selected={currentPath === item.destination}
                          sx={buttonStyles}
                        >
                          <ListItemDecorator>{item.icon}</ListItemDecorator>
                          <ListItemContent>
                            <Typography level='title-xs'>{item.head}</Typography>
                            <Typography level='body-xs'>{item.description}</Typography>
                          </ListItemContent>
                        </ListItemButton>
                      </ListItem>
                    </Link>
                  ))}
                </List>
              </ListItem>
            ))}

      </List>
      <Box sx={{ display: 'flex', gap: 1, mt: 2}}>
            
        <IconButton
          variant="soft"
          color="primary"
          sx={{
            minWidth: 40,
            minHeight: 40,
            borderRadius: '50%',
            position: 'relative',
          }}
          >
            <NotificationsRoundedIcon />
            <Chip
              size="sm"
              variant="solid"
              color="danger"
              sx={{
                position: 'absolute',
                top: 0,
                right: 0,
                p: 1,
                py: 0,
                transform: 'translate(30%, -30%)',
              }}
              >
                3
              </Chip>
        </IconButton>
        <IconButton
          onClick={() => logout()}
          variant="soft"
          sx={{
            minWidth: 40,
            minHeight: 40,
            borderRadius: '50%',
          }}
        >
          <LogoutRoundedIcon/>  
        </IconButton>
        <ColorModeToggle />
      </Box>
      </Box>
        <Snackbar
            variant="solid"
            color="danger"
            open={snackbar.open}
            onClose={handleSnackbarClose}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            startDecorator={<ErrorOutlinedIcon />}
            autoHideDuration={6000}
        >
          {snackbar.message}
        </Snackbar>
    </Sheet>
    )}

    <Box sx={{p: 3,
                flexGrow: 1,
                bgcolor: 'background.level1',
    
      width: '70%',
      '@media (max-width:1000px)': {
      }
    }}>
      <Outlet/>
    </Box>
    </Box>
    </>
  )
}


/**
* React component (page) for the dashboard homepage.
* Shows the quick overview of the current situation of communities for user.
* @returns {JSX.Element} - The rendered component.
*/
export function DashboardHomepage() {
  const [loading, setLoading] = React.useState(false);
  const [selectedPeriod, setSelectedPeriod] = React.useState('week');
  
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

  
  const stats = [
    {
      label: 'Total Members',
      value: '12.5K',
      change: '+12%',
      trend: 'up',
      icon: <PeopleRoundedIcon />,
      color: 'primary'
    },
    {
      label: 'Active Users',
      value: '8.2K',
      change: '+8%',
      trend: 'up',
      icon: <VisibilityRoundedIcon />,
      color: 'success'
    },
    {
      label: 'Engagement Rate',
      value: '85%',
      change: '+5%',
      trend: 'up',
      icon: <TrendingUpRoundedIcon />,
      color: 'warning'
    }
  ];


  const displayData = {
    members: {
      title: "Total members of communities",
      shortTitle: "Number of members",
      description: "Total number of communities members.",
      icon: <PeopleRoundedIcon/>,
      color: '#85ccff',
    },
    views: {
      title: "Views of the posts from all communities at this date.",
      shortTitle: "Views of the posts",
      description: "Total growth of number of views on posts at this date.",
      icon: <VisibilityRoundedIcon/>,
      color: "#4b45d7"
    }
  
  }



  return (
    <Box sx={{width: '100%'}}>
    <Breadcrumbs 
          size="sm"
          separator={ <KeyboardArrowRightIcon/>}>
          <Typography sx={{mt: 0}}>Dashboard</Typography>
          <Typography sx={{mt: 0, color: 'primary.plainColor'}}>Home</Typography>
      </Breadcrumbs>
    {/* Header Section */}
    <Box my={2} px={1}>
    <Typography level="h2" sx={{}}>
      Dashboard Overview
    </Typography>
    <Typography level="body-md" color="neutral">
      Welcome back! Here's what's happening with your communities.
    </Typography>
  </Box>
    <Box sx={{display: 'flex', flexDirection: 
      { xs: 'column', md: 'row' }}}>



      {/* Stats Cards Grid */}
      <Box sx={{flexDirection: 'column', display: 'flex'}}>
      <Box spacing={2} sx={{ mb: 1, flexDirection: 'row', display: 'flex', mr: 3}}>
        {stats.map((stat, index) => (
          <Box key={index} sx={{m: 1}}>
            <Card>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Avatar color={stat.color} variant='soft'>
                  {stat.icon}
                </Avatar>
                <Box>
                  <Typography level="body-sm" color="neutral">
                    {stat.label}
                  </Typography>
                  <Typography level="h3">{stat.value}</Typography>
                  <Chip
                    size="sm"
                    variant="soft"
                    color={stat.trend === 'up' ? 'success' : 'danger'}
                    startDecorator={
                      stat.trend === 'up' ? <TrendingUpRoundedIcon /> : null
                    }
                  >
                    {stat.change}
                  </Chip>
                </Box>
              </Box>
            </Card>
          </Box>
        ))}
      </Box>
      {/* Chart Section */}
      <Card sx={{ p: 2, height: 'auto' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography level="title-lg">Growth Analytics</Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            {['week', 'month', 'year'].map((period) => (
              <Button
                key={period}
                size="sm"
                variant={selectedPeriod === period ? 'solid' : 'soft'}
                onClick={() => setSelectedPeriod(period)}
              >
                {period.charAt(0).toUpperCase() + period.slice(1)}
              </Button>
            ))}
          </Box>
        </Box>
        {loading ? (
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              height: 400,
            }}
          >
            <CircularProgress />
          </Box>
        ) : (
          <Box sx={{}}>
            <TestChart sx={{height: 10}} data={data} displayData={displayData} />
            </Box>
        )}
      </Card>
      </Box>
      {/* Recent Activity Section */}
      <Card sx={{mx: 3, width: 'auto', my: 2, height: {'xs': 200, md: 'auto'}}}>
        <Typography level="title-lg" sx={{ mb: 2 }}>
          Recent Activity
        </Typography>
        <List>
          {[1, 2, 3].map((item) => (
            <ListItem
              key={item}
              endAction={
                <Typography level="body-sm" color="neutral">
                  2h ago
                </Typography>
              }
            >
              <ListItemButton sx={{
                borderRadius: 'lg',
                transition: 'background-color 0.2s ease'
              }}>
                <ListItemDecorator>
                  <Avatar size="sm" />
                </ListItemDecorator>
                <ListItemContent>
                  <Typography level="title-sm">
                    New member joined Community Alpha
                  </Typography>
                  <Typography level="body-sm" color="neutral">
                    John Doe joined your community
                  </Typography>
                </ListItemContent>
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Card>
      </Box>
    </Box>
  );
}


/**
* React component for building a community dashboard.
* @returns {JSX.Element} - The rendered component.
*/
export function DashboardBuildCommunity() {
  return <>
        <Breadcrumbs 
          size="sm"
          separator={ <KeyboardArrowRightIcon/>}>
        <Link to='..' style={{color: 'var(--joy-palette-text-tertiary)'}} >
          <Typography sx={{}}>
            Dashboard
          </Typography>
        </Link>
          <Typography sx={{mt: 0, color: 'primary.plainColor'}}>Community building</Typography>
      </Breadcrumbs>
    
      <Typography level='h2' my={2} px={1}>
            Build Community
        </Typography>
    <Box sx={{display: 'flex', justifyContent: 'center', width: '100%', my: 3}}>
    <Card sx={{width: 'auto'}}>
        <Typography level='body-md' sx={{textAlign: 'center'}}>
          What you would like to do?
        </Typography>
        <Box sx={{display: 'flex', flexDirection: 'row'}}>
        <Link to='import'>
          <Button variant="plain" size="lg" sx={{
                          p: 1.5,
                          m: 0.5,
                          transition: 'transform 0.2s ease, background-color 0.2s ease',
                          border: '1px',
                          '&:hover': {
                              transform: 'scale(1.05)',
                              bgcolor: 'primary.lightBg',
                              borderRadius: '',
                          },
                          '&:active': {
                              transform: 'scale(1.20)'
                          },
                          display: 'flex',
                          flexDirection: 'column', 
                          alignItems: 'center', 
                      }}
                      startDecorator={<AutoAwesomeIcon sx={{ marginBottom: 1, fontSize: '50px'}}/>}
                      >
                    
                          I want to import my community
          </Button>
        </Link>
        <Link to='create'>
          <Button variant="plain" size="lg" sx={{
                          p: 1.5,
                          m: 0.5,
                          transition: 'transform 0.2s ease, background-color 0.2s ease',
                          border: '1px',
                          '&:hover': {
                              transform: 'scale(1.05)',
                              bgcolor: 'primary.lightBg',
                              borderRadius: '',
                          },
                          '&:active': {
                              transform: 'scale(1.20)'
                          },
                          display: 'flex',
                          flexDirection: 'column', 
                          alignItems: 'center', 
                      }} 
                      
                      startDecorator={<AddCircleIcon sx={{ marginBottom: 1, fontSize: '50px'}}/>}
                      >
                    
                          I want to create my community
          </Button>
        </Link>
        </Box>
    </Card>
    </Box>
  </>
}



/**
 * React component for creating a new community.
 * @returns {JSX.Element} - The rendered component.
 */
export function DashboardCreateCommunity() {
  const [communityData, setCommunityData] = useState({
    name: '',
    description: '',
    logo: null,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCommunityData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    setCommunityData(prev => ({
      ...prev,
      logo: file
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission logic here
    console.log('Community Data:', communityData);
  };

  return (
    <>
      <Breadcrumbs 
        size="sm"
        separator={<KeyboardArrowRightIcon/>}
      >
        <Link to='..' style={{color: 'var(--joy-palette-text-tertiary)'}} >
          <Typography sx={{}}>
            Dashboard
          </Typography>
        </Link>
       <Link to='/dashboard/build/' style={{color: 'var(--joy-palette-text-tertiary)'}}>
        <Typography>
          Community building
          </Typography>
        </Link>
        <Typography color="primary">Create Community</Typography>
      </Breadcrumbs>

      <Typography level='h2' my={2} px={1} sx={{textAlign: 'center'}}>
            Create new community
        </Typography>

      <Card sx={{ maxWidth: 600, mx: 'auto', p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Stack spacing={3}>
            <FormControl>
              <FormLabel>Community Name</FormLabel>
              <Input
                name="name"
                value={communityData.name}
                onChange={handleInputChange}
                required
                fullWidth
              />
            </FormControl>

            <FormControl>
              <FormLabel>Description</FormLabel>
              <Textarea
                name="description"
                value={communityData.description}
                onChange={handleInputChange}
                minRows={3}
                required
                fullWidth
              />
            </FormControl>

            <FormControl>
              <FormLabel>Community Logo</FormLabel>
              <Button
                component="label"
                variant="outlined"
                startIcon={<CloudUploadIcon />}
                sx={{ mt: 1 }}
              >
                Upload Logo
                <input
                  type="file"
                  hidden
                  accept="image/*"
                  onChange={handleFileUpload}
                />
              </Button>
              {communityData.logo && (
                <Typography variant="body2" mt={1}>
                  Selected file: {communityData.logo.name}
                </Typography>
              )}
            </FormControl>

            <Button type="submit" variant="contained" size="large">
              Create Community
            </Button>
          </Stack>
        </form>
      </Card>
    </>
  );
}

/**
 * React component for importing an existing community.
 * @returns {JSX.Element} - The rendered component.
 */
export function DashboardImportCommunity() {
  const [importData, setImportData] = useState({
    platform: '',
    communityUrl: '',
    configFile: null,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setImportData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    setImportData(prev => ({
      ...prev,
      configFile: file
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission logic here
    console.log('Import Data:', importData);
  };

  return (
    <>
      <Breadcrumbs 
        size="sm"
        separator={<KeyboardArrowRightIcon/>}
      >
        <Link to='..' style={{color: 'var(--joy-palette-text-tertiary)'}} >
          <Typography sx={{}}>
            Dashboard
          </Typography>
        </Link>
       <Link to='/dashboard/build/' style={{color: 'var(--joy-palette-text-tertiary)'}}>
        <Typography>
          Community building
          </Typography>
        </Link>
        <Typography color="primary">Import Community</Typography>
      </Breadcrumbs>

      <Typography level='h2' my={2} px={1} sx={{textAlign: 'center'}}>
            Import existing community from platform
        </Typography>

      <Card sx={{ maxWidth: 600, mx: 'auto', p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Stack spacing={3}>
            <FormControl>
              <FormLabel>Select Platform</FormLabel>
              <RadioGroup
                name="platform"
                value={importData.platform}
                onChange={handleInputChange}
                row
              >

      <List sx={{
        minWidth: 240,
        '--List-gap': '0.5rem',
        '--ListItem-paddingY': '1rem',
        '--ListItem-radius': '8px',
        '--ListItemDecorator-size': '32px',}}>
            <ListItem variant="outlined">
              <div>
                <FormLabel>Telegram</FormLabel>
                <FormHelperText>Cross-platform messaging app with a focus on speed and security, 
                  it is super-fast, simple and free.</FormHelperText>
              </div>
              <Radio
                overlay
                value='telegram'
                sx={{ flexGrow: 1, flexDirection: 'row-reverse'}}
              />

            </ListItem>
            <ListItem variant="outlined">
              <div>
                <FormLabel>Vkontakte</FormLabel>
                <FormHelperText>Russia social network, the largest social network in Russia.</FormHelperText>
              </div>
              <Radio
                overlay
                value='vk'
                sx={{ flexGrow: 1, flexDirection: 'row-reverse'}}
              />

            </ListItem>
            <ListItem variant="outlined">
              <div>
                <FormLabel>Discord</FormLabel>
                <FormHelperText>Free online platform, what support calls and messages. For Gamers.</FormHelperText>
              </div>
              <Radio
                overlay
                value='discord'
                sx={{ flexGrow: 1, flexDirection: 'row-reverse'}}
              />

            </ListItem>


      </List>
              </RadioGroup>
            </FormControl>

            <FormControl>
              <FormLabel>Community URL</FormLabel>
              <Input
                name="communityUrl"
                value={importData.communityUrl}
                onChange={handleInputChange}
                placeholder="https://"
                required
                fullWidth
              />
            </FormControl>

            <FormControl>
              <FormLabel>Configuration File (Optional)</FormLabel>
              <Button
                component="label"
                variant="outlined"
                startIcon={<CloudUploadIcon />}
                sx={{ mt: 1 }}
              >
                Upload Config
                <input
                  type="file"
                  hidden
                  accept=".json,.yaml,.yml"
                  onChange={handleFileUpload}
                />
              </Button>
              {importData.configFile && (
                <Typography variant="body2" mt={1}>
                  Selected file: {importData.configFile.name}
                </Typography>
              )}
            </FormControl>

            <Button type="submit" variant="contained" size="large">
              Import Community
            </Button>
          </Stack>
        </form>
      </Card>
    </>
  );
}



/**
* React component for controlling the communities of user in
* dashboard.
* @returns {JSX.Element} - The rendered component.
*/
export function DashboardControlCommunity() {
  // State management
  const [tabIndex, setTabIndex] = React.useState(0);
  const [selectedCommunity, setSelectedCommunity] = React.useState(null);
  const [selectedCommunityInfo, setSelectedCommunityInfo] = React.useState(null);
  const [searchQuery, setSearchQuery] = React.useState('');
  const [isEditing, setIsEditing] = React.useState(false);
  const [editForm, setEditForm] = React.useState({
    name: '',
    description: '',
    short_description: ''
  });

    // Memoize the form data to prevent re-renders when not needed
    const editFormData = useMemo(() => ({
      name: editForm.name,
      description: editForm.description,
      short_description: editForm.short_description
    }), [editForm]);
  
    // Memoize form handlers
    const handleNameChange = useMemo(
      () => (e) => setEditForm({ ...editForm, name: e.target.value }),
      [editForm]
    );
  
    const handleDescriptionChange = useMemo(
      () => (e) => setEditForm({ ...editForm, description: e.target.value }),
      [editForm]
    );
  
    const handleShortDescChange = useMemo(
      () => (e) => setEditForm({ ...editForm, short_description: e.target.value }),
      [editForm]
    );
  
    
  // Styles for inputs
  const inputStyles = {
    width: '100%',
    '--Input-focusedThickness': '1px',
    bgcolor: 'background.level0',
    borderRadius: 'lg',
    '&:hover': {
      borderColor: 'background.level2',
    },
    '&:focus-within': {
      borderColor: 'background.level2',
    },
    '&:focus': {
      outline: 'none',
    },
    mb: 2,
    py: 1,
    px: 2,
    fontSize: 'sm',
    fontWeight: 'md',
    transition: 'box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out, background-color 0.2s ease-in-out',
    '&::placeholder': {
      color: 'neutral.500',
      fontStyle: 'italic',
    },
    '&:disabled': {
      bgcolor: 'neutral.100',
      color: 'neutral.400',
      cursor: 'not-allowed',
    },
  };
    
  const api = useApi();
  const [privateCommunities, setPrivateCommunities] = useState(null);
  const [loading, setLoading] = useState(true);

  // Data fetching
  useEffect(() => {

    let isMounted = true;
    const fetchData = async () => {
      if (isMounted && !privateCommunities) {
        console.log("Fetching private communities...");
        try {
          const info = await api.getPrivateCommunities();
          if (isMounted) {
            setPrivateCommunities(info);
            if (info.length > 0) {
              setSelectedCommunity(info[0]);
              const communityInfo = await api.getPrivateCommunity(info[0].id);
              setSelectedCommunityInfo(communityInfo);
              setEditForm({
                name: communityInfo.community_info.name,
                description: communityInfo.community_info.description,
                short_description: communityInfo.community_info.short_description
              });
            }
            setLoading(false);
          }
        } catch (error) {
          console.error('Failed to fetch communities list:', error);
        } finally {
          if (isMounted) {
            setLoading(false);
          }
        }
      }
    }
    fetchData();
    return () => {
      isMounted = false;
    };
  }, [api, privateCommunities]);

  // Event handlers
  const handleCommunitySelect = async(community) => {
    try {
      const community_detailed = await api.getPrivateCommunity(community.id);
      setSelectedCommunity(community);
      setSelectedCommunityInfo(community_detailed);
      setEditForm({
        name: community_detailed.community_info.name,
        description: community_detailed.community_info.description,
        short_description: community_detailed.community_info.short_description
      });
    } catch (error) {
      console.error('Failed to fetch community details:', error);
    }
  };

  const handleEditSubmit = async () => {
    try {
      await api.updateCommunityBaseInformation(selectedCommunity.id, editForm);
      const updated = await api.getPrivateCommunity(selectedCommunity.id);
      setSelectedCommunityInfo(updated);
      setIsEditing(false);
      const updatedCommunities = await api.getPrivateCommunities();
      setPrivateCommunities(updatedCommunities);
      setCo
    } catch (error) {
      console.error('Failed to update community:', error);
    }
  };

  // Filter communities based on search
  const filteredCommunities = privateCommunities ? privateCommunities.filter(community =>
    community.name.toLowerCase().includes(searchQuery.toLowerCase())
  ) : [];

  // Component sections
  const GeneralTabContent = () => (
    <>
      {isEditing ? (
        <Box sx={{ p: 2, height: '100%' }}>
        <FormControl sx={{ mb: 2, width: '100%' }}>
          <FormLabel>Community Name</FormLabel>
          <Input
            startDecorator={<BadgeRoundedIcon/>}
            value={editFormData.name}
            onChange={handleNameChange}
            sx={inputStyles}
          />
        </FormControl>
        <FormControl sx={{ mb: 2, width: '100%' }}>
          <FormLabel>Short Description</FormLabel>
          <Input
            startDecorator={<DescriptionRoundedIcon/>}
            value={editFormData.short_description}
            onChange={handleShortDescChange}
            sx={inputStyles}
          />
        </FormControl>
        <FormControl sx={{ mb: 2, width: '100%' }}>
          <FormLabel>Full Description</FormLabel>
          <Textarea
            minRows={3}
            value={editFormData.description}
            onChange={handleDescriptionChange}
            sx={inputStyles}
          />
        </FormControl>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button onClick={handleEditSubmit} color="primary">Save</Button>
          <Button onClick={() => setIsEditing(false)} variant="outlined">Cancel</Button>
        </Box>
      </Box>
      ) : (
        <>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography level="body-xs">
              {selectedCommunityInfo?.community_info.description}
            </Typography>
            <Button 
              startDecorator={<EditIcon />}
              onClick={() => setIsEditing(true)}
              size="sm"
            >
              Edit
            </Button>
          </Box>
          <Grid container spacing={2} sx={{ my: 2 }}>
            {[
              {
                label: 'Members',
                value: selectedCommunityInfo?.community_info?.members_count || 0,
                icon: <PersonIcon />,
                color: 'primary'
              },
              {
                label: 'Engagement',
                value: '100%',
                icon: <TrendingUpRoundedIcon />,
                color: 'success'
              },
              {
                label: 'Last Active',
                value: '100pm',
                icon: <CalendarMonthRoundedIcon />,
                color: 'warning'
              }
            ].map((stat, index) => (
              <Grid xs={12} md={3} key={index}>
                <Card variant='outlined' sx={{ p: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Avatar color={stat.color}>
                      {stat.icon}
                    </Avatar>
                    <Box>
                      <Typography level="body-xs">{stat.label}</Typography>
                      <Typography level="h4">{stat.value}</Typography>
                    </Box>
                  </Box>
                </Card>
              </Grid>
            ))}
          </Grid>
        </>
      )}
    </>
  );

  const PostsTabContent = () => (
    <Box sx={{ p: 2 }}>
      <Grid container spacing={1}>
        {selectedCommunityInfo?.posts?.map((post, index) => (
          <Grid item key={index} xs={12} sm={6} md={4} lg={3}>
            <Box my={0.5}>
              <Card sx={{ height: '100%' }}>
                <Typography level="title-lg" sx={{marginBottom: -1}}>
                  {post.text}
                </Typography>
                <Typography level="body-sm">
                  {post.text}
                </Typography>
                <Box>
                  <Typography 
                    startDecorator={<CalendarMonthRoundedIcon />} 
                    sx={{m: 0.2}} 
                    level="body-xs"
                  >
                    Posted at {new Date(post.created_at).toLocaleString()}
                  </Typography>
                  <Chip 
                    variant="soft" 
                    startDecorator={<OpenInNewIcon />} 
                    color="primary" 
                    size="md" 
                    sx={{borderRadius: 'sm', m: 0.2}}
                  >
                    {post.source}
                  </Chip>
                  <Chip 
                    variant="soft" 
                    startDecorator={<VisibilityRoundedIcon />} 
                    color="primary" 
                    size="md" 
                    sx={{borderRadius: 'sm', m: 0.2}}
                  >
                    {post.views} views
                  </Chip>
                </Box>
              </Card>
            </Box>
          </Grid>
        ))}
        {(!selectedCommunityInfo?.posts || selectedCommunityInfo.posts.length === 0) && (
          <Grid item xs={12}>
            <Typography level="body-lg" textAlign="center">
              No posts available
            </Typography>
          </Grid>
        )}
      </Grid>
    </Box>
  );

  console.log(filteredCommunities)

  // Main render
  return (
    <>
      {loading ? (
        <CircularProgress />
      ) : (

        <>
          <Breadcrumbs size="sm" separator={<KeyboardArrowRightIcon/>}>
            <Link to='..' style={{color: 'var(--joy-palette-text-tertiary)'}}>
              <Typography>Dashboard</Typography>
            </Link>
            <Typography sx={{mt: 0, color: 'primary.plainColor'}}>
              Manage Communities
            </Typography>
          </Breadcrumbs>

          <Box my={2} px={1}>
            <Typography level="h2">Manage Communities</Typography>
            <Typography level="body-md" color="neutral">
              Oversee and optimize your community spaces
            </Typography>
          </Box>

          <Stack direction={{ xs: 'column-reverse', md: 'row' }} spacing={1}>
            <Card sx={{ 
              width: {xs: '95%', md: '70%'}, 
              p: 3,
              minWidth: '70%', 
              maxHeight: 'auto',
            }}>
              {selectedCommunityInfo ? 
              <>
              <Box sx={{
                display: 'flex', 
                flexDirection: 'row',
              }}> 
                {selectedCommunityInfo?.community_info?.icon ? 
                  <Avatar src={`http://localhost:8000${selectedCommunityInfo.community_info.icon}`}/> : 
                  <Avatar>{selectedCommunityInfo?.community_info.name?.[0]}</Avatar>
                }
                <Box ml={1}>
                  <Typography level="title-lg" sx={{marginBottom: 0}}>
                    {selectedCommunityInfo?.community_info.name}
                  </Typography>
                  <Box sx={{display: 'flex', flexDirection: 'row'}}>
                    <Typography startDecorator={<PersonIcon/>} mr={1} level="body-xs">
                      {selectedCommunityInfo?.community_info.members_count} members
                    </Typography>
                    <Typography 
                      startDecorator={<CalendarMonthRoundedIcon/>}
                      level="body-xs"
                    >
                      Created on {new Date(selectedCommunity?.creation_date).toLocaleDateString()}
                    </Typography>
                  </Box>
                  <Typography color='neutral' level="body-xs">
                    Total growth: 
                    <Typography 
                      color="success" 
                      level="body-xs" 
                      startDecorator={<TrendingUpRoundedIcon/>}
                    > 
                      50% from last day 
                    </Typography>
                  </Typography>
                  <Box>
                    {selectedCommunityInfo?.community_info.tags.map(tag => (
                      <Chip 
                        key={tag.id}
                        variant="soft"
                        color='primary'
                        size='sm' 
                        startDecorator={
                          <Typography
                            component="span"
                            sx={{ 
                              fontFamily: 'Material Icons',
                              fontSize: '14px',
                              color: 'inherit',
                              display: 'flex',
                              alignItems: 'center',
                            }}
                          >
                            {tag.icon}
                          </Typography>
                        } 
                        sx={{borderRadius: 'sm', m: 0.5}}
                      >
                        {tag.name}
                      </Chip>
                    ))}
                  </Box>
                </Box>
              </Box>

              <Tabs 
                value={tabIndex}
                onChange={(event, value) => setTabIndex(value)}
                sx={{
                  borderRadius: 'md',
                  [`& .${tabClasses.root}`]: {
                    zIndex: 1,
                    transition: 'transform 0.2s ease, background-color 0.2s ease',
                    mx: 0.5,
                    paddingLeft: 1,
                    paddingRight: 1,
                    height: 0.1,
                    borderTopLeftRadius: '5px',
                    borderTopRightRadius: '5px',
                    '&:hover': {
                      transform: 'scale(1.05)',
                    },
                    '&[aria-selected="true"]': {
                      bgcolor: 'primary.softBgColor',
                      color: 'primary.softColor',
                      transition: 'all 0.5 ease'
                    },
                  },
                }}
              >
                <TabList>
                  <Tab>
                    <HomeRoundedIcon sx={{fontSize: 20}} />
                    <Typography level='title-sm'>General</Typography>
                  </Tab>
                  <Tab>
                    <SettingsRoundedIcon sx={{fontSize: 20}} />
                    <Typography level='title-sm'>Features</Typography>
                  </Tab>
                  <Tab>
                    <DnsRoundedIcon sx={{fontSize: 20}} />
                    <Typography level='title-sm'>Platforms</Typography>
                  </Tab>
                  <Tab>
                    <QueryStatsRoundedIcon sx={{fontSize: 20}} />
                    <Typography level='title-sm'>Statistics</Typography>
                  </Tab>
                  <Tab>
                    <MailRoundedIcon sx={{fontSize: 20}} />
                    <Typography level='title-sm'>Posts</Typography>
                  </Tab>
                </TabList>

                <TabPanel value={0} sx={{maxHeight: '1000px', overflowY: 'auto'}}>
                  <GeneralTabContent />
                </TabPanel>

                <TabPanel value={1}>
                  <FormControl sx={{my: 1}}>
                    <AccordionGroup
                      color="neutral"
                      size="sm"
                      sx={{
                        borderRadius: 'md',
                        [`& .${accordionClasses.root}`]: {
                          marginTop: '0.5rem',
                          transition: '0.2s ease, background-color 0.4 ease, transform 0.2 ease',
                          '& button:not([aria-expanded="true"])': {
                            transition: '0.2s ease',
                            paddingBottom: '0.625rem',
                          },
                          '& button:hover': {
                            background: 'transparent'
                          },
                          '& button:active': {
                            backgroundColor: 'background.level1',
                            borderRadius: 'md'
                          }
                        }
                      }}
                      variant="plain"
                      transition="0.2s"
                    >
                      <Accordion>
                        <AccordionSummary>
                          <Avatar color="primary">
                            <PersonIcon sx={{fontSize: 24}} />
                          </Avatar>
                          <ListItemContent>
                            <Typography level="title-md">Features for Members</Typography>
                            <Typography level="body-sm">
                              Change experience for Members of your community
                            </Typography>
                          </ListItemContent>
                        </AccordionSummary>
                        <AccordionDetails>
                          <List sx={{my: 1}}>
                            <ListItem>
                              <ListItemContent>
                                <Checkbox label="Allow to chat with Neural GPT models" size='sm' my={0} p={0} />
                                <FormHelperText>
                                  Members of your community will use command /conversations to chat with Neural GPT models and ask questions using Bozenka.
                                </FormHelperText>
                              </ListItemContent>
                            </ListItem>
                            <ListItem>
                              <ListItemContent>
                                <Checkbox label="Allow to generate images using Bozenka" size='sm' />
                                <FormHelperText>
                                  Members of your community will use command /imagine to start generation of images using diffusion neural models
                                </FormHelperText>
                              </ListItemContent>
                            </ListItem>
                            <ListItem>
                              <ListItemContent>
                                <Checkbox label="Enable custom welcome messages from Bozenka" size='sm' />
                                <FormHelperText>
                                  Bozenka will met new joined members with own custom message :)
                                </FormHelperText>
                              </ListItemContent>
                            </ListItem>
                            <ListItem>
                              <ListItemContent>
                                <Checkbox label="Enable bridges from different social platforms." size='sm' />
                                <FormHelperText>
                                  Bozenka will duplicate some messages of your community from one social platform in other channels of other social platform
                                </FormHelperText>
                              </ListItemContent>
                            </ListItem>
                          </List>
                        </AccordionDetails>
                      </Accordion>

                      <Accordion>
                        <AccordionSummary>
                          <Avatar color="primary">
                            <AccessibilityNewRoundedIcon sx={{fontSize: 24}}/>
                          </Avatar>
                          <ListItemContent>
                            <Typography level="title-md">Features for Administration</Typography>
                            <Typography level="body-sm">
                              Improve your community administration experience by this features.
                            </Typography>
                          </ListItemContent>
                        </AccordionSummary>
                        <AccordionDetails>
                          <List sx={{my: 1}}>
                            <ListItem>
                              <ListItemContent>
                                <Checkbox label="Enable statistics" size='sm' />
                                <FormHelperText>
                                  Bozenka will collect statistics to show it on your dashboard and community control page
                                </FormHelperText>
                              </ListItemContent>
                            </ListItem>
                            <ListItem>
                              <ListItemContent>
                                <Checkbox label="Enable Knowledge Library" size='sm' />
                                <FormHelperText>
                                  Bozenka will give abillity to create Knowledge Library, where you can publish your tutorials and rules of your community.
                                </FormHelperText>
                              </ListItemContent>
                            </ListItem>
                            <ListItem>
                              <ListItemContent>
                                <Checkbox label="Enable Moderation" size='sm' />
                                <FormHelperText>
                                  Bozenka will be able to ban, mute and kick users by your decision and decision of your administration
                                </FormHelperText>
                              </ListItemContent>
                            </ListItem>
                          </List>
                        </AccordionDetails>
                      </Accordion>
                    </AccordionGroup>
                  </FormControl>
                </TabPanel>

                <TabPanel value={2}>
                  <List>
                    {selectedCommunityInfo?.connection_data?.map((response, index) => (
                      <ListItem 
                        key={index}
                        sx={{
                          borderRadius: 'lg', 
                          p: 1, 
                          my: 1
                        }} 
                        variant='outlined'
                      >
                        <ListItemDecorator sx={{m: 1}}>
                          <LinkIcon sx={{fontSize: 40}}/>
                        </ListItemDecorator>
                        <ListItemContent>
                          <Typography level="title-md">
                            {response.platform}
                          </Typography>
                          <Box sx={{display: 'flex', flexDirection: 'row'}}>
                            <Typography startDecorator={<PersonIcon/>} mr={1} level="body-xs">
                              {response.members_count} Members
                            </Typography>
                            <Typography 
                              startDecorator={<CalendarMonthRoundedIcon/>}
                              mr={1}
                              level="body-xs"
                            >
                              Created on {new Date(response.creation_date).toLocaleDateString()}
                            </Typography>
                          </Box>
                          <Typography 
                            level="body-xs"
                            startDecorator={<AlternateEmailRoundedIcon mr={0}/>}
                          >
                            {response.name}
                          </Typography>
                        </ListItemContent>
                        <IconButton sx={{mr: 2, transition: 'all 0.3s ease'}}>
                          <DeleteRoundedIcon/>
                        </IconButton>
                      </ListItem>
                    ))}
                    {(!selectedCommunityInfo?.connection_data || selectedCommunityInfo.connection_data.length === 0) && (
                                  <Typography level="body-lg" textAlign="center">
                                  No connections available
                                </Typography>
                    )}
                  </List>
                </TabPanel>

                <TabPanel value={3}>
                  <TestChart sx={{height: 10}} data={data} displayData={displayData} />
                </TabPanel>

                <TabPanel value={4}>
                  <PostsTabContent />
                </TabPanel>
              </Tabs>
              </>
              :
                    <Typography level="body-lg" textAlign="center" sx={{p: 5}}>
                      Please, select a community from your list
                    </Typography>
              }
            </Card>

            <Card sx={{
              p: 2,
              width: { xs: '97%', md: '250px' },
              maxHeight: { xs: '300px', md: 'auto' },
              overflowY: 'auto'
            }}>
              <Box sx={{ 
                position: 'sticky', 
                top: 0, 
                bgcolor: 'background.surface', 
                zIndex: 2,
                p: 1
              }}>
                <Typography level="title-lg" mb={1}>
                  Your Communities
                </Typography>
                <Input
                  size="sm"
                  placeholder="Search communities..."
                  
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  startDecorator={<SearchIcon />}
                  sx={inputStyles}
                />
              </Box>
              { filteredCommunities ? 
              <List>
                {filteredCommunities.map((community) => (
                  <ListItem key={community.id}>
                    <ListItemButton
                      sx={{ 
                        my: 0.1, 
                        borderRadius: 'md', 
                        transition: 'background 0.3s ease',
                        '&:hover': {
                          bgcolor: 'background.level1'
                        },
                        ...(selectedCommunity?.id === community.id && {
                          bgcolor: 'background.level2'
                        })
                      }}
                      onClick={() => handleCommunitySelect(community)}
                    >
                      <ListItemDecorator>
                        {community.icon ? 
                          <Avatar src={`http://localhost:8000${community.icon}`}/> : 
                          <Avatar>{community?.name?.[0]}</Avatar>
                        }
                      </ListItemDecorator>
                      <ListItemContent sx={{ mx: 1 }}>
                        <Typography level='title-md'>
                          {community?.name}
                        </Typography>
                        <Typography level='body-xs'>
                          {community?.short_description}
                        </Typography>
                      </ListItemContent>
                    </ListItemButton>
                  </ListItem>
                ))}
              </List> : 
              <>
                <Typography>0_o</Typography>
                <Typography>There is quite empty</Typography>
              </>
              }
            </Card>
          </Stack>
        </>
      )}
    </>
  );
}


/**
* React component (Page) for controlling the account in dashboard.
* @returns {JSX.Element} - The rendered component.
*/

export function DashboardControlAccount() {
  const [activeTab, setActiveTab] = React.useState(0);
  const api = useApi();
  const [accountInfo, setAccountInfo] = useState(null);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    let isMounted = true;
    const fetchData = async () => {
      if (isMounted && !accountInfo) {
        try {
          const info = await api.getAccountInfo();
          if (isMounted) {
            setAccountInfo(info);
            console.log(info);
          }
        } catch (error) {
          console.error('Failed to fetch account info:', error);
        } finally {
          if (isMounted) {
            setLoading(false);
          }
        }
      }
    }
    fetchData();
    return () => {
      isMounted = false;
    };
  }, [api, accountInfo]);

  // Styles for inputs
  const inputStyles = {
    width: '100%',
    '--Input-focusedThickness': '1px',
    bgcolor: 'background.level0',
    borderRadius: 'lg',
    '&:hover': {
      borderColor: 'background.level2',
    },
    '&:focus-within': {
      borderColor: 'background.level2',
    },
    '&:focus': {
      outline: 'none',
    },
    mb: 2,
    py: 1,
    px: 2,
    fontSize: 'sm',
    fontWeight: 'md',
    transition: 'box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out, background-color 0.2s ease-in-out',
    '&::placeholder': {
      color: 'neutral.500',
      fontStyle: 'italic',
    },
    '&:disabled': {
      bgcolor: 'neutral.100',
      color: 'neutral.400',
      cursor: 'not-allowed',
    },
  };

  if (loading) {
    return <CircularProgress />;
  }

  // Get avatar URL or fallback to default
  const getAvatarUrl = () => {
    if (!accountInfo?.image) return null;
    return `${import.meta.env.REACT_APP_API_URL || 'http://localhost:8000'}${accountInfo.image}`;
  };

  // Get display name with fallbacks
  const getDisplayName = () => {
    return accountInfo?.display_name || accountInfo?.username || 'Anonymous User';
  };

  return (
    <Box sx={{ py: 2, px: { xs: 2, md: 4 } }}>
      <Card
        sx={{
          p: 4,
          mb: 3,
          display: 'flex',
          flexDirection: { xs: 'column', md: 'row' },
          alignItems: { xs: 'center', md: 'flex-start' },
          gap: 3,
        }}
      >
        <Avatar
          src={getAvatarUrl()}
          size="xs"
          sx={{ width: 120, height: 120 }}
        />
        <Box sx={{ flex: 1 }}>
          <Box sx={{ 
            display: 'flex', 
            justifyContent: {md: 'space-between', xs: 'center'},
            alignItems: 'flex-start',
            textAlign: {xs: 'center', md: 'left'},
            mb: 2,
          }}>
            <Box>
              <Typography level="h3">{getDisplayName()}</Typography>
              <Typography level="body-sm" color="neutral">
                {accountInfo?.status || 'No status set'}
              </Typography>
            </Box>
          </Box>
        </Box>
      </Card>

      <Tabs
        value={activeTab}
        onChange={(event, value) => setActiveTab(value)}
        sx={{
          borderRadius: 'md',
          [`& .${tabClasses.root}`]: {
            zIndex: 1,
            transition: 'transform 0.2s ease, background-color 0.2s ease',
            mx: 0.5,
            paddingLeft: 1,
            paddingRight: 1,
            borderTopLeftRadius: '5px',
            borderTopRightRadius: '5px',
            '&:hover': {
              transform: 'scale(1.05)',
            },
            '&[aria-selected="true"]': {
              bgcolor: 'primary.softBgColor',
              color: 'primary.softColor',
              transition: 'all 0.5 ease'
            },
          },
        }}
      >
        <TabList
          sx={{
            pt: 2,
            justifyContent: 'center',
            [`& .${tabClasses.root}`]: {
              fontWeight: 'lg',
              flex: 1,
              maxWidth: 200,
              p: 2,
              [`&.${tabClasses.selected}`]: {
                bgcolor: 'primary.softBg',
                color: 'primary.solidBg',
              },
            },
          }}
        >
          <Tab>
            <PersonIcon/>
            Profile
          </Tab>
          <Tab>
            <SecurityIcon/>
            Security
          </Tab>
          <Tab>
            <NotificationsRoundedIcon/>
            Notifications
          </Tab>
        </TabList>
        <Divider />
        <TabPanel value={0}>
          <Box sx={{ p: 3 }}>
            <Typography level="title-lg" sx={{ mb: 3 }}>
              Profile Information
            </Typography>
            <Grid container spacing={3}>
              <Grid xs={12} md={6}>
                <FormControl>
                  <FormLabel>Username</FormLabel>
                  <Input 
                    sx={inputStyles} 
                    startDecorator={<PersonIcon/>}
                    placeholder="Enter your username"
                    defaultValue={accountInfo?.username}
                  />
                </FormControl>
              </Grid>
              <Grid xs={12} md={6}>
                <FormControl>
                  <FormLabel>Display Name</FormLabel>
                  <Input 
                    sx={inputStyles} 
                    startDecorator={<PersonIcon/>}
                    placeholder="Enter your display name"
                    defaultValue={accountInfo?.display_name}
                  />
                </FormControl>
              </Grid>
              <Grid xs={12} md={6}>
                <FormControl>
                  <FormLabel>Email</FormLabel>
                  <Input
                    startDecorator={<MailRoundedIcon/>}
                    placeholder="Enter your email"
                    sx={inputStyles}
                    defaultValue={accountInfo?.email}
                  />
                </FormControl>
              </Grid>
              <Grid xs={12}>
                <FormControl>
                  <FormLabel>Status</FormLabel>
                  <Textarea 
                    sx={inputStyles} 
                    placeholder="Set your status"
                    defaultValue={accountInfo?.status}
                  />
                </FormControl>
              </Grid>
            </Grid>
            <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
              <Button size="lg">Save Changes</Button>
              <Button
                size="lg"
                variant="outlined"
                color="neutral"
              >
                Cancel
              </Button>
            </Box>
          </Box>
        </TabPanel>
        <TabPanel value={1}>
          <Box sx={{ p: 3 }}>
            <Typography level="title-lg" sx={{ mb: 3 }}>
              Security information
            </Typography>
            <Button sx={{mr: 1}} variant='soft' size="lg">Change Email</Button>
            <Button m={1} variant='soft' size="lg">Change Password</Button>
          </Box>
        </TabPanel>
        <TabPanel value={2}>    
          <NotificationCenter/>
        </TabPanel>
      </Tabs>
    </Box>
  );
}
