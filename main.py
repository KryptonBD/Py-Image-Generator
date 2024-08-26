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

# Load Kivy file
Builder.load_file("index.kv")


class IndexScreen(Screen):

    def generate_image(self, prompt):
        """
        Generate an image with OPEN AI's DALL-E-3 model
        """
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        return response.data[0]

    def get_image(self, image):
        """
        Download the generated image
        """
        return requests.get(image.url)

    def save_image(self, image):
        """
        Save the downloaded image
        """
        self.image_path = f"output/{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.jpg"

        with open(self.image_path, "wb") as file:
            file.write(image.content)

    def set_image(self):
        """
        Set the image as the source of the image widget
        """
        self.manager.current_screen.ids.img.source = self.image_path

    def submit_prompt(self):
        """
        Get the user propmt, generate the image, download the image and display the image
        """
        query = self.manager.current_screen.ids.user_prompt.text

        data = self.generate_image(query)
        image = self.get_image(data)
        self.save_image(image)
        self.set_image()


class RootWidget(ScreenManager):
    pass


class Main(App):

    def build(self):
        return RootWidget()


Main().run()
