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


// Material UI icons for Tabs
import BarChartRoundedIcon from '@mui/icons-material/BarChartRounded';
import CalendarMonthRoundedIcon from '@mui/icons-material/CalendarMonthRounded';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import ListItemContent from '@mui/joy/ListItemContent';
import MailRoundedIcon from '@mui/icons-material/MailRounded';
import QuizRoundedIcon from '@mui/icons-material/QuizRounded';
import InfoRoundedIcon from '@mui/icons-material/InfoRounded';
import VisibilityRoundedIcon from '@mui/icons-material/VisibilityRounded';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import PersonIcon from '@mui/icons-material/Person';




function TabsSegmentedControls() {
  const [selectedTab, setSelectedTab] = React.useState(0);
  const tabListRef = React.useRef(null);

  const posts = [
    {
      title: 'Post 1',
      author: 'John Doe',
      content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
      date: '2022-01-01',
      category: 'Vk',
      views: '1'
    },
    {
      title: 'Post 2',
      author: 'Jane Doe',
      content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
      date: '2022-01-02',
      category: 'Telegram',
      views: '10'
    },
    // Add more posts here...
  ];

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
      <Card sx={{marginTop: 2, paddingBottom: 6}}>
        <TabPanel value={0}>
          {/* Description of community */}
          <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laborum suscipit repellat, architecto at dolore odio neque eos dolorum hic aliquam velit sapiente dignissimos molestiae pariatur ducimus! Soluta voluptate ad tenetur!</p>

          
          <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laborum suscipit repellat, architecto at dolore odio neque eos dolorum hic aliquam velit sapiente dignissimos molestiae pariatur ducimus! Soluta voluptate ad tenetur!</p>
          
          Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laborum suscipit repellat, architecto at dolore odio neque eos dolorum hic aliquam velit sapiente dignissimos molestiae pariatur ducimus! Soluta voluptate ad tenetur!
          
          </TabPanel>
          <TabPanel value={2}>
            <Typography level='h2' sx={{mb: 2}}>
              Posts
            </Typography>
            <Grid container spacing={1}>
              {posts.map((post, index) => (
                <Grid item key={index} xs={12} sm={6} md={4} lg={3}>
                  <Card sx={{ height: '100%'}}>
            
                    <Typography level="title-lg" sx={{marginBottom: -1}}>
                      {post.title}
                    </Typography>
                    <Typography startDecorator={<PersonIcon/>} level="body-xs">
                      by {post.author}
                    </Typography>
                    <Typography level="body-sm">
                      {post.content}
                    </Typography>
                    
                    <Box>
                      <Typography startDecorator={<CalendarMonthRoundedIcon/>} sx={{m: 0.2}} level="body-xs">
                        Posted at {post.date}
                      </Typography>
                      <Chip variant="soft" startDecorator={<OpenInNewIcon/>} color="primary" size="md" sx={{borderRadius: 'sm', m: 0.2}}>
                        {post.category}
                      </Chip>
              
                      <Chip variant="soft" startDecorator={<VisibilityRoundedIcon/>} color="primary" size="md" sx={{borderRadius: 'sm', m: 0.2}}>
                        {post.views} views
                      </Chip>
                    </Box>
                  </Card>
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
export default TabsSegmentedControls;