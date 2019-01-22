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



# This code was a totally useless experiment. Ignore it.


def normalizeAccent(a):
    return "*" if (a == None) else ("1" if a in "1hH-" else "0")

def convertDownstepToAccent(downstep, len):
    if downstep == 0:
        accent = "0" + "1"*(len-1)
    elif downstep == 1:
        accent = "1" + "0"*(len-1)
    else:
        accent = "01" + "1"*(downstep-2) + "0"*max(len-downstep, 1)
    return accent

def generateAccentDiagram(word, downstep):
    accent = convertDownstepToAccent(downstep, len(word))
    
    dia = "<ruby>"
    
    for i in range(0, len(word)):
        a = normalizeAccent(accent[i-1] if i != 0 else None)
        a += normalizeAccent(accent[i])
        a += normalizeAccent(accent[i+1] if i != len(accent)-1 else None)
        
        mapping = {
            "000" : "___",
            "001" : "__\u2571",
            "010" : "\u00AF\u00AF\u2572",
            "011" : "\u00AF\u00AF\u00AF",
            "100" : "___",
            "101" : "__\u2571",
            "110" : "\u00AF\u00AF\u2572",
            "111" : "\u00AF\u00AF\u00AF",
            "*00" : "___",
            "*01" : "__\u2571",
            "*10" : "\u00AF\u00AF\u2572",
            "*11" : "\u00AF\u00AF\u00AF",
            "00*" : "___",
            "01*" : "\u00AF\u00AF\u00AF",
            "10*" : "___",
            "11*" : "\u00AF\u00AF\u00AF",
        }
        
        s = mapping[a] if a in mapping else "???"
        
        dia += word[i] + "<rt>" + s + "</rt>"
    
    dia += "</ruby>"
    
    return dia

def onEditFocusLost(flag, n, fidx):
    if "japanese" not in n.model()['name'].lower():
        return flag
    
    accentName = None
    diagramName = None
    exprName = None
    
    for idx, name in enumerate(mw.col.models.fieldNames(n.model())):
        if name == "Expression":
            exprName = name
            exprIdx = idx
        if name == "Accent":
            accentName = name
            accentIdx = idx
        if name == "AccentDiagram":
            diagramName = name
            diagramIdx = idx
    
    if not accentName or not diagramName or not exprName:
        return flag
    
    if fidx != exprIdx  and  fidx != accentIdx:
        return flag
    
    expr = mw.col.media.strip(n[exprName])
    accent = mw.col.media.strip(n[accentName])
    
    if not expr  or  not accent:
        return flag
    
    n[diagramName] = generateAccentDiagram(furigana.kana(expr), int(accent))
    
    return True

def RegisterPitchAccentModule():
    addHook("editFocusLost", onEditFocusLost)
