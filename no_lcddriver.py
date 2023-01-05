"""
NO LCD driver

When you run the main app with -v=yes it means you don't have a LCD 
driver installed. This is a stub to allow the app to run without it

v1.1.0  2023-01-04  Added 4 lines support
v1.0.0  2020-12-20  First version

"""
from time import sleep


class lcd:
    # initializes objects and lcd
    def __init__(self, address: int = 0x3F, columns=16, lines=2) -> None:
        """
        Parameters:
           address: int, the LCD address in hex format, grabbed by sudo i2cdetect -y 1, ie 0x3f or 0x27...
           columns: int, the columns number, ie 16 or 20
           lines: int, the lines number, ie 2 or 4

        Ouput
        - None
        """
        self.__version__ = "v1.1.0"
        print("No lcd driver initialized!")
        self.string1 = "                    "
        self.string2 = "                    "
        self.string3 = "                    "
        self.string4 = "                    "
        self.columns = columns
        self.lines = lines
        sleep(0.2)

    def lcd_display_string(self, string, line):
        
        if line == 1:
            self.string1 = (string + " " * self.columns)[: self.columns]
        elif line == 2:
            self.string2 = (string + " " * self.columns)[: self.columns]
        elif line == 3:
            self.string3 = (string + " " * self.columns)[: self.columns]
        elif line == 4:
            self.string4 = (string + " " * self.columns)[: self.columns]

        if self.lines == 2:
            print("\r", self.string1 + " --- " + self.string2, end="")
        elif self.lines == 4:
            print("\r", self.string1 + " --- " + self.string2 + " --- " + self.string3 + " --- " + self.string4, end="")

    # clear lcd and set to home
    def lcd_clear(self):
        print("clear screen")
