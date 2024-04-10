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

class PyDo:
    def __init__(self, root):
        """
        Initialize the main application window with its components.
        """
        # Set the window title and dimensions
        self.root = root
        self.root.title("PyDo")
        self.root.geometry('250x200')  # Width x Height

        # Configure the main window's background color
        self.root.configure(bg='black')
        self.root.tk_setPalette(background='black', foreground='#00FF00')
        
        # Create and pack the frame for entering new tasks at the bottom
        self.entry_frame = tk.Frame(self.root, bg='black')
        self.entry_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create and pack the entry widget for inputting new tasks
        self.task_entry = tk.Entry(self.entry_frame, insertbackground='#00FF00', fg='#00FF00', bg='black', font=('Arial', 12))
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Create and pack the button to add new tasks
        self.add_button = tk.Button(self.entry_frame, text="Add", fg='#00FF00', bg='black', command=self.add_task, font=('Arial', 12))
        self.add_button.pack(side=tk.RIGHT)
        
        # Create and pack the frame that will contain the tasks
        self.tasks_frame = tk.Frame(self.root, bg='black')
        self.tasks_frame.pack(fill=tk.BOTH, expand=True)
        
        # A list to keep track of all tasks
        self.tasks = []

        # Configure the window to stay on top and start the timer for flashing
        self.set_window_on_top()
        self.start_flash_timer()

    def add_task(self):
        """
        Add a new task to the list when the Add button is clicked.
        """
        # Get the text from the entry widget
        task_text = self.task_entry.get()
        if task_text:
            # Create a frame for the new task
            task_frame = tk.Frame(self.tasks_frame, bg='black')
            
            # Create and pack a label in the task frame for the task text
            task_label = tk.Label(task_frame, text=task_text, fg='#00FF00', bg='black', font=('Arial', 12))
            task_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Create and pack a delete button in the task frame
            delete_button = tk.Button(task_frame, text="X", command=lambda: self.delete_task(task_frame), fg='#00FF00', bg='black', font=('Arial', 8))
            delete_button.pack(side=tk.RIGHT)
            
            # Create and pack buttons to move the task up and down
            up_button = tk.Button(task_frame, text="↑", command=lambda: self.move_task_up(task_frame), fg='#00FF00', bg='black', font=('Arial', 8))
            up_button.pack(side=tk.RIGHT)
            
            down_button = tk.Button(task_frame, text="↓", command=lambda: self.move_task_down(task_frame), fg='#00FF00', bg='black', font=('Arial', 8))
            down_button.pack(side=tk.RIGHT)
            
            # Add the new task to the list of tasks and redraw the task list
            self.tasks.append((task_frame, task_text))
            self.redraw_tasks()
            self.task_entry.delete(0, tk.END)

    def delete_task(self, task_frame):
        """
        Delete a task from the list.
        """
        self.tasks = [task for task in self.tasks if task[0] != task_frame]
        task_frame.destroy()
        self.redraw_tasks()

    def move_task_up(self, task_frame):
        """
        Move a task up in the list.
        """
        index = next((i for i, task in enumerate(self.tasks) if task[0] == task_frame), None)
        if index is not None and index > 0:
            self.tasks[index - 1], self.tasks[index] = self.tasks[index], self.tasks[index - 1]
            self.redraw_tasks()

    def move_task_down(self, task_frame):
        """
        Move a task down in the list.
        """
        index = next((i for i, task in enumerate(self.tasks) if task[0] == task_frame), None)
        if index is not None and index < len(self.tasks) - 1:
            self.tasks[index + 1], self.tasks[index] = self.tasks[index], self.tasks[index + 1]
            self.redraw_tasks()

    def redraw_tasks(self):
        """
        Redraw all tasks in the list to reflect the current order.
        """
        for task_frame, _ in self.tasks:
            task_frame.pack_forget()
            task_frame.pack(fill=tk.X)

    def set_window_on_top(self):
        """
        Keep the application window always on top of other windows.
        """
        self.root.call('wm', 'attributes', '.', '-topmost', '1')

    def flash_window(self):
        """
        Flash the window to grab the user's attention.
        """
        flash_duration = 3  # seconds
        original_color = self.tasks_frame.cget('bg')
        flash_color = '#FF0000' if original_color != '#FF0000' else '#00FF00'
        end_time = time.time() + flash_duration
        while time.time() < end_time:
            self.tasks_frame.config(bg=flash_color)
            time.sleep(0.5)
            self.tasks_frame.config(bg=original_color)
            time.sleep(0.5)

    def start_flash_timer(self):
        """
        Start a timer that triggers the window flashing every 30 minutes.
        """
        interval = 1800  # 30 minutes

        def timer():
            while True:
                time.sleep(interval)
                self.flash_window()

        threading.Thread(target=timer, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PyDo(root)
    root.mainloop()
