from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import weakref
from datetime import date
from datetime import datetime
from database import Database
from database import Tasks
from functools import partial
from kivy.graphics import Color, Rectangle
import sqlite3
Builder.load_file('design.kv')

database = Database()
tasks = Tasks()
class RootWidget(ScreenManager):
    pass
class LoginScreen(Screen):
    def login(self, uname, pword):
        if database.user_exists(uname, pword):
            self.manager.current = "login_success"
            self.ids.username.canvas.after.clear()
            self.ids.password.canvas.after.clear()
            with self.ids.username.canvas.after:
                Color(22/255,57/255,109/255,1)
                Rectangle(pos=self.ids.username.pos, size=(self.ids.username.width, 1))
            with self.ids.password.canvas.after:
                Color(22/255,57/255,109/255,1)
                Rectangle(pos=self.ids.password.pos, size=(self.ids.password.width, 1))    
            self.ids.username.text = ''
            self.ids.password.text = '' 
            self.ids.errormsg.text = ''    
        else:
            self.ids.username.canvas.after.clear()
            self.ids.password.canvas.after.clear()
            with self.ids.username.canvas.after:
                Color(1,0,0,1)
                Rectangle(pos=self.ids.username.pos, size=(self.ids.username.width, 1))
            with self.ids.password.canvas.after:
                Color(1, 0,0,1)
                Rectangle(pos=self.ids.password.pos, size=(self.ids.password.width, 1))
            self.ids.errormsg.text = "[i]Invalid credentials.[/i]"


    def go_to_signup_screen(self):
        self.manager.current = "sign_up_screen"
    def go_to_forgot_password_screen(self):
        self.manager.current = "forgot_password_screen"
    def go_home(self):
        self.manager.current = "login_success"
    
    def do_everything(self, uname, pwd):
        self.login(uname, pwd)

        self.show_all_tasks()
    def show_all_tasks(self):
        tasks = Tasks()
        today = date.today()
        day = today.strftime("%d/%m/%Y")[:2]
        month = today.strftime("%d/%m/%Y")[3:5]
        year = today.strftime("%d/%m/%Y")[6:]
        self.manager.get_screen("login_success").ids.tasks.clear_widgets()
        all_tasks = tasks.todays_tasks(database.logged_in_id, day, month, year)  
        for task in all_tasks:
            layout = GridLayout(cols=2)
            task_name = Label(text=task[2])
            task_time = Label(text=task[3]+":"+task[4])
            delete_task = Button(text="Delete", on_press = partial(self.remove,layout, task))
            layout.add_widget(task_name)
            layout.add_widget(delete_task)
            
            layout.add_widget(task_time)
            self.manager.get_screen("login_success").ids.tasks.add_widget(layout)
        
    def remove(self, layout,task, delete_task):
        self.manager.get_screen("login_success").ids.tasks.remove_widget(layout)
        tasks = Tasks()
        tasks.delete_task(database.logged_in_id, task[2], task[3], task[4], task[5], task[6], task[7])
        #return tasks.todays_tasks(database.logged_in_id, day, month, year)  
    # def get_username(self, uname):
        #some stuff here that changes the text of a widget with id:greeting(see in the LoginSuccess rule in the .kv file)
    
        # self.manager.get_screen("login_success").ids.tasks.remove_widget(self.new_id)

class ForgotPasswordScreen(Screen):
    def change_password(self, uname, pword1, pword2):
        if pword1 == pword2:
            if database.update_pwd(pword1, uname):
                self.ids.errormsg.text=""
                self.ids.username.text=""
                self.ids.password.text=""
                self.ids.retyped_password.text=  ""
                self.manager.current = "password_changed_success"
                self.ids.password.canvas.after.clear()
                self.ids.retyped_password.canvas.after.clear()
                with self.ids.password.canvas.after:
                    Color(22/255,57/255,109/255)
                    Rectangle(pos = self.ids.username.pos, size=(self.ids.username.width, 1))
                with self.ids.retyped_password.canvas.after:
                    Color(22/255,57/255,109/255)
                    Rectangle(pos=self.ids.retyped_password.pos, size=(self.ids.retyped_password.width, 1))
                return True
        self.ids.errormsg.text = "[i]Password is occupied.[/i]"
        self.ids.password.canvas.after.clear()
        self.ids.retyped_password.canvas.after.clear()
        with self.ids.password.canvas.after:
            Color(1, 0,0,1)
            Rectangle(pos=self.ids.password.pos, size=(self.ids.password.width, 1))
        with self.ids.retyped_password.canvas.after:
            Color(1, 0, 0,1)
            Rectangle(pos=self.ids.retyped_password.pos, size=(self.ids.retyped_password.width, 1))
    def go_to_login_page(self):
        self.manager.current = "login_screen"


