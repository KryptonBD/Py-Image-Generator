from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
from datetime import datetime


load_dotenv()

apikey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)

Builder.load_file("index.kv")


class IndexScreen(Screen):
    def generate_image(self):
        # Get prompt enter by the user
        query = self.manager.current_screen.ids.user_prompt.text

        response = client.images.generate(
            model="dall-e-3",
            prompt=query,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        req = requests.get(image_url)

        image_path = f"output/{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.jpg"
        with open(image_path, "wb") as file:
            file.write(req.content)

        self.manager.current_screen.ids.img.source = image_path


class RootWidget(ScreenManager):
    pass


class Main(App):

    def build(self):
        return RootWidget()


Main().run()
