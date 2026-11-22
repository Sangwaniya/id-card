# ID Card Studio - Tech Area Pass Generator

A high-performance, single-file interactive web application for designing, editing, and batch-generating professional high-resolution ID cards and security passes (Air Force Station Sulur - Tech Area Pass).

![Tech Area Pass](template_front.jpg)

---

## 🚀 Quick Start (Zero Setup)

You can run and work on this repository immediately in any IDE or browser with zero required dependencies:

1. **Directly open in browser**:
   - Double-click `index.html` (or `id-card-generator.html`) in your file explorer.
2. **Or run with any local development server**:
   - **VS Code / Cursor / Windsurf**: Right-click `index.html` and click **"Open with Live Server"**.
   - **Python**: Run `python -m http.server 8000` and navigate to `http://localhost:8000`.
   - **Node.js**: Run `npx serve .` or `npx http-server`.

---

## ✨ Features

- **Front & Back Card Canvas**: High-DPI canvas rendering with seamless toggling between front and back of the ID pass.
- **Drag & Drop Layout Editing**: Unlock layout mode to visually drag, position, resize, and style text fields, photos, and QR codes.
- **Floating Inline Toolbar**: Real-time font sizing, color picker, bold/italic, alignment, and coordinate adjustments.
- **Live QR Code Integration**: Automatically encodes pass holder details, dates, and security data into scannable QR codes.
- **Multi-Person & Bulk Batch Support**: Easily switch between personnel records, add/edit cards, and export cards in bulk.
- **Export & Print Ready**: Export high-resolution PNG/JPEG images or print directly with standard ID card dimensions.
- **Self-Contained & Offline**: All base64 assets and libraries are bundled into `index.html`. No external internet connection or CDN required.

---

## 📁 Repository Structure

```text
├── index.html                 # Main self-contained web app (Trident ID Card Studio)
├── id-card-generator.html     # Alternate standalone build
├── build_app.py               # Python builder to generate/compile index.html from source templates
├── template_front.jpg         # High-resolution front card background template
├── template_back.jpg          # High-resolution back card background template
├── front_b64.txt              # Base64 string dump for front template
├── back_b64.txt               # Base64 string dump for back template
├── test_rendered_empty_back.jpg # Reference test render (back template)
├── test_standard_photo_box.jpg  # Reference test render (photo alignment box)
└── README.md                  # Project documentation
```

---

## 🛠️ Rebuilding / Modifying the App

If you update the background templates (`template_front.jpg` or `template_back.jpg`) or adjust the core template engine in `build_app.py`, recompile the standalone HTML apps with:

```bash
python build_app.py
```

This will automatically re-encode the images to Base64 and regenerate `index.html` and `id-card-generator.html`.

---

## 💻 Tech Stack

- **Frontend**: Vanilla JavaScript (ES6+), HTML5 Canvas API, CSS3
- **Asset Pipeline**: Python 3 (`base64`, `json`)
- **Compatibility**: All modern browsers (Chrome, Firefox, Safari, Edge)