class PasswordChangedSuccess(Screen):
    def go_to_login_page(self):
        self.manager.current = "login_screen"
class LoginSuccess(Screen, GridLayout):
    def logout(self):
        self.manager.current = "login_screen"
    def go_home(self):
        self.manager.current = "login_success"
    def remove_all(self, user_id):
        pass
    def go_to_datePage(self):
        self.manager.current="date_page"
        self.current_day()
        self.current_month()
        self.current_year()
    def go_to_addPage(self):
        self.manager.current = "add_page"
        self.current_day()
        self.current_month()
        self.current_year()
    def remove_all_tasks(self):
        tasks = Tasks()
        tasks.delete_all_tasks(database.logged_in_id)
        print(tasks.view(database.logged_in_id)) 

    def current_day(self):
        today = date.today()
        current_day = today.strftime("%d/%m/%Y")[:2]
        
        self.manager.get_screen("add_page").ids.day.text = current_day
        self.manager.get_screen("date_page").ids.day.text = current_day
    def current_month(self):
        today = date.today()
        current_month = today.strftime("%d/%m/%Y")[3:5]
        self.manager.get_screen("add_page").ids.month.text = current_month
        self.manager.get_screen("date_page").ids.month.text = current_month
    def current_year(self):
        today = date.today()
        current_year = today.strftime("%d/%m/%Y")[6:]
        self.manager.get_screen("add_page").ids.year.text = current_year
        self.manager.get_screen("date_page").ids.year.text = current_year
class DatePage(Screen):
    def go_home(self):
        self.manager.current = "login_success"
    def logout(self):
        self.manager.current="login_screen"
    def day_minus(self):
        today = date.today()
        month_last_day = {"01":"31","02":"28","03":"31","04":"30","05":"31","06":"30","07":"31","08":"31","09":"30", "10":"31", "11":"30","12":"31"}
        current_day = today.strftime("%d/%m/%Y")[:2]
        current_month = today.strftime("%d/%m/%Y")[3:5]
        current_year = today.strftime("%d/%m/%Y")[6:]
        # self.manager.get_screen("add_page").ids.day.text = current_day
        #[:2], [3:5], [6:]
        day_input = self.ids.day.text
        month_input = self.ids.month.text
        year_input = self.ids.year.text
        if day_input == "01":
            day_input = month_last_day[month_input]
        else:
            if int(day_input) > 10:
                day_input = str(int(day_input)-1)
            else:
                day_input = "0"+str(int(day_input)-1)
        self.ids.day.text = day_input
    def day_plus(self):
        today = date.today()
        month_last_day = {"01":"31","02":"28","03":"31","04":"30","05":"31","06":"30","07":"31","08":"31","09":"30", "10":"31", "11":"30","12":"31"}
        current_day = today.strftime("%d/%m/%Y")[:2]
        current_month = today.strftime("%d/%m/%Y")[3:5]
        current_year = today.strftime("%d/%m/%Y")[6:]
        day_input = self.ids.day.text
        month_input = self.ids.month.text
        year_input = self.ids.year.text
        if day_input == month_last_day[self.ids.month.text]:
            day_input = "01"
        else:
            #if int(day_input) >= int(current_day) and int(month_input)>= int(current_month) and int(year_input)>= int(current_year):
            if int(day_input) < 9:
                day_input = "0"+str(int(day_input)+1)
            else:
                day_input = str(int(day_input)+1)
        self.ids.day.text = day_input

    def month_plus(self):
        today = date.today()

        month_input = self.ids.month.text
        if int(month_input) == 12:
            month_input = "01"
        else:
            if int(month_input) < 9:
                month_input = "0"+str(int(month_input)+1)
            else:
                month_input = str(int(month_input)+1)
        self.ids.month.text = month_input
    def month_minus(self):
        today = date.today()
        current_day = today.strftime("%d/%m/%Y")[:2]
        current_month = today.strftime("%d/%m/%Y")[3:5]
        current_year = today.strftime("%d/%m/%Y")[6:]
        day_input = self.ids.day.text
        month_input = self.ids.month.text
        year_input = self.ids.year.text
        if month_input == "01":
            month_input = "12"
        else:
            if int(month_input)>10:
                month_input = str(int(month_input)-1)
            else:
                month_input = "0"+str(int(month_input)-1)
        self.ids.month.text = month_input
    def year_plus(self):
        self.ids.year.text = str(int(self.ids.year.text)+1)
    def year_minus(self):
        self.ids.year.text = str(int(self.ids.year.text)-1)
    def go_to_date(self):
        tasks = Tasks()
        today = date.today()
        # day = today.strftime("%d/%m/%Y")[:2]
        # month = today.strftime("%d/%m/%Y")[3:5]
        # year = today.strftime("%d/%m/%Y")[6:]
        day = self.ids.day.text
        month = self.ids.month.text
        year = self.ids.year.text
        self.manager.get_screen("login_success").ids.tasks.clear_widgets()
        all_tasks = tasks.todays_tasks(database.logged_in_id, day, month, year)  
        for task in all_tasks:
            layout = GridLayout(cols=2)
            task_name = Label(text=task[2])
            task_time = Label(text=task[3]+":"+task[4])
            delete_task = Button(text="Delete", on_press = partial(self.remove,layout, task))
            layout.add_widget(task_name)
            layout.add_widget(delete_task)
            layout.add_widget(task_time)
            self.manager.get_screen("login_success").ids.tasks.add_widget(layout)
        self.manager.current = "login_success"
    def remove(self, layout,task, delete_task):
        self.manager.get_screen("login_success").ids.tasks.remove_widget(layout)
        tasks = Tasks()
        tasks.delete_task(database.logged_in_id, task[2], task[3], task[4], task[5], task[6], task[7])
