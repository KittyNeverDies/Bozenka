import { Box, Container, Typography, Link, Grid } from '@mui/joy';

import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";

const Footer = () => {
  return (
    <Box sx={{ py: 4, backgroundColor: 'neutral.outlined' }}>
      <Container maxWidth="lg">
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Typography level="h4" sx={{ mb: 2 }}>
              Project source code
            </Typography>
            <Typography variant="body2" sx={{ mb: 2 }}>
                See source code of bozenka & help us in development.
            </Typography>
            <Link href="https://github.com/kittyneverdies/bozenka/" underline="none" sx={{ color: 'text.primary' }}>
               Check out
              <KeyboardArrowRight/>
            </Link>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography level="h4" sx={{ mb: 2 }}>
              Support
            </Typography>
            <Typography variant="body2" sx={{ mb: 2 }}>
              Get help with our community managment tool or bot from Vk, Discord or Telegram.
            </Typography>
            <Link href="/support" underline="none" sx={{ color: 'text.primary' }}>
              Contact us
              <KeyboardArrowRight/>
            </Link>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography level="h4" sx={{ mb: 2 }}>
              Privacy policy & User agrement
            </Typography>
            <Typography variant="body2" sx={{ mb: 2 }}>
              Community management guides and tutorials
            </Typography>
            <Link href="/resources" underline="none" sx={{ color: 'text.primary' }}>
              Explore
              <KeyboardArrowRight/>
            </Link>
          </Grid>
        </Grid>
        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
          <Typography variant="body2" sx={{ color: 'text.secondary' }}>
            &copy; 2024-2025 kittyneverdies. All rights reserved.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Link href="https://github.com/communitytool/communitytool" underline="none" sx={{ color: 'text.primary' }}>
              <i className="fa-brands fa-github" />
            </Link>
            <Link href="https://twitter.com/communitytool" underline="none" sx={{ color: 'text.primary' }}>
              <i className="fa-brands fa-twitter" />
            </Link>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;