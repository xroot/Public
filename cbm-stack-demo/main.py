# main.py

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        import main_cli
        main_cli.main()
    else:
        import main_gui
        main_gui.launch_gui()
