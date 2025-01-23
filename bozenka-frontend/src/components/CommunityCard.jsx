
import {Link} from 'react-router-dom';


// MUI Joy UI elements
import Card from '@mui/joy/Card';
import Avatar from '@mui/joy/Avatar';
import Divider from '@mui/joy/Divider';
import Grid from '@mui/joy/Grid';
import Typography from '@mui/joy/Typography';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import MenuItem from '@mui/joy/MenuItem';
import Chip from '@mui/joy/Chip';
import CardContent from '@mui/joy/CardContent';
import MenuButton from '@mui/joy/MenuButton';
import Menu from '@mui/joy/Menu';
import Dropdown from '@mui/joy/Dropdown';


// MUI material you icons
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import ReportIcon from '@mui/icons-material/Report';
import CalendarMonthRoundedIcon from '@mui/icons-material/CalendarMonthRounded';
import PersonIconRounded from '@mui/icons-material/PersonRounded';
import CardOverflow from '@mui/joy/CardOverflow';
import InfoIcon from '@mui/icons-material/Info';


/**
* CommunityCard component, used in community search page.
* Have inside a Card component with Avatar, description, memebers count,
* date of creation & other responsive community infromation.
* @param {Object} props - The props object.
* @param {string} props.avatarSrc - The source URL of the avatar image.
* @param {Array} props.menuItems - An array of menu items, each item is an object with color, icon, and label properties.
* @param {string} props.title - The title of the community.
* @param {string} props.description - The description of the community.
* @param {Array} props.tags - An array of tags associated with the community.
* @param {number} props.membersCount - The number of members in the community.
* @param {string} props.creationDate - The creation date of the community.
* @returns {JSX.Element} - The rendered community card.
*/
function CommunityCard({ avatarSrc, menuItems, title, description, tags, membersCount, creationDate }) {
    return (
    <Link to='/community/'>
        <Card sx={{m: 1,

            transition: 'transform 0.3s, box-shadow 0.3s',
            '&:hover': { 
                transform: 'scale(1.05)', 
                boxShadow: 'md',
            }
        }}>
            <Avatar src={avatarSrc} />
            <Dropdown>
                <MenuButton size='sm' variant='plain' sx={{ position: 'absolute', top: '0.875rem', right: '0.5rem' }}onClick={(event) => event.preventDefault() }>
                    <MoreVertIcon />
                </MenuButton>
                <Menu size='sm'>
                    <MenuItem color='danger' sx={{
                        transition: 'background-color 0.3s'
                    }}>
                        <ListItemDecorator sx={{ color: 'inherit' }}>
                            <ReportIcon />
                        </ListItemDecorator>
                        Report
                    </MenuItem>
                    <Divider />
                    {menuItems.map((item, index) => (
                        <MenuItem key={index} color={item.color} sx={{ transition: 'background-color 0.3s' }}>
                            <ListItemDecorator sx={{ color: 'inherit' }}>
                                {item.icon}
                            </ListItemDecorator>
                            {item.label}
                        </MenuItem>
                    ))}
                </Menu>
            </Dropdown>
            <CardContent>
                <Typography level="title-lg">{title}</Typography>
                <Typography level="body-sm">{description}</Typography>
                <Grid>
                    {tags.map((tag, index) => (
                        <Chip key={index} variant="outlined" startDecorator={tag.icon} sx={{ m: 0.5, borderRadius: 'sm' }}>
                            {tag.name}
                        </Chip>
                    ))}
                </Grid>
            </CardContent>
            <CardOverflow>
                <Divider inset="context" />
                <CardContent orientation="horizontal">
                    <Typography startDecorator={<PersonIconRounded />} level="body-xs" fontWeight="md" textColor="text.secondary">
                        {membersCount} members
                    </Typography>
                    <Divider orientation="vertical" />
                    <Typography startDecorator={<CalendarMonthRoundedIcon />} level="body-xs" fontWeight="md" textColor="text.secondary">
                        created on {creationDate}
                    </Typography>
                </CardContent>
            </CardOverflow>
        </Card>
    </Link>
    );
}

export default CommunityCard;

