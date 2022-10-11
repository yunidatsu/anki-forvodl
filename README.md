# anki-forvodl
A half-automatic Forvo (or similar) downloader addon for Anki 2.1

This Anki addon can be used to quickly search for pronunciations of phrases on the website forvo.com and then add them to an Anki note. It works as follows:

1. When adding or editing a note, you **select the field** you want the audio files to go in and **click the addon's button** in the editor (or use its configurable keyboard shortcut, F10 by default).
2. The addon then opens the Forvo search results page in **your system's web browser**, where you can preview them and select which of them to add to Anki.
3. You download the audio file(s) from Forvo (use the small arrow button below each entry) using your **web browser's regular download mechanism**.
4. The addon will **monitor your web browser's download directory** to automatically find the audio files you've downloaded. It will show them in a dialog in Anki where you can again preview or remove some of them.
5. You **confirm** the list of files, and the addon adds them to your note. If you want, you can skip this step and instead auto-confirm the dialog when the first audio file is found.

That's all it does. It is very basic, but I think it makes the process of adding pronunciations a lot quicker.

Bear in mind that **you need to be logged in to forvo.com** to download files there, so you need a free Forvo account.
<br>
<br>
<br>


## FAQ

**Q:** **What languages** are supported for Forvo?
<br>
**A:** The addon should work with **any language** that Forvo supports. It has a **tiny bit of Japanese-specific logic** and is by default configured for it, but that can easily be changed in the addon config. See the next question.

**Q:** How do I use it with languages **other than Japanese**?
<br>
**A:** You have to change a few config options. In Anki, go to Tools->Addons, select the addon and click "Config". The most important fields to change are `forvoLookupUrl` and `patternSourceFields`. For `forvoLookupUrl`, you should change the language code at the end of the URL (e.g. to `#ko` for Korean). For `patternSourceFields` you should add the names of all the fields that might contain the "main phrase" for your notes (this is **case-sensitive**!), e.g. add `"Korean"`.
<br>
**Note:** At least for me, the language code in the Forvo URL currently doesn't work as intended (it doesn't automatically scroll down to any language other than the top one). If someone figures out a way to fix that, I would be very interested!

**Q:** Why am I getting the error message: "**Search phrase couldn't be determined. Check your field names and config**"?
<br>
**A:** This happens when the addon can't figure out **which field in the note contains the search phrase**. Make sure that the field name containing it is listed in the config option `patternSourceFields`. Make sure you've written it in the correct case, as **it is case-sensitive!**

**Q:** Does it support **other websites** than Forvo?
<br>
**A:** Yes, it does. Actually, nothing in it is Forvo-specific, even if the name suggests that. To use another website, simply edit the config option `forvoLookupUrl`. You can even configure it to open multiple websites at the same time. To make sure the addon automatically finds the downloaded files, you will also have to change `forvoFilePattern`, so you'll have to know a bit about [Python RegEx](https://docs.python.org/3/library/re.html).

**Q:** Can I **change the download directory** that the addon monitors?
<br>
**A:** Yes. The addon tries to figure out the download directory automatically by default, but if that fails or you want to use a different one, you can modify the config option `watchedDownloadDirectories` and put in your own path.

**Q:** Does this work with **Anki 2.0**?
<br>
**A:** I don't think it does right now. It uses some features apparently introduced in Anki 2.1. It could probably be made to work with 2.0 with a few changes, I haven't tried that yet.

**Q:** Why do I have to select and download the entries myself? Can't the addon do that **on its own**?
<br>
**A:** From a technical standpoint it would be possible, although a bit difficult because it would need to handle login and possibly JavaScript. But how would it decide which of the pronunciations to use? It could use the most voted-for entry, but for now I decided that it's easier and less error-prone to let a human pick.

**Q:** Is there a way to **bulk-add** pronunciations?
<br>
**A:** No, for the same reason as the previous question.

**Q:** Isn't this against the **Forvo ToS**?
<br>
**A:** I don't know, but I'm willing to take the risk. The addon does **not** use the Forvo API. Using the API would mean that I had to pay a monthly fee on behalf of everyone who uses the addon (I think), which I don't want to do. There have been suggestions to have each individual user pay for a private license and then use their own API keys, but Forvo explicitly forbids that.<br>
All the addon currently does is streamline the process of opening Forvo's publicly accessible website from Anki, and then adding the downloaded files to Anki quickly. It does not do anything that a normal user couldn't do on forvo.com legally and for free, and doesn't put Forvo's website under any more stress than regular users would do.
