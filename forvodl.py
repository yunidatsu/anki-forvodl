# anki-forvodl - A half-automatic Forvo downloader addon for Anki
# Copyright (C) 2019, 2022 yunidatsu
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import html
import re
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from anki.hooks import addHook
import anki.sound

from .util import *
from . import furigana


config = mw.addonManager.getConfig(__name__)

lastEditFocusGainedField = None


# When shown, this dialog will begin watching the configured watched
# download directories for any new Forvo audio files and then display
# them in a dynamic list where the user can preview and remove them
# from the list if necessary.
class DownloaderDialog(QDialog):
    def __init__(self, parent):
        super(DownloaderDialog, self).__init__(parent)
        
        self.watcher = DownloadWatcher(self)
        
        watchedDirs = config["watchedDownloadDirectories"]
        
        # Add auto-discovered download directories only if none
        # were manually configured
        if not watchedDirs  or  len(watchedDirs) == 0:
            watchedDirs = FindDownloadDirectories()
        
        for dir in watchedDirs:
            if QFileInfo(dir).isDir():
                self.watcher.addWatchedDirectory(dir)
        
        self.initUI()
        
        self.watcher.downloadNoticed.connect(self.onDownloadNoticed)
        self.watcher.startWatching()
        
    def initUI(self):
        self.setWindowTitle("Forvo Downloader")
    
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        descText = "<html>"
        descText += "Download files into one of these directories and they will be picked up:"
        descText += "<ul>"
        
        for dir in self.watcher.getWatchedDirectories():
            descText += "<li>" + dir + "</li>"
        
        descText += "</ul>"
        descText += "Audio files to add:"
        descText += "</html>"
        
        self.descLabel = QLabel(descText, self)
        self.descLabel.setTextFormat(Qt.RichText)
        self.mainLayout.addWidget(self.descLabel)
        
        self.audioListWidget = QWidget(self)
        self.audioListLayout = QGridLayout(self.audioListWidget)
        self.mainLayout.addWidget(self.audioListWidget)
        
        self.audioListLayout.setColumnStretch(1, 1)
        
        self.autoConfirmBox = QCheckBox("Auto-confirm on first download", self)
        self.autoConfirmBox.setCheckState(Qt.Checked if config["autoConfirmFirstDownload"] else Qt.Unchecked)
        self.mainLayout.addWidget(self.autoConfirmBox)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.mainLayout.addWidget(self.buttonBox)
        
        self.accepted.connect(self.onAccept)
    
    def onAccept(self):
        if self.autoConfirmBox.checkState() == Qt.Checked:
            config["autoConfirmFirstDownload"] = True
        else:
            config["autoConfirmFirstDownload"] = False
        mw.addonManager.writeConfig(__name__, config)
    
    def removeAudioFileFromList(self, file):
        # Qt, why???
        #
        # Based on: https://stackoverflow.com/a/19256990
        
        i = self.audioListLayout.count()-1
        while i >= 0:
            r, c, rs, cs = self.audioListLayout.getItemPosition(i)
            widget = self.audioListLayout.itemAt(i).widget()
            ifile = widget.property("forvodl-audio-file")
            
            if ifile == file:
                self.audioListLayout.takeAt(i)
                widget.deleteLater()
                self.audioListLayout.setRowMinimumHeight(r, 0)
                self.audioListLayout.setRowStretch(r, 0)
            
            i -= 1
    
    def isValidAudioFile(self, file):
        fname = QFileInfo(file).fileName()
        pattern = config["forvoFilePattern"]
        return True if re.match(pattern, fname) else False
    
    @pyqtSlot()
    def onAudioPlayPressed(self):
        btn = self.sender()
        file = btn.property("forvodl-audio-file")
        
        anki.sound.play(file)
    
    @pyqtSlot()
    def onAudioRemovePressed(self):
        btn = self.sender()
        file = btn.property("forvodl-audio-file")
        
        self.removeAudioFileFromList(file)
    
    def onDownloadNoticed(self, file):
        if self.isValidAudioFile(file):
            row = self.audioListLayout.rowCount()
            
            playButton = QPushButton(QIcon(os.path.join(assetDir, "audio-play.png")), None)
            playButton.setProperty("forvodl-audio-file", file)
            playButton.clicked.connect(self.onAudioPlayPressed)
            self.audioListLayout.addWidget(playButton, row, 0)
            
            audioLabel = QLabel(QFileInfo(file).fileName())
            audioLabel.setProperty("forvodl-audio-file", file)
            self.audioListLayout.addWidget(audioLabel, row, 1)
            
            removeButton = QPushButton(QIcon(os.path.join(assetDir, "audio-remove.png")), None)
            removeButton.setProperty("forvodl-audio-file", file)
            removeButton.clicked.connect(self.onAudioRemovePressed)
            self.audioListLayout.addWidget(removeButton, row, 2)
            
            if self.autoConfirmBox.checkState() == Qt.Checked:
                QTimer.singleShot(0, self.accept)
    
    def getAudioFiles(self):
        files = []
        for i in range(0, self.audioListLayout.rowCount()):
            item = self.audioListLayout.itemAtPosition(i, 0)
            
            if item and item.widget():
                file = item.widget().property("forvodl-audio-file")
                files.append(file)
        return files

