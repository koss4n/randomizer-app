#Main application file
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from FileInteractor import *
import random

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

catagories_list = FileInteractor.current_catagories()
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #All available options in current catagory
        self.options = []
        #vars for keeping track on checkbox items to manipulate
        self.options_delete = []
        self.options_delete_items_count = 0
        
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        # configure grid layout (4x4)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
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
        
        #Button for deleting checked items in scrollbar_frame
        self.side_scroll_frame = ctk.CTkFrame(self, width=300)
        self.side_scroll_frame.grid(row=0, column=2, rowspan=4, sticky="wns", padx=(20,0),pady=(20,280))
       
        #Delete item button
        self.delete_button = ctk.CTkButton(self.side_scroll_frame, text = "Delete Item", state='disabled',
                                                  command = self.delete_items_in_catagory_event)
        self.delete_button.grid(row=1,column=0,padx=30,pady=(10, 0))
        
        #Add item button
        self.add_button = ctk.CTkButton(self.side_scroll_frame, text = "Add Item", state='normal',
                                                  command=self.open_input_dialog_event)
        self.add_button.grid(row=0,column=0,padx=30,pady=(10, 0))
        
        #Roll random item button
        self.roll_button = ctk.CTkButton(self.side_scroll_frame, text = "Roll", state='normal',
                                                  command=self.choose_random)
        self.roll_button.grid(row=4,column=0,padx=30,pady=(10, 0))
        
    #Changes apperance of app
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
    
    #Updates scrollbar_frame with options in catagory
    def change_options_event(self, new_catagory: str):
        
        for widgets in self.scrollable_frame.winfo_children():
            widgets.destroy()
            
        self.options = FileInteractor.options_list(new_catagory)
        index = 0
           
        for i in self.options:
            
           check_var = ctk.StringVar(value="off")  
           
           def on_checkbox_click(option=i, var=check_var):
               
               #Manipulates options_delete which goes to delete_button
                if var.get() == option:
                    if option not in self.options_delete:
                        self.options_delete.append(option)
                        self.options_delete_items_count += 1
                else:
                    if option in self.options_delete:
                        self.options_delete.remove(option)
                        self.options_delete_items_count -= 1
                
                #Manipulates state of delete_button depending on if items are checked or not
                if self.options_delete_items_count != 0:
                    self.delete_button.configure(state='normal')
                else:
                    self.delete_button.configure(state='disabled')
                    
         
           checkbox = ctk.CTkCheckBox(master=self.scrollable_frame, text = i, variable=check_var, onvalue= i, offvalue= "off",
                                      command= on_checkbox_click)
           checkbox.grid(row=index, column = 0, padx = 10, pady=(0,20), sticky="w")
           index += 1
        
        
        
    
        
        
    #Removes checked items
    def delete_items_in_catagory_event(self):
        
        #Removes items in options_delete from options 
        for i in self.options_delete:
            self.options.remove(i)
            
        #Resets options_delete & count
        self.options_delete = []
        self.options_delete_items_count = 0
        
        #Rewrites catagory txt file without deleted options and resets frame
        current_catagory = self.catagories_optionmenu.get()
        FileInteractor.delete_options(current_catagory, self.options)
        self.change_options_event(current_catagory)
        
    #Add item to catagory
    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Add Option to Catagory", title="Add Item")
        current_catagory = self.catagories_optionmenu.get()
        item = dialog.get_input()
        
        #Raise error message
        if item in self.options:
            CTkMessagebox(master = self, title="Error", message="Item already exists in catagory", icon='cancel', option_1="OK", justify="center").tkraise()
            
        #Add item to catagory
        else:
            FileInteractor.add_option_to_catagory(current_catagory,item)
            self.change_options_event(current_catagory)
        
    def choose_random(self):
        #Choose random item from list
        random_option = random.choice(self.options)
        #Func to present option & get response
        def message_popup(choosen_item):
            msg = CTkMessagebox(master = self, title="Option Rolled", message=choosen_item, icon='check', option_1="OK",option_2="Re-roll", justify="center")
            msg.tkraise()
            response = msg.get()
            if response == "Re-roll":
                temp = self.options
                temp.remove(choosen_item)
                random_temp = random.choice(temp)
                temp.append(choosen_item)
                message_popup(random_temp)
        
        message_popup(random_option)
            
        
        
    
            
        
if __name__ == "__main__":
    app = App()
    app.change_options_event(catagories_list[0])
    app.mainloop()  