import os
import sys
import subprocess

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except ImportError:
    print("tkinter is required to run this script.")
    sys.exit(1)

# Ensure jupytext is installed
def ensure_jupytext():
    try:
        import jupytext
    except ImportError:
        print("jupytext not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jupytext"])

def select_py_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Select Python (.py) files to convert",
        filetypes=[("Python Files", "*.py")],
    )
    return list(file_paths)

def convert_py_to_ipynb(py_files):
    for py_file in py_files:
        ipynb_file = os.path.splitext(py_file)[0] + ".ipynb"
        print(f"Converting {py_file} to {ipynb_file} ...")
        result = subprocess.run(
            [sys.executable, "-m", "jupytext", "--to", "notebook", py_file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"Saved: {ipynb_file}")
        else:
            print(f"Error converting {py_file}:\n{result.stderr}")

def main():
    ensure_jupytext()
    py_files = select_py_files()
    if py_files:
        convert_py_to_ipynb(py_files)
        messagebox.showinfo("Done", "All files converted successfully.")
    else:
        print("No files selected.")

if __name__ == "__main__":
    main()