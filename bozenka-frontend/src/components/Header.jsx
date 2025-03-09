// React stuff
import * as React from 'react';
import {Link} from 'react-router-dom';

import useMediaQuery from '@mui/material/useMediaQuery';
import { useLocation } from 'react-router-dom';


// Joy UI components
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import Tooltip from '@mui/joy/Tooltip';
import IconButton from '@mui/joy/IconButton';
import Drawer from '@mui/joy/Drawer';
import Stack from '@mui/joy/Stack';
import Button from '@mui/joy/Button';
import Sheet from '@mui/joy/Sheet';
import Divider from '@mui/joy/Divider';
import ListItem from '@mui/joy/ListItem';
import Chip from '@mui/joy/Chip';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemContent from "@mui/joy/ListItemContent"
import ListSubheader from '@mui/joy/ListSubheader';
import Avatar from '@mui/joy/Avatar';
import ListItemDecorator from "@mui/joy/ListItemDecorator";
import List from '@mui/joy/List';
import { Radio, RadioGroup } from '@mui/joy';

// Material UI icons
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";
import SettingsSuggestIcon from '@mui/icons-material/SettingsSuggest';
import GroupRoundedIcon from '@mui/icons-material/GroupRounded';
import LogoutIcon from '@mui/icons-material/Logout';
import InputRoundedIcon from '@mui/icons-material/InputRounded';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import MenuIcon from '@mui/icons-material/Menu';
import LoginIcon from '@mui/icons-material/Login';
import HandymanRoundedIcon from '@mui/icons-material/HandymanRounded';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import SettingsRoundedIcon from'@mui/icons-material/SettingsRounded';
import TrendingUpRoundedIcon from '@mui/icons-material/TrendingUpRounded';
import NotificationsRoundedIcon from '@mui/icons-material/NotificationsRounded';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';


// Our elements
import ColorModeToggle from './ColorModeToggle';

/**
 * @description A functional component that renders header for all pages.
 * @returns {JSX.Element}
 */
export default function JoyHeader() {
  /**
  * @description Header for all pages in Joy UI Style.
  * @type {JSX.Element}
  */

  const [openDrawer, setOpenDrawer] = React.useState(false);
  const location = useLocation(); // Import useLocation from react-router-dom
  const isDashboard = location.pathname.includes('/dashboard');
  const isMobile = useMediaQuery('@media (max-width:1000px)'); // Use MUI's useMediaQuery

  const toggleDrawer = (isOpen) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }
    setOpenDrawer(isOpen);
  };

  
  // Dashboard navigation buttons (moved from Dashboard.jsx)
  const buttons = {
    'Communities': [
      {
        head: 'Manage communities',
        description: 'Manage your communities, add administrators, create posts, etc.',
        destination: '/dashboard/communities',
        icon: <HandymanRoundedIcon />
      },
      {
        head: 'Community building',
        description: 'Create or import your own social home or club by interests.',
        destination: '/dashboard/build',
        icon: <AddRoundedIcon />
      },
    ],
    "Account": [
      {
        head: 'Manage account',
        description: 'Manage your security, privacy of your account. Change avatar or name.',
        destination: '/dashboard/account',
        icon: <SettingsRoundedIcon />
      },
    ]
  };

  return (
    <>
    
    {/* 
        Joy header content.
    */}
    <Box
      sx={{
        display: 'flex',
        height: '100%',
        justifyContent: 'space-between', // Distribute space between logo and icons
        textAlign: "center",
        alignItems: 'center',
        p: 2,
        size: 'ms',
        position: 'sticky',
        top: 0,
        borderBottom: '1px solid',
        backgroundColor: 'background.surface',
        borderColor: 'background.level2',
        zIndex: 1100,
      }}
    >

      
      {/* 
        Bozenka logotype
      */}

      <Link to='/' sx={{'textDecoration': 'None'}}>
        <Typography level="h3" component="h3" size='xs'>
          Bozenka
        </Typography>
      </Link>

      
      {/* 
        Box of login & communities button
      */}
      <Box sx={{ display: 'flex', alignItems: 'center' 
      }}>

      {/* 
          Menu button

                    <Tooltip title="Menu" color='primary' variant="soft" size="md" sx={{
            boxShadow: 'none',
            fontWeight: 'bold'                                                 
          }}>
            <IconButton
            sx={{
              transition: 'transform 0.2s ease, background-color 0.2s ease',
              m: 0.5,
              marginRight: 1.2,
              '&:hover': {
                transform: 'scale(1.05)',
                bgcolor: 'primary.lightBg',
                borderRadius: '',
              },
              '&:active': {
                transform: 'scale(1.20)'
              }
            }}  
            onClick={toggleLoginDrawer(true)} variant="plain">
              <MenuIcon />
            </IconButton>
          </Tooltip>
        */}

        {
          /* 
            Menu button
          */
        }
        {(!isDashboard && !isMobile || isMobile) && (
          <Tooltip title="Menu" color='primary' variant="soft" size="md" sx={{
            boxShadow: 'none',
            fontWeight: 'bold'
          }}>
            <IconButton onClick={toggleDrawer(true)} 
                sx={{
                  transition: 'transform 0.2s ease, background-color 0.2s ease',
                  m: 0.5,
                  marginRight: 1.2,
                  '&:hover': {
                    transform: 'scale(1.05)',
                    bgcolor: 'primary.lightBg',
                    borderRadius: '',
                  },
                  '&:active': {
                    transform: 'scale(1.20)'
                  }
                }} >
              <MenuIcon />
            </IconButton>
          </Tooltip>
       )}
        {/* 
          Login button
        */}
        <Tooltip title="Login" color='primary' variant="soft" size="md" sx={{
            boxShadow: 'none',
            fontWeight: 'bold'
          }}
        >
        <Link to='/login'>
          <IconButton onClick={() => {}}
            sx={{
            transition: 'transform 0.2s ease, background-color 0.2s ease',
            m: 0.5,
            marginRight: 1.2,
            '&:hover': {
              transform: 'scale(1.05)',
              bgcolor: 'primary.lightBg',
              borderRadius: '',
            },
            '&:active': {
              transform: 'scale(1.20)'
            }
            }}
          
          variant="plain">
            <InputRoundedIcon/>
          </IconButton>
          </Link>
        </Tooltip>

        
        {/* 
          Communities button
        */}
        <Tooltip title="Communities" color='primary' variant="soft" size="md" sx={{
            boxShadow: 'none',
            fontWeight: 'bold'
          }}>
          <Link to='/communities'>
          <IconButton onClick={() => {}} 
            sx={{
            transition: 'transform 0.2s ease, background-color 0.2s ease',
            m: 0.5,
            marginRight: 1.2,
            '&:hover': {
              transform: 'scale(1.05)',
              bgcolor: 'primary.lightBg',
              borderRadius: '',
            },
            '&:active': {
              transform: 'scale(1.20)'
            }
            }} variant="plain">
            <GroupRoundedIcon/>
          </IconButton>
          </Link>
        </Tooltip>
      </Box>
    </Box>
    {/* 
       Drawer, that opens on menu button click.
    */}
    
    <Drawer open={openDrawer} onClose={toggleDrawer(false)}>

     
    <Sheet
              role="presentation"
              onClick={toggleDrawer(false)}
              onKeyDown={toggleDrawer(false)}
          sx={{
            p: 2,
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
          <Link to="/dashboard/">
          <ListItem key='home' sx={{
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
                              <ListItem key={btn.head} sx={{
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
    </Drawer>
  </>
  );
}
