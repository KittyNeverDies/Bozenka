// React related components
import * as React from 'react';
import { Outlet, Link } from 'react-router-dom';
import useMediaQuery from '@mui/material/useMediaQuery';


// MUI Joy UI controls
import {FormControl, FormLabel, FormHelperText, List, ListItem, ListSubheader} from '@mui/joy';
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
import Chip from '@mui/joy/Chip';
import ListItemContent from '@mui/joy/ListItemContent';
import AspectRatio from '@mui/joy/AspectRatio';
import IconButton from '@mui/joy/IconButton';
import Sheet from '@mui/joy/Sheet';
import ListItemButton from '@mui/joy/ListItemButton';
import Breadcrumbs from '@mui/joy/Breadcrumbs';
import { useColorScheme} from '@mui/joy/styles';
import Checkbox from '@mui/joy/Checkbox';




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
import DarkModeRoundedIcon from '@mui/icons-material/DarkModeRounded';
import LightModeRoundedIcon from '@mui/icons-material/LightModeRounded';
import NotificationsRoundedIcon from '@mui/icons-material/NotificationsRounded';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';
import LinkIcon from '@mui/icons-material/Link';



function ColorModeToggle() {
  const { mode, setMode } = useColorScheme();
  return (
    <IconButton
      variant="soft"
      onClick={() => setMode(mode === 'dark' ? 'light' : 'dark')}
      sx={{
        minWidth: 40,
        minHeight: 40,
        borderRadius: '50%',
      }}
    >
      {mode === 'dark' ? <LightModeRoundedIcon /> : <DarkModeRoundedIcon />}
    </IconButton>
  );
}


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
              <Avatar
                src="https://images.unsplash.com/photo-1507833423370-a126b89d394b?auto=format&fit=crop&w=90"
                size="lg"
              />
              <Box>
                <Typography level="h5" element="h5" fontWeight='bold'>
                  Welcome, user.
                </Typography>
                <Typography color='neutral' level="body-xs">
            Total growth: <Typography color="success" level="body-xs" startDecorator={<TrendingUpRoundedIcon/>}> 50% from last day </Typography>
          </Typography>     
                <Typography level="body-xs">
                  Have a nice day!
                </Typography>
              </Box>
        </Box>
        <Box sx={{px: 0.8}}>
        <List
              size="sm"
              sx={{
                '--ListItem-radius': '8px',
                '--ListItemDecorator-size': '32px',
              }}
            >
          <Link to="">
          <ListItem  sx={{
                                my: 0.4,
                              }} >
                <ListItemButton sx={{transition: '0.2s ease background-color'}}>
                  <ListItemDecorator> 
                    <HomeRoundedIcon /> 
                  </ListItemDecorator>
                  <ListItemContent>
                      <Typography level='title-xs'>
                          Home
                      </Typography>
                      <Typography level='body-xs'>
                          Overivew of your Dashboard.
                     </Typography>
                   </ListItemContent>
                  </ListItemButton>
            </ ListItem>

            </Link>
          {Object.keys(buttons).map((button) => (
            <ListItem nested>
              <ListSubheader>
                  {button}
              </ListSubheader>
              <List>
              {buttons[button].map( (btn) => (
                            <Link to={btn.destination}>
                              <ListItem sx={{
                                my: 0.4,
                              }} variant='plain'>
                                <ListItemButton sx={{transition: '0.2s ease background-color'}}>
                                  <ListItemDecorator>
                                    {btn.icon}
                                  </ListItemDecorator>
                                  <ListItemContent>
                                    <Typography level='title-xs'>
                                    {btn.head}
                                    </Typography>
                                    <Typography level='body-xs'>
                                    {btn.description}
                                    </Typography>
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
    </Sheet>
    )}

    <Box sx={{p: 3,
                flexGrow: 1,
                bgcolor: 'background.level1',
    
      width: '70%',
      height: '100vh',
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
      <Card sx={{ p: 2 }}>
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
          <AspectRatio ratio="2">
            <TestChart data={data} displayData={displayData} />
          </AspectRatio>
        )}
      </Card>
      </Box>
      {/* Recent Activity Section */}
      <Card sx={{mx: 3, width: 300}}>
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
              <ListItemButton>
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
        <Box sx={{display: 'flex', flexDirection: 'row'}}>
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
        </Box>
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
    
        <Box my={2} px={1}>
          <Typography level="h2">Manage Communities</Typography>
          <Typography level="body-md" color="neutral">
            Oversee and optimize your community spaces
          </Typography>
        </Box>
      <Stack  direction={{ xs: 'column-reverse', md: 'row' }}  spacing={1} >
        <Card sx={{ 
          width: {xs: '95%', md: '70%'}, p: 3,
          minWidth: '70%', 
                  maxHeight: { xs: 'auto', md: '600px' },
          
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

            <Box>
            <Chip variant="outlined" 
                            startDecorator={<CalendarMonthRoundedIcon/>} 
                            sx={{borderRadius: 'sm', m: 0.5}}>
                            Tag 1
                        </Chip>
                        <Chip variant="outlined" 
                            startDecorator={<CalendarMonthRoundedIcon/>} 
                            sx={{borderRadius: 'sm', m: 0.5}}>
                            Tag 1
                        </Chip>
            </Box>
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
          <TabPanel value={0} sx={{maxHeight: '200px', overflowY: 'auto'}}>
            <Typography level='body-xs'>
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Obcaecati delectus perferendis modi eaque consequuntur accusamus. Maiores architecto sequi natus eaque consectetur neque veritatis ipsa cum hic soluta. Id, temporibus vel? Quisquam, quisquam!
            </Typography>
                          {/* Quick Stats */}
                          <Grid container spacing={2} sx={{ my: 2 }}>
                {[
                  {
                    label: 'Members',
                    value: 100,
                    icon: <PeopleRoundedIcon />,
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
                ].map((stat) => (
                  <Grid xs={12} md={3} >
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
        
          </TabPanel>
          <TabPanel value={1}>
            <FormControl sx={{my: 1}}>
              <Checkbox label="Function 1" size='sm' />
              <FormHelperText>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quis sint enim nihil soluta sapiente voluptas iure. Vero cumque voluptas hic, ipsum, cupiditate sint enim architecto, velit voluptate est aut voluptates?</FormHelperText>
            </FormControl>
            <FormControl sx={{my: 1}}>
              <Checkbox label="Function 1" size='sm' />
              <FormHelperText>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quis sint enim nihil soluta sapiente voluptas iure. Vero cumque voluptas hic, ipsum, cupiditate sint enim architecto, velit voluptate est aut voluptates?</FormHelperText>
            </FormControl>
            <FormControl sx={{my: 1}}>
              <Checkbox label="Function 1" size='sm' />
              <FormHelperText>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quis sint enim nihil soluta sapiente voluptas iure. Vero cumque voluptas hic, ipsum, cupiditate sint enim architecto, velit voluptate est aut voluptates?</FormHelperText>
            </FormControl>
            
          </TabPanel>
          <TabPanel value={2}>
            <Typography>


            </Typography>
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


export function DashboardControlAccount() {
  const [activeTab, setActiveTab] = React.useState(0);

  const userProfile = {
    name: "John Doe",
    email: "john@example.com",
    avatar: "https://images.unsplash.com/photo-1507833423370-a126b89d394b?auto=format&fit=crop&w=90",
    role: "Community Manager",
    joinDate: "September 2023",
    bio: "Passionate about building and growing online communities",
    socialLinks: {
      telegram: "@johndoe",
      vk: '@johndoe',
    }
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
          src={userProfile.avatar}
          size="xs"
          sx={{ width: 120, height: 120 }}
        />
        <Box sx={{ flex: 1 }}>
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            mb: 2,
          }}>
            <Box>
              <Typography level="h3">{userProfile.name}</Typography>
              <Typography level="body-sm" color="neutral">
                {userProfile.role}
              </Typography>
            </Box>
            <Button
              variant="outlined"
              color="neutral"
              startDecorator={<SettingsRoundedIcon />}
            >
              Edit Profile
            </Button>
          </Box>
          <Typography level="body-md" sx={{ mb: 2 }}>
            {userProfile.bio}
          </Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            {Object.entries(userProfile.socialLinks).map(([platform, link]) => (
              <Chip
                size="sm"
                variant="soft"
                color="primary"
                startDecorator={<LinkIcon />}
              >
                {platform}
              </Chip>
            ))}
          </Box>
        </Box>
      </Card>

      <Tabs
        value={activeTab}
        onChange={(event, value) => setActiveTab(value)}
        sx={{
          bgcolor: 'background.surface',
          borderRadius: 'md',
          boxShadow: 'sm',
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
          <Tab>Profile</Tab>
          <Tab>Security</Tab>
          <Tab>Notifications</Tab>
          <Tab>Billing</Tab>
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
                  <FormLabel>Full Name</FormLabel>
                  <Input defaultValue={userProfile.name} />
                </FormControl>
              </Grid>
              <Grid xs={12} md={6}>
                <FormControl>
                  <FormLabel>Email</FormLabel>
                  <Input defaultValue={userProfile.email} />
                </FormControl>
              </Grid>
              <Grid xs={12}>
                <FormControl>
                  <FormLabel>Bio</FormLabel>
                  <Input
                    multiline
                    minRows={3}
                    defaultValue={userProfile.bio}
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
      </Tabs>
    </Box>
  );
}