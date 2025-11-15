"""
ABS Labour Force Data Fetcher - GUI Application
Beautiful, user-friendly interface for running data collection scripts.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import subprocess
import json
import os
from datetime import datetime
import queue

class ABSDataFetcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ABS Labour Force Data Fetcher")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Queue for thread-safe communication
        self.log_queue = queue.Queue()
        self.progress_queue = queue.Queue()
        
        # State variables
        self.is_running = False
        self.current_process = None
        
        # Session statistics
        self.session_fetched = 0
        self.session_failed = 0
        self.session_not_available = 0
        
        # Color scheme
        self.bg_color = "#f0f0f0"
        self.accent_color = "#2196F3"
        self.success_color = "#4CAF50"
        self.warning_color = "#FF9800"
        self.error_color = "#F44336"
        
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
        self.update_status_panel()
        self.check_queues()
        
    def setup_ui(self):
        """Setup the main UI layout."""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # ===== HEADER =====
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(
            header_frame,
            text="🇦🇺 ABS Labour Force Data Fetcher",
            font=("Helvetica", 18, "bold")
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Automated data collection with checkpoint support",
            font=("Helvetica", 10)
        )
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        # Help button
        help_button = tk.Button(
            header_frame,
            text="❓ Help",
            command=self.show_help,
            bg="#9C27B0",
            fg="black",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            cursor="hand2"
        )
        help_button.grid(row=0, column=1, rowspan=2, padx=(10, 0))
        
        # ===== API KEY PANEL =====
        api_frame = ttk.LabelFrame(main_frame, text="🔑 API Configuration", padding="10")
        api_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        api_frame.columnconfigure(1, weight=1)
        
        ttk.Label(api_frame, text="API Key:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, width=50, font=("Courier", 10))
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        save_api_button = tk.Button(
            api_frame,
            text="💾 Save",
            command=self.save_api_key,
            bg=self.success_color,
            fg="black",
            font=("Helvetica", 9, "bold"),
            padx=10,
            pady=5,
            relief=tk.RAISED,
            cursor="hand2"
        )
        save_api_button.grid(row=0, column=2)
        
        ttk.Label(api_frame, text="Get your API key from: https://developer.vic.gov.au", 
                 font=("Helvetica", 8), foreground="#666").grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # ===== STATUS PANEL =====
        status_frame = ttk.LabelFrame(main_frame, text="📊 Status", padding="10")
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        status_frame.columnconfigure(3, weight=1)
        
        # Left column
        ttk.Label(status_frame, text="Last Run:", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.last_run_label = ttk.Label(status_frame, text="Never", font=("Helvetica", 9))
        self.last_run_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="Total Records:", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.total_records_label = ttk.Label(status_frame, text="0", font=("Helvetica", 9))
        self.total_records_label.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="Completed:", font=("Helvetica", 9, "bold")).grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        self.completed_label = ttk.Label(status_frame, text="0 / 1620", font=("Helvetica", 9))
        self.completed_label.grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="This Session:", font=("Helvetica", 9, "bold")).grid(row=3, column=0, sticky=tk.W, padx=(0, 5))
        self.session_label = ttk.Label(status_frame, text="Fetched: 0 | Failed: 0", font=("Helvetica", 9))
        self.session_label.grid(row=3, column=1, sticky=tk.W)
        
        # Right column
        ttk.Label(status_frame, text="Data Freshness:", font=("Helvetica", 9, "bold")).grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        self.freshness_label = ttk.Label(status_frame, text="Unknown", font=("Helvetica", 9))
        self.freshness_label.grid(row=0, column=3, sticky=tk.W)
        
        ttk.Label(status_frame, text="Latest Month:", font=("Helvetica", 9, "bold")).grid(row=1, column=2, sticky=tk.W, padx=(20, 5))
        self.latest_month_label = ttk.Label(status_frame, text="Unknown", font=("Helvetica", 9))
        self.latest_month_label.grid(row=1, column=3, sticky=tk.W)
        
        ttk.Label(status_frame, text="Status:", font=("Helvetica", 9, "bold")).grid(row=2, column=2, sticky=tk.W, padx=(20, 5))
        self.status_label = ttk.Label(status_frame, text="Ready", font=("Helvetica", 9), foreground=self.success_color)
        self.status_label.grid(row=2, column=3, sticky=tk.W)
        
        # ===== CONTROL PANEL =====
        control_frame = ttk.LabelFrame(main_frame, text="🎮 Controls", padding="10")
        control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.fetch_button = tk.Button(
            button_frame,
            text="▶️ Fetch Data",
            command=self.run_fetch,
            bg=self.accent_color,
            fg="black",
            font=("Helvetica", 11, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.fetch_button.grid(row=0, column=0, padx=(0, 10))
        
        self.refresh_button = tk.Button(
            button_frame,
            text="🔄 Force Refresh",
            command=self.force_refresh,
            bg=self.warning_color,
            fg="black",
            font=("Helvetica", 11, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.refresh_button.grid(row=0, column=1, padx=(0, 10))
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹️ Stop",
            command=self.stop_process,
            bg=self.error_color,
            fg="black",
            font=("Helvetica", 11, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.stop_button.grid(row=0, column=2)
        
        # Progress bar
        progress_frame = ttk.Frame(control_frame)
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=400
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.progress_label = ttk.Label(progress_frame, text="0%", font=("Helvetica", 9))
        self.progress_label.grid(row=0, column=1)
        
        # ===== LOG PANEL =====
        log_frame = ttk.LabelFrame(main_frame, text="📝 Activity Log", padding="10")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text area with scrollbar
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Courier", 9),
            bg="#ffffff",
            fg="#333333"
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colored output
        self.log_text.tag_config("info", foreground="#2196F3")
        self.log_text.tag_config("success", foreground="#4CAF50", font=("Courier", 9, "bold"))
        self.log_text.tag_config("warning", foreground="#FF9800")
        self.log_text.tag_config("error", foreground="#F44336", font=("Courier", 9, "bold"))
        self.log_text.tag_config("checkpoint", foreground="#9C27B0", font=("Courier", 9, "bold"))
        
        # Clear log button
        clear_button = ttk.Button(log_frame, text="Clear Log", command=self.clear_log)
        clear_button.grid(row=1, column=0, sticky=tk.E, pady=(5, 0))
        
        # ===== FOOTER =====
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        refresh_status_button = ttk.Button(
            footer_frame,
            text="🔄 Refresh Status",
            command=self.update_status_panel
        )
        refresh_status_button.grid(row=0, column=0, sticky=tk.W)
        
        footer_label = ttk.Label(
            footer_frame,
            text="Ministry of Health | Policy Research",
            font=("Helvetica", 8),
            foreground="#666666"
        )
        footer_label.grid(row=0, column=1, sticky=tk.E)
        footer_frame.columnconfigure(1, weight=1)
        
        self.log_message("Welcome! Click 'Fetch Data' to start collecting ABS labour force data.", "success")
        
        # Load saved API key (must be after log_text is created)
        self.load_api_key()
        
    def update_status_panel(self):
        """Update the status panel with checkpoint information."""
        checkpoint_file = "abs_fetch_checkpoint.json"
        
        if os.path.exists(checkpoint_file):
            try:
                with open(checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)
                
                # Update labels
                last_run = checkpoint.get('last_run')
                if last_run:
                    try:
                        dt = datetime.fromisoformat(last_run)
                        self.last_run_label.config(text=dt.strftime("%Y-%m-%d %H:%M"))
                        
                        # Calculate freshness
                        days_ago = (datetime.now() - dt).days
                        if days_ago == 0:
                            freshness_text = "Today"
                            freshness_color = self.success_color
                        elif days_ago == 1:
                            freshness_text = "Yesterday"
                            freshness_color = self.success_color
                        elif days_ago < 7:
                            freshness_text = f"{days_ago} days ago"
                            freshness_color = self.success_color
                        elif days_ago < 30:
                            freshness_text = f"{days_ago} days ago"
                            freshness_color = self.warning_color
                        else:
                            freshness_text = f"{days_ago} days ago (Needs refresh)"
                            freshness_color = self.error_color
                        
                        self.freshness_label.config(text=freshness_text, foreground=freshness_color)
                    except:
                        self.last_run_label.config(text="Unknown")
                else:
                    self.last_run_label.config(text="Never")
                
                # Total records
                total_records = checkpoint.get('total_records', 0)
                self.total_records_label.config(text=f"{total_records:,}")
                
                # Completed combinations
                completed = len(checkpoint.get('completed_combinations', {}))
                self.completed_label.config(text=f"{completed} / 1620")
                
                # Latest month
                latest_months = []
                for combo_data in checkpoint.get('completed_combinations', {}).values():
                    latest_month = combo_data.get('latest_month')
                    if latest_month:
                        latest_months.append(latest_month)
                
                if latest_months:
                    latest = max(latest_months)
                    self.latest_month_label.config(text=latest)
                else:
                    self.latest_month_label.config(text="Unknown")
                
                self.log_message("Status updated from checkpoint", "info")
                
            except Exception as e:
                self.log_message(f"Error reading checkpoint: {e}", "error")
                self.last_run_label.config(text="Error")
                self.freshness_label.config(text="Error")
        else:
            self.last_run_label.config(text="Never")
            self.total_records_label.config(text="0")
            self.completed_label.config(text="0 / 1620")
            self.freshness_label.config(text="No data yet")
            self.latest_month_label.config(text="N/A")
            self.log_message("No checkpoint found. Ready for first run.", "info")
    
    def log_message(self, message, level="info"):
        """Add a message to the log with timestamp and color."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, formatted_message, level)
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Clear the log text area."""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared", "info")
    
    def update_session_stats(self):
        """Update the session statistics label."""
        stats_text = f"✅ {self.session_fetched} | ❌ {self.session_failed} | 🚫 {self.session_not_available}"
        self.session_label.config(text=stats_text)
    
    def load_api_key(self):
        """Load API key from config file."""
        config_file = "abs_api_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    api_key = config.get('api_key', '')
                    self.api_key_var.set(api_key)
                    if api_key:
                        self.log_message(f"API key loaded ({api_key[:8]}...{api_key[-4:]})", "info")
            except Exception as e:
                self.log_message(f"Error loading API key: {e}", "error")
        else:
            self.log_message("No API key configured. Please enter your API key above.", "warning")
    
    def save_api_key(self):
        """Save API key to config file."""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("No API Key", "Please enter an API key before saving.")
            return
        
        config_file = "abs_api_config.json"
        try:
            config = {'api_key': api_key}
            with open(config_file, 'w') as f:
                json.dump(config, f)
            self.log_message(f"✅ API key saved ({api_key[:8]}...{api_key[-4:]})", "success")
            messagebox.showinfo("Success", "API key saved successfully!")
        except Exception as e:
            self.log_message(f"Error saving API key: {e}", "error")
            messagebox.showerror("Error", f"Failed to save API key: {e}")
    
    def show_help(self):
        """Show help dialog with explanations of all buttons and icons."""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - ABS Data Fetcher")
        help_window.geometry("700x600")
        help_window.resizable(False, False)
        
        # Make it modal
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Create scrollable frame
        canvas = tk.Canvas(help_window, bg="white")
        scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Help content
        help_text = tk.Text(scrollable_frame, wrap=tk.WORD, width=80, height=35, 
                           font=("Helvetica", 11), bg="white", relief=tk.FLAT)
        help_text.pack(padx=20, pady=20)
        
        # Configure tags for formatting
        help_text.tag_config("title", font=("Helvetica", 16, "bold"), foreground="#2196F3")
        help_text.tag_config("section", font=("Helvetica", 13, "bold"), foreground="#333", spacing1=10)
        help_text.tag_config("button", font=("Helvetica", 11, "bold"), foreground="#2196F3")
        help_text.tag_config("icon", font=("Helvetica", 11, "bold"))
        help_text.tag_config("normal", font=("Helvetica", 11))
        
        # Insert help content
        help_content = """ABS Data Fetcher - Quick Help Guide

