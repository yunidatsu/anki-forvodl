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

from aqt import mw

from .util import *
from .forvodl import *
from .pitchacc import *


RegisterForvoDownloadModule()

#cb = QApplication.clipboard()
#phrase = cb.text()
#RunForvoDownload(phrase, mw)
