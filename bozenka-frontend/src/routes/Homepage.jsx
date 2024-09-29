
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



function FeatureCard({ feature }){
    /* 
    Card, what describes feature of bozenka
    :)
    */
    const {icon, name, description} = feature 
    return (
        <Card sx={{
            width: 200,
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


function HomePage(){
    /*
    Home page of bozenka.
    Should be placed in main :)
    */
    const features = [
        {
            icon: <GroupIcon sx={{fontSize: 50}}/>,
            name: "Unified Management",
            description: "Manage all your communities from a single dashboard and don't care about different social networks."
        },
        {
            icon: <AnalyticsIcon sx={{fontSize: 50}} />,
            name: "Analytics",
            description: "Get insights into your community's engagement and growth without any problems and limits."
        },
        {
            icon: <AutoAwesomeIcon sx={{fontSize: 50}} />,
            name: "Automation",
            description: "Automate repetitive tasks and moderation."
        },
        {
            icon: <CodeIcon sx={{fontSize: 50}} />,
            name: "Open Source & Freedom",
            description: "Help in development, launch for yourself and understand how it works inside. All code is licensed under GPL-V3."
        },
        {
            icon: <GroupsIcon sx={{fontSize: 50}} />,
            name: "Socialization",
            description: "Connect with like-minded people and find a community that shares your interests."
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
                        border: '1px',
                    }}>
                        Get started
                    </Button>
                </Box>
            </Box>
            <Box sx={{
                backgroundColor: 'background.level1',
                pb: 5,
                borderRadius: 'lg',
                ml: 1,
                mr: 1,
            }}>
            <Typography level='h1' sx={{
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
            {/* Main introduction page */}
            <Box sx={{
                paddingTop: 18,
                height: 500,

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
                    <Button variant="soft" size="lg" sx={{
                        justifyContent: "center",
                        p: 2
                    }}>
                        Check out telegram channel
                    </Button>
                </Box>
            </Box>
        </>
    );
}

export default HomePage;