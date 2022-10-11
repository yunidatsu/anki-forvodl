**YOU NEED TO RESTART ANKI FOR CHANGES TO TAKE EFFECT!**


**patternSourceFields**: List of fields to consider for the Forvo search phrase. The first field in this list that matches will be used. This is case-sensitive!

**forvoLookupUrl**: URL to be opened in the browser when searching. The placeholder {phrase} will be replaced by the search phrase. Multiple URLs can be provided, e.g. to select the best audio from different websites (example: `"forvoLookupUrl" : ["https://forvo.com/word/{phrase}/#ja", "https://jisho.org/search/{phrase}"]`)

**watchedDownloadDirectories**: List of directories to watch for downloaded Forvo files, e.g. your web browser's 'Downloads' directory. If (and only if) this list is empty, the addon will try to locate it automatically.

**forvoFilePattern**: Regex used to determine if a downloaded file is a Forvo audio file.

**forvoEditorButtonShortcut**: Shortcut for the tiny button in the editor.

**autoConfirmFirstDownload**: Automatically confirm the dialog and insert the first audio file that's downloaded.

**autoPromptOnEmptyFields**: A list of fields. If the first matching field from this list comes in focus while it's empty, a Forvo search will automatically be initiated. This is case-sensitive!

**autoPromptOnEmptyNoteTypes**: Used in conjunction with *autoPromptOnEmptyFields*, only start automatic search on focus for notes whose type name contains one of the words from this list. The special value "all" (**outside** of a list!) enables it for all note types. Example: To enable auto-search only for Japanese notes, try `"autoPromptOnEmptyNoteTypes" : ["japanese"]`.

**japaneseNoteTypes**: A list of words to look for in the note type name to decide if a note is Japanese. This is only used to remove any kana in brackets from the search phrase if it's formatted like "先生[せんせい]".
