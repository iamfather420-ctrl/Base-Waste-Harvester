# main.py - Base Waste Harvester Mobile Application
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import json
import os


class BaseWasteHarvesterApp(App):
    def build(self):
        # Set window properties
        Window.clearcolor = get_color_from_hex('#1e2124')
        Window.size = (540, 960)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = Label(
            text='Base Waste Harvester',
            font_size='32sp',
            bold=True,
            color=get_color_from_hex('#ffffff'),
            size_hint_y=0.15
        )
        main_layout.add_widget(header)
        
        # Status section
        status_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.25)
        
        status_label = Label(
            text='Status:\nOPERATIONAL',
            font_size='18sp',
            color=get_color_from_hex('#00ff00'),
            halign='center'
        )
        status_layout.add_widget(status_label)
        
        health_label = Label(
            text='System Health:\nOPTIMAL',
            font_size='18sp',
            color=get_color_from_hex('#00ff00'),
            halign='center'
        )
        status_layout.add_widget(health_label)
        
        main_layout.add_widget(status_layout)
        
        # Metrics section
        metrics_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.25)
        
        waste_label = Label(
            text='Waste Processed:\n0 units',
            font_size='16sp',
            color=get_color_from_hex('#ffffff'),
            halign='center'
        )
        metrics_layout.add_widget(waste_label)
        
        efficiency_label = Label(
            text='Efficiency:\n100%',
            font_size='16sp',
            color=get_color_from_hex('#ffffff'),
            halign='center'
        )
        metrics_layout.add_widget(efficiency_label)
        
        main_layout.add_widget(metrics_layout)
        
        # Action buttons
        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.25)
        
        start_button = Button(
            text='Start Reclamation',
            size_hint_y=0.5,
            background_color=get_color_from_hex('#282b30')
        )
        start_button.bind(on_press=self.on_start_pressed)
        button_layout.add_widget(start_button)
        
        status_button = Button(
            text='View Status',
            size_hint_y=0.5,
            background_color=get_color_from_hex('#282b30')
        )
        status_button.bind(on_press=self.on_status_pressed)
        button_layout.add_widget(status_button)
        
        main_layout.add_widget(button_layout)
        
        # Footer
        footer = Label(
            text='v0.1 | Blockchain Cleaner',
            font_size='12sp',
            color=get_color_from_hex('#666666'),
            size_hint_y=0.1
        )
        main_layout.add_widget(footer)
        
        return main_layout
    
    def on_start_pressed(self, instance):
        print("[ACTION] Start Reclamation pressed")
        # Placeholder for reclamation logic
        pass
    
    def on_status_pressed(self, instance):
        print("[ACTION] View Status pressed")
        # Placeholder for status display logic
        pass


if __name__ == '__main__':
    BaseWasteHarvesterApp().run()
