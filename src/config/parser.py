def parse_config(filepath: str) -> dict[str, str]:
    """Parse config file, check for missing / unauthorized key.

    Args:
        filepath: File to be parsed.

    Returns:
        A dictionary containing required data for maze.

    Raises:
        ValueError: If key missing / unauthorized.
    """
    required_keys = {
        "width", "height", "entry",
        "exit", "output_file", "perfect"
    }
    optional_keys = {"seed"}
    data = {}
    with open(filepath, "r") as file:
        for line in file:
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            if "=" not in clean_line:
                raise ValueError(f"{clean_line} has no '='")
            key, value = clean_line.split("=", 1)
            data[key.lower().strip()] = value.strip()

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key.upper()}")
    for key in data:
        if key not in required_keys.union(optional_keys):
            raise ValueError(f"Unauthorized key: {key.upper()}")
    return data
