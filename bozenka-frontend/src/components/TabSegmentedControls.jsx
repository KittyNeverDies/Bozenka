// React related components
import * as React from 'react';

// Joy UI Components
import Card from '@mui/joy/Card';
import Grid from '@mui/joy/Grid';
import Avatar from '@mui/joy/Avatar';
import AccordionDetails from '@mui/joy/AccordionDetails';
import AccordionSummary from '@mui/joy/AccordionSummary';
import Typography from '@mui/joy/Typography';
import * as React from 'react';
import Tabs from '@mui/joy/Tabs';
import TabList from '@mui/joy/TabList';
import Tab, { tabClasses } from '@mui/joy/Tab';
import AccordionGroup from '@mui/joy/AccordionGroup';
import Accordion from '@mui/joy/Accordion';
import TabPanel from '@mui/joy/TabPanel';


// Material UI icons for Tabs
import BarChartRoundedIcon from '@mui/icons-material/BarChartRounded';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import ListItemContent from '@mui/joy/ListItemContent';
import MailRoundedIcon from '@mui/icons-material/MailRounded';
import QuizRoundedIcon from '@mui/icons-material/QuizRounded';
import InfoRoundedIcon from '@mui/icons-material/InfoRounded';



/**
 * @description This function renders a segmented tabs component with Joy UI.
 * @returns {JSX.Element}
 */
function TabsSegmentedControls() {
    /**
     * @description This state variable holds the index of the currently selected tab.
     * @type {number}
     */
    const [selectedTab, setSelectedTab] = React.useState(0);
    /**
     * @description This ref is used to get a reference to the tab list element.
     * @type {React.RefObject<HTMLDivElement>}
     */
    const tabListRef = React.useRef(null);

    /**
     * @description This function handles the tab change event.
     * @param {React.ChangeEvent<HTMLDivElement>} event - The event object.
     * @param {number} newValue - The index of the new tab.
     */
    const handleTabChange = (event, newValue) => {
      setSelectedTab(newValue);
    };

    /**
     * @description This useEffect hook is used to update the tab indicator position and size.
     * @param {number} selectedTab - The index of the currently selected tab.
     */
    React.useEffect(() => {
      /**
       * @description This function updates the tab indicator position and size.
       */
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

    /**
     * @description This function renders the segmented tabs component.
     * @returns {JSX.Element}
     */
    return (
      <Tabs 
        aria-label="tabs" 
        value={selectedTab} 
        onChange={handleTabChange}
        sx={{} /* Add your styles here */}>
        <TabList
          ref={tabListRef}
          disableUnderline
          sx={{} /* Add your styles here */}>
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
              <Grid>

              </Grid>
            </TabPanel>
            <TabPanel value={3}>
            <AccordionGroup
                  color="neutral"
                  size="sm"
                  
                  sx={{} /* Add your styles here */}>
                    
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