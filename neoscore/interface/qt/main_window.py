import os
import resources
from time import time
from typing import Optional, Tuple

from PyQt5 import QtCore, QtWidgets, uic

# cannot import setup/show again here, circular import
# from neoscore.core.neoscore import setup, show
from neoscore.core.text import Text
from neoscore.core.point import ORIGIN
from neoscore.common import *

QT_PRECISE_TIMER = 0


class MainWindow(QtWidgets.QMainWindow):
    """The primary entry point for all UI code.

    This bootstraps the ``main_window.ui`` structure.
    """

    _ui_path = os.path.join(os.path.dirname(__file__), "main_window.ui")

    def __init__(self):
        super().__init__()
        uic.loadUi(MainWindow._ui_path, self)
        self.refresh_func = None
        self.mouse_event_handler = None
        self._frame = 0  # Frame counter used in debug mode
                
        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_as.triggered.connect(self.saveAsFile)
        self.actionCut.triggered.connect(self.cutFile)
        self.actionCopy.triggered.connect(self.copyFile)
        self.actionPaste.triggered.connect(self.pasteFile)

        self.addPageButton.clicked.connect(self.addPage)
        self.delPageButton.clicked.connect(self.removePage)
        
        self.gCleff_Button.clicked.connect(self.createClef)
        self.staff1Line_Button.clicked.connect(self.createStaff1Line)

        # staves 
        self.staff1Line_Button.clicked.connect(self.createStaff1Line)
        self.staff2Lines_button.clicked.connect(self.createStaff2Lines)
        self.staff3Lines_button.clicked.connect(self.createStaff3Lines)
        self.staff4Lines_button.clicked.connect(self.createStaff4Lines)
        self.staff5Lines_button.clicked.connect(self.createStaff5Lines)
        self.staff6Lines_button.clicked.connect(self.createStaff6Lines)
        self.staff1LineWide_button.clicked.connect(self.createStaff1LineWide)
        self.staff2LinesWide_button.clicked.connect(self.createStaff2LinesWide)
        self.staff3LinesWide_button.clicked.connect(self.createStaff3LinesWide)
        self.staff4LinesWide_button.clicked.connect(self.createStaff4LinesWide)
        self.staff5LinesWide_button.clicked.connect(self.createStaff5LinesWide)
        self.staff6LinesWide_button.clicked.connect(self.createStaff6LinesWide)
        self.staff1LineNarrow_button.clicked.connect(self.createStaff1LineNarrow)
        self.staff2LinesNarrow_button.clicked.connect(self.createStaff2LinesNarrow)

        # barlines
        self.barlineSingle_button.clicked.connect(self.createBarlineSingle)
        self.barlineDouble_button.clicked.connect(self.createBarlineDouble)
        self.barlineFinal_button.clicked.connect(self.createBarlineFinal)
        self.barlineReverseFinal_button.clicked.connect(self.createBarlineReverseFinal)
        self.barlineHeavy_button.clicked.connect(self.createBarlineHeavy)
        self.barlineHeavyHeavy_button.clicked.connect(self.createBarlineHeavyHeavy)
        self.barlineDashed_button.clicked.connect(self.createBarlineDashed)
        self.barlineDotted_button.clicked.connect(self.createBarlineDotted)
        self.barlineShort_button.clicked.connect(self.createBarlineShort)
        self.barlineTick_button.clicked.connect(self.createBarlineTick)

        # repeats
        self.repeatLeft_button.clicked.connect(self.createRepeatLeft)
        self.repeatRight_button.clicked.connect(self.createRepeatRight)
        self.repeatRightLeft_button.clicked.connect(self.createRepeatRightLeft)
        self.repeatDots_button.clicked.connect(self.createRepeatDots)
        self.repeatDot_button.clicked.connect(self.createRepeatDot)
        self.dalSegno_button.clicked.connect(self.createDalSegno)
        self.daCapo_button.clicked.connect(self.createDaCapo)
        self.segno_button.clicked.connect(self.createSegno)
        self.coda_button.clicked.connect(self.createCoda)
        self.codaSquare_button.clicked.connect(self.createCodaSquare)
        self.segnoSerpent1_button.clicked.connect(self.createSegnoSerpent1)
        self.segnoSerpent2_button.clicked.connect(self.createSegnoSerpent2)
        self.leftRepeatSmall_button.clicked.connect(self.createLeftRepeatSmall)
        self.rightRepeatSmall_button.clicked.connect(self.createRightRepeatSmall)



        
    # Hide Widget Menu
        self.scrollArea.setHidden(True)
        
    # Hide Dropdowns
        self.Staff_dropdown.setHidden(True)
        self.Stave_dropdown.setHidden(True)
        self.Barlines_dropdown.setHidden(True)
        self.Repeats_dropdown.setHidden(True)
        self.Clefs.setHidden(True)
        self.Time_dropdown.setHidden(True)
        self.Note_Heads_dropdown.setHidden(True)
        self.Slash_dropdown.setHidden(True)
        self.Round_dropdown.setHidden(True)
        self.Note_Clusters_dropdown.setHidden(True)
    
    def newFile(self):
        print("New file clicked")
        
    def openFile(self):
        print("Open file clicked")
        
    def saveFile(self):
        print("Save file clicked")
        
    def saveAsFile(self):
        print("Save as file clicked")
        
    def cutFile(self):
        print("Cut file clicked")
        
    def copyFile(self):
        print("Copy file clicked")
        
    def pasteFile(self):
        print("Paste file clicked")
        
    def updatePage(self):
        neoscore.app_interface.clear_scene() 
        neoscore.document.render(True, Brush("#FFFFFF"))
        # self.graphicsView.viewport().update()
        self.refresh()

    def addPage(self):
        new_page_index = len(neoscore.document.pages)
        print(new_page_index)

        Text(ORIGIN, neoscore.document.pages[new_page_index], f"This is page {new_page_index + 1}")
        neoscore.document.pages[new_page_index]
        

        # render the document again to show the new page
        self.updatePage()
    
    #TODO needs to remove deleted page from being rendered on graphicsView
    
    def removePage(self):
        if len(neoscore.document.pages) > 0:
            # Remove the last page
            last_page_index = len(neoscore.document.pages) - 1
            print(last_page_index)
            neoscore.document.pages.pop(last_page_index)

        else:
            print("No pages to remove.")
            
        # render the document again to reflect the removed page
        self.updatePage()
    
    # Create Cleff Object

    def createClef(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "gClef", font)
        self.updatePage()
        
    def createStaff1Line(self):
        font = MusicFont("Bravura", Unit(10))
        staffLineObject = MusicText(ORIGIN, None, "staff1Line", font)
        # staffLineObject.rotation = 90
        # staffLineObject.scale = 2
        self.updatePage()
    
    def createStaff2Lines(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff2Lines", font)
        self.updatePage()
    
    def createStaff3Lines(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff3Lines", font)
        self.updatePage()
    
    def createStaff4Lines(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff4Lines", font)
        self.updatePage()
    
    def createStaff5Lines(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff5Lines", font)
        self.updatePage()
    
    def createStaff6Lines(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff6Lines", font)
        self.updatePage()
    
    def createStaff1LineWide(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff1LineWide", font)
        self.updatePage()
    
    def createStaff2LinesWide(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff2LinesWide", font)
        self.updatePage()
    
    def createStaff3LinesWide(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff3LinesWide", font)
        self.updatePage()
    
    def createStaff4LinesWide(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff4LinesWide", font)
        self.updatePage()
    
    def createStaff5LinesWide(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff5LinesWide", font)
        self.updatePage()

    def createStaff6LinesWide(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff6LinesWide", font)
        self.updatePage()

    def createStaff1LineNarrow(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff1LineNarrow", font)
        self.updatePage()
    
    def createStaff2LinesNarrow(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "staff2LinesNarrow", font)
        self.updatePage()
    
    def createBarlineSingle(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "barlineSingle", font)
        self.updatePage()

    def createBarlineDouble(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "barlineDouble", font)
        self.updatePage()
    
    def createBarlineFinal(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "barlineFinal", font)
        self.updatePage()
    
    def createBarlineReverseFinal(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "barlineReverseFinal", font)
        self.updatePage()
    
    def createBarlineHeavy(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "barlineHeavy", font)
        self.updatePage()

    def createBarlineHeavyHeavy(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "barlineHeavyHeavy", font)
        self.updatePage()
    
    def createBarlineDashed(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "barlineDashed", font)
        self.updatePage()
    
    def createBarlineDotted(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "barlineDotted", font)
        self.updatePage()
    
    def createBarlineShort(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "barlineShort", font)
        self.updatePage()
    
    def createBarlineTick(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "barlineTick", font)
        self.updatePage()
    
    def createRepeatLeft(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "repeatLeft", font)
        self.updatePage()
    
    def createRepeatRight(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "repeatRight", font)
        self.updatePage()
    
    def createRepeatRightLeft(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "repeatRightLeft", font)
        self.updatePage()
    
    def createRepeatDots(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "repeatDots", font)
        self.updatePage()
    
    def createRepeatDot(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "repeatDot", font)
        self.updatePage()
    
    def createDalSegno(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "dalSegno", font)
        self.updatePage()

    def createDaCapo(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "daCapo", font)
        self.updatePage()
    
    def createSegno(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "segno", font)
        self.updatePage()
    
    def createCoda(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "coda", font)
        self.updatePage()
    
    def createCodaSquare(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "codaSquare", font)
        self.updatePage()
    
    def createSegnoSerpent1(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "segnoSerpent1", font)
        self.updatePage()

    def createSegnoSerpent2(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "segnoSerpent2", font)
        self.updatePage()
    
    def createLeftRepeatSmall(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "leftRepeatSmall", font)
        self.updatePage()
    
    def createRightRepeatSmall(self):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, "rightRepeatSmall", font)
        self.updatePage()
    
    def show(
        self,
        min_size: Optional[Tuple[int, int]] = None,
        max_size: Optional[Tuple[int, int]] = None,
        fullscreen: bool = False,
    ):
        if min_size:
            self.setMinimumSize(QtCore.QSize(min_size[0], min_size[1]))
        if max_size:
            self.setMaximumSize(QtCore.QSize(max_size[0], max_size[1]))
        QtCore.QTimer.singleShot(0, QT_PRECISE_TIMER, self.refresh)  # noqa
        if fullscreen:
            super().showFullScreen()
        else:
            super().show()

    @QtCore.pyqtSlot()
    def refresh(self):
        start_time = time()
        if self.refresh_func:
            requested_delay_s = self.refresh_func(start_time)
            requested_delay_ms = int(requested_delay_s * 1000)
            QtCore.QTimer.singleShot(
                requested_delay_ms, QT_PRECISE_TIMER, self.refresh  # noqa
            )
            # if env.DEBUG:
            #     update_time = time() - start_time
            #     refresh_fps = int(1 / (time() - start_time))
            #     if self._frame % 30 == 0:
            #         print(
            #             f"Scene update took {int(update_time * 1000)} ms ({refresh_fps} / s)"
            #         )
            #         print(f"requested delay was {requested_delay_ms} ms")
            #     self._frame += 1
        # The viewport is unconditionally updated because we disable automatic updates
        self.graphicsView.viewport().update()