// React related components
import * as React from 'react';
import { Outlet, Link } from 'react-router-dom';
import useMediaQuery from '@mui/material/useMediaQuery';


// MUI Joy UI controls
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
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import ListItemContent from '@mui/joy/ListItemContent';
import ListItemButton from '@mui/joy/ListItemButton';
import Breadcrumbs from '@mui/joy/Breadcrumbs';


// Our own controls
import TestChart from '../components/GrowthChart';


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
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';


export function DashboardLayout(){
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

  const isMobile = useMediaQuery('@media (max-width:1000px)'); // Use MUI's useMediaQuery

  return(
    <>
    <Box sx={{ display: 'flex', height: '100vh',

      '@media (max-width:1000px)': {
        height: '100%'
      }
     }}>
    {(!isMobile) && (
      <Box sx={{
        backgroundColor: 'background.surface', 
        float: 'left', border: '1px solid', 
        borderColor: 'background.level2', borderTop: '0px',
        display: 'flex',
        flexDirection: 'column',
        fontFamily: 'Inter',
        width: '300px',
        minWidth: '22%',
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
    )}

    <Box sx={{p: 3,
      width: '70%',
      '@media (max-width:1000px)': {
        width: '100%'
      }
    }}>
      <Outlet/>
    </Box>
    </Box>
    </>
  )
}



// Define the DashboardHomepage component
export function DashboardHomepage() {
  
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
        <Breadcrumbs size='sm' 
          separator={<KeyboardArrowRightIcon/>} >
          <Link>
            Dashboard
          </Link>
          <Link>
            Home
          </Link>
        </Breadcrumbs>
        <Typography level='h2' my={2} px={1}>
            Home
        </Typography>
      <Card sx={{ height: '60vh', mt: 1, width: 'min-content'
       }}>
        <TestChart icons={icons} data={data} displayData={displayData}/>
      </Card>  
    </>
  );
}




export function DashboardBuildCommunity() {
  return <>
        <Breadcrumbs 
          size="sm"
          separator={ <KeyboardArrowRightIcon/>}>
          <Typography sx={{mt: 0}}>Dashboard</Typography>
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
                        },
                        display: 'flex',
                        flexDirection: 'column', 
                        alignItems: 'center', 
                    }}
                    startDecorator={<AutoAwesomeIcon sx={{ marginBottom: 1, fontSize: '50px'}}/>}
                    >
                  
                        I want to import my community
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
                        },
                        display: 'flex',
                        flexDirection: 'column', 
                        alignItems: 'center', 
                    }} 
                    
                    startDecorator={<AddCircleIcon sx={{ marginBottom: 1, fontSize: '50px'}}/>}
                    >
                  
                        I want to create my community
        </Button>
    </Card>
    </Box>
  </>
}


export function DashboardControlCommunity() {
  const [tabIndex, setTabIndex] = React.useState(0);

  // Sample data for communities
  const communities = [
    { id: 1, name: "Community Alpha", avatar: "A" },
    { id: 2, name: "Community Beta", avatar: "B" },
    { id: 3, name: "Community Gamma", avatar: "C" },
    { id: 4, name: "Community Delta", avatar: "D" },
  ];

  return (
    <>
          {/* Center Content */}
    <Breadcrumbs 
          size="sm"
          separator={ <KeyboardArrowRightIcon/>}>
          <Typography sx={{mt: 0}}>Dashboard</Typography>
          <Typography sx={{mt: 0, color: 'primary.plainColor'}}>Manage Communities</Typography>
      </Breadcrumbs>
    
      <Typography level='h2' my={2} px={1}>
            Manage communities
        </Typography>
      <Stack  direction={{ xs: 'column-reverse', md: 'row' }}  spacing={1} >
        <Card sx={{ 
          width: {xs: '95%', md: '70%'}, p: 3,
          minWidth: '70%', 
          
          }}>
          <Box sx={{
            display: 'flex', 
            flexDirection: 'column', my: 1,
            overflow: 'auto' 
          }}> 
            
            <Avatar src="https://images.unsplash.com/photo-1507833423370-a126b89d394b?auto=format&fit=crop&w=90" />
            <Typography level="title-lg"
                sx={{marginBottom: 0}}>
                  Community
            </Typography>
            <Box sx={{display: 'flex', flexDirection: 'row'}}>
              <Typography startDecorator={<PersonIcon/>} mr={1} level="body-xs">
                 100 Members
              </Typography>
              <Typography 
                  startDecorator={<CalendarMonthRoundedIcon/>}
                  level="body-xs">
                    Created on 9th September, 1999
              </Typography>
            </Box>
            
            <Typography color='neutral' level="body-xs">
              Total growth: <Typography 
                                color="success" 
                                level="body-xs" 
                                startDecorator={<TrendingUpRoundedIcon/>}> 
                                50% from last day 
                </Typography>
            </Typography>
        </Box>

        {/* Tab System */}
        <Tabs value={tabIndex}
              onChange={(event, value) => setTabIndex(value)}
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
              }}>
          <TabList>
            <Tab>General</Tab>
            <Tab>Settings</Tab>
            <Tab>Platforms</Tab>
            <Tab>Stats</Tab>
            <Tab>Posts</Tab>
          </TabList>
          <TabPanel value={0}>
            <Typography level='body-xs'>
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Obcaecati delectus perferendis modi eaque consequuntur accusamus. Maiores architecto sequi natus eaque consectetur neque veritatis ipsa cum hic soluta. Id, temporibus vel? Quisquam, quisquam!
            </Typography>
          </TabPanel>
          <TabPanel value={1}>
            <Typography>Manage members of the community here.</Typography>
          </TabPanel>
          <TabPanel value={2}>
            <Typography>Community settings and configurations.</Typography>
          </TabPanel>
        </Tabs>
      </Card>

      {/* Community List on the Right */}
      <Card sx={{
        p: 2,
        width: { xs: '97%', md: '250px' },
        maxHeight: { xs: '300px', md: 'auto' },
        overflowY: 'auto'
      }}>
        <Box sx={{ position: 'sticky', 
                    top: 0, 
                    bgcolor: 'background.surface', 
                    zIndex: 2,
                    p: 1
        }}>
          <Typography level="title-lg" mb={1}>
            Your Communities
          </Typography>       
        </Box>
        <List>
          {communities.map((community) => (
            <ListItem key={community.id}>
              <ListItemButton sx={{my: 0.1, borderRadius: 'md', 
                transition: 'background 0.3s ease'
              }}>
                <ListItemDecorator>
                  <Avatar>{community.avatar}</Avatar>
                </ListItemDecorator>
                <ListItemContent sx={{mx: 1}}>
                  <Typography level='title-md'>
                    {community.name}
                  </Typography>
                  <Typography level='body-xs'>
                    {community.name}
                  </Typography>
                </ListItemContent>
                </ListItemButton>
            </ListItem>
            
          ))}
        </List>
      </Card>
    </Stack>
    </>
  );
}