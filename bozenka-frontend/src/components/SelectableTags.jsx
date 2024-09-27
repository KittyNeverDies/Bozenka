import Chip from '@mui/joy/Chip';

/**
 * @function SelectableTags
 * @description This function renders chip tags that can be selected and deselected. Mostly used for tags of communities.
 * @param {Object} props - The props object passed to the component.
 * @param {Object} props.Tag - The tag object containing the icon and name of the tag.
 * @param {Object} props.Tag.icon - The icon of the tag.
 * @param {Object} props.Tag.name - The name of the tag.
 * @returns {JSX.Element} - The JSX element representing the selectable tags.
 */
function SelectableTags({ Tag }) {
    /**
     * @description The tag object containing the icon and name of the tag.
     * @type {Object}
     */
    const {icon, name} = Tag

    /**
     * @description A boolean state variable that indicates whether the tag is selected or not.
     * @type {boolean}
     */
    const [isSelected, SetSelected] = useState(false);

    /**
     * @description The JSX element representing the selectable tags.
     * @type {JSX.Element}
     */
    return (
        <Chip
            sx={
                /**
                 * @description The styling object for the Chip component.
                 * @type {Object}
                 */
                {
                    m: 0.4
                }
            }
            variant='soft'
            onClick={() => SetSelected(!isSelected)}
            color={isSelected == true ? 'primary' : 'neutral'}
            startDecorator={icon} // Add some spacing between tags
        >
            {name}
        </Chip>
    )
}

export default SelectableTags;