═══════════════════════════════════════════════════

🔑 API KEY CONFIGURATION

API Key Field
   • Enter your API key from https://developer.vic.gov.au
   • Format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   • Click "💾 Save" to store it securely
   • Saved API key loads automatically on startup
   • Required before you can fetch data

Getting Your API Key
   1. Go to https://developer.vic.gov.au
   2. Register or log in
   3. Create API Access Request for "ABS Labour Force API"
   4. Copy your API key
   5. Paste it in the API Key field above
   6. Click Save!

═══════════════════════════════════════════════════

🎮 CONTROL BUTTONS

▶️ Fetch Data (Blue Button)
   • Starts data collection from ABS API
   • First run: ~65 minutes (fetches all data)
   • Monthly run: ~10 seconds (if data < 30 days old)
   • Progress saved every 2 minutes (checkpoint)
   • Automatically creates formatted CSV at the end
   • Safe to stop and resume later

🔄 Force Refresh (Orange Button)
   • Deletes checkpoint and forces full re-fetch
   • Use when you need guaranteed fresh data
   • Next run will take ~65 minutes
   • Asks for confirmation before proceeding

⏹️ Stop (Red Button)
   • Safely stops current operation
   • Progress is automatically saved to checkpoint
   • Can resume by clicking "Fetch Data" again
   • Only active when a process is running