class AddPage(Screen):
    def logout(self):
        self.manager.current = "login_screen"
    def go_home(self):
        self.manager.current = "login_success"
    def add_task(self):
        #today = datetime.today()
        now = datetime.now()
        task = self.ids.task.text
        hour = self.ids.hour.text
        minute = self.ids.minute.text
        day = self.ids.day.text
        month = self.ids.month.text
        year = self.ids.year.text

#current_time = now.strftime("%H:%M:%S")

        tasks.insert(database.logged_in_id, task, hour,minute,day,month,year)
        print(tasks.view(database.logged_in_id))
        self.ids.task.name = ""
        self.go_home()
        self.show_all_tasks()
        self.manager.current = "login_success"
    def show_all_tasks(self):
        tasks = Tasks()
        today = date.today()
        day = today.strftime("%d/%m/%Y")[:2]
        month = today.strftime("%d/%m/%Y")[3:5]
        year = today.strftime("%d/%m/%Y")[6:]
        self.manager.get_screen("login_success").ids.tasks.clear_widgets()
        all_tasks = tasks.todays_tasks(database.logged_in_id, day, month, year)  
        for task in all_tasks:
            layout = GridLayout(cols=2)
            task_name = Label(text=task[2])
            task_time = Label(text=task[3]+":"+task[4])
            delete_task = Button(text="Delete", on_press = partial(self.remove,layout, task))
            layout.add_widget(task_name)
            layout.add_widget(delete_task)
            
            layout.add_widget(task_time)
            self.manager.get_screen("login_success").ids.tasks.add_widget(layout)
    def remove(self, layout,task, delete_task):
        self.manager.get_screen("login_success").ids.tasks.remove_widget(layout)
        tasks = Tasks()
        tasks.delete_task(database.logged_in_id, task[2], task[3], task[4], task[5], task[6], task[7])
    def hour_plus(self):
        current_hour = self.ids.hour.text
        if current_hour == "23":
            current_hour = "00"
        else:
            if int(current_hour) < 9:
                current_hour = "0"+str(int(current_hour)+1)
            else:
                current_hour = str(int(current_hour)+1)
        self.ids.hour.text = current_hour
    def hour_minus(self):
        current_hour = self.ids.hour.text
        if current_hour == "00":
            current_hour = "23"
        else:
            if int(current_hour) > 10:
                current_hour = str(int(current_hour)-1)
            else:
                current_hour = "0"+str(int(current_hour)-1)
        self.ids.hour.text = current_hour
    def minute_plus(self):
        current_minute = self.ids.minute.text
        if current_minute == "59":
            current_minute = "00"
        else:
            if int(current_minute) < 9:
                current_minute = "0"+str(int(current_minute)+1)
            else:
                current_minute = str(int(current_minute)+1)
        self.ids.minute.text = current_minute
    def minute_minus(self):
        current_minute = self.ids.minute.text
        if current_minute == "00":
            current_minute = "59"
        else:
            if int(current_minute) > 10:
                current_minute = str(int(current_minute)-1)
            else:
                current_minute = "0"+str(int(current_minute)-1)
        self.ids.minute.text = current_minute
    def day_minus(self):
        today = date.today()
        month_last_day = {"01":"31","02":"28","03":"31","04":"30","05":"31","06":"30","07":"31","08":"31","09":"30", "10":"31", "11":"30","12":"31"}
        current_day = today.strftime("%d/%m/%Y")[:2]
        current_month = today.strftime("%d/%m/%Y")[3:5]
        current_year = today.strftime("%d/%m/%Y")[6:]
        # self.manager.get_screen("add_page").ids.day.text = current_day
        #[:2], [3:5], [6:]
        day_input = self.ids.day.text
        month_input = self.ids.month.text
        year_input = self.ids.year.text
        if day_input == "01":
            day_input = month_last_day[month_input]
        else:
            if int(day_input) > 10:
                day_input = str(int(day_input)-1)
            else:
                day_input = "0"+str(int(day_input)-1)
        self.ids.day.text = day_input
    def day_plus(self):
        today = date.today()
        month_last_day = {"01":"31","02":"28","03":"31","04":"30","05":"31","06":"30","07":"31","08":"31","09":"30", "10":"31", "11":"30","12":"31"}
        current_day = today.strftime("%d/%m/%Y")[:2]
        current_month = today.strftime("%d/%m/%Y")[3:5]
        current_year = today.strftime("%d/%m/%Y")[6:]
        day_input = self.ids.day.text
        month_input = self.ids.month.text
        year_input = self.ids.year.text
        if day_input == month_last_day[self.ids.month.text]:
            day_input = "01"
        else:
            #if int(day_input) >= int(current_day) and int(month_input)>= int(current_month) and int(year_input)>= int(current_year):
            if int(day_input) < 9:
                day_input = "0"+str(int(day_input)+1)
            else:
                day_input = str(int(day_input)+1)
        self.ids.day.text = day_input

    def month_plus(self):
        today = date.today()

        month_input = self.ids.month.text
        if int(month_input) == 12:
            month_input = "01"
        else:
            if int(month_input) < 9:
                month_input = "0"+str(int(month_input)+1)
            else:
                month_input = str(int(month_input)+1)
        self.ids.month.text = month_input
    def month_minus(self):
        today = date.today()
        current_day = today.strftime("%d/%m/%Y")[:2]
        current_month = today.strftime("%d/%m/%Y")[3:5]
        current_year = today.strftime("%d/%m/%Y")[6:]
        day_input = self.ids.day.text
        month_input = self.ids.month.text
        year_input = self.ids.year.text
        if month_input == "01":
            month_input = "12"
        else:
            if int(month_input)>10:
                month_input = str(int(month_input)-1)
                
            else:
                month_input = "0"+str(int(month_input)-1)
        self.ids.month.text = month_input
    def year_plus(self):
        self.ids.year.text = str(int(self.ids.year.text)+1)
    def year_minus(self):
        self.ids.year.text = str(int(self.ids.year.text)-1)
