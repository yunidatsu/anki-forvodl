# anki-forvodl - A half-automatic Forvo downloader addon for Anki
# Copyright (C) 2019 yunidatsu
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


from aqt.qt import *
from aqt.utils import showInfo

assetDir = os.path.join(os.path.dirname(__file__), "assets")

class DownloadWatcher(QObject):
    downloadNoticed = pyqtSignal('QString')

    def __init__(self, parent):
        super(DownloadWatcher, self).__init__(parent)
        self.knownFiles = []
        self.settlingFiles = []
        self.watching = False
        self.watcher = QFileSystemWatcher(self)
        
        self.settleTimer = QTimer(self)
        self.settleTimer.setInterval(250)
        self.settleTimer.timeout.connect(self.settleTimerTimeout)
        self.settleTimer.start()
    
    def addWatchedDirectory(self, dir):
        self.watcher.addPath(dir)
    
    def startWatching(self):
        if not self.watching:
            self.discoverNewFiles()
            self.watcher.directoryChanged.connect(self.onDirChanged)
            self.watching = True
    
    def getWatchedDirectories(self):
        return self.watcher.directories()
    
    def discoverNewFiles(self):
        newKnownFiles = []
        newFiles = []
        
        for dirpath in self.watcher.directories():
            dir = QDir(dirpath)
            for fname in dir.entryList():
                fpath = QFileInfo(dir, fname).absoluteFilePath()
                if not fpath in self.knownFiles:
                    newFiles.append(fpath)
                newKnownFiles.append(fpath)
        
        self.knownFiles = newKnownFiles
        return newFiles
    
    def onDirChanged(self, dir):
        newFiles = self.discoverNewFiles()
        for file in newFiles:
            if not file in self.settlingFiles:
                self.settlingFiles.append(file)
    
    def settleTimerTimeout(self):
        newSettlingFiles = []
        settledFiles = []
        
        for file in self.settlingFiles:
            info = QFileInfo(file)
            
            if info.size() != 0:
                settledFiles.append(file)
            else:
                newSettlingFiles.append(file)
        
        self.settlingFiles = newSettlingFiles
        
        for file in settledFiles:
            self.downloadNoticed.emit(file)

def FindDownloadDirectories():
    return QStandardPaths.standardLocations(QStandardPaths.DownloadLocation)

# Find the aqt Editor object associated with the currently focused widget.
# This is quite hacky, but many hooks don't get the editor object passed, so
# this is the only way.
def FindFocusedEditor():
    focusWidget = QApplication.focusWidget()
    
    webViewWidget = focusWidget
    while webViewWidget != None  and  webViewWidget.metaObject().className() != "EditorWebView":
        webViewWidget = webViewWidget.parent()
    
    if webViewWidget == None:
        return None
    
    return webViewWidget.editor
