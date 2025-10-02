
#  ClamWatch (ClamAV-based Folder Scanner)

A simple **Python + Tkinter antivirus GUI** that scans files and folders using **ClamAV (`clamscan`)**.  
The tool lets you select a folder, scans all files inside recursively, and reports whether each file is **clean, infected, or errored**.  

---

##  Features

-  **Folder Scan** – recursively scan all files inside a directory.  
-  **GUI with Tkinter** – clean interface with Treeview for results.  
-  **ClamAV Integration** – uses `clamscan` backend for virus detection.  
-  **Colored Results** –  
  -  Green → Clean  
  -  Red → Infected  
  - Orange → Error/Unknown  
-  **Summary Report** – shows total scanned, clean, infected, and errors.  
-  **Threaded Scan** – UI remains responsive while scanning.  



---

##  Installation & Setup

### 1. Install ClamAV
- **Windows**:  
  Download and install from [ClamAV Official Site](https://www.clamav.net/downloads).  
  Make sure `clamscan.exe` is in:  
```

C:\Program Files\ClamAV\clamscan.exe

````
- **Linux (Debian/Ubuntu)**:
```bash
sudo apt update
sudo apt install clamav clamav-daemon
````

### 2. Install Python dependencies

```bash
pip install tk
```

*(Tkinter usually comes pre-installed with Python, but install if missing.)*

### 3. Run the App

```bash
python antivirus_gui.py
```

---

##  Usage

1. Launch the app.
2. Browse and select a **folder**.
3. Click **Scan**.
4. Watch results update in real-time.
5. Summary will show clean, infected, and error counts.

---

## Project Structure

```
├── antivirus_gui.py    # Main application code
├── README.md           # Documentation
```

---

