def binary_to_decimal(binary_string):
    """
    Convert binary string to decimal integer

    Args:
        binary_string: Binary string (e.g., "110")

    Returns:
        Decimal integer (e.g., 6)
    """
    decimal = 0
    power = len(binary_string) - 1

    for bit in binary_string:
        if bit == "1":
            decimal += 2**power
        power -= 1

    return decimal


def create_zero_array(height, width):
    """
    Create 2D array filled with zeros

    Args:
        height, width: Array dimensions

    Returns:
        2D list filled with zeros
    """
    return [[0 for _ in range(width)] for _ in range(height)]


def get_neighbor_positions(row, col, height, width):
    """
    Get valid neighbor positions based on pixel location
    Returns neighbors in clockwise order from top-left

    Handles:
    - Corner pixels: 3 neighbors
    - Edge pixels: 5 neighbors
    - Interior pixels: 8 neighbors

    Args:
        row, col: Current pixel position
        height, width: Image dimensions

    Returns:
        List of (row, col) tuples for valid neighbors
    """
    # Define all 8 possible neighbors (clockwise from top-left)
    all_neighbors = [
        (row - 1, col - 1),  # top-left
        (row - 1, col),  # top
        (row - 1, col + 1),  # top-right
        (row, col + 1),  # right
        (row + 1, col + 1),  # bottom-right
        (row + 1, col),  # bottom
        (row + 1, col - 1),  # bottom-left
        (row, col - 1),  # left
    ]

    # Filter valid neighbors (within image bounds)
    valid_neighbors = []
    for r, c in all_neighbors:
        if 0 <= r < height and 0 <= c < width:
            valid_neighbors.append((r, c))

    return valid_neighbors


def get_neighbor_intensities(msb_image, row, col, neighbor_positions):
    """
    Extract 3-MSB values for given neighbor positions

    Args:
        msb_image: 3-MSB image array (values 0-7)
        row, col: Center pixel position
        neighbor_positions: List of (row, col) tuples

    Returns:
        List of 3-MSB values (0-7)
    """
    intensities = []
    for r, c in neighbor_positions:
        intensities.append(msb_image[r][c])

    return intensities


def compare_to_center(neighbor_values, center_value):
    """
    Compare each neighbor to center pixel (both are 3-MSB values 0-7)

    Args:
        neighbor_values: List of neighbor 3-MSB values (0-7)
        center_value: Center pixel 3-MSB value (0-7)

    Returns:
        Binary string with length equal to number of neighbors
        Examples: "101" (3 neighbors), "11010" (5 neighbors), "11010011" (8 neighbors)
    """
    binary_code = ""
    for neighbor in neighbor_values:
        if neighbor >= center_value:
            binary_code += "1"
        else:
            binary_code += "0"

    return binary_code


def count_transitions(binary_string):
    """
    Count bit transitions in binary pattern (linear, not circular)
    Works with any length binary string (3, 5, or 8 bits)

    Args:
        binary_string: Binary string of any length

    Returns:
        Number of transitions

    Examples:
        "110" → 1 transition (1→1 same, 1→0 change)
        "11010" → 3 transitions
        "11010011" → 4 transitions
    """
    transition_count = 0

    # Compare adjacent bits
    for i in range(len(binary_string) - 1):
        if binary_string[i] != binary_string[i + 1]:
            transition_count += 1

    return transition_count


def classify_texture(transition_count, binary_length):
    """
    Classify texture based on transition ratio (adaptive threshold)

    Uses percentage-based threshold to handle different neighbor counts:
    - Corner pixels: 3 neighbors → max 2 transitions
    - Edge pixels: 5 neighbors → max 4 transitions
    - Interior pixels: 8 neighbors → max 7 transitions

    Args:
        transition_count: Number of transitions counted
        binary_length: Length of binary pattern (3, 5, or 8)

    Returns:
        0 = smooth (≤50% transitions), 1 = rough (>50% transitions)

    Examples:
        3 bits: 1/2=50% → smooth, 2/2=100% → rough
        5 bits: 2/4=50% → smooth, 3/4=75% → rough
        8 bits: 3/7=43% → smooth, 4/7=57% → rough
    """
    max_possible_transitions = binary_length - 1

    # Avoid division by zero (shouldn't happen with our setup)
    if max_possible_transitions == 0:
        return 0  # single bit, consider smooth

    transition_ratio = transition_count / max_possible_transitions

    # Threshold: 50% or less = smooth
    if transition_ratio <= 0.5:
        return 0  # smooth
    else:
        return 1  # rough


def compute_lbp_texture_map(msb_image):
    """
    Compute texture map using LBP on 3-MSB image
    Uses adaptive threshold based on neighbor count

    Args:
        msb_image: 2D list of 3-MSB values (0-7)

    Returns:
        Texture map: 2D list with 0 (smooth) and 1 (rough)
    """
    height = len(msb_image)
    width = len(msb_image[0])

    # Initialize texture map
    texture_map = create_zero_array(height, width)

    # Process each pixel
    for row in range(height):
        for col in range(width):
            # Get center pixel 3-MSB value
            center_value = msb_image[row][col]

            # Get valid neighbor positions
            neighbor_positions = get_neighbor_positions(row, col, height, width)

            # Get neighbor 3-MSB values
            neighbor_values = get_neighbor_intensities(
                msb_image, row, col, neighbor_positions
            )

            # Generate binary code by comparing neighbors to center
            binary_code = compare_to_center(neighbor_values, center_value)

            # Count transitions in the FULL binary code
            transitions = count_transitions(binary_code)

            # Classify texture using adaptive threshold
            texture_class = classify_texture(transitions, len(binary_code))

            # Store in texture map
            texture_map[row][col] = texture_class

    return texture_map
