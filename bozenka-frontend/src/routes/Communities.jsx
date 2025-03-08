// React stuff
import { useState } from 'react';


import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';
import Card from '@mui/joy/Card';
import Typography from '@mui/joy/Typography';
import Box from '@mui/joy/Box';
import { Breadcrumbs } from '@mui/joy';
import Grid from '@mui/joy/Grid';

// Material UI icons
import InfoIcon from '@mui/icons-material/Info';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import SearchIcon from '@mui/icons-material/Search';
import CancelIcon from '@mui/icons-material/Cancel';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import SchoolIcon from '@mui/icons-material/School';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';
import CodeIcon from '@mui/icons-material/Code';
import BrushIcon from '@mui/icons-material/Brush';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import LocalFloristIcon from '@mui/icons-material/LocalFlorist';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import MenuBookIcon from '@mui/icons-material/MenuBook';

// Own elements.
import FiltersCard from '../components/FiltersCard';
import CommunityCard from '../components/CommunityCard';



// Mock data of communites list
const massive = [
  {
    avatarSrc: "https://images.unsplash.com/photo-1603415526960-f7e0328c63b1?auto=format&fit=crop&w=90",
    menuItems: [
      { icon: <OpenInNewIcon />, label: 'Discord' },
      { icon: <OpenInNewIcon />, label: 'Telegram' },
    ],
    title: "React Developers Hub",
    description: "A vibrant community for developers passionate about React.js and its ecosystem. Share projects, ask questions, and collaborate!",
    tags: [{ icon: <CodeIcon />, name: "React" }, { icon: <SchoolIcon />, name: "Learning" }, { icon: <InfoIcon />, name: "Frontend" }],
    membersCount: '5.2k',
    creationDate: '12th March, 2021'
  },
  {
    avatarSrc: "https://images.unsplash.com/photo-1552374196-c4e7ffc6e126?auto=format&fit=crop&w=90",
    menuItems: [
      { icon: <OpenInNewIcon />, label: 'Telegram' },
      { icon: <OpenInNewIcon />, label: 'Discord' },
    ],
    title: "Indie Game Devs Unite",
    description: "Connect with fellow independent game developers. Discuss game design, programming, art, and marketing strategies.",
    tags: [{ icon: <SportsEsportsIcon />, name: "Gaming" }, { icon: <CodeIcon />, name: "Development" }, { icon: <BrushIcon />, name: "Art" }],
    membersCount: '980',
    creationDate: '2nd August, 2020'
  },
  {
    avatarSrc: "https://images.unsplash.com/photo-1544725176-7c40e5a71c5e?auto=format&fit=crop&w=90",
    menuItems: [
      { icon: <OpenInNewIcon />, label: 'Discord' },
      { icon: <OpenInNewIcon />, label: 'Telegram' },
    ],
    title: "Digital Artists Collective",
    description: "A space for digital artists of all levels to share their work, get feedback, and find inspiration. From illustration to 3D modeling!",
    tags: [{ icon: <BrushIcon />, name: "Art" }, { icon: <CameraAltIcon />, name: "Design" }, { icon: <InfoIcon />, name: "Digital" }],
    membersCount: '2.7k',
    creationDate: '20th May, 2022'
  },
  {
    avatarSrc: "https://images.unsplash.com/photo-1547425260-76bcadfb4f2c?auto=format&fit=crop&w=90",
    menuItems: [
      { icon: <OpenInNewIcon />, label: 'Discord' },
      { icon: <OpenInNewIcon />, label: 'Vkontakte' },
    ],
    title: "Urban Photography Explorers",
    description: "For photographers who love capturing the beauty and grit of urban environments. Share your shots, tips, and favorite locations.",
    tags: [{ icon: <CameraAltIcon />, name: "Photography" }, { icon: <InfoIcon />, name: "Urban" }, { icon: <InfoIcon />, name: "Travel" }],
    membersCount: '1.3k',
    creationDate: '5th November, 2019'
  },
  {
    avatarSrc: "https://images.unsplash.com/photo-1589571894960-20bbe2828d0a?auto=format&fit=crop&w=90",
    menuItems: [
      { icon: <OpenInNewIcon />, label: 'Telegram' },
      { icon: <OpenInNewIcon />, label: 'Discord' }
    ],
    title: "Python Programming Enthusiasts",
    description: "Discuss all things Python! From beginner questions to advanced topics, data science, web development with Django/Flask, and more.",
    tags: [ { icon: <CodeIcon />, name: "Python" }, { icon: <InfoIcon />, name: "Programming" }, { icon: <SchoolIcon />, name: "Data Science" }],
    membersCount: '7.1k',
    creationDate: '18th June, 2018'
  },
  {
    avatarSrc: "https://images.unsplash.com/photo-1628890923662-2cb23c61693a?auto=format&fit=crop&w=90",
    menuItems: [
      { icon: <OpenInNewIcon />, label: 'Discord' },
      { icon: <OpenInNewIcon />, label: 'Facebook' },
    ],
    title: "Gardening & Plant Lovers",
    description: "A community for those who love gardening, houseplants, and everything green! Share your plant progress, ask for advice, and swap seeds.",
    tags: [{ icon: <LocalFloristIcon />, name: "Gardening" }, { icon: <InfoIcon />, name: "Plants" }, { icon: <InfoIcon />, name: "Nature" }],
    membersCount: '3.4k',
    creationDate: '1st April, 2023'
  },
    {
    avatarSrc: "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=90",
    menuItems: [
      { icon: <OpenInNewIcon />, label: 'Telegram' },
      { icon: <OpenInNewIcon />, label: 'Discord' },
    ],
    title: "Fitness & Wellness Journey",
    description: "Motivate and support each other on our fitness and wellness journeys. Share workout routines, healthy recipes, and progress updates.",
    tags: [{ icon: <FitnessCenterIcon />, name: "Fitness" }, { icon: <InfoIcon />, name: "Wellness" }, { icon: <InfoIcon />, name: "Health" }],
    membersCount: '6.8k',
    creationDate: '29th July, 2021'
  },
    {
    avatarSrc: "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?auto=format&fit=crop&w=90",
    menuItems: [
        { icon: <OpenInNewIcon />, label: 'Discord' },
        { icon: <OpenInNewIcon />, label: 'Vkontakte' },
    ],
    title: "Bookworms & Literature Fans",
    description: "Discuss your favorite books, authors, and literary genres. Share recommendations, reviews, and engage in thoughtful conversations.",
    tags: [{ icon: <MenuBookIcon />, name: "Books" }, { icon: <InfoIcon />, name: "Literature" }, { icon: <SchoolIcon />, name: "Reading" }],
    membersCount: '4.5k',
    creationDate: '10th October, 2020'
  }
];

/**
* @description A community search page
* @type {JSX.Element}
*/
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
                                <Button variant='soft' 
                                    sx={{borderRadius: 'sm', 
                                        px: 2, py: 0.5,
                                        border: '1px solid',
                                        borderColor: 'primary.200',
                                        transition: 'background-color 0.2s'
                                    }} 
                                    startDecorator={<CancelIcon />} onClick={handleClear}>
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
                <div 
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                    gap: '16px',
                    padding: '16px',
                    width: '95%',
                    justifyContent: 'center'}}>
                        {/* Community cards go here */}
                        {
                            massive.map((community, index) => (
                                <CommunityCard
                                    avatarSrc={community.avatarSrc}
                                    menuItems={community.menuItems}
                                    title={community.title}
                                    description={community.description}
                                    tags={community.tags}
                                    membersCount={community.membersCount}
                                    creationDate={community.creationDate}
                                />
                            ))

                            
                        }
                    </div>
                </Box>
            </Box>
        </Box>
        </>
    );
}

export default CommunitiesSearch;