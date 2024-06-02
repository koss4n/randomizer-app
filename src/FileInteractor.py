import random
import os

directory = "data/"

#Abstract class for interacting with .txt files
class FileInteractor():

        
        
    #Returns all of the existing categories file names as a List
    def current_categories():
        with open(directory+"Categories.txt", "r") as editor:
            #Reads every line, and removes \n
            categories = editor.read().splitlines()
        editor.close()    
        return categories
        
            
            
    #Creates a new category      
    def add_category(category):
        #Adds a new category name to the Categories.txt file
        with open(directory + "Categories.txt", "a") as editor:
            editor.write( category+"\n")
            editor.close()
        #Creates a new txt file with param @category name 
        with open(directory+category+".txt", "a") as editor:
            editor.close()
         
      
            
    #Adds option to category    
    @staticmethod
    def add_option_to_category(category, option):
        option_list = FileInteractor.options_list(category)
        option_list.append(option)
        length_list = len(option_list)
        with open(directory+category+".txt", "w+") as editor:
            for i in range(length_list):
                editor.write(option_list[i]+"\n")
        #Adds the @option to the @category txt file
            
    #Deletes items in a category from a given list
    def delete_options(category:str, options:list):
       length_list = len(options)
       with open(directory+category+".txt", "w+") as editor:
        
        for i in range(length_list):
            editor.write(options[i]+"\n")
        editor.close() 
        
   
    
    def options_list(user_category):
        #fix new line issue
        #user_category = user_category.replace("\n", "")
        with open(directory + user_category+".txt", "r") as editor:
            listOfOptions: list[str] = editor.read().splitlines()
        return listOfOptions
        
       
        #Select random option in a category
    def select_random_option(category):
        listOfOptions = FileInteractor.options_list(category)
        listLength: int = len(listOfOptions)
        randomNumber = random.randint(0,listLength)
        return listOfOptions[randomNumber]
        
        
                
     #Delete category file & entry
    def delete_category(category):
        file = directory+category+".txt"
        if os.path.exists(file):
            os.remove(file)
            categories = FileInteractor.current_categories()
            categories.remove(category)
            with open(directory + "Categories"+".txt", "w+") as editor:
                for i in range(len(categories)):
                    editor.write(categories[i]+"\n")
                editor.close()
                
                
        else:
            print("Error file doesn't exist")