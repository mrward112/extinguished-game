import tkinter as tk
from tkinter import messagebox
import main

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")

        # Set the window size to match the game's screen size
        self.game_screen_width = 800
        self.game_screen_height = 600
        self.center_window(self.game_screen_width, self.game_screen_height)

        # Create Canvas with black background
        self.canvas = tk.Canvas(self.root, width=self.game_screen_width, height=self.game_screen_height, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Initialize variables for buttons
        self.play_button = None
        self.settings_button = None
        self.exit_button = None

        # Create Main Menu
        self.main_menu()

    def center_window(self, width, height):
        # Get the screen's width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate the position to center the window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the geometry of the window
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def clear_screen(self):
        # Destroy all buttons and labels within the canvas
        for widget in self.canvas.winfo_children():
            widget.destroy()
        
        # Pack the canvas again to avoid TclError
        self.canvas.pack(fill="both", expand=True)

    def main_menu(self):
        self.clear_screen()

        self.root.title("Main Menu")

        self.play_button = self.add_button("Play", self.play_menu, 200)
        self.settings_button = self.add_button("Settings", self.settings_menu, 300)
        self.exit_button = self.add_button("Exit", self.root.quit, 400)

    def add_button(self, text, command, y):
        button = tk.Button(self.canvas, text=text, command=command, width=20, height=2)
        self.canvas.create_window(self.game_screen_width//2, y, window=button)
        return button

    def play_menu(self):
        self.clear_screen()

        self.root.title("Select Difficulty")

        self.add_button("Intro", lambda: self.start_game("Intro"), 150)
        self.add_button("Easy", lambda: self.start_game("Easy"), 200)
        self.add_button("Medium", lambda: self.start_game("Medium"), 250)
        self.add_button("Hard", lambda: self.start_game("Hard"), 300)
        self.add_button("Back", self.main_menu, 400)

    def settings_menu(self):
        self.clear_screen()

        self.root.title("Settings")

        tk.Label(self.canvas, text="Settings", font=('Arial', 24)).place(x=self.game_screen_width//2-70, y=50)

        tk.Label(self.canvas, text="Volume", font=('Arial', 14)).place(x=self.game_screen_width//2-35, y=150)
        # Calculate the appropriate length for the Scale based on button width
        scale_length = 20 * 20  # Assuming average button width of 20 characters
        volume_scale = tk.Scale(self.canvas, from_=1, to=10, orient=tk.HORIZONTAL, length=scale_length)
        volume_scale.place(x=self.game_screen_width//2-scale_length//2, y=180)

        self.add_button("Credits", self.show_credits, 250)
        self.add_button("Back", self.main_menu, 400)

    def show_credits(self):
        messagebox.showinfo("Credits", "1. Derek Arima (Documentation Manager) \n2. Jake Graham (Quality Assurance) \n3. Merrick Ward (Configuration Manager) \n4. Michael Child (Team Leader) \n5. Nathan Jensen (Graphic Designer) \n6. Wolf Wetzel (Project Manager)")

    def start_game(self, difficulty):
        # Run the main.py script
        if difficulty == "Intro":
            main.main(1)
        elif difficulty == "Easy":
            main.main(2)
        elif difficulty == "Medium":
            messagebox.showinfo("Game Start", f"Starting {difficulty} level!")
        elif difficulty == "Hard":
            messagebox.showinfo("Game Start", f"Starting {difficulty} level!")
        else:
            messagebox.showinfo("Game Start", f"Starting {difficulty} level!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()