═══════════════════════════════════════════════════

📊 STATUS PANEL FIELDS

Last Run
   • When data was last collected
   • Format: YYYY-MM-DD HH:MM

Total Records
   • Total number of data records in your dataset
   • ~930,000 records for complete dataset

Completed
   • Progress: X / 1620 combinations
   • 1620 = total possible data combinations

This Session
   • ✅ Fetched: Successful data requests
   • ❌ Failed: Real errors (check logs)
   • 🚫 Not Available: Data combinations that don't exist (normal)

Data Freshness
   • How old your data is
   • Colors:
     - Green: Fresh (< 7 days)
     - Orange: Aging (7-30 days)
     - Red: Needs refresh (> 30 days)

Latest Month
   • Most recent data point in your dataset
   • Format: YYYY-MM (e.g., 2025-10)

Status
   • Current operation status
   • "Ready" = idle, can start new operation
   • "Fetching..." = data collection in progress
   • "Fixing..." = CSV formatting in progress

═══════════════════════════════════════════════════

📝 ACTIVITY LOG COLORS

🔵 Blue Text (Info)
   • General information and progress updates
   • "Progress: [50/1620] (3.1%)"

🟢 Green Text (Success)
   • Successful operations
   • "✅ AUSTRALIA/CIVILIAN_POPULATION/MALES/ORIGINAL: 573 records"

