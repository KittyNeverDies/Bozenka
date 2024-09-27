import Slider from "@mui/joy/Slider";

/**
 * @function RangeSlider
 * @description Component for a range slider.
 * @param {string} label - Text used as aria-label for the slider.
 * @param {string} textOfValue - Text used for displaying the value of the slider.
 * @param {number} maxValue - Maximum value of the slider.
 * @param {number} minValue - Minimum value of the slider.
 * @returns {JSX.Element} - Range slider component.
 */
function RangeSlider(label, textOfValue, maxValue, minValue) {
    /**
     * @description Code of range slider from MUI documentation.
     */
   
    const [value, setValue] = useState([minValue, maxValue]);
    
    /**
     * @description Handler for changing the value of the slider.
     * @param {object} event - Event that is called when the value of the slider changes.
     * @param {number[]} newValue - New value of the slider.
     */
    const handleChange = (event, newValue) => {
          setValue(newValue);
    };
    /**
     * @description Function for displaying the value of the slider.
     * @param {number} value - Current value of the slider.
     * @returns {string} - String with the current value and the text that was passed as the textOfValue parameter.
     */
    const valueText = (value) => {
        return `${value} ${textOfValue}`;
    }

    return (
        <>
            <Slider
                sx={{
                    marginLeft: 2
                }}
                getAriaLabel={() => label}
                value={value}
                onChange={handleChange}
                valueLabelDisplay="auto"
                getAriaValueText={valueText}
        />
        </>
    )
}

