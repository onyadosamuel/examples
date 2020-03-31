
try:
    filU = open('codewars/SORTnames.txt','r') # OPEN THE SORTnames.txt file 
    
    new = [] # A LIST THAT STORES THE SORTED NAMES AFTER THE WHOLE ITERATION

    for look in filU: # LOOP THROUGH THE SORTnames.txt file line after line
        a = look.split(',') # SEPARATE NAMES ON EACH USING THE COMMA AND IT RETURNS A LIST OF EACH LINE 
        for put in a:   # LOOP THROUGH EACH LINE AS A LIST
            if put != '\n': # IF THE ELEMENT IS NOT A NEWLINE CHARACTER
                new.append(put) # PUT THEM INTO THE NEW LIST
            else:   # IF IT IS A NEWLINE CHARACTER DONT DO ANYTHING
                pass

    newNames = new.sort() # SORT THE NAMES IN THE NEW LIST AND STORE IN THE newNames LISR
    print(new)

    filD = open('codewars/SORTNewnames.txt','w') # OPEN THE SORTNewnames FILE TO RECEIVE THE SORTED NAMES
    num = 1 # COUNTER TO NUMBER THE SORTED NAMES IN THE FILE
    for keep in new: # LOOP THROUGH THE SORTED LIST
        filD.write(str(num)+'.'+keep+'\n') # WRITES THEM TO THE SORTNewnames WITH EACH NAME ON A NEWLINE
        num = num + 1 # UPDATES THE COUNTER TO NUMBER THE NAMES 
except Exception as error: # IF THERE IS AN ERRO
    print('please there is a problem:',error) # PRINT AN ERROR MESSAGE

finally: # IF THE PROGRAM RUNS SMOOTHLY OR NOT 
    filU.close() # CLOSE THE filU FILE
    filD.close() # CLOSE THE filB FILE