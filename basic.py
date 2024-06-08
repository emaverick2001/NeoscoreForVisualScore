from neoscore.core.neoscore import setup, show
from neoscore.core.paper import LETTER
from neoscore.core.text import Text
from neoscore.core.point import ORIGIN
from neoscore.common import *

setup(LETTER)
# hard code for now
# font = MusicFont("Bravura", Unit(10))
# MusicText(ORIGIN, None, "staff1Line", font)
# MusicText(ORIGIN, None, "gClef", font)
# second_page = neoscore.document.pages[1]
# third_page = neoscore.document.pages[2]
show()