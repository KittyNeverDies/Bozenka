// React related components
import * as React from 'react';

// MUI Joy components
import Accordion, { accordionClasses } from '@mui/joy/Accordion';
import AccordionDetails from '@mui/joy/AccordionDetails';
import AccordionSummary from '@mui/joy/AccordionSummary';
import AccordionGroup from '@mui/joy/AccordionGroup';
import Avatar from '@mui/joy/Avatar';
import Box from '@mui/joy/Box';
import Card from '@mui/joy/Card';
import Chip from '@mui/joy/Chip';
import Grid from '@mui/joy/Grid';
import List from '@mui/joy/List';
import ListItem, {listItemClasses} from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemContent from '@mui/joy/ListItemContent';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import Stack from '@mui/joy/Stack';
import Tab, { tabClasses } from '@mui/joy/Tab';
import Tabs from '@mui/joy/Tabs';
import TabList from '@mui/joy/TabList';
import TabPanel from '@mui/joy/TabPanel';
import Typography from '@mui/joy/Typography';

// MUI Icons
import BarChartRoundedIcon from '@mui/icons-material/BarChartRounded';
import CalendarMonthRoundedIcon from '@mui/icons-material/CalendarMonthRounded';
import InfoRoundedIcon from '@mui/icons-material/InfoRounded';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import LocalOfferRoundedIcon from '@mui/icons-material/LocalOfferRounded';
import MailRoundedIcon from '@mui/icons-material/MailRounded';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import PersonIcon from '@mui/icons-material/Person';
import QuizRoundedIcon from '@mui/icons-material/QuizRounded';
import MultipleStopRoundedIcon from '@mui/icons-material/MultipleStopRounded';
import FilterNoneRoundedIcon from '@mui/icons-material/FilterNoneRounded';
import GroupRoundedIcon from '@mui/icons-material/GroupRounded';

function TabsSegmentedControls() {
  const [selectedTab, setSelectedTab] = React.useState(0);
  const tabListRef = React.useRef(null);

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
          borderColor: 'neutral.outlinedBorder',
          flexWrap: 'wrap',
          justifyContent: 'center',
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
        <Tab 
            key='About' 
            disableIndicator
          >
            <InfoRoundedIcon/>
            About
          </Tab>
        <Tab 
            key='Stats' 
            disableIndicator
          >
            <ListItemDecorator>
              <BarChartRoundedIcon/>
            </ListItemDecorator>
            Stats
        </Tab>
        
        <Tab 
            key='Posts' 
            disableIndicator
          >
            <ListItemDecorator>
              <MailRoundedIcon/>
            </ListItemDecorator>
            Posts
        </Tab>
        
        <Tab 
            key='KnowledgeLibrary' 
            disableIndicator
          >
            <ListItemDecorator>
              <QuizRoundedIcon/>
            </ListItemDecorator>
            Knowledge Library
        </Tab>
      </TabList>
      <Card sx={{marginTop: 2}}>
        <TabPanel value={0}>
          <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laborum suscipit repellat, architecto at dolore odio neque eos dolorum hic aliquam velit sapiente dignissimos molestiae pariatur ducimus! Soluta voluptate ad tenetur!</p>

          
          <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laborum suscipit repellat, architecto at dolore odio neque eos dolorum hic aliquam velit sapiente dignissimos molestiae pariatur ducimus! Soluta voluptate ad tenetur!</p>
          
          Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laborum suscipit repellat, architecto at dolore odio neque eos dolorum hic aliquam velit sapiente dignissimos molestiae pariatur ducimus! Soluta voluptate ad tenetur!
          
          </TabPanel>
          <TabPanel value={2}>
            Sorry for this joke. I'm sorry for this joke.
          </TabPanel>
          <TabPanel value={3}>
          <AccordionGroup
                color="neutral"
                size="sm"
                
                sx={{
                    borderRadius: 'md',
                    
        [`& .${accordionClasses.root}`]: {
            marginTop: '0.5rem',
            transition: '0.2s ease',
            '& button:not([aria-expanded="true"])': {
              transition: '0.2s ease',
              paddingBottom: '0.625rem',
            },
            '& button:hover': {
              background: 'transparent',
            },
          }
                }}
                variant="plain"
                transition="0.2s">
                  
                  <Accordion>
                    <AccordionSummary>
                        <Avatar color="primary">
                            <InfoRoundedIcon/>
                        </Avatar>
                        <ListItemContent>
                            <Typography level="title-md">Your lorem ipsum</Typography>
                            <Typography level="body-sm">Lorem Ipsum tutorial</Typography>
                        </ListItemContent>
                    </AccordionSummary>
                    <AccordionDetails>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Delectus perspiciatis cupiditate nam accusantium corporis obcaecati labore, dolores placeat aliquid doloremque impedit, sapiente aspernatur sit vero qui incidunt ipsa aliquam molestias.</AccordionDetails>
                  </Accordion>
          </AccordionGroup>
          </TabPanel>
      </Card>
    </Tabs>
  );
}


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
                    <Typography level='title-sm' 
                        startDecorator={<LocalOfferRoundedIcon/>}>
                        Tags
                    </Typography>
                    
                    <Grid>
                        <Chip variant="soft" color="primary" 
                            startDecorator={<CalendarMonthRoundedIcon/>} 
                            sx={
                                {
                                    borderRadius: 'sm',
                                    m: 0.5
                                }
                            }>
                            BAY BLADE
                        </Chip>
                        
                        <Chip variant="soft" color="primary" 
                            startDecorator={<CalendarMonthRoundedIcon/>} 
                            sx={
                                {
                                    borderRadius: 'sm',
                                    m: 0.5
                                }
                            }>
                            BAY BLADE
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
            </Stack>
            
            <TabsSegmentedControls sx={{flex: 1}}/>
            
        </Box>
    )
}


export default Community;