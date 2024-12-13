// React related components
import * as React from 'react';
import { Outlet, Link } from 'react-router-dom';


import {FormControl, FormLabel, FormHelperText, List, ListItem} from '@mui/joy';
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
import Stepper from '@mui/joy/Stepper';
import Step from '@mui/joy/Step';
import StepIndicator from '@mui/joy/StepIndicator';
import Breadcrumbs from '@mui/joy/Breadcrumbs';


import TestChart from '../components/GrowthChart';


import SearchIcon from '@mui/icons-material/SearchRounded';
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import HandymanRoundedIcon from '@mui/icons-material/HandymanRounded';
import TrendingUpRoundedIcon from '@mui/icons-material/TrendingUpRounded';
import VisibilityRoundedIcon from '@mui/icons-material/VisibilityRounded';
import PeopleRoundedIcon from '@mui/icons-material/PeopleRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';


export function DashboardLayout(){


  const buttons = {
    'Communities': [
        {
          head: 'Manage communities', 
          description: 'Manage your communities, add administrators, create posts, etc.', 
          destination: 'dashboard/communities',
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
  


  return(
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <Box sx={{
        backgroundColor: 'background.surface', 
        float: 'left', border: '1px solid', 
        borderColor: 'background.level2', borderTop: '0px',
        display: 'flex',
        flexDirection: 'column',
        fontFamily: 'Inter',
        width: '300',
        minWidth: '14%',
        boxSizing: 'border-box',
      }}>
        <Stack sx={{ 
          alignItems: 'left', 
          display: 'flex',  
          justifyContent: 'center', p: 2 
        }}>
          <Avatar
            src="https://images.unsplash.com/photo-1507833423370-a126b89d394b?auto=format&fit=crop&w=90"
            size="lg"
          />
          <Typography level="h5" mt={1} element="h5" fontWeight='bold'>
            Welcome, user.
          </Typography>

          <Typography color='neutral' level="body-xs">
            Total growth: <Typography color="success" level="body-xs" startDecorator={<TrendingUpRoundedIcon/>}> 50% from last day </Typography>
          </Typography>
          
          <Typography level="body-xs">Have a nice day!</Typography>
        </Stack>
      
        <Box sx={{px: 0.8}}>
          <Link to="">
            <Button variant='plain' color='neutral'
                size='sm'
                startDecorator={<HomeRoundedIcon/>}
                sx={{
                  width: '100%',
                  fontSize: 'xs',
                  my: 0.2,
                  justifyContent: 'left',
                  fontWeight: '500',
                  transition: '0.2s ease background-color'
                }}>
              Home
            </Button>
            </Link>
          {Object.keys(buttons).map((button) => (
            <>
              <Typography
              level="body-xs"
              textTransform="uppercase"
              sx={{ 
                letterSpacing: '0.15rem', 
                paddingLeft: 2, 
                paddingBottom: 1, 
                paddingTop: 2}}>
                  {button}
              </Typography>
              {buttons[button].map( (btn) => (
                            <Link to={btn.destination}>
                              <Button variant='plain'
                              color='neutral'
                              size='sm'
                              sx={{
                                width: '100%',
                                fontSize: 'xs',
                                my: 0.2,
                                justifyContent: 'left',
                                
                                fontWeight: '500',
                                transition: '0.3s ease background-color'
                              }}
                              startDecorator={btn.icon}
                            >
                              {btn.head}
                            </Button>
                          </Link>
              ))}
              </>
          ))}
        </Box>
    </Box>

    <Box sx={{p: 2}}>
      <Outlet/>
    </Box>
    </Box>
  )
}



// Define the DashboardHomepage component
export function DashboardHomepage() {
  // Define the buttons data

  const buttonss = [
    {
      head: 'Search community',
      description: 'Find your social home or place for ads. Here is freedom of choice.',
      icon: <SearchIcon />,
    },
    {
      head: 'Community-building',
      description: 'Create or import your own social home or club by interests.',
      icon: <AddRoundedIcon />,
    },
    {
      head: 'Manage community',
      description: 'Manage your communities, add administrators, create posts, etc.',
      icon: <HandymanRoundedIcon />
    },
    {
      head: 'Manage account',
       description: 'Manage your security, privacy of your account. Change avatar or name.',

    }
  ];


  
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
    },
    views: {
      title: "Views of the posts from all communities at this date.",
      shortTitle: "Views of the posts",
      description: "Total growth of number of views on posts at this date.",
      icon: <VisibilityRoundedIcon/>,
    }
  
  }

  const icons = {
    members: <PeopleRoundedIcon />,
    views: <VisibilityRoundedIcon/>,
  };

  return (
     
    <>
      {/* Welcome card */}

        <Breadcrumbs size='sm' >
          <Link>
            Dashboard
          </Link>
          <Link>
            Home
          </Link>
        </Breadcrumbs>
        <Typography level='h2' my={1} px={1}>
            Home
        </Typography>
      <Card sx={{ height: '60vh', mt: 1 }}>
        <TestChart icons={icons} data={data} displayData={displayData}/>
      </Card>  
    </>
  );
}




export function DashboardBuildCommunity() {
  return <>
    <Card>
        <Button variant="plain" size="lg" sx={{
                        p: 1.5,
                        transition: 'transform 0.2s ease, background-color 0.2s ease',
                        border: '1px',
                        '&:hover': {
                            transform: 'scale(1.05)',
                            bgcolor: 'primary.lightBg',
                            borderRadius: '',
                        },
                        '&:active': {
                            transform: 'scale(1.20)'
                        }
                    }} 
                    >
                  
                        I want to edit my community
        </Button>
        <Button variant="plain" size="lg" sx={{
                        p: 1.5,
                        transition: 'transform 0.2s ease, background-color 0.2s ease',
                        border: '1px',
                        '&:hover': {
                            transform: 'scale(1.05)',
                            bgcolor: 'primary.lightBg',
                            borderRadius: '',
                        },
                        '&:active': {
                            transform: 'scale(1.20)'
                        }
                    }} 
                    >
                  
                        I want to create my community
        </Button>
    </Card>
  </>
}

export function DashboardControlCommunity() {
  return (
    <Stack m={2} sx={{}}>
      <Card sx={{ width: 'auto' }}>
        <Typography level="h3" mt={1} element="h1">
          Edit your community
        </Typography>
        <Divider sx={{ my: 2 }} />
        {/* Edit community form here */}
      </Card>
    </Stack>
  );
}