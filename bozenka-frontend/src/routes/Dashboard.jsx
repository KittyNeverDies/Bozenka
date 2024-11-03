import Card from '@mui/joy/Card';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import Stack from '@mui/joy/Stack';
import Avatar from '@mui/joy/Avatar';
import Grid from '@mui/joy/Grid';
import Button from '@mui/joy/Button';
import Link from '@mui/joy/Link';
import Divider from '@mui/joy/Divider';

import SearchIcon from '@mui/icons-material/SearchRounded';
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import HandymanRoundedIcon from '@mui/icons-material/HandymanRounded';
import TrendingUpRoundedIcon from '@mui/icons-material/TrendingUpRounded';

// Define a reusable HomePageButton component
function HomePageButton({ head, description, icon }) {
  return (
    <Card sx={{
      width: 200,
      transition: 'transform 0.3s, box-shadow 0.3s, background-color 0.3s',
      '&:hover': { 
          transform: 'scale(1.05)', 
          boxShadow: 'md',
      }
    }}>
      <Avatar color="primary">{icon}</Avatar>
      <Typography level="title-lg" sx={{ marginBottom: 0 }} element="h1">
        {head}
      </Typography>
      <Typography level="body-xs" sx={{ marginTop: -1.2 }}>
        {description}
      </Typography>
    </Card>
  );
}

// Define the DashboardHomepage component
export function DashboardHomepage() {
  // Define the buttons data
  const buttons = [
    {
      head: 'Search for communities',
      description: 'Find your social home or place for ads. Here is freedom of choice.',
      icon: <SearchIcon />,
    },
    {
      head: 'Add or create your community',
      description: 'Create or import your own social home or club by interests.',
      icon: <AddRoundedIcon />,
    },
    {
      head: 'Manage your communities',
      description: 'Manage your communities, add administrators, create posts, etc.',
      icon: <HandymanRoundedIcon />
    },
    {
      head: 'Manage your account',
       description: 'Manage your security, privacy of your account. Change avatar or name.',

    }
  ];

  return (
    <Stack m={2} sx={{ alignItems: 'center', display: 'flex', justifyContent: 'center', width: 'auto', mb: 10 }}>
      {/* Welcome card */}
      <Card sx={{ width: 'auto', size: 'lg',  py: 5, px: 10, backgroundColor: 'transparent', borderColor: 'transparent', }}>
        <Stack sx={{ alignItems: 'center', display: 'flex',  justifyContent: 'center' }}>
          <Avatar
            src="https://images.unsplash.com/photo-1507833423370-a126b89d394b?auto=format&fit=crop&w=90"
            size="lg"
          />
          <Typography level="h3" mt={1} element="h1">
            Welcome, user.
          </Typography>

          <Typography color='neutral' level="body-xl">
            Total growth: <Typography color="success" level="body-xl" startDecorator={<TrendingUpRoundedIcon/>}> 50% from last day </Typography>
          </Typography>
          
          <Typography level="body-sm">Have a nice day!</Typography>
        </Stack>
      </Card>

      {/* Buttons grid */}
      <Grid container spacing={1} mt={1} sx={{ display: 'flex', justifyContent: 'center' }}>
        {buttons.map((button, index) => (
          <Grid key={index}>
            <HomePageButton {...button} />
          </Grid>
        ))}
      </Grid>


    </Stack>
  );
}

export function DashboardAddCommunity() {
  return (
    <Stack m={2} sx={{ alignItems: 'center', display: 'flex', justifyContent: 'center', width: 'auto' }}>
      <Card variant="soft" sx={{ width: 'auto' }}>
        <Typography level="h3" mt={1} element="h1">
          Add your community
        </Typography>
        <Divider sx={{ my: 2 }} />
        {/* Add community form here */}
      </Card>
    </Stack>
  );
}

export function DashboardEditCommunity() {
  return (
    <Stack m={2} sx={{}}>
      <Card sx={{ width: 'auto' }}>
        <Typography level="h3" mt={1} element="h1">
          Edit your community
        </Typography>
        <Divider sx={{ my: 2 }} />
        {/* Edit community form here */}
      </Card>
    </Stack>
  );
}