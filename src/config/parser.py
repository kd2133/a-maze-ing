from .maze_config import MazeConfig

def parse_config(filepath: str) -> MazeConfig:
    """
    Parses the config.txt and returns a MazeConfig instance, so we can pass it to functions as args if needed and for dot-notation

    Args: (filepath: str | Path), path to config, takes either string or Path from pathlib(as we use)

    Returns: MazeConfig instance with the attributes (width, height, etc.)

    Parsing Logic:
        1:  - open file and strip line
            - if clean_line emtpy after strip or starts with # -> skip
            - if there are strings but no '=' -> raise ValueError
            - split string at '=' and store strings inside of key, value
            - if there is still whitespace -> strip it, and normalize to lower()
            - assign value to key inside of dict "data"
            - raise OSError if something goes wrong with processing/opening file

        2:  - loop through required_keys and check if we have missing keys
            -loop through data and check if we have unauthorized keys
        
        3:  - normalize value of 'PERFECT', set the bool depending on the value (true or false)
            - else raise error

        4:  - take entry and exit string, split it at ',', put the values inside of x, y
            - then put x, y into entry_pos and exit_pos to make it a tuple and convert them to int
            - if the points were written with a '.' instead of ','-> replace '.' with ','
            - return MazeConfig instance with the attributes
            - if error occurs during convertion
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
    try:
        width = int(data['width'])
        height = int(data['height'])

        x, y = data['entry'].replace('.', ',').split(",")
        entry_pos = int(x), int(y)
        x, y = data['exit'].replace('.', ',').split(",")
        exit_pos = int(x), int(y)
        perfect_val = data['perfect'].lower()

        if perfect_val == 'true':
            perfect_bool = True
        elif perfect_val == 'false':
            perfect_bool = False 
        else:
            raise ValueError(f"Invalid boolean expression for PERFECT: {data['perfect']}")

        if 'seed' in data:
            seed_value = int(data['seed'])
        else:
            seed_value = None
        return MazeConfig(
            width=width,
            height=height,
            entry_pos=entry_pos,
            exit_pos=exit_pos,
            output_file=data['output_file'],
            perfect=perfect_bool,
            seed=seed_value
        )
    except ValueError as e:
        raise ValueError(f"conversion error: {e}")
        

if __name__ == "__main__":
    try:
        parse_config("../config.txt")
    except ValueError as e:
        print(f"Error: {e}")