
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




function CommunityCard() {

    return (
        <Card sx={{m: 1 }}>
            <Avatar 
                src="https://images.unsplash.com/photo-1507833423370-a126b89d394b?auto=format&fit=crop&w=90" 
            />
            <Dropdown>
                <MenuButton size='sm' variant='plain'
                sx={{ position: 'absolute', top: '0.875rem', right: '0.5rem' }}>
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
                    <MenuItem sx={{
                        transition: 'background-color 0.3s'
                    }}>
                        Discord
                        <OpenInNewIcon />
                    </MenuItem>
                    <MenuItem sx={{
                        transition: 'background-color 0.3s'
                    }}>
                        Telegram
                        <OpenInNewIcon />
                    </MenuItem>
                    <MenuItem sx={{
                        transition: 'background-color 0.3s'
                    }}>
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
                            m: 0.5,
                            borderRadius: 'sm'
                        }}>
                        First Tag
                    </Chip>
                    <Chip variant="outlined"
                        startDecorator={<InfoIcon/>}
                        sx={{
                            m: 0.5,
                            borderRadius: 'sm'
                        }}>
                        Second Tag
                    </Chip>
                    <Chip variant="outlined"
                        startDecorator={<InfoIcon/>}
                        sx={{
                            m: 0.5,
                            borderRadius: 'sm'
                        }}>
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

export default CommunityCard;

