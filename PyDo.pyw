# PyDo To-Do Application

'''

██████╗ ██╗   ██╗██████╗  ██████╗ 
██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗
██████╔╝ ╚████╔╝ ██║  ██║██║   ██║
██╔═══╝   ╚██╔╝  ██║  ██║██║   ██║
██║        ██║   ██████╔╝╚██████╔╝
╚═╝        ╚═╝   ╚═════╝  ╚═════╝ 
                                  
                  
'''
import customtkinter as ctk
import threading
import time
import os

# Main class for the PyDo application
class PyDo:
    # Constructor to initialize the application
    def __init__(self, root):
        # Setting up the main window with title and size
        self.root = root
        self.root.title("PyDo")  # Window title
        self.root.geometry('300x400')  # Window size: width x height

        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # File where tasks will be saved
        self.tasks_file = "tasks.txt"
        # Initialize an empty list to keep track of tasks
        self.tasks = []
        
        # Frame for entering new tasks
        self.entry_frame = ctk.CTkFrame(self.root)
        self.entry_frame.pack(side=ctk.BOTTOM, fill=ctk.X)
        
        # Entry widget for inputting tasks
        self.task_entry = ctk.CTkEntry(self.entry_frame, font=('Arial', 12))
        self.task_entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        
        # Button to add new tasks to the list
        self.add_button = ctk.CTkButton(self.entry_frame, text="Add", command=self.add_task, font=('Arial', 12), width=50)
        self.add_button.pack(side=ctk.RIGHT)
        
        # Frame to display current tasks
        self.tasks_frame = ctk.CTkFrame(self.root)
        self.tasks_frame.pack(fill=ctk.BOTH, expand=True)
        
        # Load previously saved tasks from file
        self.load_tasks()
        # Keep application window always on top
        self.set_window_on_top()
        # Start a timer to periodically flash the tasks window
        self.start_flash_timer()

    # Load tasks from a file, creating each task in the UI
    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as file:
                for line in file:
                    self.add_task_from_file(line.strip())

    # Add task from user input
    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            self.add_task_to_list(task_text)
            self.save_tasks()
            self.task_entry.delete(0, ctk.END)

    # Helper function to add task from file
    def add_task_from_file(self, task_text):
        if task_text:
            self.add_task_to_list(task_text)

    # Add a task to the task list and display it
    def add_task_to_list(self, task_text):
        task_frame = ctk.CTkFrame(self.tasks_frame)
        task_label = ctk.CTkLabel(task_frame, text=task_text, font=('Arial', 12))
        task_label.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        
        # Buttons for task manipulation: delete, move up, and move down
        delete_button = ctk.CTkButton(task_frame, text="X", command=lambda: self.delete_task(task_frame), font=('Arial', 8), width=20)
        delete_button.pack(side=ctk.RIGHT)
        up_button = ctk.CTkButton(task_frame, text="↑", command=lambda: self.move_task_up(task_frame), font=('Arial', 8), width=20)
        up_button.pack(side=ctk.RIGHT)
        down_button = ctk.CTkButton(task_frame, text="↓", command=lambda: self.move_task_down(task_frame), font=('Arial', 8), width=20)
        down_button.pack(side=ctk.RIGHT)
        
        # Add the new task to the internal list and redraw the task list
        self.tasks.append((task_frame, task_label, task_text))
        self.redraw_tasks()

    # Save the current task list to a file
    def save_tasks(self):
        with open(self.tasks_file, "w") as file:
            for _, _, task_text in self.tasks:
                file.write(task_text + "\n")

    # Delete a task from the list and UI
    def delete_task(self, task_frame):
        self.tasks = [task for task in self.tasks if task[0] != task_frame]
        task_frame.destroy()
        self.redraw_tasks()
        self.save_tasks()

    # Move a task up in the list
    def move_task_up(self, task_frame):
        index = next((i for i, task in enumerate(self.tasks) if task[0] == task_frame), None)
        if index is not None and index > 0:
            self.tasks[index - 1], self.tasks[index] = self.tasks[index], self.tasks[index - 1]
            self.redraw_tasks()
            self.save_tasks()

    # Move a task down in the list
    def move_task_down(self, task_frame):
        index = next((i for i, task in enumerate(self.tasks) if task[0] == task_frame), None)
        if index is not None and index < len(self.tasks) - 1:
            self.tasks[index + 1], self.tasks[index] = self.tasks[index], self.tasks[index + 1]
            self.redraw_tasks()
            self.save_tasks()

    # Redraw the tasks in the UI to reflect the current order
    def redraw_tasks(self):
        for task_frame, _, _ in self.tasks:
            task_frame.pack_forget()
            task_frame.pack(fill=ctk.X)

    # Keep the PyDo application window always on top of other windows
    def set_window_on_top(self):
        self.root.call('wm', 'attributes', '.', '-topmost', '1')

    # Flash the task window to grab the user's attention
    def flash_window(self):
        flash_duration = 5  # seconds
        flash_color = '#FF0000'
        original_color = self.tasks_frame.cget("fg_color")
        end_time = time.time() + flash_duration

        def flash():
            while time.time() < end_time:
                for task_frame, task_label, _ in self.tasks:
                    task_frame.configure(fg_color=flash_color)
                    task_label.configure(fg_color=flash_color)
                time.sleep(0.5)
                for task_frame, task_label, _ in self.tasks:
                    task_frame.configure(fg_color=original_color)
                    task_label.configure(fg_color=original_color)
                time.sleep(0.5)

        threading.Thread(target=flash, daemon=True).start()

    # Start a timer that triggers the window flashing effect
    def start_flash_timer(self):
        interval = 18  # 30 minutes

        # Timer function to flash the window periodically
        def timer():
            while True:
                time.sleep(interval)
                self.flash_window()

        threading.Thread(target=timer, daemon=True).start()

# Main execution point of the script
if __name__ == "__main__":
    root = ctk.CTk()
    app = PyDo(root)
    root.mainloop()
