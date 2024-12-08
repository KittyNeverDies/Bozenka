// Some react stuff
import { useRef } from 'react';
import {Link} from 'react-router-dom';


// MUI joy elements
import Typography from '@mui/joy/Typography';
import Button from "@mui/joy/Button";
import Box from "@mui/joy/Box";
import Card from '@mui/joy/Card';
import Chip from '@mui/joy/Chip';


// MUI icons
import AnalyticsIcon from "@mui/icons-material/Analytics";
import GroupIcon from "@mui/icons-material/Group";
import GroupsIcon from "@mui/icons-material/Groups";
import CodeIcon from "@mui/icons-material/Code";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import KeyboardDoubleArrowDownRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowDownRounded';
import OpenInNewRoundedIcon from '@mui/icons-material/OpenInNewRounded';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';


/**
* FeatureCard component
* Card that describes a feature of bozenka.
* Used in homepage, to be simple.
* @param {Object} feature - The feature object containing icon, name, and description.
* @returns {JSX.Element} - The rendered feature card.
*/
function FeatureCard({ feature }){
    const {icon, name, description} = feature 
    return (
        <Card color='primary' invertedColors variant='solid' sx={{
            width: 200,
            height: 150,
            transition: 'transform 0.3s, box-shadow 0.3s',
            '&:hover': { 
                transform: 'scale(1.05)', 
                boxShadow: 'md',
            }
        }}> 
            <Chip
                size="lg"
                variant="soft"
                startDecorator={icon}
                sx={{ alignSelf: 'flex-start', borderRadius: 'xl', fontWeight: 'bold' }}
            >
                {name}
            </Chip>
            <Typography level='body-sm' sx={{
                pt: 2, 
            }}>{description} </Typography>


        </Card>
    );
}


/**
* HomePage component
* Home page of bozenka utility, what should introduce bozenka for new users.
* @returns {JSX.Element} - The rendered home page.
*/
function HomePage(){
    const KeyFeatures = useRef(null)
    const scrollToFeatures = () => KeyFeatures.current.scrollIntoView()    

    const features = [
        {
            icon: <GroupIcon />,
            name: "Management",
            description: "Manage all your communities from a single dashboard."
        },
        {
            icon: <AnalyticsIcon  />,
            name: "Analytics",
            description: "Effortlessly track your community's engagement and growth."
        },
        {
            icon: <AutoAwesomeIcon  />,
            name: "Automation",
            description: "Automate repetitive tasks and moderation."
        },
        {
            icon: <CodeIcon  />,
            name: "Open Source",
            description: "Code under GPL-v3 license"
        },
        {
            icon: <GroupsIcon />,
            name: "Socialization",
            description: "Connect with like-minded individuals to form a community."
        }
    ]


    return (
        <>
        
            {/* Main introduction page */}
            <Box sx={{
                height: 500,
                paddingTop: 10,
                paddingBottom: 3,
                backgroundImage: ({ palette }) =>
                    `linear-gradient(to bottom, ${palette.background.level1}, ${palette.background.body})`,
                mb: 10
                
            }}>
                <Typography level='h1' element="h1" sx={{
                    textAlign: "center",
                    paddingTop: 10,
                    
                    
                }}>
                    Manage Your Community Across Platforms
                </Typography>
            
                <Typography level='h4' sx={{
                    textAlign: "center",
                }}>Streamline your community management on Discord, Telegram, and VK with Bozenka project.
                </Typography>
                <Box textAlign="center" sx={{p:5}}>
                    <Button variant="soft" size="lg" sx={{
                        justifyContent: "center",
                        p: 2,
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
                    }} endDecorator={<KeyboardDoubleArrowDownRoundedIcon/>}
                    onClick={scrollToFeatures}
                    >
                        Get started
                    </Button>
                </Box>
            </Box>

            {/* Features section. */}
            <Box sx={{
                backgroundColor: 'background.level1',
                pb: 5,
                borderRadius: 'lg',
                ml: 1,
                mr: 1,
            }}>
            <Typography level='h1' ref={KeyFeatures} sx={{
                textAlign: "center",
                paddingTop: 10,
                paddingBottom: 4
            }}>
                Key Features
            </Typography>
            <Box sx={{ 
                display: 'flex', 
                flexWrap: 'wrap', 
                gap: 4, justifyContent: 'center' 
            }}>
                {features.map((feature, index) => (
                <FeatureCard key={index} feature={feature} />
                ))}
            </Box>

            </Box>
            {/* Ending of the page */}
            <Box sx={{
                paddingTop: 18,
                height: 500,
                
                backgroundImage: ({ palette }) =>
                    `linear-gradient(to bottom, ${palette.background.body}, ${palette.background.level1})`,
                paddingBottom: 3,
            }}>
                <Typography level='h1' element="h1" sx={{
                    textAlign: "center",
                    paddingTop: 10,
                }}>
                   Ready to Elevate Your Community Management?
                </Typography>
            
                <Typography level='h4' sx={{
                    textAlign: "center",
                }}>
                    Start your journey of nextgen community management now. Stay tuned for updates.
                </Typography>
                <Box textAlign="center" sx={{p:5}}>
                    <Link to="https://t.me/bozodevelopment/">
                    <Button variant="soft" size="lg" endDecorator={<OpenInNewRoundedIcon/>} sx={{
                        justifyContent: "center",
                        p: 2,
                        
                        transition: 'transform 0.2s ease, background-color 0.2s ease',
                        '&:hover': {
                            transform: 'scale(1.05)',
                            bgcolor: 'primary.lightBg',
                            borderRadius: '',
                        },
                        '&:active': {
                            transform: 'scale(1.20)'
                        }
                    }}>
                        Check out telegram channel
                    </Button>
                    </Link>
                </Box>
            </Box>
        </>
    );
}

export default HomePage;