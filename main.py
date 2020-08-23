from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
import json,glob
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from pathlib import Path
from datetime import datetime
import random
import time
Builder.load_file("design.kv")

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current="sign_up_screen"
    def login(self,u,p):
        with open("users.json") as file:
            users=json.load(file)
        if u in users and users[u]['password']==p:
            self.ids.login_wrong.text=""
            self.ids.username.text=""
            self.ids.password.text=""
            self.manager.current="login_screen_success"
        else:
            anim=Animation(color=(0.6,0.7,0.1,1))
            anim.start(self.ids.login_wrong)
            self.ids.login_wrong.text="Wrong username or password"
    def forgot(self):
        self.manager.current="forgot"

class ForgotScreen(Screen):
    def res(self,nu,np):
        with open("users.json") as file:
            users=json.load(file)
        if nu in users and np!="":
            users[nu]['password']=np
            with open("users.json",'w') as file:
                json.dump(users,file)
            self.ids.pass_reset.text="Password has been reset"   
        else:
            self.ids.pass_reset.text="Username does not exist" 
            
    def log(self):
        self.manager.current="login_screen"
 

class SignUpScreen(Screen):
    def add_user(self,u,p):
        with open(r"data.json") as file:
            users=json.load(file)
        
        if u=="" or p=="":
            self.ids.empty.text="Username or password cannot be empty"
        else:
            users[u]={'username':u,'password':p,'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
            with open("users.json",'w') as file:
                json.dump(users,file)


            self.manager.current="sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction="right"
        self.manager.current="login_screen"
        

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.ids.feeling.text=""
        self.manager.transition.direction="right"
        self.manager.current="login_screen"
    def get_quote(self,feel):
        feel=feel.lower()
        available_feelings=glob.glob("quotes/*txt")
        available_feelings=[Path(filename).stem for filename in available_feelings]
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes=file.readlines()
            self.ids.quote.text=random.choice(quotes)
        else:
            self.ids.quote.text="Try another feelings"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass



class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()