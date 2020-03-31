class numString:
    num = [] # stores the numbers in the user input
    letters = [] # stores the letters in the user input
    def num_string(self):
        """this is method that determines the number of letters and numbers in a user input"""
        self.user_input = str(input("Enter text here: ")) # this is the prompt the gets the use input
        for see in self.user_input: # loop through the user input
            if see.isdigit() == True: # if the string is a number
                self.num.append(see) # store that number in the num list
            elif see.isalpha() == True:                    # if the sting is a letter 
                self.letters.append(see) # store it in the letters list
            else:                        # if the string is neither a letter nor a number
                pass                     # do nothing or print nothing

        self.len_num = len(self.num)    # counts the number of numbers in the num list
        self.len_letter = len(self.letters) # counts the number of letters in the letters list

        print("There are {let} letters and {num} numbers".format(let=self.len_letter,num=self.len_num)) # output the number of letters and numbers in the user input

obj = numString() # create an object for the numString class
obj.num_string() # call the num_string method in the class
