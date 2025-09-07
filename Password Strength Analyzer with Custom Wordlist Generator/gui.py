
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from generator import generate_candidates
from analyzer import assess_password

def build_gui():
    root = tk.Tk()
    root.title("Password Analyzer & Wordlist Generator")

    ttk.Label(root, text="Hints (comma separated):").grid(row=0, column=0)
    hints_entry = ttk.Entry(root, width=60)
    hints_entry.grid(row=0, column=1)

    def on_generate():
        hints = [h.strip() for h in hints_entry.get().split(',') if h.strip()]
        if not hints:
            messagebox.showwarning("No hints", "Please enter at least one hint")
            return
        out = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text","*.txt")])
        if not out:
            return
        candidates = generate_candidates(hints, max_output=2000)
        with open(out, 'w', encoding='utf8') as f:
            f.write('\n'.join(candidates))
        messagebox.showinfo("Done", f"Wrote {len(candidates)} candidates")

    def on_analyze():
        pwd = password_entry.get()
        if not pwd:
            messagebox.showwarning("Empty", "Enter a password to analyze")
            return
        res = assess_password(pwd)
        messagebox.showinfo("Analysis", f"Score: {res['zxcvbn_score']}\nEntropy: {res['estimated_entropy_bits']} bits\nFeedback: {res['zxcvbn_feedback']}")

    ttk.Button(root, text="Generate Wordlist", command=on_generate).grid(row=1, column=1, sticky='w')
    ttk.Label(root, text="Password to analyze:").grid(row=2, column=0)
    password_entry = ttk.Entry(root, width=40, show='*')
    password_entry.grid(row=2, column=1)
    ttk.Button(root, text="Analyze", command=on_analyze).grid(row=3, column=1, sticky='w')

    root.mainloop()

if __name__ == '__main__':
    build_gui()
