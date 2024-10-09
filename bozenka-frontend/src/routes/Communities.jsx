// React stuff
import { useState } from 'react';


import SearchIcon from '@mui/icons-material/Search';
import CancelIcon from '@mui/icons-material/Cancel';

import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';
import Card from '@mui/joy/Card';
import Typography from '@mui/joy/Typography';
import Box from '@mui/joy/Box';

// Material UI icons
import InfoIcon from '@mui/icons-material/Info';

// Own elements.
import FiltersCard from '../components/FiltersCard';
import CommunityCard from '../components/CommunityCard';


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