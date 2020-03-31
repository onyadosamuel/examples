from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
import pymongo
from pymongo import MongoClient
from kivy.clock import Clock
from kivy.properties import NumericProperty
import random

# connecting to my mongo client
client = MongoClient('localhost',27017)

# creating my database collection
db = client['mathApp']
collection = db['mathApp']



class ImageButton(ButtonBehavior,Image):
    pass
class HomeScreen(Screen):
    pass
class SignScreen(Screen):
    pass

class CreateScreen(Screen):
    pass

class WorkScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass


kv = Builder.load_file('Brain_math.kv')
class meApp(App):
    store = []  # variable that stores the randomly generated numbers
    num_default = 1 # default speed of the user
    score = 0 # this is the current score of the user
    def build(self):
        return kv

    def on_start(self):
        self.root.ids['work'].ids['current_speed'].text = str(self.num_default) + ' number(s) per second' # this is the default speed of the user
        self.root.ids['work'].ids['current_score'].text = '0' # the default score

    def Sign_user(self):
        self.Sign_username = self.root.ids['sign'].ids['si_username'].text  # variable for the sign in username
        self.Sign_password = self.root.ids['sign'].ids['si_password'].text  # variable for the sign in password
        self.Work_user = self.root.ids['work'].ids['current_user'].text  # variable for the work screen current user
        self.user_saved_info = collection.find_one({'username':self.Sign_username,'password':self.Sign_password}) # variable for user infomation in database

        # GET ALL MY DOCUMENTS IN MY DATABASE
        self.result = collection.find({})  # variable for all documents in my database
        # SEARCH THROUGH THE DATABASE IF THE ENTERED USERNAME AND PASSWORD EXITS
        if self.user_saved_info in self.result: # if the entered info is in the database
            self.root.ids['work'].ids['current_user'].text = self.Sign_username # set the current user in the work screen to the username entered
            self.root.current = 'work'  # go to the work window
        else:
            self.root.current = 'sign'  # stay on the sign in screen if the entered info is not in the database
            self.root.ids['sign'].ids['check'].text = 'username and password not\nfound plesae create an account' # print this error message to the user



    def Create_user(self):
        self.Create_username = self.root.ids['create'].ids['cr_username'].text # variable to get username from username textinput
        self.Create_new_password = self.root.ids['create'].ids['cr_newpass'].text # variable to get new password from new password textinput
        self.Create_confirm_password = self.root.ids['create'].ids['cr_confirmpass'].text # variable to get password validation from confirm password textinput


        # user information to be fed into the database
        user_info = {'username':self.Create_username,'password':self.Create_new_password,'speed':'','score':''}

        # CHECKING IF TEXT IN NEW_PASSWORD AND CONFIRM_PASSWORD ARE THE SAME
        if self.Create_new_password == self.Create_confirm_password:
            # put user info into the database if the two passwords match
            collection.insert_one(user_info)

            # go to the sign in screen
            self.root.current = 'sign'
        else:
            # stay on the create account screen
            self.root.current = 'create'
            # print this error message to the user
            self.root.ids['create'].ids['sp4'].text = 'Passwords does not match'

    def Work_user_start(self):
        if self.root.ids['work'].ids['min_range'].text != '' and self.root.ids['work'].ids['max_range'].text != '': # if the minimum and maximum number are not empty
            self.start_event = Clock.schedule_interval(self.random_number,1/self.num_default )  # clock function that runs the random_number a certain number of times on the screen
            Clock.schedule_once(self.Work_user_stop,10/self.num_default) # this stops the random number generation after 10 seconds
            Clock.schedule_once(self.answer_req, 11)
        else:
            self.root.ids['work'].ids['upsheet'].text = 'Please enter the minimum ,maximum numbers and \nnumber of words per second you want to use' # prompt the user to enter fill in the max and min boxes
            Clock.schedule_once(self.clean_sheet,3) # clean the top sheet after 4 seconds

    def answer_req(self,*args):
        self.ans_req_evt = self.root.ids['work'].ids['sheet'].text = 'Answer' # this prompts the user for the answer
    def Work_user_wps(self):
        self.work_wps = self.root.ids['work'].ids['wps'].text # this recieves the number of words per second
        self.num_default = int(self.work_wps)
        self.root.ids['work'].ids['current_speed'].text = str(self.num_default)+' number(s) per second' # this updates the speed label with the current speed of the user

    def Work_user_reset(self):
        self.root.ids['work'].ids['sheet'].text = '0' # this cleans the screen and set the value of the screen to zero

    def Work_user_answer(self):
        self.number_answer = sum(self.store) # variable for the answer of the randomly generates numbers
        self.user_answer = self.root.ids['work'].ids['answer'].text # variable that stores answer from the user
        print(self.store)
        print(self.number_answer)
        if self.user_answer != '': # if the answer box is not empty upon validation or pressiing the enter key
            if self.number_answer == int(self.user_answer): # if the user's answer is correct
                self.root.ids['work'].ids['upsheet'].text = 'Congratulatons you had the right answer ! ! ! !' # congratulate the user for getting the answer correct
                self.score  += 10 # this updates the score with a 10
                self.root.ids['work'].ids['current_score'].text = str(self.score) # this shows the score of the user on the screen
                self.store[:] = []  # set the list as an empty list
                Clock.schedule_once(self.clean_sheet, 3)  # clean the top sheet after 4 seconds
            else:
                self.root.ids['work'].ids['upsheet'].text = 'Sorry you had the wrong answer' # give the user a message when the answer is wrong
                self.score -= 10  # this updates the score with a  decrease of 10
                self.root.ids['work'].ids['current_score'].text = str(self.score)  # this shows the score of the user on the screen
                Clock.schedule_once(self.clean_sheet, 3)  # clean the top sheet after 4 seconds
        else:
            self.root.ids['work'].ids['upsheet'].text = 'Please provide an answer' # give an error message if the answer box is empty upon validation or pressing the enter key
            Clock.schedule_once(self.clean_sheet, 3)  # clean the top sheet after 4 seconds

    def Work_user_stop(self,*args):
        self.start_event.cancel() # cancels the random number generation

    def Work_user_update(self):
        collection.update_one({'name':self.root.ids['work'].ids['upsheet'].text},{'$set':{'score':self.score,'speed':self.num_default}}) # update the user databse each time user leaves page
        print(self.num_default)
        self.root.current = 'home' # go to the home screen

    def random_number(self,*args):
        self.work_minimum_number = self.root.ids['work'].ids['min_range'].text  # variable for the minimum number
        self.work_maximum_number = self.root.ids['work'].ids['max_range'].text  # variable for the maxinmum number
        self.root.ids['work'].ids['sheet'].text = str(random.randrange(int(self.work_minimum_number),int(self.work_maximum_number))) # generate random number to the screen
        self.store.append(int(self.root.ids['work'].ids['sheet'].text))  # adds the randomly generated numbers to the store list
        print(self.root.ids['work'].ids['sheet'].text)

    def clean_sheet(self,*args):
        self.root.ids['work'].ids['upsheet'].text = ''  # clean the topsheet

if __name__ == "__main__":
    meApp().run()
