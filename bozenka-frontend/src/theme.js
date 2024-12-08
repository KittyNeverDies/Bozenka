// theme.js
import { extendTheme } from '@mui/joy/styles';

const softTheme = extendTheme({
  typography: {
    fontFamily: 'Inter, Arial, sans-serif',
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      md: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      xl2: '1.5rem',
      xl3: '1.875rem',
      xl4: '2.25rem',
      xl5: '3rem',
      xl6: '3.75rem',
    },
    fontWeight: {
      xs: 300,
      sm: 400,
      md: 500,
      lg: 600,
      xl: 700,
    },
    lineHeight: {
      sm: 1.4,
      md: 1.6,
      lg: 1.8,
    },
    letterSpacing: {
      sm: '0.02em',
      md: '0.04em',
      lg: '0.06em',
    },
  },
  radius: {
    xs: '4px',
    sm: '8px',
    md: '12px',
    lg: '16px',
    xl: '24px',
  },
  shadow: {
    xs: '0px 1px 2px rgba(0, 0, 0, 0.05)',
    sm: '0px 2px 4px rgba(0, 0, 0, 0.1)',
    md: '0px 4px 6px rgba(0, 0, 0, 0.1)',
    lg: '0px 8px 12px rgba(0, 0, 0, 0.15)',
    xl: '0px 12px 16px rgba(0, 0, 0, 0.2)',
  },
  components: {
    JoyButton: {
      styleOverrides: {
        root: ({ ownerState, theme }) => ({
          borderRadius: theme.radius.md,
          textTransform: 'none',
          transition: 'all 0.3s ease-in',
          ...(ownerState.color === 'primary' && {
            ...(ownerState.variant === 'soft' && {
              backgroundColor: theme.palette[ownerState.color].softBg,
              color: theme.palette[ownerState.color].plainColor,
              '&:hover': {
                backgroundColor: theme.palette[ownerState.color].softHoverBg,
              },
              '&:active': {
                backgroundColor: theme.palette[ownerState.color].softActiveBg,
              },
            }),
          }),
        }),
        sizeMd: ({ theme }) => ({
          padding: `${theme.spacing(1)} ${theme.spacing(2)}`, // Using spacing for padding
        }),
        sizeLg: ({ theme }) => ({
          padding: `${theme.spacing(1.5)} ${theme.spacing(2.5)}`, // Using spacing for padding
        }),
      },
    },
    JoyCard: {
      styleOverrides: {
        root: ({ theme }) => ({
          borderRadius: theme.radius.lg,
          boxShadow: theme.shadow.xs,
          transition: 'all 0.2s ease-in-out',
          backgroundColor: 'background.surface',
        }),
      },
    },
    JoyInput: {
      styleOverrides: {
        root: ({ theme, ownerState }) => ({
          borderRadius: theme.radius.sm,
          border: `1px solid ${theme.palette.neutral.outlinedBorder}`,
          backgroundColor: "background.surface",
          '&::before': {
            transition: 'box-shadow .15s ease-in-out',
          },
                  
        }),
        input: ({ theme }) => ({
          fontSize: theme.typography.fontSize.sm,
          padding: `${theme.spacing(0.5)} ${theme.spacing(1)}`,
          color: theme.palette.text.primary
        }),
      },
    },
    JoyChip: {
      styleOverrides: {
        root: ({ theme }) => ({
          borderRadius: theme.radius.xl,
          padding: `${theme.spacing(0.5)} ${theme.spacing(1.5)}`,
          fontSize: theme.typography.fontSize.sm,
          transition: 'all 0.2s ease-in-out',
        }),
      },
    },
    JoyDivider: {
      styleOverrides: {
        root: ({ theme }) => ({
          borderColor: theme.palette.neutral.outlinedBorder,
        }),
      },
    },
    JoyTooltip: {
      styleOverrides: {
        tooltip: ({ theme }) => ({
          backgroundColor: theme.palette.neutral.solidColor,
          color: theme.palette.background.surface,
          fontSize: theme.typography.fontSize.sm,
          padding: `${theme.spacing(1)} ${theme.spacing(1.5)}`,
          borderRadius: theme.radius.sm,
          transition: 'all 0.2s ease-in-out',
        }),
      },
    },
  },
});

export default softTheme;