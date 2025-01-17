// Some react stuff
import { useRef } from 'react';
import {Link} from 'react-router-dom';


// MUI joy elements
import Typography from '@mui/joy/Typography';
import Button from "@mui/joy/Button";
import Box from "@mui/joy/Box";
import Card from '@mui/joy/Card';


// MUI icons
import AnalyticsIcon from "@mui/icons-material/Analytics";
import GroupIcon from "@mui/icons-material/Group";
import GroupsIcon from "@mui/icons-material/Groups";
import CodeIcon from "@mui/icons-material/Code";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import KeyboardDoubleArrowDownRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowDownRounded';


/**
* FeatureCard component
* Card that describes a feature of bozenka.
* Used in homepage, to be simple.
* @param {Object} feature - The feature object containing icon, name, and description.
* @returns {JSX.Element} - The rendered feature card.
*/
function FeatureCard({ feature }){
    /* 
    Card, what describes feature of bozenka
    :)
    */
    const {icon, name, description} = feature 
    return (
        <Card sx={{
            width: 220,
            transition: 'transform 0.3s, box-shadow 0.3s',
            '&:hover': { 
                transform: 'scale(1.05)', 
                boxShadow: 'md',
            }
        }}> 
            <div>
                <Box sx={{mb: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', height: 80}}>
                        {icon}
                </Box>
                
                <Typography level="title-lg" sx={{mb: 1}}>{name}</Typography>
                <Typography level="body-sm" sx={{}}>{description}</Typography>
            </div>
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
            icon: <GroupIcon sx={{fontSize: 50}} />,
            name: "Management",
            description: "Manage all your communities from a single dashboard."
        },
        {
            icon: <AnalyticsIcon sx={{fontSize: 50}}   />,
            name: "Analytics",
            description: "Effortlessly track your community's engagement and growth."
        },
        {
            icon: <AutoAwesomeIcon sx={{fontSize: 50}}   />,
            name: "Automation",
            description: "Automate repetitive tasks and moderation."
        },
        {
            icon: <CodeIcon sx={{fontSize: 50}}   />,
            name: "Open Source",
            description: "Code under GPL-v3 license"
        },
        {
            icon: <GroupsIcon sx={{fontSize: 50}} />,
            name: "Socialization",
            description: "Connect with like-minded individuals to form a community."
        }
    ]


    return (
        <>
            <Box sx={{
                paddingTop: 2,
                paddingBottom: 3,
                backgroundImage: ({ palette }) =>
                    `radial-gradient(circle,  ${palette.background.body}, ${palette.background.level1} 80%, #d8dee9 100%)`,
            }}>
                <Card sx={{
                    borderColor: 'none',
                    m: 2
                }}>
                <Typography level='h1' element="h1" sx={{
                    textAlign: "left",
                    paddingTop: 8,
                    paddingBottom: 0,
                    my: 0,
                    px: 2,
                    
                    
                }}>
                    Manage Your Community Across Platforms
                </Typography>
                <Typography level='body-md' sx={{
                    textAlign: "left",
                    my: 0,
                    paddingTop: 0,
                    fontWeight: 'regular',
                    px: 2
                }}>
                    Streamline your community management on Discord, Telegram, and VK with Bozenka project.
                </Typography>
                <Box sx={{textAlign: 'right'}}>
                    <Link to='/communities/'>
                        <Button variant="soft" size="lg" sx={{
                            justifyContent: "right",
                            p: 1.5,
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
                            }} 
                            endDecorator={<KeyboardDoubleArrowDownRoundedIcon/>}>
                            Get started
                        </Button>
                    </Link>
                </Box>
                </Card>
                <Box sx={{ 
                    display: 'flex', 
                    flexWrap: 'wrap', 
                    gap: 4, 
                    m: 2
                }}>
                    {features.map((feature, index) => (
                        <FeatureCard key={index} feature={feature} />
                    ))}
            </Box>
            </Box>
        </>
    );
}

export default HomePage;