#IMPORTS
import os
import platform
import webbrowser
from kivy.app import App
from kivy.config import Config

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox

import sos

if platform.system() == 'Linux':
    Config.set('graphics', 'width', '1920')
    Config.set('graphics', 'height', '1080')
    Config.set('graphics', 'resiable', 0)
else:
    Config.set('graphics', 'fullscreen', 'auto')
Config.write()


class SOS(FloatLayout, App):
    """
    The class for SOS game start screen
    """
    def __init__(self, **kwargs):
        
        """
        The constructor
        """
        
        FloatLayout.__init__(self)
        self.back = AsyncImage(source=os.path.abspath('back.jpeg'))
        self.back.allow_stretch = True
        self.back.keep_ratio = False
        self.add_widget(self.back)
        self.gmLabel1 = Label(text='Simple Game',
                        font_size=20,
                        pos_hint={'center_x': .45, 'center_y': .7},
                        color=(0, 0, 0, 1))
        self.add_widget(self.gmLabel1)

        self.check = CheckBox(active=True,
                           group = 'group',
                           pos_hint={'center_x': .45, 'center_y': .6},
                           color=(0, 0, 0, 1))

        self.add_widget(self.check)

        self.gmLabel2 = Label(text='General Game',
                           font_size=20,
                           pos_hint={'center_x': .55, 'center_y': .7},
                           color=(0, 0, 0, 1))

        self.add_widget(self.gmLabel2)

        self.check = CheckBox(active=True,
                           group = 'group',
                           pos_hint={'center_x': .55, 'center_y': .6},
                           color=(0, 0, 0, 1))
        self.add_widget(self.check)

     
        self.gamemode = Label(text='Game Mode',
                           pos_hint={'center_x': .5,'center_y': .6},
                           color=(0, 0, 0, 1))
        self.add_widget(self.gamemode)

        self.check.bind(active=self.check_box)
        

        self.me = Label(text='',
                        font_size=25,
                        pos_hint={'center_x': .91, 'center_y': .05},
                        color=(0.207, 0.635, 0.423, 0.9))
        self.gamenametv = Label(text='SOS Game',
                                font_size=100,
                                pos_hint={'center_x': .5, 'center_y': .9},
                                color=(0, 0, 0, 1))
        self.start_btn = Button(text='2 player game',
                                size_hint=(.15, .1),
                                pos_hint={'center_x': .5, 'center_y': .5},
                                on_release=lambda x: self.two_player_popup())
        self.ai_start_btn = Button(text='Game against AI',
                                size_hint=(.15, .1),
                                pos_hint={'center_x': .5, 'center_y': .375},
                                on_release=lambda x: self.ai_popup())
        self.exit_btn = Button(text='Exit',
                                size_hint=(.15, .1),
                                pos_hint={'center_x': .5, 'center_y': .25},
                                on_release=lambda x: self.on_exit())

        self.add_widget(self.me)
        self.add_widget(self.gamenametv)
        self.add_widget(self.start_btn)
        self.add_widget(self.ai_start_btn)
        self.add_widget(self.exit_btn)
        self.popup_content = BoxLayout(orientation = 'vertical')
        self.gamecontent = GameLayout()
        self.start = Button(text='Start game',
                            size_hint=(None, None),
                            size=(552,100),
                            on_release=self.on_start_pressed)
        self.popup_content.add_widget(self.gamecontent)
        self.gamecontent.player1.size_hint = (None, None)
        self.gamecontent.player1.size = (552,50)
        self.gamecontent.player2.size_hint = (None, None)
        self.gamecontent.player2.size = (552, 50)
        self.popup_content.add_widget(self.start)
        self.gamepopup = Popup(title='Start a game',
                                     content=self.popup_content,
                                     size_hint=(None, None),
                                     size=(600,325))
        self.game = 0


    def build(self):
        """
        builds the screen
        """
        return self
 
    def check_box(self, instance, isActive):

       if isActive:
           self.gamemode.text = "General Game"
       else:
           self.gamemode.text = "Simple Game"
         
   
    def on_start_pressed(self, instance):
        """
        called when the button in the popup is pressed.
        returns starts the game and applies new settings.
        """
        self.remove_widget(self.gmLabel1)
        self.remove_widget(self.gmLabel2)
        self.remove_widget(self.check)
        self.remove_widget(self.gamemode)
        self.remove_widget(self.gamenametv)
        self.remove_widget(self.start_btn)
        self.remove_widget(self.ai_start_btn)
        self.remove_widget(self.exit_btn)
        self.game = sos.Game(self.root, self.gamecontent.name1input.text, self.gamecontent.name2input.text, self.gamecontent.n, self.gamecontent.n)
        self.gamepopup.dismiss()
        self.add_widget(self.game)
        

    def two_player_popup(self):
        """
        opens gamepopup
        """
        self.gamepopup.open()

    def ai_popup(self):
        """
        opens gamepopup, but with P2 as a AI.
        """
        self.gamecontent.name2input.text = 'AI'
        self.gamecontent.name2input.disabled = True
        self.gamepopup.open()

    def on_exit(self):
        """
        stops the program
        """
        exit()


class GameLayout(BoxLayout):
    """
    The class for gamepopup
    """
    def __init__(self, **kwargs):
        """
        the constructor
        """
        BoxLayout.__init__(self)
        self.orientation = 'vertical'
        self.n = 9
        self.player1 = BoxLayout(orientation='horizontal')
        self.player2 = BoxLayout(orientation='horizontal')
        self.name1instruction = Label(text='Player 1 name: ',
                                      font_size=25,
                                      color=(1, 1, 1, 1))
        self.name1input = TextInput(multiline=False)
        self.player1.add_widget(self.name1instruction)
        self.player1.add_widget(self.name1input)
        self.add_widget(self.player1)
        self.name2instruction = Label(text='Player 2 name: ',
                                      font_size=25,
                                      color=(1, 1, 1, 1))
        self.name2input = TextInput(multiline=False)
        self.player2.add_widget(self.name2instruction)
        self.player2.add_widget(self.name2input)
        self.add_widget(self.player2)


if __name__ == '__main__':
    g = SOS()
    g.run()