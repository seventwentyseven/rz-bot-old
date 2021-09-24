class colors:
    class embeds:
        # These are just hex, as # is not working in python (crub your comments)
        # You just swap this hash with "0x" so for example instead of
        #  #FFFFFF for white you'll put here 0xFFFFFF
        red = 0xff3838
        green = 0x2ed573
        blue = 0x0984e3
        purple = 0x8e44ad

    # terminal colors, don't touch these. There's nothing you can change.
    end="\033[0m"       # Text Reset

    # Regular Colors
    black="\033[0;30m"        # Black
    red="\033[0;31m"          # Red
    green="\033[0;32m"        # Green
    yellow="\033[0;33m"       # Yellow
    blue="\033[0;34m"         # Blue
    purple="\033[0;35m"       # Purple
    cyan="\033[0;36m"         # Cyan
    white="\033[0;37m"        # White