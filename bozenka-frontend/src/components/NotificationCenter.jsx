import React from "react";

import { Sheet, Box, Typography, List, ListItem, Button, Chip, ListItemButton, ListItemContent } from "@mui/joy";

/**
* React component for the notification center.
* @returns {JSX.Element} - The rendered component.
*/
function NotificationCenter() {
  const [notifications, setNotifications] = React.useState([
    {
      id: 1,
      type: 'mention',
      content: 'John mentioned you in Community Alpha',
      time: '2 min ago',
      read: false
    },
    {
      id: 2,
      type: 'activity',
      content: 'New member joined Community Beta',
      time: '1 hour ago',
      read: false
    },
    {
      id: 3,
      type: 'alert',
      content: 'Unusual activity detected in your community',
      time: '3 hours ago',
      read: true
    }
  ]);

  return (
    <Sheet
      sx={{
        borderRadius: 'md',
        p: 2,
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        maxHeight: '80vh',
        overflow: 'auto'
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography level="title-lg">Notifications</Typography>
        <Button
          size="sm"
          variant="plain"
          color="neutral"
          onClick={() => {
            setNotifications(notifications.map(n => ({ ...n, read: true })));
          }}
        >
          Mark all as read
        </Button>
      </Box>

      <List
        sx={{
          '--ListItem-radius': '8px',
          '--ListItem-gap': '8px',
        }}
      >
        {notifications.map((notification) => (
          <ListItem
            key={notification.id}
            sx={{
              bgcolor: notification.read ? 'transparent' : 'primary.softBg',
              mb: 1,
            }}
          >
            <ListItemButton
              sx={{
                p: 2,
                borderRadius: 'md',
              }}
            >
              <ListItemContent>
                <Typography level="title-sm">
                  {notification.content}
                </Typography>
                <Typography level="body-xs" color="neutral">
                  {notification.time}
                </Typography>
              </ListItemContent>
              {!notification.read && (
                <Chip
                  size="sm"
                  color="primary"
                  variant="solid"
                >
                  New
                </Chip>
              )}
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Sheet>
  );
}

export default NotificationCenter;
