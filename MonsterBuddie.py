import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import openai
import urllib.request
from datetime import datetime
from math import floor

openai.api_key = os.getenv("OPENAI_API_KEY")


class Tamagotchi(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.padding = 50

        button_layout = BoxLayout(orientation="vertical", size_hint=(0.3, .9))

        self.name_label = Label(text="Enter a name for your Tamagotchi:")
        button_layout.add_widget(self.name_label)

        self.name_input = TextInput(multiline=False)
        button_layout.add_widget(self.name_input)

        self.type_label = Label(text="Enter a type for your Tamagotchi:")
        button_layout.add_widget(self.type_label)

        self.type_input = TextInput(multiline=False)
        button_layout.add_widget(self.type_input)

        self.create_button = Button(text="Create Tamagotchi")
        self.create_button.bind(on_press=self.create_tamagotchi)
        button_layout.add_widget(self.create_button)

        self.feed_button = Button(text="Feed")
        self.feed_button.bind(on_press=self.feed)
        button_layout.add_widget(self.feed_button)

        self.play_button = Button(text="Play")
        self.play_button.bind(on_press=self.play)
        button_layout.add_widget(self.play_button)

        self.sleep_button = Button(text="Sleep")
        self.sleep_button.bind(on_press=self.sleep)
        button_layout.add_widget(self.sleep_button)

        self.status_label = Label(text="")
        button_layout.add_widget(self.status_label)

        self.mood_label = Label(text=' current mood')
        button_layout.add_widget(self.mood_label)

        self.add_widget(button_layout)

        self.image_layout = BoxLayout(orientation="vertical", size_hint=(0.7, .9))
        self.add_widget(self.image_layout)

        self.tamagotchi = None

        

    def create_tamagotchi(self, instance):
        name = self.name_input.text.strip()
        type = self.type_input.text.strip()

        # Remove the first two input boxes and their prompts
        self.remove_widget(self.name_label)
        self.remove_widget(self.name_input)
        self.remove_widget(self.type_label)
        self.remove_widget(self.type_input)


        if name and type:
            self.tamagotchi = TamagotchiGame(name, type)
            self.name_label.text = f"Tamagotchi: {name} ({type})"
            self.name_input.text = ""
            self.type_input.text = ""
            self.status_label.text = "Tamagotchi created."

            # Remove the first two input boxes and their prompts
            self.remove_widget(self.name_label)
            self.remove_widget(self.name_input)
            self.remove_widget(self.type_label)
            self.remove_widget(self.type_input)

            # Display the image as the background
            self.display_image_background(type)

            # Schedule the update function
            Clock.schedule_interval(self.update_tamagotchi, 1)

    def feed(self, instance):
        if self.tamagotchi:
            self.tamagotchi.feed()
            self.status_label.text = "You feed your Tamagotchi."
            self.update_tamagotchi_mood()
        else:
            self.status_label.text = "Create a Tamagotchi first."

    def play(self, instance):
        if self.tamagotchi:
            self.tamagotchi.play()
            self.status_label.text = "You play with your Tamagotchi."
            self.update_tamagotchi_mood()
        else:
            self.status_label.text = "Create a Tamagotchi first."

    def sleep(self, instance):
        if self.tamagotchi:
            self.tamagotchi.sleep()
            self.status_label.text = "You put your Tamagotchi to sleep."
            self.update_tamagotchi_mood()
        else:
            self.status_label.text = "Create a Tamagotchi first."

    def update_tamagotchi(self, dt):
        if self.tamagotchi is not None:
            self.tamagotchi.update()
            #self.hunger_label.text = f"Hunger: {self.tamagotchi.hunger}"
            #self.energy_label.text = f"Energy: {self.tamagotchi.energy}"
            #self.boredom_label.text = f"Boredom: {self.tamagotchi.boredom}"
            if not self.tamagotchi.is_alive:
                self.status_label.text = "Your Tamagotchi has passed away. Game over!"
                Clock.unschedule(self.update_tamagotchi)

    def display_image_background(self, type):
        prompt = f"'{type}'"
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        image_url = response['data'][0]['url']
        print(image_url)

        directory = "C:/Users/hhhhhhhhh/MadBuddie"   # Replace with the desired directory path
        file_name = os.path.join(directory, "image" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        urllib.request.urlretrieve(image_url, file_name)

        # Create an instance of AsyncImage with the downloaded image
        image = AsyncImage(source=file_name, size_hint=(1, 1))

        # Clear the image layout and add the AsyncImage to the image layout
        self.image_layout.clear_widgets()
        self.image_layout.add_widget(image)

    def update_tamagotchi_mood(self):
        if self.tamagotchi.is_happy():
            self.display_happy_image()
        else:
            self.display_image_background(self.tamagotchi.type)



from math import floor

class TamagotchiGame:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.hunger = 0
        self.boredom = 0
        self.energy = 100
        self.is_alive = True
        self.minutes_elapsed = 0
        self.mood = 'mehhh'

    def feed(self):
        if self.is_alive:
            self.hunger -= 10
            if self.hunger == 0:
                self.hunger = 0
            self.energy += 5
            if self.energy > 100:
                self.energy = 100
        else:
            self.is_alive = False

    def play(self):
        if self.is_alive:
            self.boredom -= 10
            if self.boredom < 0:
                self.boredom = 0
            self.energy -= 10
            if self.energy < 0:
                self.energy = 0
        else:
            self.is_alive = False

    def sleep(self):
        if self.is_alive:
            self.energy += 10
            if self.energy > 100:
                self.energy = 100
            self.boredom += 5
            if self.boredom > 100:
                self.boredom = 100
        else:
            self.is_alive = False

    def update(self):
        if self.is_alive:
            self.hunger += 5
            self.boredom += 5
            self.minutes_elapsed += 1

            if self.minutes_elapsed % 2 == 0:
                self.hunger -= 1
                if self.hunger < 0:
                    self.hunger = 0

            if self.hunger >= 100 or self.boredom >= 100:
                self.is_alive = False

    def is_happy(self):
        return self.energy >= 70 and self.hunger <= 30 and self.boredom <= 30



class TamagotchiApp(App):
    def build(self):
        return Tamagotchi()


if __name__ == "__main__":
    TamagotchiApp().run()

