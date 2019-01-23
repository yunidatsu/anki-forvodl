# anki-forvodl
A half-automatic Forvo downloader addon for Anki 2.1

This Anki addon can be used to quickly search for pronunciations of phrases on the website forvo.com and then add them to an Anki note. It works as follows:

1. When adding or editing a note, you **select the field** you want the audio files to go in and **click the addon's button** in the editor (or use its keyboard shortcut).
2. The addon then opens the Forvo search results page in **your system's web browser**, where you can preview them and select which of them to add to Anki.
3. You download the audio file(s) from Forvo (use the small arrow button below each entry) using your **web browser's regular download mechanism**.
4. The addon will **monitor your web browser's download directory** to automatically find the audio files you've downloaded. It will show them in a dialog in Anki where you can again preview or remove some of them.
5. You **confirm** the list of files, and the addon adds them to your note. If you want, you can skip this step and instead auto-confirm the dialog when the first audio file is found.

That's all it does. It is very basic, but I think it makes the process of adding pronunciations a lot quicker.
<br>
<br>
<br>


## FAQ

**Q:** Does this work with Anki 2.0?
<br>
**A:** I don't think it does right now. It uses some features apparently introduced in Anki 2.1. It could probably be made to work with 2.0 with a few changes, I haven't tried that yet.

**Q:** Why do I have to select and download the entries myself? Can't the addon do that on its own?
<br>
**A:** From a technical standpoint it would be possible, although a bit difficult because it would need to handle login and possibly JavaScript. But how would it decide which of the pronunciations to use? It could use the most voted-for entry, but for now I decided that it's easier and less error-prone to let a human pick.

**Q:** Is there a way to bulk-add pronunciations?
<br>
**A:** No, for the same reason as the previous question.

**Q:** Isn't this against the Forvo ToS?
<br>
**A:** I don't know, but I'm willing to take the risk. The addon does **not** use the Forvo API. Using the API would mean that I had to pay a monthly fee on behalf of everyone who uses the addon (I think), which I don't want to do. There have been suggestions to have each individual user pay for a private license and then use their own API keys, but Forvo explicitly forbids that.<br>
All the addon currently does is streamline the process of opening Forvo's publicly accessible website from Anki, and then adding the downloaded files to Anki quickly. It does not do anything that a normal user couldn't do on forvo.com legally and for free, and doesn't put Forvo's website under any more stress than regular users would do.
