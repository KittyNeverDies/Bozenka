import Card from '@mui/joy/Card';
import Avatar from '@mui/joy/Avatar';
import Divider from '@mui/joy/Divider';
import Grid from '@mui/joy/Grid';
import Typography from '@mui/joy/Typography';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import MenuItem from '@mui/joy/MenuItem';
import Chip from '@mui/joy/Chip';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import ReportIcon from '@mui/icons-material/Report';
import CalendarMonthRoundedIcon from '@mui/icons-material/CalendarMonthRounded';
import PersonIconRounded from '@mui/icons-material/PersonRounded';
import CardOverflow from '@mui/joy/CardOverflow';
import InfoIcon from '@mui/icons-material/Info';
import CardContent from '@mui/joy/CardContent';
import Menu from '@mui/joy/Menu';



function CommunityCard(community) {
    const { icon,
        name,
        small_description,
        id, members_count, creation_date } = community;

    return (
        <Card sx={{ width: '100%', mt: 1 }}>
            <Avatar src="https://images.unsplash.com/photo-1507833423370-a126b89d394b?auto=format&fit=crop&w=90" />
            <Dropdown>
                <MenuButton size='sm' variant='plain' sx={{ position: 'absolute', top: '0.875rem', right: '0.5rem' }}>
                    {icon}
                </MenuButton>
                <Menu size='sm'>
                    <MenuItem color='danger'>
                        <ListItemDecorator sx={{ color: 'inherit' }}>
                            <ReportIcon />
                        </ListItemDecorator>
                        Report
                    </MenuItem>
                    <Divider />
                    <MenuItem>
                        Discord
                        <OpenInNewIcon />
                    </MenuItem>
                    <MenuItem>
                        Telegram
                        <OpenInNewIcon />
                    </MenuItem>
                    <MenuItem>
                        Vkontakte
                        <OpenInNewIcon />
                    </MenuItem>
                </Menu>
            </Dropdown>
            <CardContent>
                <Typography level="title-lg">{name}</Typography>
                <Typography level="body-sm">{small_description}</Typography>
                <Grid>
                    <Chip variant="outlined"
                        startDecorator={<InfoIcon/>}
                        sx={{
                            m: 0.5
                        }}
                    >
                        First Tag
                    </Chip>
                    <Chip variant="outlined"
                        startDecorator={<InfoIcon/>}
                        sx={{
                            m: 0.5
                        }}
                    >
                        Second Tag
                    </Chip>
                    <Chip variant="outlined"
                        startDecorator={<InfoIcon/>}
                        sx={{
                            m: 0.5
                        }}
                    >
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
                        {members_count} members
                    </Typography>
                    <Divider orientation="vertical" />
                    <Typography 
                        startDecorator={<CalendarMonthRoundedIcon/>} level="body-xs" fontWeight="md"  textColor="text.secondary">
                        created on {creation_date}
                    </Typography>
                </CardContent>
            </CardOverflow>
        </Card>
    );
}