import { Link } from 'react-router-dom';

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
import { Breadcrumbs } from '@mui/joy';
import Stack from '@mui/joy/Stack';
import AccordionSummary from '@mui/joy/AccordionSummary';
import ListItemContent from '@mui/joy/ListItemContent';
import Checkbox from '@mui/joy/Checkbox';
import List from '@mui/joy/List';
import ListItem from '@mui/joy/ListItem';
import CircularProgress from '@mui/joy/CircularProgress';

// Material UI icons
import InfoIcon from '@mui/icons-material/Info';
import CancelIcon from '@mui/icons-material/Cancel';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import LocalOfferRoundedIcon from '@mui/icons-material/LocalOfferRounded';
import ListRoundedIcon from '@mui/icons-material/ListRounded';
import PeopleRoundedIcon from '@mui/icons-material/PeopleRounded';

// Our component
import RangeSlider from './RandeSlider';
import SelectableTags from './SelectableTags';

/**
 * @description A functional component that renders range sliders for filters card
 * @returns {JSX.Element}
 */
function RangeSliders() {
    return (
        <>
            <Box sx={{ width: 250, marginTop: 2 }}>
                <Typography gutterBottom>
                    Community members count range
                </Typography>
                <RangeSlider
                    label="Community members count range"
                    textOfValue="members"
                    maxValue="100"
                    minValue="0"
                />
            </Box>

            <Box sx={{ width: 250 }}>
                <Typography gutterBottom>
                    Community growth range
                </Typography>
                <RangeSlider
                    label="Community members count range"
                    textOfValue="Members"
                    maxValue="100"
                    minValue="0"
                />
            </Box>
        </>
    );
}


/**
 * @description A functional component that renders a card with filters to filter communities
 * @param {Object} props - Component props
 * @param {Array} props.availableTags - Array of available tags
 * @param {Array} props.selectedTags - Array of selected tags
 * @param {Function} props.onTagSelect - Callback when a tag is selected/deselected
 * @param {Function} props.onClearAll - Callback to clear all filters
 * @returns {JSX.Element}
 */
function FiltersCard({ availableTags = [], selectedTags = [], onTagSelect, onClearAll }) {
    const hasActiveFilters = selectedTags.length > 0;

    return (
        <Stack sx={{
            flexDirection: 'column',
            '@media (max-width: 720px)': {
                width: '120%',
                position: 'relative',
                left: 'unset',
            },
            mr: 1,
        }}>
            <Breadcrumbs size="sm" separator={<KeyboardArrowRightIcon />}>
                <Link to="/" style={{ color: 'var(--joy-palette-text-tertiary)' }}>
                    <Typography sx={{ mt: 0 }}>Home</Typography>
                </Link>
                <Typography sx={{ mt: 0, color: 'primary.plainColor' }}>Communities</Typography>
            </Breadcrumbs>

            <Card variant="outlined" sx={{
                width: 300,
                mr: 3,
                top: 16,
                maxHeight: 'calc(100vh - 32px)',
                overflowY: 'auto',
                marginBottom: '25px',
                '@media (max-width: 720px)': {
                    width: '95%',
                    position: 'relative',
                    left: 'unset',
                },
            }}>
                <Typography level="h4" sx={{
                    paddingTop: 2,
                    paddingLeft: 2,
                    paddingRight: 2,
                }}>
                    Filters
                </Typography>

                {hasActiveFilters && (
                    <Button
                        variant="soft"
                        size="sm"
                        startDecorator={<CancelIcon />}
                        onClick={onClearAll}
                        sx={{
                            width: 150,
                            marginLeft: 1,
                            marginBottom: 1,
                            transition: 'transform 0.2s ease',
                            '&:hover': {
                                transform: 'scale(1.05)',
                                bgcolor: 'primary.lightBg',
                            },
                        }}
                    >
                        Clear Filters
                    </Button>
                )}

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
                        },
                    }}
                    variant="plain"
                >
                    {/* Tags Filter */}
                    <Accordion defaultExpanded>
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
                            <Box sx={{
                                maxHeight: 200,
                                overflowY: 'auto',
                                p: 1,
                                display: 'flex',
                                flexWrap: 'wrap',
                                gap: 0.5,
                            }}>
                                {availableTags.length === 0 ? (
                                    <Box sx={{ display: 'flex', alignItems: 'center', p: 1 }}>
                                        <CircularProgress size="sm" />
                                        <Typography level="body-sm" sx={{ ml: 1 }}>
                                            Loading tags...
                                        </Typography>
                                    </Box>
                                ) : (
                                    availableTags.map((tag) => (
                                        <SelectableTags
                                            key={tag.id}
                                            Tag={{
                                                icon: tag.icon,
                                                name: tag.name
                                            }}
                                            isSelected={selectedTags.some(t => t.id === tag.id)}
                                            onSelect={() => onTagSelect(tag)}
                                        />
                                    ))
                                )}
                            </Box>
                        </AccordionDetails>
                    </Accordion>

                    {/* Members Filter */}
                    <Accordion>
                        <AccordionSummary>
                            <Avatar color="primary">
                                <PeopleRoundedIcon />
                            </Avatar>
                            <ListItemContent>
                                <Typography level="title-md">Members</Typography>
                                <Typography level="body-sm">Filter by member count & growth</Typography>
                            </ListItemContent>
                        </AccordionSummary>
                        <AccordionDetails>
                            <RangeSliders />
                        </AccordionDetails>
                    </Accordion>

                    {/* List Options */}
                    <Accordion>
                        <AccordionSummary>
                            <Avatar color="primary">
                                <ListRoundedIcon />
                            </Avatar>
                            <ListItemContent>
                                <Typography level="title-md">Count per page</Typography>
                                <Typography level="body-sm">How many communities to show per page</Typography>
                            </ListItemContent>
                        </AccordionSummary>
                        <AccordionDetails>
                            <RadioGroup defaultValue="5">
                                <Grid>
                                    {[20, 15, 10, 5].map((value) => (
                                        <Radio
                                            key={value}
                                            value={value.toString()}
                                            variant="outlined"
                                            size="sm"
                                            sx={{ m: 0.5 }}
                                            label={`${value} per Page`}
                                        />
                                    ))}
                                </Grid>
                            </RadioGroup>
                        </AccordionDetails>
                    </Accordion>
                </AccordionGroup>
            </Card>
        </Stack>
    );
}

export default FiltersCard;