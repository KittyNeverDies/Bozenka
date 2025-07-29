
// React stuff
import { useState, useEffect, useCallback, useMemo } from 'react';
import debounce from 'lodash/debounce';

// Mui Joy stuff
import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';
import Card from '@mui/joy/Card';
import Typography from '@mui/joy/Typography';
import Box from '@mui/joy/Box';
import {Breadcrumbs, Snackbar} from '@mui/joy';
import Grid from '@mui/joy/Grid';
import CircularProgress from '@mui/joy/CircularProgress';
import Icon from '@mui/material/Icon';

// Material UI icons
import InfoIcon from '@mui/icons-material/Info';
import ErrorOutlinedIcon from '@mui/icons-material/ErrorOutlined';
import SearchIcon from '@mui/icons-material/Search';
import CancelIcon from '@mui/icons-material/Cancel';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';



// Own elements.
import FiltersCard from 'src/components/FiltersCard';
import CommunityCard from 'src/components/CommunityCard';

// Api
import BaseClientAPI from 'src/api/BaseClientAPI.js';

/**
* @description A community search page
* @type {JSX.Element}
*/
function CommunitiesSearch() {
    const [communities, setCommunities] = useState([]);
    const [filteredCommunities, setFilteredCommunities] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [isFocused, setIsFocused] = useState(false);
    const [availableTags, setAvailableTags] = useState([]);
    const [selectedTags, setSelectedTags] = useState([]);

    const [snackbar, setSnackbar] = useState({
        open: false,
        message: ''
    });



    // Fetch tags and communities on mount
    useEffect(() => {
        const fetchData = async () => {
            const api = new BaseClientAPI();
            try {
                // Fetch both tags and communities in parallel
                const [tagsResponse, communitiesResponse] = await Promise.all([
                    api.getTags(),
                    api.getCommunities()
                ]);

                if (tagsResponse?.error || communitiesResponse?.error) {
                    throw new Error(tagsResponse?.error || communitiesResponse?.error);
                }

                setAvailableTags(tagsResponse);
                setCommunities(communitiesResponse);
                setFilteredCommunities(communitiesResponse);
            } catch (error) {
                console.error('Failed to fetch data:', error);
                setSnackbar({
                    open: true,
                    message: `Failed to load communities. Please try again later. ${error.message}`
                });

            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);


    const handleSnackbarClose = () => {
        setSnackbar({
            ...snackbar,
            open: false
        });
    };


    // Handle tag selection
    const handleTagSelect = useCallback((tag) => {
        setSelectedTags(prev => {
            const isSelected = prev.some(t => t.id === tag.id);
            if (isSelected) {
                return prev.filter(t => t.id !== tag.id);
            } else {
                return [...prev, tag];
            }
        });
    }, []);

    // Memoized search function that includes tag filtering
    const searchCommunities = useCallback((searchTerm, communities, selectedTags) => {
        let filtered = communities;

        // First filter by selected tags if any
        if (selectedTags.length > 0) {
            filtered = communities.filter(community =>
                selectedTags.every(selectedTag =>
                    community.tags.some(tag => tag.id === selectedTag.id)
                )
            );
        }

        // Then filter by search term if any
        if (searchTerm.trim()) {
            const searchTermLower = searchTerm.toLowerCase().trim();
            filtered = filtered.filter(community => {
                const titleMatch = (community.name || "").toLowerCase().includes(searchTermLower);
                const descriptionMatch = (community.short_description || "").toLowerCase().includes(searchTermLower);
                const tagsMatch = community.tags?.some(tag =>
                    (tag.name || "").toLowerCase().includes(searchTermLower)
                ) || false;

                return titleMatch || descriptionMatch || tagsMatch;
            });
        }

        return filtered;
    }, []);

    // Debounced search effect
    const debouncedSearch = useMemo(
        () => debounce((searchTerm, communities, selectedTags) => {
            const filtered = searchCommunities(searchTerm, communities, selectedTags);
            setFilteredCommunities(filtered);
        }, 300),
        [searchCommunities]
    );

    // Effect to trigger search on term or selected tags change
    useEffect(() => {
        if (!communities.length) return;
        debouncedSearch(searchTerm, communities, selectedTags);
    }, [searchTerm, communities, selectedTags, debouncedSearch]);

    // Cleanup debounce on unmount
    useEffect(() => {
        return () => {
            debouncedSearch.cancel();
        };
    }, [debouncedSearch]);

    // Handle clearing all filters
    const handleClearAll = useCallback(() => {
        setSearchTerm('');
        setSelectedTags([]);
        setFilteredCommunities(communities);
    }, [communities]);

    return (
        <>
            <Box sx={{ p: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'flex-start', flexWrap: 'wrap' }}>
                    <FiltersCard
                        availableTags={availableTags}
                        selectedTags={selectedTags}
                        onTagSelect={handleTagSelect}
                        onClearAll={handleClearAll}
                    />
                    <Box sx={{ flex: 1 }}>
                        <Input
                            placeholder='Search for communities...'
                            startDecorator={<SearchIcon />}
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            onFocus={() => setIsFocused(true)}
                            onBlur={() => setIsFocused(false)}
                            sx={{
                                '--Input-focusedThickness': '1px',
                                bgcolor: 'background.surface',
                                borderRadius: 'lg',
                                '&:hover': {
                                    bgcolor: 'background.level1',
                                },
                                '&:focus-within': {
                                    bgcolor: 'background.level1',
                                },
                                mt: 1,
                                mb: 1,
                                py: 1.5,
                                px: 2,
                            }}
                            endDecorator={
                                (searchTerm || selectedTags.length > 0) && (
                                    <Button
                                        variant='soft'
                                        sx={{
                                            borderRadius: 'sm',
                                            px: 2,
                                            py: 0.5,
                                        }}
                                        startDecorator={<CancelIcon />}
                                        onClick={handleClearAll}
                                    >
                                        Clear All
                                    </Button>
                                )
                            }
                        />

                        {/* Selected Tags Display */}
                        {selectedTags.length > 0 && (
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                                {selectedTags.map(tag => (
                                    <Button
                                        key={tag.id}
                                        size="sm"
                                        variant="soft"
                                        color="primary"
                                        endDecorator={<CancelIcon />}
                                        onClick={() => handleTagSelect(tag)}
                                        sx={{ borderRadius: 'xl' }}
                                    >
                                        {tag.name}
                                    </Button>
                                ))}
                            </Box>
                        )}

                        {/* Search tip card */}
                        {isFocused && !searchTerm && selectedTags.length === 0 && (
                            <Card variant="outlined" sx={{ mt: 1, animation: 'sizeIn 0.3s' }}>
                                <Box sx={{ display: 'flex', alignItems: 'center', p: 2 }}>
                                    <InfoIcon sx={{ mr: 1 }} />
                                    <Box>
                                        <Typography level="title-lg">Search tip</Typography>
                                        <Typography level="body-sm">
                                            Use tags or enter keywords to find specific communities
                                        </Typography>
                                    </Box>
                                </Box>
                            </Card>
                        )}

                        {/* Communities grid */}
                        <div
                            style={{
                                display: 'grid',
                                gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                                gap: '16px',
                                padding: '16px',
                                width: '95%',
                                justifyContent: 'center'
                            }}
                        >
                            {loading ? (
                                <Typography>Loading...</Typography>
                            ) : filteredCommunities.length === 0 ? (
                                <Typography level="body-lg" sx={{ textAlign: 'center', gridColumn: '1/-1' }}>
                                    No communities found matching your criteria
                                </Typography>
                            ) : (
                                filteredCommunities.map((community) => (
                                    <CommunityCard
                                        key={community.id}
                                        id={community.id}
                                        avatarSrc={`${import.meta.env.REACT_APP_API_URL || 'http://localhost:8000'}${community.icon}`}
                                        menuItems={[
                                            { icon: <OpenInNewIcon />, label: 'Discord' },
                                            { icon: <OpenInNewIcon />, label: 'Telegram' },
                                            { icon: <OpenInNewIcon />, label: 'Vkontakte' },
                                        ]}
                                        title={community.name}
                                        description={community.short_description}
                                        tags={community.tags.map(tag => ({ icon: tag.icon, name: tag.name }))}
                                        membersCount={community.members_count}
                                        creationDate={new Date(community.creation_date).toLocaleDateString()}
                                    />
                                ))
                            )}
                        </div>
                    </Box>
                </Box>
                <Snackbar
                    variant="solid"
                    color="danger"
                    open={snackbar.open}
                    onClose={handleSnackbarClose}
                    anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
                    startDecorator={<ErrorOutlinedIcon />}
                    autoHideDuration={6000}
                >
                    {snackbar.message}
                </Snackbar>

            </Box>
        </>
    );
}

export default CommunitiesSearch;