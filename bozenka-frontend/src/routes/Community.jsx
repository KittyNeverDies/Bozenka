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

// Our componenets
import CommunitySegmentedInfo from '../components/CommunitySegmentedInfo';
import CommunityApiClient from '../api/CommunityApiClient';

// React Router
import { useParams } from 'react-router-dom';


/**
* Community page, should be displayed for some community id, 
* with based information about it. (description, etc).
* @returns {JSX.Element} - The rendered community page.
*/
function Community() {
    const [community, setCommunityInfo] = React.useState({}) // Initialize as object
    const params = useParams();
    const [loading, setLoading] = React.useState(true);

    if (!params.id) {
        return <Typography>
            Please, don't try to break me by not passing community.
        </Typography>
    }
    

    // Fetch tags and communities on mount
    React.useEffect(() => {
        const fetchData = async () => {
            const api = new CommunityApiClient();
            try {
                // Fetch both tags and communities in parallel
                const communityInfo = await api.getCommunity(params.id)
                setCommunityInfo(communityInfo)
            } catch (error) {
                console.error('Failed to fetch data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    // Function to render icon component based on tag icon
    const renderIcon = (icon) => {
        return (
            <Typography
                component="span"
                sx={{ 
                    fontFamily: 'Material Icons',
                    fontSize: '14px',
                    color: 'inherit',
                    display: 'flex',
                    alignItems: 'center',
                }}
            >
                {icon}
            </Typography>
        );
    };

    if (loading) {
        return <Typography>Loading...</Typography>;
    }

    return (
        <Box sx={{
                m: 2,
                display: 'flex',
                flexDirection: 'row',
                '@media (max-width: 670px)': { // Mobile responsiveness
                  flexDirection: 'column',
                }}} >
            <Stack sx={{
                    flexDirection: 'column',
                    width: 300,
                    '@media (max-width: 670px)': { // Mobile responsiveness
                      width: '100%',
                      position: 'relative',
                      left: 'unset',
                      mr: 0,
                  }}
            }>
                  <Box sx={{mb: 2}}>
                    <Breadcrumbs 
                        size='sm'
                        separator={<KeyboardArrowRightIcon/>}
                        sx={{
                          "--Breadcrumbs-gap": "3px"
                        }}
                    >
                      <Typography  sx={{mt: 0}}>Home</Typography>
                      <Typography  sx={{mt: 0}}>Communities</Typography>
                      <Typography  sx={{pt: 0, color: 'primary.plainColor'}}>{community.community_info?.name}</Typography>
                    </Breadcrumbs>
                  </Box>
                <Card>
                    <Avatar 
                        src={`http://127.0.0.1:8000${community.community_info?.icon}`} // Using optional chaining
                        variant='outlined'
                    />
                    <Box>
                        <Typography level="title-lg"
                            sx={{
                                marginBottom: 0
                            }}>
                            {community.community_info?.name}
                        </Typography>
                        <Typography
                        startDecorator={<PersonIcon/>}
                        level="body-xs">
                            {community.community_info?.members_count} Members
                        </Typography>
                        <Typography 
                            startDecorator={<CalendarMonthRoundedIcon/>}
                            level="body-xs">
                            Created on {new Date(community.community_info?.creation_date).toLocaleDateString()}
                        </Typography>
                        <Typography level="body-sm">{community.community_info?.description || 'No description provided'}</Typography>
                    </Box>
                </Card>
                <Card sx={{marginTop: 2}}>
                    <Typography level='title-lg'
                        startDecorator={<LocalOfferRoundedIcon/>}>
                        Tags
                    </Typography>
                    
                    <Grid sx={{flexWrap: 'wrap'}}>
                        {community.community_info?.tags.map((tag) => (
                            <Chip 
                                key={tag.id} 
                                variant="soft" 
                                color="primary" 
                                startDecorator={renderIcon(tag.icon)} 
                                sx={{borderRadius: 'sm', m: 0.5}}>
                                {tag.name}
                            </Chip>
                        ))}
                    </Grid>
                </Card>
                {community.social_links && (<Card sx={{marginTop: 2}} size='sm'>
                    <Typography level='title-lg' sx={{paddingLeft: 2, paddingTop: 2}}
                      startDecorator={<GroupRoundedIcon/>}
                    >
                        Links
                    </Typography>
                    <List>
                        {community.social_links.map((connection) =>
                        (
                        <Link to={connection.link}>
                            <ListItem sx={{margin: 0.2}}>
                            <ListItemButton sx={{borderRadius: 'sm', transition: 'background-color 0.2s ease'}}>
                                <ListItemDecorator>
                                <OpenInNewIcon /></ListItemDecorator>
                                <ListItemContent>connection.platform</ListItemContent>
                                <KeyboardArrowRight />
                            </ListItemButton>
                            </ListItem>
                            </Link>
                        ))}

                        
                        {/* Add your social links here based on community.social_links */}
                    </List>
                </Card>)}
                { community.managers && (<Card sx={{marginTop: 2}} size='sm'>
                    <Typography level='title-lg' startDecorator={<MultipleStopRoundedIcon/>} sx={{paddingLeft: 2, paddingTop: 2}}>
                        Contacts
                    </Typography>
                    
                    <List>
                        {/* String(val).charAt(0).toUpperCase() + String(val).slice(1) */}
                        {community.managers.map((manager) => (<ListItem sx={{margin: 0.2}}>
                        <ListItemButton sx={{borderRadius: 'sm', transition: 'background-color 0.2s ease'}}>
                            <ListItemDecorator>
                              <Avatar size="md" src={`http://localhost:8000${manager.avatar}`} variant='outlined' />
                            </ListItemDecorator>
                            <ListItemContent sx={{ml: 1.5}}>
                                <Typography level="title-sm">{manager.user.display_name ? manager.user.display_name : manager.user.username}</Typography>
                                <Typography level="body-sm">{String(manager.status).charAt(0).toUpperCase() + String(manager.status).slice(1)} </Typography>
                            </ListItemContent>
                            <KeyboardArrowRight />
                          </ListItemButton>
                      </ListItem>))}
                        {/* Add your contacts list here based on community.managers */}
                    </List>
                </Card>)}
                {/* Rest of the component remains the same */}
            </Stack>
            <CommunitySegmentedInfo 
                community_description={community.description}
                growth_stats={community.growth_stats}
                er_stats={community.er_stats}
                sx={{flex: 1}} 
            />
        </Box>
    )
}

export default Community;