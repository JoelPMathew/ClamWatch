import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ---------------- Helper Function ----------------
def scan_file(file_path):
    if not os.path.exists(file_path):
        return {"file": file_path, "status": "error", "output": "File does not exist"}

    file_path = os.path.normpath(file_path)
    clamscan_path = r"C:\Program Files\ClamAV\clamscan.exe"
    if not os.path.exists(clamscan_path):
        clamscan_path = "clamscan"

    cmd = [clamscan_path, "--no-summary", file_path]

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = (proc.stdout.strip() + "\n" + proc.stderr.strip()).strip()
        if "FOUND" in output:
            return {"file": file_path, "status": "infected", "output": output}
        elif "OK" in output:
            return {"file": file_path, "status": "clean", "output": ""}
        else:
            return {"file": file_path, "status": "error", "output": output or "Unknown error"}
    except Exception as e:
        return {"file": file_path, "status": "error", "output": str(e)}

# ---------------- GUI ----------------
class AntivirusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Antivirus (Folder Scan)")
        self.root.geometry("900x600")
        self.create_widgets()

    def create_widgets(self):
        # Top frame
        frame_top = ttk.Frame(self.root, padding=10)
        frame_top.pack(fill="x")

        self.path_var = tk.StringVar()
        ttk.Entry(frame_top, textvariable=self.path_var, width=80).pack(side="left", padx=5)
        ttk.Button(frame_top, text="Browse Folder", command=self.browse_folder).pack(side="left", padx=5)
        ttk.Button(frame_top, text="Scan", command=self.start_scan_thread).pack(side="left", padx=5)

        # Treeview
        frame_tree = ttk.Frame(self.root, padding=10)
        frame_tree.pack(fill="both", expand=True)

        columns = ("file", "status", "signature")
        self.tree = ttk.Treeview(frame_tree, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="w", width=300 if col=="file" else 150)
        self.tree.pack(fill="both", expand=True)

        vsb = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # Summary
        self.summary_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.summary_var, padding=5).pack()

        # Treeview tag colors
        self.tree.tag_configure("infected", foreground="red")
        self.tree.tag_configure("clean", foreground="green")
        self.tree.tag_configure("error", foreground="orange")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def start_scan_thread(self):
        folder_path = self.path_var.get().strip()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return
        # Disable buttons while scanning
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                for btn in child.winfo_children():
                    if isinstance(btn, ttk.Button):
                        btn.config(state="disabled")
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.summary_var.set("Scanning... Please wait.")
        threading.Thread(target=self.scan_folder, args=(folder_path,), daemon=True).start()

    def scan_folder(self, folder_path):
        clean_count = 0
        infected_count = 0
        error_count = 0

        files_to_scan = []
        for root_dir, _, files in os.walk(folder_path):
            for file in files:
                files_to_scan.append(os.path.join(root_dir, file))

        total_files = len(files_to_scan)

        for idx, file_path in enumerate(files_to_scan, start=1):
            result = scan_file(file_path)
            status = result["status"]
            signature = result["output"].replace("\n", " ")

            # Update GUI from main thread
            self.root.after(0, self.update_tree, result["file"], status, signature)

            if status == "infected":
                infected_count += 1
            elif status == "clean":
                clean_count += 1
            else:
                error_count += 1

        # Final summary update
        self.root.after(0, self.update_summary, total_files, clean_count, infected_count, error_count)

    def update_tree(self, file_path, status, signature):
        iid = self.tree.insert("", "end", values=(file_path, status.upper(), signature))
        if status == "infected":
            self.tree.item(iid, tags=("infected",))
        elif status == "clean":
            self.tree.item(iid, tags=("clean",))
        else:
            self.tree.item(iid, tags=("error",))

    def update_summary(self, total, clean, infected, errors):
        self.summary_var.set(f"Scanned: {total} | Clean: {clean} | Infected: {infected} | Errors: {errors}")
        messagebox.showinfo("Scan Complete", f"Scan finished!\nInfected: {infected} | Clean: {clean} | Errors: {errors}")
        # Re-enable buttons
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                for btn in child.winfo_children():
                    if isinstance(btn, ttk.Button):
                        btn.config(state="normal")

# ---------------- Run GUI ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AntivirusGUI(root)
    root.mainloop()
