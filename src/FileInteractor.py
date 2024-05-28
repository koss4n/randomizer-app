import random

directory = "data/"

#Abstract class for interacting with .txt files
class FileInteractor():

        
        
    #Returns all of the existing catagories file names as a List
    @staticmethod
    def current_catagories():
        with open(directory+"Catagories.txt", "r") as editor:
            #Reads every line, and removes \n
            catagories = editor.read().splitlines()
        editor.close()    
        return catagories
        
            
            
    #Creates a new catagory      
    @staticmethod
    def add_catagory(catagory):
        
        with open("Catagories.txt", "a") as editor:
            editor.write("\n" + catagory)
        #Adds a new catagory name to the Catagories.txt file 
        with open(directory+catagory+".txt", "a") as editor:
            editor.write("")
        #Creates a new txt file with param @catagory name 
        editor.close()
            
    #Adds option to catagory    
    @staticmethod
    def add_to_option_to_catagory(catagory, option):
        with open(directory+catagory+".txt", "a+") as editor:
            editor.write("\n" + option)
        #Adds the @option to the @catagory txt file
            
    #Deletes items in a catagory from a given list
    def delete_options(catagory:str, options:list):
       with open(directory+catagory+".txt", "w") as editor:
        editor.write(options[0])
        options.remove(options[0])
        for i in options:
            editor.write("\n" + i)
        editor.close() 
        
   
    
    def options_list(userCatagory):
        #fix new line issue
        #userCatagory = userCatagory.replace("\n", "")
        with open(directory + userCatagory+".txt", "r") as editor:
            listOfOptions: list[str] = editor.read().splitlines()
        return listOfOptions
        
       
        #Select random option in a catagory
    def select_random_option(catagory):
        listOfOptions = FileInteractor.options_list(catagory)
        listLength: int = len(listOfOptions)
        randomNumber = random.randint(0,listLength)
        return listOfOptions[randomNumber]
        
        
                
