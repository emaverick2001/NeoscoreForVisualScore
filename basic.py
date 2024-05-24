from neoscore.core.neoscore import setup, show
from neoscore.core.text import Text
from neoscore.core.point import ORIGIN
from neoscore.common import *

setup()
Text(ORIGIN, None, "Hello, neoscore!")
# second_page = neoscore.document.pages[1]
# third_page = neoscore.document.pages[2]
show()