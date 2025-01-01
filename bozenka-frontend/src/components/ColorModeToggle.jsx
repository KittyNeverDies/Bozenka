import { useColorScheme } from "@mui/joy";
import IconButton from "@mui/joy/IconButton";


import LightModeRoundedIcon from '@mui/icons-material/LightModeRounded';
import DarkModeRoundedIcon from '@mui/icons-material/DarkModeRounded';



export default function ColorModeToggle() {
    const { mode, setMode } = useColorScheme();
    return (
      <IconButton
        variant="soft"
        onClick={() => setMode(mode === 'dark' ? 'light' : 'dark')}
        sx={{
          minWidth: 40,
          minHeight: 40,
          borderRadius: '50%',
        }}
      >
        {mode === 'dark' ? <LightModeRoundedIcon /> : <DarkModeRoundedIcon />}
      </IconButton>
    );
  }