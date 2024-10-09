
// Joy UI components
import Button from '@mui/joy/Button';
import Card from '@mui/joy/Card';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import Avatar from '@mui/joy/Avatar';
import Radio from '@mui/joy/Radio';
import RadioGroup from '@mui/joy/RadioGroup';
import Grid from '@mui/joy/Grid';
import Accordion, { accordionClasses } from '@mui/joy/Accordion';
import AccordionDetails from '@mui/joy/AccordionDetails';
import AccordionGroup from '@mui/joy/AccordionGroup';
import AccordionSummary from '@mui/joy/AccordionSummary';
import ListItemContent from '@mui/joy/ListItemContent';

// Material UI icons
import InfoIcon from '@mui/icons-material/Info';
import CancelIcon from '@mui/icons-material/Cancel';
import LocalOfferRoundedIcon from '@mui/icons-material/LocalOfferRounded';
import ListRoundedIcon from '@mui/icons-material/ListRounded';
import PeopleRoundedIcon from '@mui/icons-material/PeopleRounded';

import SelectableTags from './SelectableTags';
import RangeSlider from './RandeSlider';



/**
 * @description A functional component that renders range sliders for filters card
 * @returns {JSX.Element}
 */
function RangeSliders() {    
    /**
    * @description Range sliders for filters card
    * @type {JSX.Element}
    */
  
    return (
    <>
      <Box sx={{ width: 250, marginTop: 2}}>
        <Typography gutterBottom>
            Community members count range
        </Typography>
        <RangeSlider 
            label="Community members count range"
            textOfValue="members" maxValue="100" minValue="0" />
      </Box>
      
      <Box sx={{ width: 250 }}>
        <Typography gutterBottom>
            Community growth range
        </Typography>
        <RangeSlider
            label="Community members count range" 
            textOfValue="Members" maxValue="100" minValue="0"
        />
      </Box>
    </>
    );
  }



/**
 * @description A functional component that renders a card with filters to filter communities
 * @returns {JSX.Element}
 */
function FiltersCard() {
    /**
    * @description The main card that contains all the filters.
    * @type {JSX.Element}
    */
    return (
        <Card 
            variant="outlined" 
            sx={{ 
                width: 300, 
                mr: 2, 
                top: 16, // Adjust as needed
                maxHeight: 'calc(100vh - 32px)', // Adjust as needed
                overflowY: 'auto',
                marginBottom: '25px',
                '@media (max-width: 670px)': { // Mobile responsiveness
                    width: '100%',
                    position: 'relative',
                    left: 'unset',
                    mr: 0,
                }
            }}
        >
            <Typography level="h4" sx={{
                paddingTop: 2,
                paddingLeft: 2,
                paddingRight: 2,
             }}>
                Filters
            </Typography>
            <Button
                    variant='soft'
                    size='sm'
                    startDecorator={<CancelIcon/>}
                    sx={{
                        width: 150,
                        marginLeft: 1,
                        transition: 'transform 0.2s ease, background-color 0.2s ease',
                        border: '1px',
                        '&:hover': {
                            transform: 'scale(1.05)',
                            bgcolor: 'primary.lightBg',
                            borderRadius: '',
                        },
                        '&:active': {
                            transform: 'scale(1.20)'
                        }
                    }}>
                    Clear Filters
                </Button>
            <AccordionGroup
                color="neutral"
                size="sm"
                
                sx={{
                    borderRadius: 'md',
                    
        [`& .${accordionClasses.root}`]: {
            marginTop: '0.5rem',
            transition: '0.2s ease, background-color 0.4 ease, transform 0.2 ease',
            '& button:not([aria-expanded="true"])': {
              transition: '0.2s ease',
              paddingBottom: '0.625rem',
            },
            '& button:hover': {
              background: 'transparent'
            },
            
            '& button:active': {
                backgroundColor: 'background.level1',
                borderRadius: 'md'
            }
          }
                }}
                variant="plain"
                transition="0.2s">
                {/* Filters for communtites */}
                <Accordion>
                    <AccordionSummary>
                        <Avatar color="primary">
                            <LocalOfferRoundedIcon />
                        </Avatar>
                        <ListItemContent>
                            <Typography level="title-md">Tags</Typography>
                            <Typography level="body-sm">Filter communities by interests</Typography>
                        </ListItemContent>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Grid sx={{ 
                            overflowY: 'auto', maxHeight: 100, 
                        }}> 
                            <SelectableTags Tag={{'icon': <InfoIcon/>, 'name': 'Test tag'}}/>
                            <SelectableTags Tag={{'icon': <InfoIcon/>, 'name': 't tag'}}/>
                            <SelectableTags Tag={{'icon': <InfoIcon/>, 'name': 'Test tag'}}/>
                            <SelectableTags Tag={{'icon': <InfoIcon/>, 'name': 't tag'}}/>
                            <SelectableTags Tag={{'icon': <InfoIcon/>, 'name': 'Test tag'}}/>
                            <SelectableTags Tag={{'icon': <InfoIcon/>, 'name': 'Test tag'}}/>
                            {/* Add your filter options here */}
                        </Grid>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary>
                        <Avatar color="primary">
                            <PeopleRoundedIcon />
                        </Avatar>
                        <ListItemContent>
                            <Typography level="title-md">Members</Typography>
                            <Typography level="body-sm">Filter communities by count of memebers & growth.</Typography>
                        </ListItemContent>
                    </AccordionSummary>
                    <AccordionDetails>
                        <RangeSliders/>
                    </AccordionDetails>
                </Accordion>
            </AccordionGroup>
            <Typography level="h4" sx={{paddingLeft: 2}}>
                List options
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
                            <ListRoundedIcon />
                        </Avatar>
                        <ListItemContent>
                            <Typography level="title-md">Count per page</Typography>
                            <Typography level="body-sm">How much show communties per page.</Typography>
                        </ListItemContent>
                    </AccordionSummary>
                    <AccordionDetails>
                            <RadioGroup defaultValue='5'>
                                <Grid>
                                <Radio value='20'
                                    variant="outlined" 
                                    size='sm'
                                    sx={{
                                        m: 0.5
                                    }}
                                    label='20 per Page' />
                                <Radio value='15'
                                    variant="outlined"
                                    size='sm' 
                                    sx={{
                                        m: 0.5
                                    }}
                                    label='15 per Page' />
                                <Radio value='10' 
                                    variant="outlined"
                                    size='sm' 
                                    sx={{
                                        m: 0.5
                                    }}
                                    label='10 per Page' />
                                <Radio value='5'
                                    size='sm' 
                                    sx={{
                                        m: 0.5
                                    }}
                                    variant="outlined" 
                                    label='5 per Page' />
                                </Grid>
                            </RadioGroup>
                    </AccordionDetails>
                </Accordion>
            </AccordionGroup>
        </Card>
    );
}

export default FiltersCard;