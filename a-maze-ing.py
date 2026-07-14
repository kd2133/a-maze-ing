import sys
import traceback
from src.config.parser import parse_config

# except Exception also sicherheitsnetz fuer unerwartete bugs, und traceback damit wir sehen was es ist weil Exception auch unsere coding Fehler handled und wir ohne traceback vielleicht nicht drauf kommen wuerden?
# noch hinzufuegen maybe: prints auf stderr statt stdout, und sys.exit() nach exception?
def main() -> None:
    try:
        filename = "config.txt"
        config = parse_config(filename)



    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except OSError as e:
        print(f"Error while accessing file '{filename}': {e}")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
