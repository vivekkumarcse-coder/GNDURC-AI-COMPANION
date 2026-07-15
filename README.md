# Guru Nanak Dev RCC Information Chatbot

A portable, desktop-based graphical information chatbot built natively in Python using the Tkinter framework. This utility acts as an offline, interactive portal for student queries, structured data retrieval, and institutional support.

## 🚀 Core Features

- **Crash-Proof Dropdown Input:** Replaces open text entries with a `readonly` themed `ttk.Combobox` menu, eliminating manual typing errors and input vulnerabilities.
- **Dynamic Content Renderer:** Interprets custom markdown strings inline, displaying bold highlights, customized text padding, and clean layout dividers.
- **Resilient Asset Handling:** Includes an inline graphical engine that processes text tokens using regular expressions (`re`) to locate and load image assets. 
- **Graceful Error Recovery:** Built using a global `try-except` compilation wrap over the Python Imaging Library (`PIL`). If asset files are missing, a `PIL_AVAILABLE` boolean flag safely falls back to clean text placeholders instead of causing a runtime crash.
- **Smart Asset Scaling:** Automatically intercepts local graphic attachments (e.g., fee schedules, campus directories) and scales them down dynamically to a maximum rendering threshold (`IMAGE_MAX_WIDTH = 480`) to ensure UI display consistency.
- **Web Hyperlink Interceptor:** Employs the native `webbrowser` module to securely trigger and pass external website hyperlinks directly out to the host machine's default browser.

---

## 📂 Project Directory Structure

To ensure that images load inside the chatbot UI log, place your asset files inside the same folder directory as your Python script:

```text
├── chatbot.py               # Main Python application script
├── data.json                # Externalized dataset matrix (Optional/Week 3)
├── requirements.txt         # Project package dependencies
├── README.md                # System documentation manual
├── fees.jpeg                # Fee schedule graphic asset
├── Academic-calender.jpg    # University session calendar asset
├── engineering1.jpeg        # Engineering department contact asset 1
├── engineering2.jpeg        # Engineering department contact asset 2
├── electronic.jpeg          # ECE department contact asset
├── commerce.jpeg            # Business/Commerce contact asset
└── law.jpeg                 # Law department contact asset
