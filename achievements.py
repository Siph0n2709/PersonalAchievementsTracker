from tkinter import * 
import tkinter as tk
# from tkinter import ttk # ttk is not used in your provided code for these elements
from datetime import datetime # Added for timestamping

root = Tk()
root.title("Daily Achievements")
root.geometry("500x500")

titleLabel = tk.Label(root, text="Daily Achievements", font=("Arial", 16))
titleLabel.pack(pady=10)

date_str_var = tk.StringVar() 
def update_date():
    current_date = datetime.now().strftime("%B %d, %Y")
    date_str_var.set("Today's Date: " + current_date)
update_date()
dateLabel = tk.Label(root, textvariable=date_str_var, font=("Arial", 12))
dateLabel.pack(pady=5)

# Variables for Checkbuttons
schoolwork_var = tk.BooleanVar()
leetcode_var = tk.BooleanVar()
show_entry_var = tk.BooleanVar() 
show_entry_var.set(False) 

schoolworkCheck = tk.Checkbutton(root, text="Complete Schoolwork", font=("Arial", 12), variable=schoolwork_var)
schoolworkCheck.pack(anchor='center', padx=20, pady=2)

leetCodeCheck = tk.Checkbutton(root, text="Solve 3 LeetCode Problems", font=("Arial", 12), variable=leetcode_var)
leetCodeCheck.pack(anchor='center', padx=20, pady=2)

# This is the function that needed the fix:
def toggle_entry_visibility():
    if show_entry_var.get():
        if not detail_entry.winfo_ismapped():
            # Ensure detail_entry is packed directly after the gym checkbox
            detail_entry.pack(pady=(5,2), padx=10, fill=tk.X, after=show_details_checkbox)
    else:
        detail_entry.pack_forget()

show_details_checkbox = tk.Checkbutton(
    root,
    text="Gym Day?",
    font=("Arial", 12),
    variable=show_entry_var, 
    command=toggle_entry_visibility 
)
show_details_checkbox.pack(pady=2, padx=10, anchor='center')

detail_entry_placeholder = "Enter gym details here..."
detail_entry = tk.Entry(root, width=50, font=("Arial", 12), justify='center')
detail_entry.insert(0, detail_entry_placeholder)
# IMPORTANT: Call toggle_entry_visibility AFTER detail_entry is created and show_details_checkbox is packed.
# The initial pack order is important if the checkbox starts as checked (though it doesn't here).

daily_achievements_placeholder = "Enter your daily achievements here..."
dailyAchievements = tk.Entry(root, font=("Arial", 12), justify='center')
dailyAchievements.insert(0, daily_achievements_placeholder)
dailyAchievements.pack(pady=(5,10), padx=10, fill=tk.X) 

# Initial call to set visibility based on the default state of show_entry_var
toggle_entry_visibility()


# --- Function to handle submit action ---
def submit_action():
    # 1. Retrieve Data
    log_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_date_val = date_str_var.get().replace("Today's Date: ", "")

    schoolwork_done = schoolwork_var.get()
    leetcode_done = leetcode_var.get()
    gym_day_selected = show_entry_var.get()
    
    gym_details_text = detail_entry.get()
    achievements_text = dailyAchievements.get()

    # Prepare content for the file
    file_lines = []
    file_lines.append(f"Log Timestamp: {log_timestamp}\n")
    file_lines.append(f"Report Date: {report_date_val}\n\n")
    file_lines.append("Tasks:\n")
    file_lines.append(f"- Complete Schoolwork: {'Yes' if schoolwork_done else 'No'}\n")
    file_lines.append(f"- Solve 3 LeetCode Problems: {'Yes' if leetcode_done else 'No'}\n")
    file_lines.append(f"- Gym Day: {'Yes' if gym_day_selected else 'No'}\n")

    if gym_day_selected:
        if gym_details_text != detail_entry_placeholder and gym_details_text.strip():
            file_lines.append(f"  Gym Details: {gym_details_text}\n")
        else:
            file_lines.append("  Gym Details: (Not specified or placeholder left)\n")
    
    file_lines.append("\nOther Achievements:\n")
    if achievements_text != daily_achievements_placeholder and achievements_text.strip():
        file_lines.append(f"{achievements_text}\n")
    else:
        file_lines.append("(Not specified or placeholder left)\n")
    file_lines.append("-" * 30 + "\n\n")

    # 2. Store Data to File
    try:
        with open("daily_achievements_log.txt", "a", encoding="utf-8") as f:
            f.writelines(file_lines)
        print("Data saved to daily_achievements_log.txt")
    except Exception as e:
        print(f"Error saving data to file: {e}")

    # 3. Clear Everything from the Screen
    for widget in root.winfo_children():
        widget.destroy()

    # 4. Display "Well Done! Goodbye."
    final_message_label = tk.Label(
        root, 
        text="Well Done! Goodbye.", 
        font=("Arial", 20, "bold"), 
        fg="green" 
    )
    final_message_label.pack(expand=True, pady=50)

# --- Submit Button ---
submitButton = tk.Button(root, text="Submit Achievements", font=("Arial", 12), command=submit_action)
submitButton.pack(pady=10)

root.mainloop()