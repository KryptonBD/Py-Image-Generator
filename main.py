from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

Builder.load_file("index.kv")


class IndexScreen(Screen):
    def generate_image(self):
        self.manager.current_screen.ids.img.source = "home.jpg"


class RootWidget(ScreenManager):
    pass


class Main(App):

    def build(self):
        return RootWidget()


Main().run()
