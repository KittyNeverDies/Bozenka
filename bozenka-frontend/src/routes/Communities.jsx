// React stuff
import { useState } from 'react';


import SearchIcon from '@mui/icons-material/Search';
import CancelIcon from '@mui/icons-material/Cancel';

import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';
import Card from '@mui/joy/Card';
import Typography from '@mui/joy/Typography';
import Avatar from '@mui/joy/Avatar';
import Dropdown from '@mui/joy/Dropdown';
import MenuButton from '@mui/joy/MenuButton';
import Menu from '@mui/joy/Menu';
import MenuItem from '@mui/joy/MenuItem';
import Box from '@mui/joy/Box';
import Chip from '@mui/joy/Chip';
import Radio from '@mui/joy/Radio';
import RadioGroup from '@mui/joy/RadioGroup';
import Grid from '@mui/joy/Grid';
import Accordion, { accordionClasses } from '@mui/joy/Accordion';
import AccordionDetails from '@mui/joy/AccordionDetails';
import AccordionGroup from '@mui/joy/AccordionGroup';
import AccordionSummary from '@mui/joy/AccordionSummary';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import ListItemContent from '@mui/joy/ListItemContent';
import CardContent from '@mui/joy/CardContent';
import CardOverflow from '@mui/joy/CardOverflow';
import Slider from '@mui/joy/Slider';
import Divider from '@mui/joy/Divider';

// Material UI icons
import InfoIcon from '@mui/icons-material/Info';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import ReportIcon from '@mui/icons-material/Report';
import LocalOfferRoundedIcon from '@mui/icons-material/LocalOfferRounded';
import ListRoundedIcon from '@mui/icons-material/ListRounded';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import PeopleRoundedIcon from '@mui/icons-material/PeopleRounded';
import PersonIconRounded from '@mui/icons-material/PersonRounded';
import CalendarMonthRoundedIcon from '@mui/icons-material/CalendarMonthRounded';


/**
 * @function SelectableTags
 * @description This function renders chip tags that can be selected and deselected. Mostly used for tags of communities.
 * @param {Object} props - The props object passed to the component.
 * @param {Object} props.Tag - The tag object containing the icon and name of the tag.
 * @param {Object} props.Tag.icon - The icon of the tag.
 * @param {Object} props.Tag.name - The name of the tag.
 * @returns {JSX.Element} - The JSX element representing the selectable tags.
 */
function SelectableTags({ Tag }) {
    /**
     * @description The tag object containing the icon and name of the tag.
     * @type {Object}
     */
    const {icon, name} = Tag

    /**
     * @description A boolean state variable that indicates whether the tag is selected or not.
     * @type {boolean}
     */
    const [isSelected, SetSelected] = useState(false);

    /**
     * @description The JSX element representing the selectable tags.
     * @type {JSX.Element}
     */
    return (
        <Chip
            sx={
                /**
                 * @description The styling object for the Chip component.
                 * @type {Object}
                 */
                {
                    m: 0.4
                }
            }
            variant='soft'
            onClick={() => SetSelected(!isSelected)}
            color={isSelected == true ? 'primary' : 'neutral'}
            startDecorator={icon} // Add some spacing between tags
        >
            {name}
        </Chip>
    )
}



function RangeSlider(label, textOfValue, maxValue, minValue) {
    /*
        Code of range slider from MUI documentation.
    */
   
    const [value, setValue] = useState([minValue, maxValue]);
    

    const handleChange = (event, newValue) => {
          setValue(newValue);
    };
    const valueText = (value) => {
        return `${value} ${textOfValue}`;
    }

    return (
        <>
            <Slider
                sx={{
                    marginLeft: 2
                }}
                getAriaLabel={() => label}
                value={value}
                onChange={handleChange}
                valueLabelDisplay="auto"
                getAriaValueText={valueText}
        />
        </>
    )
}