🟣 Purple Text (Checkpoint)
   • Checkpoint saves (every ~2 minutes)
   • "💾 Checkpoint saved (50 successful, 0 failed)"

🟠 Orange Text (Warning)
   • Data not available (404s - normal)
   • "🚫 AUSTRALIA/.../SEASONALLY_ADJUSTED: Not available in API"

🔴 Red Text (Error)
   • Real errors that need attention
   • Authentication failures, network issues, etc.

═══════════════════════════════════════════════════

🎯 ICONS & SYMBOLS

✅ - Success / Data fetched
❌ - Error / Failed request
🚫 - Not available (404)
💾 - Checkpoint saved
🔵 - Info message
🟢 - Success message
🟣 - Checkpoint message
🟠 - Warning message
🔴 - Error message

═══════════════════════════════════════════════════

💡 TIPS

1. Monthly Routine
   • Just click "Fetch Data" once a month
   • If data < 30 days old, completes in seconds!

2. First Time Use
   • First run takes ~65 minutes
   • Watch for purple checkpoint saves
   • Don't worry about orange "not available" messages

3. After Crash
   • Just click "Fetch Data" again
   • Script resumes from last checkpoint automatically

4. Progress Bar
   • Shows 0-100% progress
   • Updates during data fetch
   • May jump in increments (not smooth)

5. Force Refresh
   • Use quarterly for highest quality data
   • Or when troubleshooting issues

═══════════════════════════════════════════════════

❓ Need More Help?

