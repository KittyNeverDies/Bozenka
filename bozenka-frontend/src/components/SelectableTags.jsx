import Chip from '@mui/joy/Chip';
import Typography from '@mui/joy/Typography';

/**
 * @function SelectableTags
 * @description This function renders chip tags that can be selected and deselected
 * @param {Object} props - The props object
 * @param {Object} props.Tag - The tag object containing icon and name
 * @param {boolean} props.isSelected - Whether the tag is selected
 * @param {Function} props.onSelect - Callback when tag is clicked
 * @returns {JSX.Element}
 */
function SelectableTags({ Tag, isSelected, onSelect }) {
    const { icon, name } = Tag;

    return (
        <Chip
            sx={{
                m: 0.4,
                borderRadius: 'sm',
                transition: 'all 0.3s ease',
                '&:hover': {
                    backgroundColor: "background.level2",
                    transform: 'translateY(-1px)',
                },
                '&:active': {
                    transform: 'translateY(0)',
                },
                cursor: 'pointer',
            }}
            variant={isSelected ? 'solid' : 'soft'}
            onClick={onSelect}
            color={isSelected ? 'primary' : 'neutral'}
            startDecorator={
                <Typography
                    component="span"
                    sx={{ 
                        fontFamily: 'Material Icons',
                        fontSize: '14px',
                        color: 'inherit',
                        display: 'flex',
                        alignItems: 'center',
                    }}
                >
                    {icon}
                </Typography>
            }
        >
            {name}
        </Chip>
    );
}

export default SelectableTags;