#Main application file
import customtkinter as ctk
from FileInteractor import *

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

catagories_list = FileInteractor.current_catagories()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        #Logo for app
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Randomizer App", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        #Button for choosing catagory with options
        self.catagories_optionmenu_label = ctk.CTkLabel(self.sidebar_frame, text="Catagories", anchor="w")
        self.catagories_optionmenu_label.grid(row=2,column=0,padx=20,pady=(10,0))
        
        self.catagories_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values = catagories_list,
                                                       command = self.change_options_event)
        self.catagories_optionmenu.grid(row=3,column=0,padx=20,pady=(10,10))
        
        
        #Button for changing app appearance
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        
        #Scrollable frame with options in choosen catagory
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Options")
        self.scrollable_frame.grid(row=0,column=1,padx=(20, 0),pady=(20,0), sticky="wns")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
    #Changes apperance of app
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
    
    #Updates scrollbar_frame with options in catagory
    def change_options_event(self, new_catagory: str):
        self.scrollable_frame.clipboard_clear()
        options = FileInteractor.options_list(new_catagory)
        index = 0
        for i in options:
           checkbox = ctk.CTkCheckBox(master=self.scrollable_frame, text = i)
           checkbox.grid(row=index, column = 0, padx = 10, pady=(0,20), sticky="w")
           index += 1
            
            
            
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()  