See documentation files:
• GUI_GUIDE.md - Complete user manual
• ABS_DATA_ONBOARDING.md - Full system docs
• CHECKPOINT_GUIDE.md - Checkpoint details
"""
        
        help_text.insert("1.0", help_content)
        help_text.config(state=tk.DISABLED)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        button_frame = ttk.Frame(help_window)
        button_frame.pack(side="bottom", pady=10)
        
        close_button = tk.Button(
            button_frame,
            text="Got it!",
            command=help_window.destroy,
            bg=self.success_color,
            fg="black",
            font=("Helvetica", 11, "bold"),
            padx=30,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        close_button.pack()
        
        # Center the window
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (help_window.winfo_width() // 2)
        y = (help_window.winfo_screenheight() // 2) - (help_window.winfo_height() // 2)
        help_window.geometry(f'+{x}+{y}')
    
    def set_buttons_state(self, running=False):
        """Enable or disable buttons based on running state."""
        state = tk.DISABLED if running else tk.NORMAL
        self.fetch_button.config(state=state)
        self.refresh_button.config(state=state)
        self.stop_button.config(state=tk.NORMAL if running else tk.DISABLED)
    
    def run_fetch(self):
        """Run the data fetch script in a separate thread."""
        if self.is_running:
            messagebox.showwarning("Already Running", "A process is already running. Please wait or stop it first.")
            return
        
        # Check if API key is configured
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showerror("No API Key", "Please enter and save your API key before fetching data.")
            return
        
        self.is_running = True
        self.set_buttons_state(running=True)
        self.progress_var.set(0)
        self.status_label.config(text="Fetching data...", foreground=self.accent_color)
        
        # Reset session counters
        self.session_fetched = 0
        self.session_failed = 0
        self.session_not_available = 0
        self.update_session_stats()
        
        self.log_message("Starting data fetch...", "info")
        
        thread = threading.Thread(target=self._run_fetch_thread, daemon=True)
        thread.start()
    
    def _run_fetch_thread(self):
        """Thread worker for running fetch script."""
        try:
            # Get API key from the entry field
            api_key = self.api_key_var.get().strip()
            
            self.current_process = subprocess.Popen(
                ['python3', 'fetch_abs_data_auto.py', '--api-key', api_key],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Read output line by line
            for line in self.current_process.stdout:
                line = line.strip()
                if line:
                    self.log_queue.put(line)
                    
                    # Parse progress
                    if "Progress:" in line and "[" in line and "/" in line:
                        try:
                            # Extract [current/total]
                            parts = line.split("[")[1].split("]")[0]
                            current, total = parts.split("/")
                            progress = (int(current) / int(total)) * 100
                            self.progress_queue.put(progress)
                        except:
                            pass
            
            self.current_process.wait()
            
            if self.current_process.returncode == 0:
                self.log_queue.put("SUCCESS:Data fetch completed successfully!")
                self.progress_queue.put(100)
            else:
                self.log_queue.put(f"ERROR:Data fetch failed with exit code {self.current_process.returncode}")
            
        except Exception as e:
            self.log_queue.put(f"ERROR:Exception during fetch: {e}")
        finally:
            self.log_queue.put("DONE")
    
    def run_fix_csv(self):
        """Run the CSV fix script."""
        if self.is_running:
            messagebox.showwarning("Already Running", "A process is already running. Please wait or stop it first.")
            return
        
        self.is_running = True
        self.set_buttons_state(running=True)
        self.status_label.config(text="Fixing CSV...", foreground=self.accent_color)
        self.log_message("Starting CSV fix...", "info")
        
        thread = threading.Thread(target=self._run_fix_csv_thread, daemon=True)
        thread.start()
    
    def _run_fix_csv_thread(self):
        """Thread worker for running CSV fix script."""
        try:
            self.current_process = subprocess.Popen(
                ['python3', 'fix_abs_csv.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            output, _ = self.current_process.communicate()
            
            for line in output.split('\n'):
                if line.strip():
                    self.log_queue.put(line.strip())
            
            if self.current_process.returncode == 0:
                self.log_queue.put("SUCCESS:CSV fix completed successfully!")
            else:
                self.log_queue.put(f"ERROR:CSV fix failed with exit code {self.current_process.returncode}")
        
        except Exception as e:
            self.log_queue.put(f"ERROR:Exception during CSV fix: {e}")
        finally:
            self.log_queue.put("DONE")
    
    def force_refresh(self):
        """Force a full refresh by deleting checkpoint."""
        if self.is_running:
            messagebox.showwarning("Process Running", "Cannot force refresh while a process is running.")
            return
        
        result = messagebox.askyesno(
            "Force Refresh",
            "This will delete the checkpoint and fetch ALL data from scratch (~65 minutes).\n\nAre you sure?"
        )
        
        if result:
            checkpoint_file = "abs_fetch_checkpoint.json"
            if os.path.exists(checkpoint_file):
                try:
                    os.remove(checkpoint_file)
                    self.log_message("Checkpoint deleted. Next run will fetch all data.", "warning")
                    self.update_status_panel()
                except Exception as e:
                    self.log_message(f"Error deleting checkpoint: {e}", "error")
            else:
                self.log_message("No checkpoint to delete.", "warning")
    
    def stop_process(self):
        """Stop the currently running process."""
        if self.current_process:
            result = messagebox.askyesno("Stop Process", "Are you sure you want to stop the current process?")
            if result:
                self.current_process.terminate()
                self.log_message("Process stopped by user", "warning")
                self.is_running = False
                self.set_buttons_state(running=False)
                self.status_label.config(text="Stopped", foreground=self.warning_color)
    
    def check_queues(self):
        """Check message queues for updates from worker threads."""
        # Check log queue
        try:
            while True:
                message = self.log_queue.get_nowait()
                
                if message == "DONE":
                    self.is_running = False
                    self.set_buttons_state(running=False)
                    self.status_label.config(text="Ready", foreground=self.success_color)
                    self.update_status_panel()
                elif message.startswith("SUCCESS:"):
                    self.log_message(message.replace("SUCCESS:", ""), "success")
                elif message.startswith("ERROR:"):
                    self.log_message(message.replace("ERROR:", ""), "error")
                elif "💾 Checkpoint saved" in message or "Checkpoint saved" in message:
                    self.log_message(message, "checkpoint")
                    # Extract stats from checkpoint message if present
                    if "(" in message and "successful" in message:
                        try:
                            parts = message.split("(")[1].split(")")[0]
                            if "successful" in parts:
                                success_num = int(parts.split("successful")[0].strip())
                                self.session_fetched = success_num
                            if "failed" in parts:
                                failed_num = int(parts.split("failed")[0].split(",")[-1].strip())
                                self.session_failed = failed_num
                            self.update_session_stats()
                        except:
                            pass
                elif "🚫" in message or ("Not available in API" in message):
                    self.session_not_available += 1
                    self.update_session_stats()
                    self.log_message(message, "warning")
                elif "✅" in message and "records" in message and "latest:" in message:
                    # This is a successful fetch message with details
                    self.log_message(message, "success")
                elif "ERROR" in message and "Error fetching" in message:
                    self.session_failed += 1
                    self.update_session_stats()
                    self.log_message(message, "error")
                elif "❌" in message or "Error" in message or "Failed" in message:
                    self.log_message(message, "error")
                elif "✅" in message or "Success" in message or "Complete" in message:
                    self.log_message(message, "success")
                elif "⚠️" in message or "Warning" in message:
                    self.log_message(message, "warning")
                elif "Progress:" in message:
                    self.log_message(message, "info")
                    # Update session stats from progress message
                    if "Fetched:" in message:
                        try:
                            parts = message.split("Fetched:")[1].split(",")[0].strip()
                            self.session_fetched = int(parts)
                            if "Failed:" in message:
                                failed_parts = message.split("Failed:")[1].split(",")[0].strip()
                                self.session_failed = int(failed_parts)
                            self.update_session_stats()
                        except:
                            pass
                else:
                    self.log_message(message, "info")
        except queue.Empty:
            pass
        
        # Check progress queue
        try:
            while True:
                progress = self.progress_queue.get_nowait()
                self.progress_var.set(progress)
                self.progress_label.config(text=f"{progress:.1f}%")
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_queues)

def main():
    """Main entry point."""
    root = tk.Tk()
    app = ABSDataFetcherGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()

