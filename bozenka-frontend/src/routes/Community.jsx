// React related components
import * as React from 'react';

// MUI Joy components
import Avatar from '@mui/joy/Avatar';
import Box from '@mui/joy/Box';
import Card from '@mui/joy/Card';
import Chip from '@mui/joy/Chip';
import Grid from '@mui/joy/Grid';
import List from '@mui/joy/List';
import { Breadcrumbs } from '@mui/joy';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemContent from '@mui/joy/ListItemContent';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import Stack from '@mui/joy/Stack';
import Typography from '@mui/joy/Typography';

// MUI Icons
import CalendarMonthRoundedIcon from '@mui/icons-material/CalendarMonthRounded';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import LocalOfferRoundedIcon from '@mui/icons-material/LocalOfferRounded';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import PersonIcon from '@mui/icons-material/Person';
import MultipleStopRoundedIcon from '@mui/icons-material/MultipleStopRounded';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import GroupRoundedIcon from '@mui/icons-material/GroupRounded';

import TabsSegmentedControls from '../components/TabSegmentedControls';


function Community() {
    return (
        <Box sx={
            {
                m: 2,
                display: 'flex',
                flexDirection: 'row',
                '@media (max-width: 670px)': { // Mobile responsiveness
                  flexDirection: 'column',
                }
            }
        }>
            <Stack sx={
                {
                    flexDirection: 'column',
                    width: 300,
                    '@media (max-width: 670px)': { // Mobile responsiveness
                      width: '100%',
                      position: 'relative',
                      left: 'unset',
                      mr: 0,
                  }
                }
            }>
                <Card sx={{p: 0, mb: 2}}>
                  <Box>
                    <Breadcrumbs 
                        separator={<KeyboardArrowRightIcon/>}
                        sx={{
                          "--Breadcrumbs-gap": "3px"
                        }}
                    >
                      <Typography level="body-md" sx={{mt: 0}}>Home</Typography>
                      <Typography level="body-md" sx={{mt: 0}}>Communities</Typography>
                      <Typography level="body-md" sx={{pt: 0, color: 'primary.plainColor'}}>Community Name</Typography>
                    </Breadcrumbs>
                  </Box>
                </Card>
                <Card>
                    <Avatar src="https://images.unsplash.com/photo-1507833423370-a126b89d394b?auto=format&fit=crop&w=90" />
                    <Box> 
                        <Typography level="title-lg"
                            sx={
                                {
                                    marginBottom: 0
                                }
                            }>Community</Typography>
                        <Typography
                        startDecorator={<PersonIcon/>}
                        level="body-xs">
                            100 Members
                        </Typography>
                        <Typography 
                            startDecorator={<CalendarMonthRoundedIcon/>}
                            level="body-xs">
                            Created on 9th September, 1999
                        </Typography>
                        <Typography level="body-sm">Lorem ipsum dolor sit amet consectetur adipisicing elit. Iste fugiat illum laudantium modi doloribus magni totam enim ducimus.</Typography>
                    </Box>
                </Card>
                <Card sx={{marginTop: 2}}>
                    <Typography level='title-lg'
                        startDecorator={<LocalOfferRoundedIcon/>}>
                        Tags
                    </Typography>
                    
                    <Grid>
                        <Chip variant="soft" color="primary" 
                            startDecorator={<CalendarMonthRoundedIcon/>} 
                            sx={{borderRadius: 'sm', m: 0.5}}>
                            Tag 1
                        </Chip>
                        <Chip variant="soft" color="primary" 
                            startDecorator={<CalendarMonthRoundedIcon/>} 
                            sx={{borderRadius: 'sm', m: 0.5}}>
                            Tag 2
                        </Chip>
                    </Grid>
                </Card>
                
                <Card sx={{marginTop: 2}} size='sm'>
                    <Typography level='title-lg' sx={{paddingLeft: 2, paddingTop: 2}}
                      startDecorator={<GroupRoundedIcon/>}
                    >
                        Links
                    </Typography>
                    <List>
                        <ListItem sx={{margin: 0.2}}>
                            <ListItemButton sx={{borderRadius: 'sm', transition: 'background-color 0.2s ease'}}>
                                <ListItemDecorator>
                                <OpenInNewIcon /></ListItemDecorator>
                                <ListItemContent>Vkontakte</ListItemContent>
                                <KeyboardArrowRight />
                            </ListItemButton>
                        </ListItem>
                        
                        <ListItem sx={{margin: 0.2}}>
                            <ListItemButton sx={{borderRadius: 'sm', transition: 'background-color 0.2s ease'}}>
                                <ListItemDecorator>
                                <OpenInNewIcon /></ListItemDecorator>
                                <ListItemContent>Discord</ListItemContent>
                                <KeyboardArrowRight />
                            </ListItemButton>
                        </ListItem>
                        
                        <ListItem sx={{margin: 0.2}}>
                            <ListItemButton sx={{borderRadius: 'sm', transition: 'background-color 0.2s ease'}}>
                                <ListItemDecorator>
                                <OpenInNewIcon /></ListItemDecorator>
                                <ListItemContent>Telegram</ListItemContent>
                                <KeyboardArrowRight />
                            </ListItemButton>
                        </ListItem>
                    </List>
                </Card>
                
                <Card sx={{marginTop: 2}} size='sm'>
                    <Typography level='title-lg' startDecorator={<MultipleStopRoundedIcon/>} sx={{paddingLeft: 2, paddingTop: 2}}>
                        Contacts
                    </Typography>
                    
                    <List>
                      <ListItem sx={{margin: 0.2}}>
                        <ListItemButton sx={{borderRadius: 'sm', transition: 'background-color 0.2s ease'}}>
                            <ListItemDecorator>
                              <Avatar size="md" variant='outlined' />
                            </ListItemDecorator>
                            <ListItemContent sx={{ml: 1.5}}>
                                <Typography level="title-sm">User1</Typography>
                                <Typography level="body-sm">Owner</Typography>
                            </ListItemContent>
                            <KeyboardArrowRight />
                          </ListItemButton>
                      </ListItem>
                      
                      <ListItem sx={{margin: 0.2}}>
                        <ListItemButton sx={{borderRadius: 'sm', transition: 'background-color 0.2s ease'}}>
                            <ListItemDecorator>
                              <Avatar size="md" variant='outlined' />
                            </ListItemDecorator>
                            <ListItemContent sx={{ml: 1.5}}>
                                <Typography level="title-sm">User2</Typography>
                                <Typography level="body-sm">Administration</Typography>
                            </ListItemContent>
                            <KeyboardArrowRight />
                          </ListItemButton>
                      </ListItem>
                    </List>
                </Card>
            </Stack>
            
            <TabsSegmentedControls sx={{flex: 1}}/>
            
        </Box>
    )
}


export default Community;