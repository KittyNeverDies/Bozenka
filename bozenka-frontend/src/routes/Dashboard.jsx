// React related components
import * as React from 'react';


import {FormControl, FormLabel, FormHelperText, List, ListItem} from '@mui/joy';
import Card from '@mui/joy/Card';
import Input from '@mui/joy/Input';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import Stack from '@mui/joy/Stack';
import Avatar from '@mui/joy/Avatar';
import Grid from '@mui/joy/Grid';
import Button from '@mui/joy/Button';
import Link from '@mui/joy/Link';
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


// Define a reusable HomePageButton component
function HomePageButton({ head, description, icon }) {
  return (
    <Card sx={{
      width: 200,
      transition: 'transform 0.3s, box-shadow 0.3s, background-color 0.3s',
      '&:hover': { 
          transform: 'scale(1.05)', 
          boxShadow: 'md',
          
      }
    }}>
      <Avatar color="primary">{icon}</Avatar>
      <Typography level="title-lg" sx={{ marginBottom: 0 }} element="h1">
        {head}
      </Typography>
      <Typography level="body-xs" sx={{ marginTop: -1.2 }}>
        {description}
      </Typography>
    </Card>
  );
}

// Define the DashboardHomepage component
export function DashboardHomepage() {
  // Define the buttons data
  const buttons = {
    'Communities': [
        {
          head: 'Manage communities', 
          description: 'Manage your communities, add administrators, create posts, etc.', 
          icon: <HandymanRoundedIcon />
        },
        {
          head: 'Community building',
          description: 'Create or import your own social home or club by interests.',
          icon: <AddRoundedIcon />
        },
      ],
      "Account": [
        {
          head: 'Manage account', 
          description: 'Manage your security, privacy of your account. Change avatar or name.', 
          icon: <SettingsRoundedIcon />
        },
      ]
  };
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
              ))}

              </>
          ))}
        </Box>
    </Box>

    <Stack m={2} sx={{ display: 'flex', width: 'auto'}}>
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
    </Stack>
    </Box>
  );
}




export function DashboardAddCommunity() {
  const [selectedTab, setSelectedTab] = React.useState(0);
  const tabListRef = React.useRef(null);

  const inputStyles = {
    width: 'fit-content',
    '--Input-focusedThickness': '1px',
    bgcolor: 'background.surface',
    borderRadius: 'lg',
    '&:hover': {
      bgcolor: 'background.level1',
      borderColor: 'primary.300',
    },
    '&:focus-within': {
      borderColor: 'background.level2',
      bgcolor: 'background.level1',
    },
    '&:focus': {
      outline: 'none',
    },
    mt: 1,
    mb: 1,
    py: 1.5,
    px: 2,
    fontSize: 'sm',
    fontWeight: 'md',
    border: '1px solid',
    borderColor: 'neutral.300',
    transition: 'box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out, background-color 0.2s ease-in-out',
    '&::placeholder': {
      color: 'neutral.500',
      fontStyle: 'italic',
    },
    '&:disabled': {
      bgcolor: 'neutral.100',
      color: 'neutral.400',
      cursor: 'not-allowed',
    }};
  
  const handleTabChange = (event, newValue) => {
    setSelectedTab(newValue);
  };

  React.useEffect(() => {
    const updateTabIndicator = () => {
      if (tabListRef.current) {
        const tabs = tabListRef.current.querySelectorAll(`.${tabClasses.root}`);
        const activeTab = tabs[selectedTab];
        if (activeTab) {
          const tabListRect = tabListRef.current.getBoundingClientRect();
          const activeTabRect = activeTab.getBoundingClientRect();
          
          const offsetLeft = activeTabRect.left - tabListRect.left;
          const offsetTop = activeTabRect.top - tabListRect.top;

          tabListRef.current.style.setProperty('--tab-left', `${offsetLeft}px`);
          tabListRef.current.style.setProperty('--tab-top', `${offsetTop}px`);
          tabListRef.current.style.setProperty('--tab-width', `${activeTabRect.width}px`);
          tabListRef.current.style.setProperty('--tab-height', `${activeTabRect.height}px`);
        }
      }
    };

    updateTabIndicator();
    window.addEventListener('resize', updateTabIndicator);
    return () => window.removeEventListener('resize', updateTabIndicator);
  }, [selectedTab]);

  return (
    <Stack m={2} sx={{ display: 'flex', width: 'auto' }}>
      <Card sx={{ width: 'auto' }}>
        <Typography level="h3" mt={1} element="h1">
          Add your community
        </Typography>
        <Divider sx={{ my: 2 }} />
        
    <Tabs 
      aria-label="tabs" 
      value={selectedTab} 
      onChange={handleTabChange}
      
      sx={{
        bgcolor: 'transparent',
        width: '100%', // Set width to 100% to make it responsive
        marginLeft: 2,
        '@media (max-width: 670px)': { // Mobile responsiveness
          width: '100%',
          marginLeft: 0,
        }
      }}
    >
      <TabList
        ref={tabListRef}
        disableUnderline
     
        sx={{
          marginTop: 1,
          p: 0.5,
          gap: 0.5,
          borderRadius: 'sm',
          bgcolor: 'background.surface',
          position: 'relative',
          border: '1px solid',
          borderColor: 'Transparent',
          flexWrap: 'wrap',
          justifyContent: 'center',
          my: 0,
          alignSelf: 'center',
          width: 'auto',
          '&::before': {
            content: '""',
            position: 'absolute',
            left: 'var(--tab-left, 4px)',
            top: 'var(--tab-top, 4px)',
            width: 'var(--tab-width, 0)',
            height: 'var(--tab-height, 100%)',
            bgcolor: 'primary.softBg',
            borderRadius: 'lg',
            transition: 'all 0.3s ease',
          },
          [`& .${tabClasses.root}`]: {
            zIndex: 1,
            transition: 'transform 0.2s ease, background-color 0.2s ease',
            m: 0.5,
            my: 0.2,
            borderRadius: 'lg',
            paddingLeft: 1,
            paddingRight: 1,
            '&:hover': {
              transform: 'scale(1.05)',
              bgcolor: 'primary.lightBg',
              borderRadius: 'lg',
            },
            '&[aria-selected="true"]': {
              bgcolor: 'transparent',
              color: 'primary.plainColor',
              borderRadius: 'lg'
            },
          },
        }}
      >
        <Tab></Tab>
      </TabList>
      <TabPanel value={0}>
        <FormControl>
          <FormLabel>
            Name of your community
          </FormLabel>
          <Input my={0} sx={inputStyles}  />
          <FormHelperText>
              This name will be displayed on the community page.
          </FormHelperText>
        </FormControl>
        <FormControl sx={{my: 1}}>
          <FormLabel>
            Description
          </FormLabel>
          <Input my={0} sx={inputStyles}  />
          <FormHelperText>
              This description will be displayed on the community page.
          </FormHelperText>
        </FormControl>
      </TabPanel>
      </Tabs>
      </Card>
    </Stack>
  );
}

export function DashboardEditCommunity() {
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