def RunForvoDownload(phrase, parentWin):
    lookupUrls = config["forvoLookupUrl"]
    if not isinstance(lookupUrls, list):
        lookupUrls = [lookupUrls]

    # Open Forvo in external browser
    for url in lookupUrls:
        link = url.format(phrase=phrase)
        QDesktopServices.openUrl(QUrl(link))
    
    # Show dialog and wait for audio files to be confirmed
    dialog = DownloaderDialog(parentWin)

    if dialog.exec_():
        return dialog.getAudioFiles()
    
    return []

# Called when the Forvo search is about to start. Should return the phrase to
# search for, probably by looking at one of the note fields.
def selectForvoSearchPhrase(n):
    exprName = None
    srcFields = config["patternSourceFields"]
    
    # Double loop because srcFields is meant to be ordered by priority
    for fieldCandidate in srcFields:
        for idx, name in enumerate(mw.col.models.fieldNames(n.model())):
            if name == fieldCandidate:
                exprName = name
                exprIdx = idx
                break
    
    if not exprName:
        return None

    noteTypeName = n.note_type()["name"].lower()
    
    phrase = StripHtml(mw.col.media.strip(n[exprName]))

    # Check if this is a Japanese note
    japaneseNote = False
    for cand in config.get("japaneseNoteTypes", ["japanese"]):
        if cand.lower() in noteTypeName:
            japaneseNote = True
            break

    # For Japanese notes only, we'll try to extract just the kanji part in
    # case we have a mixed string like "先生[せんせい]"
    if japaneseNote:
        phrase = furigana.kanji(phrase)

    return phrase

def RunForvoDownloadFromEditor(editor):
    # Select search phrase from the editor
    phrase = selectForvoSearchPhrase(editor.note)
    
    if phrase == None:
        showInfo("Search phrase couldn't be determined. Check your field names and config!")
        return None
    
    # Open Forvo and watch for files
    return RunForvoDownload(phrase, editor.parentWindow)

def RunForvoDownloadFromNote(note, parentWin):
    # Select search phrase from the note
    phrase = selectForvoSearchPhrase(note)
    
    if phrase == None:
        showInfo("Search phrase couldn't be determined. Check your field names and config!")
        return None
    
    # Open Forvo and watch for files
    return RunForvoDownload(phrase, parentWin)

def onForvoLookupButton(editor):
    files = RunForvoDownloadFromEditor(editor)
    
    if not files:
        return
    
    # Add confirmed files to the editor
    for file in files:
        editor.addMedia(file)

def addEditorButtons(buttons, editor):
    editor._links['forvodl_forvolookup'] = onForvoLookupButton
    forvoButton = editor._addButton (
        os.path.join(assetDir, "forvo-button.png"),
        "forvodl_forvolookup", "Forvo Lookup (" + config["forvoEditorButtonShortcut"] + ")")
    return buttons + [forvoButton]

# Wrapper class because we need a reference to the editor
class ForvoLookupEditorShortcut:
    def __init__(self, editor):
        self.editor = editor
    
    def trigger(self):
        onForvoLookupButton(self.editor)

def addEditorShortcuts(cuts, editor):
    shortcut = ForvoLookupEditorShortcut(editor)
    cuts.append((config["forvoEditorButtonShortcut"], shortcut.trigger))
    return cuts

def onEditFocusGained(n, fidx):
    global lastEditFocusGainedField

    # Only run auto-prompt logic when the focused field has actually changed.
    # Otherwise we'll repeatedly prompt again if the user presses "Cancel" on the dialog.
    field = {"note" : n.id, "fidx" : fidx}
    if field == lastEditFocusGainedField:
        return
    lastEditFocusGainedField = field

    noteTypeName = n.note_type()['name'].lower()

    validNoteType = False
    if config.get("autoPromptOnEmptyNoteTypes", "all") == "all":
        # Run auto-prompt logic on all note types
        validNoteType = True
    else:
        # Only run auto-prompt logic on note types from the whitelist
        for cand in config["autoPromptOnEmptyNoteTypes"]:
            if cand.lower() in noteTypeName:
                validNoteType = True
                break

    if not validNoteType:
        return
    
    targetName = None
    
    for targetField in config["autoPromptOnEmptyFields"]:
        for idx, name in enumerate(mw.col.models.fieldNames(n.model())):
            if name == targetField:
                targetName = name
                targetIdx = idx
                break
    
    if not targetName:
        return
    if fidx != targetIdx:
        return
    if n[targetName] != "":
        return
    
    # Hack, because unfortunately, we have no reference to the editor
    editor = FindFocusedEditor()
    
    if editor:
        onForvoLookupButton(editor)

def RegisterForvoDownloadModule():
    addHook("setupEditorButtons", addEditorButtons)
    addHook("setupEditorShortcuts", addEditorShortcuts)
    
    if len(config["autoPromptOnEmptyFields"]) != 0:
        addHook("editFocusGained", onEditFocusGained)
