from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
class RootWidget(ScreenManager):
    pass





class Widgets(ScreenManager):
    def open_popup(self):
        show_popup()


class P(GridLayout):
    pass
def show_popup():
    show = P()
    popupWindow = Popup(title="Popup window", content=show)
    popupWindow.open()

class MainApp(App):
    def build(self):
        return Widgets()


if __name__ == "__main__":
    MainApp().run()