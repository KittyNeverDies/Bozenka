import Typography from "@mui/joy/Typography";
import Box from "@mui/joy/Box";


/**
* React component for displaying a 404 error page.
* @returns {JSX.Element} - A JSX element representing the 404 error page.
*/
export default function Page404(){
    return <>
    <Box sx={{ alignContent: 'center' }}>
        <Box sx={{
            'max-width': '1200px',
            margin: '0 auto',
            padding: '0 20px',
            height: 300,
            my: 10
        }}>
            <Typography sx={{
                fontSize: 100,
                
            }} my={1}>
                    (o_0)
            </Typography>
            <Typography>
                Sorry, but for right now this page doesn't exists.
            </Typography>
        </Box>
    </Box>
    </>
}