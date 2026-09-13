import customtkinter as ctk

class SnippetApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Dictionary to store snippets temporarily in memory 
        # Format: {Title: {"code": code_text, "language": programming_language}}
        self.snippets = {}
        
        # State variable to track which snippet is currently loaded in the editor
        self.current_loaded_title = None

        # Configure the main application window
        self.title("Code Snippet Library")
        self.geometry("950x600")
        
        # Configure the grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Add a title to the sidebar
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Snippet Library", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Add a dropdown menu for language filtering
        self.language_option = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["All", "Python", "C++", "HTML", "SQL", "JavaScript"],
            command=self.update_snippet_list
        )
        self.language_option.grid(row=1, column=0, padx=20, pady=(10, 10))
        
        # Label for saved snippets section
        self.saved_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Saved Snippets:",
            font=ctk.CTkFont(weight="bold")
        )
        self.saved_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        
        # Scrollable frame to display saved snippets dynamically
        self.snippet_list_frame = ctk.CTkScrollableFrame(self.sidebar_frame, width=160)
        self.snippet_list_frame.grid(row=3, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Add a header for the editor area
        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="Editor - New Snippet", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Add a textbox to display and edit code snippets
        self.code_textbox = ctk.CTkTextbox(
            self.main_frame, 
            font=ctk.CTkFont(family="Consolas", size=14)
        )
        self.code_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Insert some placeholder text
        placeholder_text = "# Write or paste your code snippet here...\n"
        self.code_textbox.insert("0.0", placeholder_text)

        # --- Action Buttons ---
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="e")

        # Add button to delete the currently loaded snippet
        self.delete_button = ctk.CTkButton(
            self.button_frame, 
            text="Delete", 
            command=self.delete_snippet,
            fg_color="#ef4444", # Red color for destructive action
            hover_color="#dc2626",
            width=80
        )
        self.delete_button.grid(row=0, column=0, padx=(0, 10))

        # Add button to clear the editor
        self.clear_button = ctk.CTkButton(
            self.button_frame, 
            text="Clear Editor", 
            command=self.clear_editor,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            width=100
        )
        self.clear_button.grid(row=0, column=1, padx=(0, 10))

        # Add button to copy code
        self.copy_button = ctk.CTkButton(
            self.button_frame, 
            text="Copy Code", 
            command=self.copy_to_clipboard,
            width=100
        )
        self.copy_button.grid(row=0, column=2, padx=(0, 10))
        
        # Dropdown to select the language of the snippet being saved
        self.snippet_language_option = ctk.CTkOptionMenu(
            self.button_frame, 
            values=["Python", "C++", "HTML", "SQL", "JavaScript"],
            width=110
        )
        self.snippet_language_option.grid(row=0, column=3, padx=(0, 10))

        # Add button to save snippet
        self.save_button = ctk.CTkButton(
            self.button_frame, 
            text="Save Snippet", 
            command=self.save_snippet,
            width=120
        )
        self.save_button.grid(row=0, column=4)
        
    def clear_editor(self):
        # Delete all text and reset header
        self.code_textbox.delete("1.0", "end")
        self.header_label.configure(text="Editor - New Snippet")
        # Reset the current loaded snippet state
        self.current_loaded_title = None
        
    def copy_to_clipboard(self):
        # Copy text to clipboard and show visual feedback
        code_text = self.code_textbox.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(code_text)
        
        self.copy_button.configure(text="Copied!")
        self.after(1500, lambda: self.copy_button.configure(text="Copy Code"))
        
    def save_snippet(self):
        # Prompt for title
        dialog = ctk.CTkInputDialog(text="Enter a title for your snippet:", title="Save Snippet")
        snippet_title = dialog.get_input()
        
        if snippet_title:
            code_text = self.code_textbox.get("1.0", "end-1c")
            snippet_lang = self.snippet_language_option.get()
            
            # Save both the code and the chosen language in the dictionary
            self.snippets[snippet_title] = {
                "code": code_text,
                "language": snippet_lang
            }
            
            self.current_loaded_title = snippet_title
            self.header_label.configure(text=f"Editor - {snippet_title}")
            
            # Refresh the list to reflect the new snippet
            self.update_snippet_list()

    def delete_snippet(self):
        # Only attempt to delete if a snippet is actually loaded
        if self.current_loaded_title and self.current_loaded_title in self.snippets:
            # Remove the snippet from the dictionary
            del self.snippets[self.current_loaded_title]
            
            # Clear the editor screen and reset state
            self.clear_editor()
            
            # Update the UI list on the left
            self.update_snippet_list()
            
    def update_snippet_list(self, selected_filter=None):
        if selected_filter is None:
            selected_filter = self.language_option.get()
            
        # Clear existing buttons in the scrollable frame
        for widget in self.snippet_list_frame.winfo_children():
            widget.destroy()
            
        # Create a new button only for snippets that match the selected filter
        for title, data in self.snippets.items():
            if selected_filter == "All" or data["language"] == selected_filter:
                btn = ctk.CTkButton(
                    self.snippet_list_frame, 
                    text=title, 
                    command=lambda t=title: self.load_snippet(t),
                    fg_color="transparent",
                    border_width=1,
                    text_color=("gray10", "gray90")
                )
                btn.pack(pady=5, padx=5, fill="x")
            
    def load_snippet(self, title):
        # Load the saved code and update the UI to match its properties
        snippet_data = self.snippets[title]
        
        self.code_textbox.delete("1.0", "end")
        self.code_textbox.insert("0.0", snippet_data["code"])
        self.header_label.configure(text=f"Editor - {title}")
        
        # Update the loaded state so the delete button knows what to target
        self.current_loaded_title = title
        
        # Also change the language dropdown to match the loaded snippet
        self.snippet_language_option.set(snippet_data["language"])

if __name__ == "__main__":
    app = SnippetApp()
    app.mainloop()