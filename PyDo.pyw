# PyDo To-Do Application

'''

██████╗ ██╗   ██╗██████╗  ██████╗ 
██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗
██████╔╝ ╚████╔╝ ██║  ██║██║   ██║
██╔═══╝   ╚██╔╝  ██║  ██║██║   ██║
██║        ██║   ██████╔╝╚██████╔╝
╚═╝        ╚═╝   ╚═════╝  ╚═════╝ 
                                  
                  
'''
import tkinter as tk
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
        self.root.geometry('250x200')  # Window size: width x height

        # Set the window background and text color
        self.root.configure(bg='black')  # Background color
        self.root.tk_setPalette(background='black', foreground='#00FF00')  # Text color
        
        # File where tasks will be saved
        self.tasks_file = "tasks.txt"
        # Initialize an empty list to keep track of tasks
        self.tasks = []
        
        # Frame for entering new tasks
        self.entry_frame = tk.Frame(self.root, bg='black')
        self.entry_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Entry widget for inputting tasks
        self.task_entry = tk.Entry(self.entry_frame, insertbackground='#00FF00', fg='#00FF00', bg='black', font=('Arial', 12))
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Button to add new tasks to the list
        self.add_button = tk.Button(self.entry_frame, text="Add", fg='#00FF00', bg='black', command=self.add_task, font=('Arial', 12))
        self.add_button.pack(side=tk.RIGHT)
        
        # Frame to display current tasks
        self.tasks_frame = tk.Frame(self.root, bg='black')
        self.tasks_frame.pack(fill=tk.BOTH, expand=True)
        
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
            self.task_entry.delete(0, tk.END)

    # Helper function to add task from file
    def add_task_from_file(self, task_text):
        if task_text:
            self.add_task_to_list(task_text)

    # Add a task to the task list and display it
    def add_task_to_list(self, task_text):
        task_frame = tk.Frame(self.tasks_frame, bg='black')
        task_label = tk.Label(task_frame, text=task_text, fg='#00FF00', bg='black', font=('Arial', 12))
        task_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Buttons for task manipulation: delete, move up, and move down
        delete_button = tk.Button(task_frame, text="X", command=lambda: self.delete_task(task_frame), fg='#00FF00', bg='black', font=('Arial', 8))
        delete_button.pack(side=tk.RIGHT)
        up_button = tk.Button(task_frame, text="↑", command=lambda: self.move_task_up(task_frame), fg='#00FF00', bg='black', font=('Arial', 8))
        up_button.pack(side=tk.RIGHT)
        down_button = tk.Button(task_frame, text="↓", command=lambda: self.move_task_down(task_frame), fg='#00FF00', bg='black', font=('Arial', 8))
        down_button.pack(side=tk.RIGHT)
        
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
            task_frame.pack(fill=tk.X)

    # Keep the PyDo application window always on top of other windows
    def set_window_on_top(self):
        self.root.call('wm', 'attributes', '.', '-topmost', '1')

    # Flash the task window to grab the user's attention
    def flash_window(self):
        flash_duration = 5  # seconds
        flash_color = '#FF0000'
        end_time = time.time() + flash_duration
        while time.time() < end_time:
            for task_frame, task_label, _ in self.tasks:
                task_frame.config(bg=flash_color)
                task_label.config(bg=flash_color)
            time.sleep(0.5)
            for task_frame, task_label, _ in self.tasks:
                task_frame.config(bg='black')
                task_label.config(bg='black')
            time.sleep(0.5)

    # Start a timer that triggers the window flashing effect
    def start_flash_timer(self):
        interval = 1800  # 30 minutes

        # Timer function to flash the window periodically
        def timer():
            while True:
                time.sleep(interval)
                self.flash_window()

        threading.Thread(target=timer, daemon=True).start()

# Main execution point of the script
if __name__ == "__main__":
    root = tk.Tk()
    app = PyDo(root)
    root.mainloop()
