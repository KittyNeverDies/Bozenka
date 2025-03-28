// React stuff
import * as React from 'react';
import {useEffect, useState} from "react";
import {Link} from 'react-router-dom';

import useMediaQuery from '@mui/material/useMediaQuery';
import { useLocation } from 'react-router-dom';


// Joy UI components
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import Tooltip from '@mui/joy/Tooltip';
import IconButton from '@mui/joy/IconButton';
import Drawer from '@mui/joy/Drawer';
import Sheet from '@mui/joy/Sheet';
import ListItem from '@mui/joy/ListItem';
import Chip from '@mui/joy/Chip';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemContent from "@mui/joy/ListItemContent"
import ListSubheader from '@mui/joy/ListSubheader';
import Avatar from '@mui/joy/Avatar';
import ListItemDecorator from "@mui/joy/ListItemDecorator";
import List from '@mui/joy/List';

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
import {useApi} from "../api/hooks/useApi.js";
import {useAuth} from "../api/contexts/AuthContext.jsx";
import CircularProgress from "@mui/joy/CircularProgress";


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

    const [loading, setLoading] = useState(true);

    const {isAuthenticated, logout} = useAuth();

    // Everything is need for getting account info;
    const api = useApi();
    const [accountInfo, setAccountInfo] = useState(null);


    // Get current route path
    const currentPath = location.pathname;

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

    {/* Joy header content. */}
    <Box
      sx={{
        display: 'flex',
        height: '100%',
        justifyContent: 'space-between',
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
          {(((!isDashboard && !isMobile) || isMobile) && isAuthenticated) && (
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

          {!isAuthenticated && (<Tooltip title="Login" color='primary' variant="soft" size="md" sx={{
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
        </Tooltip>)}


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
            {loading ? (
                <CircularProgress size="sm" />
            ) : (
                <>
                    {accountInfo.icon ? <Avatar src={`${import.meta.env.REACT_APP_API_URL || 'http://localhost:8000'}${accountInfo.icon}`}/> : <Avatar>{accountInfo?.display_name?.[0] || accountInfo?.username?.[0] || 'user'}</Avatar>}
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
            >            <Link to="/dashboard/" style={{ textDecoration: 'none' }}>
                <ListItem>
                    <ListItemButton
                        selected={currentPath === '/dashboard/'}
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
          variant="soft"
          onClick={() => logout()}
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
