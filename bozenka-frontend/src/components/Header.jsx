// React stuff
import * as React from 'react';
import {Link} from 'react-router-dom';

// Joy UI components
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import Tooltip from '@mui/joy/Tooltip';
import IconButton from '@mui/joy/IconButton';
import Drawer from '@mui/joy/Drawer';
import Divider from '@mui/joy/Divider';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemContent from "@mui/joy/ListItemContent"
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

/**
 * @description A functional component that renders header for all pages.
 * @returns {JSX.Element}
 */
export default function JoyHeader() {
  /**
  * @description Header for all pages in Joy UI Style.
  * @type {JSX.Element}
  */

  const [openLoginDrawer, setOpenLoginDrawer] = React.useState(false);

  const toggleLoginDrawer = (isOpen) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
        return;
    }
    setOpenLoginDrawer(isOpen);
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
    <Drawer open={openLoginDrawer} onClose={toggleLoginDrawer(false)}>
        <Box
            role="presentation"
            onClick={toggleLoginDrawer(false)}
            onKeyDown={toggleLoginDrawer(false)}
        >
            <Typography level="h3"
                
                sx={{ p: 2, borderBottom: '1px solid', borderColor: 'divider' }}
            >Menu</Typography>
      <Typography
        id="ellipsis-list-demo"
        level="body-xs"
        textTransform="uppercase"
      sx={{ 
        letterSpacing: '0.15rem', 
        paddingLeft: 2, 
        paddingBottom: 1, 
        paddingTop: 2}}>
                    Communities
      </Typography>
      <List>
        <ListItem key="Dashboard">
            <ListItemButton>
                <ListItemDecorator>
                    <AutoGraphIcon/>
                </ListItemDecorator>
                <ListItemContent>        
                    <Typography level="title-sm">
                        Dashboard
                    </Typography>
                    <Typography level="body-sm" noWrap>
                        Check out all statistics in one place.
                    </Typography>
                </ListItemContent>
                <KeyboardArrowRight/>
            </ListItemButton>
        </ListItem>
        <ListItem key="Communities">
            <ListItemButton>
                <ListItemDecorator>
                    <SettingsSuggestIcon/>
                </ListItemDecorator>
                <ListItemContent>        
                    <Typography level="title-sm">
                        Manage Communities
                    </Typography>
                    <Typography level="body-sm" noWrap>
                        Set up bozenka to work with your communities 
                    </Typography>
                </ListItemContent>
                <KeyboardArrowRight/>
            </ListItemButton>
        </ListItem>
        <ListItem key="AddCommunity">
            <ListItemButton>
                <ListItemDecorator>
                    <AddCircleIcon/>
                </ListItemDecorator>
                <ListItemContent>        
                    <Typography level="title-sm">
                        Connect Your Community
                    </Typography>
                    <Typography level="body-sm" noWrap>
                        Connect it, to manage it.
                    </Typography>
                </ListItemContent>
                <KeyboardArrowRight/>
            </ListItemButton>
        </ListItem>
      </List>
      <Typography
                id="ellipsis-list-demo"
                level="body-xs"
                textTransform="uppercase"
                sx={{ letterSpacing: '0.15rem', paddingLeft: 2, paddingBottom: 1, paddingTop: 2}}
                >
                    Account
               </Typography>
      <List>
        <ListItem key="LogOut">
            <ListItemButton>
                <ListItemDecorator>
                    <LogoutIcon/>
                </ListItemDecorator>
                <ListItemContent>        
                    <Typography level="title-sm">
                        Logout of Account
                    </Typography>
                    <Typography level="body-sm" noWrap>
                        Get out of bozenka account. Why?
                    </Typography>
                </ListItemContent>
                <KeyboardArrowRight/>
            </ListItemButton>
        </ListItem>
        
      <ListItem key="AccountSettings">
            <ListItemButton>
                <ListItemDecorator>
                    <SettingsSuggestIcon/>
                </ListItemDecorator>
                <ListItemContent>        
                    <Typography level="title-sm">
                        Account Settings
                    </Typography>
                    <Typography level="body-sm" noWrap>
                        Control your account and set account settings.
                    </Typography>
                </ListItemContent>
                <KeyboardArrowRight/>
            </ListItemButton>
        </ListItem>
      </List>
      <Box
          sx={{
            display: 'flex',
            gap: 1,
            p: 1.5,
            pb: 2,
            borderTop: '1px solid',
            borderColor: 'divider',
            position: 'absolute',
            bottom: 0,
            width: '100%'
          }}
        >
          <Avatar size="md" />
          <div>
            <Typography level="title-sm">Username</Typography>
            <Typography level="body-sm">joined 20 Jun 2023</Typography>
          </div>
        </Box>
      
    </Box>
  </Drawer>
  </>
  );
}