function RangeSliders() {
    /*
        Thats a range slider
        Based on one from MUI documentation.
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


  function FiltersCard() {
    /*
        Card with filters in it :)
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

function CommunityCard() {
    // const { icon, name, small_description, id } = community;

    return (
        <Card sx={{m: 1 }}>
            <Avatar src="https://images.unsplash.com/photo-1507833423370-a126b89d394b?auto=format&fit=crop&w=90" />
            <Dropdown>
                <MenuButton size='sm' variant='plain' sx={{ position: 'absolute', top: '0.875rem', right: '0.5rem' }}>
                    <MoreVertIcon />
                </MenuButton>
                <Menu size='sm'>
                    <MenuItem color='danger'>
                        <ListItemDecorator sx={{ color: 'inherit' }}>
                            <ReportIcon />
                        </ListItemDecorator>
                        Report
                    </MenuItem>
                    <Divider />
                    <MenuItem>
                        Discord
                        <OpenInNewIcon />
                    </MenuItem>
                    <MenuItem>
                        Telegram
                        <OpenInNewIcon />
                    </MenuItem>
                    <MenuItem>
                        Vkontakte
                        <OpenInNewIcon />
                    </MenuItem>
                </Menu>
            </Dropdown>
            <CardContent>
                <Typography level="title-lg">Testing stuff?</Typography>
                <Typography level="body-sm">Lorem ipsum lorem ipsum. Lorem lorem ipsum ipsum.</Typography>
                <Grid>
                    <Chip variant="outlined"
                        startDecorator={<InfoIcon/>}
                        sx={{
                            m: 0.5
                        }}
                    >
                        First Tag
                    </Chip>
                    <Chip variant="outlined"
                        startDecorator={<InfoIcon/>}
                        sx={{
                            m: 0.5
                        }}
                    >
                        Second Tag
                    </Chip>
                    <Chip variant="outlined"
                        startDecorator={<InfoIcon/>}
                        sx={{
                            m: 0.5
                        }}
                    >
                        Third Tag
                    </Chip>
                </Grid>
            </CardContent>
            
            <CardOverflow>
                <Divider inset="context" />
                <CardContent orientation="horizontal">
                    <Typography
                        startDecorator={<PersonIconRounded/>} 
                        level="body-xs" fontWeight="md" textColor="text.secondary">
                        650 members
                    </Typography>
                    <Divider orientation="vertical" />
                    <Typography 
                        startDecorator={<CalendarMonthRoundedIcon/>} level="body-xs" fontWeight="md"  textColor="text.secondary">
                        created on 9th September, 1999
                    </Typography>
                </CardContent>
            </CardOverflow>
        </Card>
    );
}

function CommunitiesSearch() {
    const [searchTerm, setSearchTerm] = useState('');
    const [isFocused, setIsFocused] = useState(false);

    const handleClear = () => {
        setSearchTerm('');
    };

    return (
    <>
        <Box sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'flex-start', flexWrap: 'wrap' }}>
                <FiltersCard />
                <Box sx={{ flex: 1 }}>
                    
                    <Input
                        sx={{
                            '--Input-focusedThickness': '1px',
                            bgcolor: 'background.surface',
                            borderRadius: 'lg',
                            '&:hover': {
                              bgcolor: 'background.level1',
                              borderColor: 'primary.300',
                            },
                            '&:focus-within': {
                              borderColor: 'background.level2',
                              bgcolor: 'background.level1',
                            },
                            '&:focus': {
                              outline: 'none',
                            },
                            mt: 1,
                            mb: 1,
                            py: 1.5,
                            px: 2,
                            fontSize: 'sm',
                            fontWeight: 'md',
                            border: '1px solid',
                            borderColor: 'neutral.300',
                            transition: 'box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out, background-color 0.2s ease-in-out',
                            '&::placeholder': {
                              color: 'neutral.500',
                              fontStyle: 'italic',
                            },
                            '&:disabled': {
                              bgcolor: 'neutral.100',
                              color: 'neutral.400',
                              cursor: 'not-allowed',
                            },
                          }}
                        placeholder='Search for communities...'
                        startDecorator={<SearchIcon />}
                        endDecorator={
                        <>
                            
                            {searchTerm && (
                                <Button variant='plain' startDecorator={<CancelIcon />} onClick={handleClear}>
                                    Clear
                                </Button>
                            )}
                            
                        </>
                        }
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        onFocus={() => setIsFocused(true)}
                        onBlur={() => setIsFocused(false)}
                    />
                    
                    {isFocused && searchTerm === '' && (
                        <Card variant="outlined" sx={{ mt: 1, animation: 'sizeIn 0.3s' }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', p: 2 }}>
                                <InfoIcon sx={{ mr: 1 }} />
                                <Box>
                                    <Typography level="title-lg">Search tip</Typography>
                                    <Typography level="body-sm">
                                        Enter specific words related to your search query to get relevant results
                                    </Typography>
                                </Box>
                            </Box>
                        </Card>
                    )}
                    <Box sx={{ display: 'flex', flexWrap: "wrap" }}>
                        <CommunityCard />
                        <CommunityCard />
                        <CommunityCard />
                        <CommunityCard />
                        <CommunityCard />
                        <CommunityCard />
                        <CommunityCard />
                    </Box>
                    {/* Community cards go here */}
                </Box>
            </Box>
        </Box>
        </>
    );
}

export default CommunitiesSearch;