class SignUpScreen(Screen):
    def add_user(self, uname,email, pword1, pword2):
        signup = database.insert(uname, pword1, email)
        if pword1 == pword2:
            if signup[0]:
                self.manager.current = 'sign_up_success'
                self.ids.username.canvas.after.clear()
                self.ids.email.canvas.after.clear()
                self.ids.password.canvas.after.clear()
                self.ids.retyped_password.canvas.after.clear()
                with self.ids.username.canvas.after:
                    Color(22/255,57/255,109/255,1)
                    Rectangle(pos=self.ids.username.pos, size=(self.ids.username.width, 1))
                with self.ids.password.canvas.after:
                    Color(22/255,57/255,109/255,1)
                    Rectangle(pos=self.ids.password.pos, size=(self.ids.password.width, 1))
                with self.ids.email.canvas.after:
                    Color(22/255,57/255,109/255,1)
                    Rectangle(pos=self.ids.email.pos, size=(self.ids.email.width, 1))
                with self.ids.retyped_password.canvas.after:
                    Color(22/255,57/255,109/255,1)
                    Rectangle(pos=self.ids.retyped_password.pos, size=(self.ids.retyped_password.width,1))
                self.ids.username.text=""
                self.ids.password.text=""
                self.ids.retyped_password.text=""
                self.ids.email.text = ""
                self.ids.errormsg = ""

        
        
    def go_to_login_page(self):
        self.manager.current="login_screen"
class SignUpSuccess(Screen):
    def switch_to_login_page(self):
        self.manager.current = 'login_screen'
class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()
