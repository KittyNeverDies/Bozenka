// React related components
import * as React from 'react';

// Joy UI Components
import Card from '@mui/joy/Card';
import Grid from '@mui/joy/Grid';
import Chip from '@mui/joy/Chip';
import Box from '@mui/joy/Box';
import Avatar from '@mui/joy/Avatar';
import Accordion, { accordionClasses } from '@mui/joy/Accordion';
import AccordionDetails from '@mui/joy/AccordionDetails';
import AccordionSummary from '@mui/joy/AccordionSummary';
import AccordionGroup from '@mui/joy/AccordionGroup';
import Typography from '@mui/joy/Typography';
import Tabs from '@mui/joy/Tabs';
import TabList from '@mui/joy/TabList';
import Tab, { tabClasses } from '@mui/joy/Tab';
import TabPanel from '@mui/joy/TabPanel';


import TestChart from './GrowthChart';


import {useTheme} from '@mui/joy';

// Material UI icons for Tabs
import BarChartRoundedIcon from '@mui/icons-material/BarChartRounded';
import CalendarMonthRoundedIcon from '@mui/icons-material/CalendarMonthRounded';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import ListItemContent from '@mui/joy/ListItemContent';
import MailRoundedIcon from '@mui/icons-material/MailRounded';
import QuizRoundedIcon from '@mui/icons-material/QuizRounded';
import InfoRoundedIcon from '@mui/icons-material/InfoRounded';
import VisibilityRoundedIcon from '@mui/icons-material/VisibilityRounded';
import PeopleRoundedIcon from '@mui/icons-material/PeopleRounded';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import PersonIcon from '@mui/icons-material/Person';




function CommunitySegmentedInfo({community_description, growth_stats, er_stats, posts }) {
  const [selectedTab, setSelectedTab] = React.useState(0);
  const tabListRef = React.useRef(null);

  // Data for stats visualization (mapped from growth_stats and er_stats)
  // Will be 100% reworked in future
  const data = growth_stats.map((stat, index) => ({
    name: stat.date,
    views: stat.views || 0, // If views are in growth_stats
    members: stat.members_count || 0,
    amt: stat.members_count || 0,
    er: er_stats?.[index]?.er || 0, // Match ER with corresponding date
  }));

  // Display data configuration (should be mapped from server data)
  const displayData = {
    members: {
      title: "The number of community members",
      shortTitle: "Number of members",
      description: "Total number of community members.",
      icon: <PeopleRoundedIcon />,
      color: theme.palette.primary[500],
    },
    views: {
      title: "Views of the posts",
      shortTitle: "Views of the posts",
      description: "Total growth of number of views on posts.",
      icon: <VisibilityRoundedIcon />,
      color: theme.palette.success[500]
    }
  };

  // Icons configuration (not mapped from server data)
  const icons = {
    members: <PeopleRoundedIcon />,
    views: <VisibilityRoundedIcon />,
  };

  // Posts data (mapped from server)
  const postsData = posts || [];

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
        width: '100%',
        marginLeft: 2,
        '@media (max-width: 670px)': {
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
            <InfoRoundedIcon />
            About
          </Tab>
        <Tab 
            key='Stats' 
            disableIndicator
          >
            <ListItemDecorator>
              <BarChartRoundedIcon />
            </ListItemDecorator>
            Stats
        </Tab>
        
        <Tab 
            key='Posts' 
            disableIndicator
          >
            <ListItemDecorator>
              <MailRoundedIcon />
            </ListItemDecorator>
            Posts
        </Tab>
        
        <Tab 
            key='KnowledgeLibrary' 
            disableIndicator
          >
            <ListItemDecorator>
              <QuizRoundedIcon />
            </ListItemDecorator>
            Knowledge Library
        </Tab>
      </TabList>
      <Card sx={{marginTop: 2, paddingBottom: 6, height: '100%'}}>
        <TabPanel value={0}>
          <Typography>
            {community_description}
          </Typography>
        </TabPanel>
        <TabPanel value={1}>
          <Typography level='h2' sx={{mb: 2}}>
            Stats
          </Typography>
            <TestChart icons={icons} data={data} displayData={displayData} />
        </TabPanel>
        <TabPanel value={2}>
          <Typography level='h2' sx={{mb: 2}}>
            Posts
          </Typography>
          <Grid container spacing={1}>
            {postsData.map((post, index) => (
              <Grid item key={index} xs={12} sm={6} md={4} lg={3}>
                <Box my={0.5}>
                <Card sx={{ height: '100%' }}>
                
                  <Typography level="body-sm">
                    {post.text}
                  </Typography>
                  
                  <Box>
                    <Typography startDecorator={<CalendarMonthRoundedIcon />} sx={{m: 0.2}} level="body-xs">
                      Posted at {new Date(post.created_at).toLocaleDateString()}
                    </Typography>
                    <Chip variant="soft" startDecorator={<OpenInNewIcon />} color="primary" size="md" sx={{borderRadius: 'sm', m: 0.2}}>
                      {post.source}
                    </Chip>

                    <Chip variant="soft" startDecorator={<VisibilityRoundedIcon />} color="primary" size="md" sx={{borderRadius: 'sm', m: 0.2}}>
                      {post.views} views
                    </Chip>
                  </Box>
                </Card>
                </Box>
              </Grid>
            ))}
          </Grid>
        </TabPanel>
        <TabPanel value={3}>
        
        <Typography level='h2' sx={{mb: 2}}>
            Knowledge Library
        </Typography>
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
              transition="0.2">
                <Accordion>
                  <AccordionSummary>
                      <Avatar color="primary">
                          <InfoRoundedIcon />
                      </Avatar>
                      <ListItemContent>
                          <Typography level="title-md">Community Guidelines</Typography>
                          <Typography level="body-sm">Learn how to behave in our community</Typography>
                      </ListItemContent>
                  </AccordionSummary>
                  <AccordionDetails>
                    {displayData.members.description}
                  </AccordionDetails>
                </Accordion>
        </AccordionGroup>
        </TabPanel>
      </Card>
    </Tabs>
  );
}
export default CommunitySegmentedInfo;