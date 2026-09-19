# Local PDF & Word Converter

A private, offline web app that converts **PDF ⇄ Word** documents right on your own computer. No files are ever uploaded anywhere — everything stays on your device.

---

## Features (Version 1)

- **PDF → Word (.docx)** with high-quality layout preservation.
- **Word → PDF** (uses Microsoft Word on Windows, LibreOffice on Linux/Mac).
- **Drag-and-drop web dashboard** — drop files in your browser and click Convert.
- **Batch converting** — convert multiple files at once.
- **Auto mode** — the app guesses the right target format (PDF → Word, Word → PDF) automatically.
- **100% offline & private** — the browser interface is served from your own machine on `http://127.0.0.1:8000`.
- Supports `.pdf`, `.docx` and `.doc` files up to **60 MB**.

---

## Requirements

- **Python 3.9 or newer** installed on your computer.
  - Windows: download from <https://www.python.org/downloads/> — tick **"Add Python to PATH"** during install.
- **Word→PDF converter (one of these):**
  - Windows: **Microsoft Word 2013 or newer** (recommended), **or** LibreOffice.
  - Linux / Mac: **LibreOffice** (an open-source office suite).
- PDF→Word works with just Python, no extra software.

---

## How to Run (Windows)

1. Install Python from <https://www.python.org/downloads/> (tick **"Add Python to PATH"**).
2. Open the `local-pdf-converter` folder.
3. **Double-click `run.bat`**. It will:
   - Install the needed libraries automatically (first run only takes a minute).
   - Start the app and open your browser at `http://127.0.0.1:8000`.
4. Drag your PDF or Word files into the page, click **Convert**, then **Download** the result.
5. Keep the black window open while you use the converter. Close it to stop the app.

### How to Run (Linux / Mac)

```bash
cd local-pdf-converter
python3 -m pip install -r requirements.txt
python3 app.py
```

Then open http://127.0.0.1:8000 in your browser.

---

## How It Works

- The smaller library **pdf2docx** handles **PDF → Word**.
- **docx2pdf** (which drives Microsoft Word on Windows) handles **Word → PDF**.
- If Word is missing, the app automatically falls back to **LibreOffice** for Word → PDF.
- Each conversion runs in a temporary folder and is deleted right after the file is sent to your browser — nothing is left behind.

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| "Word is not installed" error | Install Microsoft Word **or** LibreOffice, then retry. |
| Python not recognized | Reinstall Python and tick **"Add Python to PATH"**. |
| Port is already in use | Close any other app on port 8000, or edit the port in `app.py`. |
| Fonts look different after PDF→Word | This is normal — PDF→Word preserves text and images, but exact pixel-perfect layout is not always possible. |

---

## Version History

### Version 1 (Current)
- Initial release: PDF ⇄ Word conversion, drag-and-drop UI, batch mode, auto target detection, private local server.