#Main application file
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from FileInteractor import *
import random

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

categories_list = FileInteractor.current_categories()
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #All available options in current category
        self.options = []
        #vars for keeping track on checkbox items to manipulate
        self.options_delete = []
        self.options_delete_items_count = 0
        self.widgets_list = []
        
        self.title("Randomizer App.py")
        self.geometry(f"{600}x{420}")
        # configure grid layout (4x4)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        #Logo for app
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Randomizer App", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        #Button for choosing category with options
        self.categories_optionmenu_label = ctk.CTkLabel(self.sidebar_frame, text="Categories", anchor="w")
        self.categories_optionmenu_label.grid(row=2,column=0,padx=20,pady=(10,0))
        
        self.categories_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values = categories_list,
                                                       command = self.change_options_event)
        self.categories_optionmenu.grid(row=3,column=0,padx=20,pady=(10,10))
        self.categories_optionmenu.set("")
        
        #Button for adding new category
        self.categories_add_button = ctk.CTkButton(self.sidebar_frame, text = "Add New Category",
                                                   command=self.add_category_event)
        self.categories_add_button.grid(row=4,column=0,padx=20,pady=(0,100))
        
         #Button for deleting category
        self.categories_del_button = ctk.CTkButton(self.sidebar_frame, text = "Delete Category", state = 'disabled',
                                                   command=self.delete_category_event)
        self.categories_del_button.grid(row=4,column=0,padx=20,pady=(0,20))
        
        
        #Button for changing app appearance
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        
        #Scrollable frame with options in choosen category
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Options")
        self.scrollable_frame.grid(row=0,column=1,padx=(20, 0),pady=(20,0), sticky="wns")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        #Button for deleting checked items in scrollbar_frame
        self.side_scroll_frame = ctk.CTkFrame(self, width=300)
        self.side_scroll_frame.grid(row=0, column=2, sticky="wns", padx=(20,0),pady=(80,60))
       
        #Delete item button
        self.delete_button = ctk.CTkButton(self.side_scroll_frame, width=100, text = "Delete Item", state='disabled',
                                                  command = self.delete_items_in_category_event)
        self.delete_button.grid(row=3,column=0,padx=10,pady=(10, 0))
        
        #Add item button
        self.add_button = ctk.CTkButton(self.side_scroll_frame, width=100, text = "Add Item", state='disabled',
                                                  command=self.add_option_event)
        self.add_button.grid(row=2,column=0,padx=10,pady=(40, 0))
        
        #Roll random item button
        self.roll_button = ctk.CTkButton(self.side_scroll_frame, width=100, text = "Roll", state='normal',
                                                  command=self.choose_random)
        self.roll_button.grid(row=1,column=0,padx=10,pady=(20, 0))
        
        
        #WIP Testing design
        self.widgets_list.append(self.add_button)
        self.widgets_list.append(self.roll_button)
        self.widgets_list.append(self.delete_button)
        self.widgets_list.append(self.appearance_mode_optionemenu)
        self.widgets_list.append(self.categories_optionmenu)
        self.widgets_list.append(self.categories_add_button)
        self.widgets_list.append(self.categories_del_button)
        
    #Changes apperance of app
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Dark":
            for widget in self.widgets_list:
                widget.configure(fg_color="#5F9EA0", text_color="AliceBlue")
        else:
            for widget in self.widgets_list:
             widget.configure(fg_color="#D8BFD8", text_color="white") 
    
    #Updates scrollbar_frame with options in category
    def change_options_event(self, new_category: str):
        
        self.add_button.configure(state='normal')
        self.categories_del_button.configure(state='normal')
        for widgets in self.scrollable_frame.winfo_children():
            widgets.destroy()
            
        self.options = FileInteractor.options_list(new_category)
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
    def delete_items_in_category_event(self):
        
        #Removes items in options_delete from options 
        for i in self.options_delete:
            self.options.remove(i)
            
        #Resets options_delete & count
        self.options_delete = []
        self.options_delete_items_count = 0
        self.delete_button.configure(state='disabled')
        
        #Rewrites category txt file without deleted options and resets frame
        current_category = self.categories_optionmenu.get()
        FileInteractor.delete_options(current_category, self.options)
        self.change_options_event(current_category)
        
    #Add item to category
    def add_option_event(self):
        
        dialog = ctk.CTkInputDialog(text="Add Option to Category", title="Add Item")
        item = dialog.get_input()
       
        current_category = self.categories_optionmenu.get()
        
        #Raise error message
        if item in self.options:
            CTkMessagebox(master = self, title="Error", message="Item already exists in category", icon='cancel', option_1="OK", justify="center").tkraise()
            
        #Add item to category
        else:
            try:
                FileInteractor.add_option_to_category(current_category,item)
                self.change_options_event(current_category)
            except TypeError:
                pass
            
     
    #Add item to category
    def add_category_event(self):
        dialog = ctk.CTkInputDialog(text="Write Category Name", title="Add Category")
        current_category = self.categories_optionmenu.get()
        item = dialog.get_input()
        
       
        
        #Raise error message
        if item in categories_list:
            CTkMessagebox(master = self, title="Error", message="Category already exists", icon='cancel', option_1="OK", justify="center").tkraise()
        #Error if input string is empty
        elif item == "":
            CTkMessagebox(master = self, title="Error", message="Name can't be empty", icon='cancel', option_1="OK", justify="center").tkraise()    
        #If no error, add item to category
        else:
            #Passes TypeError exception if user closes window
            try:
                FileInteractor.add_category(item)
                categories_list.append(item)
                self.categories_optionmenu.configure(values=categories_list)
            except TypeError:
                pass
            
    #Function for deleting category, removes data from txt files and resets states of buttons affected by category
    def delete_category_event(self):
        del_category = self.categories_optionmenu.get()
        
        confirmation_box = CTkMessagebox(master = self, title="Delete category", message="Are you sure you want to delete "+del_category + "?", icon='question', option_1="YES", option_2="NO",
                                         justify="center", option_focus=2)
        confirmation_box.tkraise()
        user_answer = confirmation_box.get() 
        
        if user_answer == "YES":
            self.add_button.configure(state='disabled')
            self.categories_del_button.configure(state='disabled')
            FileInteractor.delete_category(del_category)
            categories_list.remove(del_category)
            self.categories_optionmenu.configure(values=categories_list)
            self.categories_optionmenu.set("")
            for widgets in self.scrollable_frame.winfo_children():
                widgets.destroy()
        
        
            
        
            
    def choose_random(self):
        #Choose random item from list
        
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
        
        #Passes if there are no options.
        try:
            random_option = random.choice(self.options)
            message_popup(random_option)
        except IndexError:
            pass
       
            
    
            
        
if __name__ == "__main__":
    app = App()
    app.mainloop()  
