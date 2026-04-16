"""
Туристический гид по ХМАО-Югре
Интерактивное приложение с картами, маршрутами и событиями
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

# Цвета брендбука Югры
BRAND_GREEN = [0.106, 0.369, 0.125, 1]
BRAND_BLUE = [0.051, 0.275, 0.439, 1]
BRAND_WHITE = [1, 1, 1, 1]

Window.clearcolor = BRAND_WHITE


class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.go_to_main(), 2)
    def go_to_main(self):
        self.manager.current = 'main'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        title = Label(text="ЮграТур\nИнтерактивный гид по ХМАО-Югре", font_size='24sp', color=BRAND_GREEN, size_hint=(1, 0.3), halign='center', valign='middle')
        title.bind(size=title.setter('text_size'))
        btn_map = Button(text="🗺️ Карта и объекты", size_hint=(1, 0.15), background_color=BRAND_GREEN)
        btn_map.bind(on_press=self.go_to_map)
        btn_routes = Button(text="🚶 Туристические маршруты", size_hint=(1, 0.15), background_color=BRAND_BLUE)
        btn_routes.bind(on_press=self.go_to_routes)
        btn_events = Button(text="📅 События и фестивали", size_hint=(1, 0.15), background_color=BRAND_GREEN)
        btn_events.bind(on_press=self.go_to_events)
        btn_profile = Button(text="👤 Личный кабинет", size_hint=(1, 0.15), background_color=BRAND_BLUE)
        btn_profile.bind(on_press=self.go_to_profile)
        btn_weather = Button(text="🌤️ Погода в Югре", size_hint=(1, 0.15), background_color=BRAND_GREEN)
        btn_weather.bind(on_press=self.go_to_weather)
        layout.add_widget(title)
        layout.add_widget(btn_map)
        layout.add_widget(btn_routes)
        layout.add_widget(btn_events)
        layout.add_widget(btn_profile)
        layout.add_widget(btn_weather)
        self.add_widget(layout)
    def go_to_map(self, instance): self.manager.current = 'map'
    def go_to_routes(self, instance): self.manager.current = 'routes'
    def go_to_events(self, instance): self.manager.current = 'events'
    def go_to_profile(self, instance): self.manager.current = 'profile'
    def go_to_weather(self, instance): self.manager.current = 'weather'


class MapScreen(Screen):
    def on_enter(self):
        self.display_objects()
    def display_objects(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        header = Label(text="🏔️ Достопримечательности Югры", font_size='20sp', color=BRAND_GREEN, size_hint=(1, 0.1))
        scroll = ScrollView(size_hint=(1, 0.8))
        objects_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        objects_list.bind(minimum_height=objects_list.setter('height'))
        objects_data = [
            {"name": "Археопарк «Самаровский останец»", "desc": "Парк с бронзовыми скульптурами мамонтов", "hours": "09:00-20:00"},
            {"name": "Музей геологии, нефти и газа", "desc": "Уникальные экспонаты нефтегазовой отрасли", "hours": "10:00-18:00"},
            {"name": "Природный парк «Самаровский чугас»", "desc": "Кедровый лес в черте города", "hours": "Круглосуточно"},
            {"name": "Церковь Воскресения Христова", "desc": "Православный храм в русском стиле", "hours": "07:00-19:00"},
            {"name": "Парк «Бориса Лосева»", "desc": "Городской парк с фонтанами", "hours": "Круглосуточно"},
        ]
        for obj in objects_data:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=10, spacing=5)
            name_label = Label(text=f"📍 {obj['name']}", font_size='16sp', bold=True, size_hint_y=None, height=30, halign='left')
            name_label.bind(size=name_label.setter('text_size'))
            desc_label = Label(text=obj['desc'], font_size='12sp', size_hint_y=None, height=40, halign='left')
            desc_label.bind(size=desc_label.setter('text_size'))
            hours_label = Label(text=f"⏰ {obj['hours']}", font_size='11sp', color=BRAND_GREEN, size_hint_y=None, height=20, halign='left')
            hours_label.bind(size=hours_label.setter('text_size'))
            card.add_widget(name_label)
            card.add_widget(desc_label)
            card.add_widget(hours_label)
            objects_list.add_widget(card)
        scroll.add_widget(objects_list)
        btn_back = Button(text="← Назад", size_hint=(1, 0.1), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(btn_back)
        self.clear_widgets()
        self.add_widget(layout)
    def go_back(self, instance): self.manager.current = 'main'


class RoutesScreen(Screen):
    def on_enter(self):
        self.display_routes()
    def display_routes(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        header = Label(text="🚶 Популярные маршруты", font_size='20sp', color=BRAND_GREEN, size_hint=(1, 0.1))
        scroll = ScrollView(size_hint=(1, 0.8))
        routes_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        routes_list.bind(minimum_height=routes_list.setter('height'))
        routes_data = [
            {"name": "Исторический центр Ханты-Мансийска", "dist": "3.5 км", "time": "2 часа", "diff": "Лёгкий"},
            {"name": "Археологическая тропа", "dist": "5 км", "time": "3 часа", "diff": "Средний"},
            {"name": "Вдоль Иртыша", "dist": "8 км", "time": "4 часа", "diff": "Средний"},
            {"name": "Парки и скверы города", "dist": "4 км", "time": "2.5 часа", "diff": "Лёгкий"},
        ]
        for route in routes_data:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=80, padding=10)
            name_label = Label(text=f"🗺️ {route['name']}", font_size='15sp', bold=True, size_hint_y=None, height=25, halign='left')
            name_label.bind(size=name_label.setter('text_size'))
            info_label = Label(text=f"📏 {route['dist']}  ⏱️ {route['time']}  ⭐ {route['diff']}", font_size='12sp', size_hint_y=None, height=20, halign='left')
            info_label.bind(size=info_label.setter('text_size'))
            card.add_widget(name_label)
            card.add_widget(info_label)
            routes_list.add_widget(card)
        scroll.add_widget(routes_list)
        btn_back = Button(text="← Назад", size_hint=(1, 0.1), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(btn_back)
        self.clear_widgets()
        self.add_widget(layout)
    def go_back(self, instance): self.manager.current = 'main'


class EventsScreen(Screen):
    def on_enter(self):
        self.display_events()
    def display_events(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        header = Label(text="📅 Ближайшие события", font_size='20sp', color=BRAND_GREEN, size_hint=(1, 0.1))
        scroll = ScrollView(size_hint=(1, 0.8))
        events_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        events_list.bind(minimum_height=events_list.setter('height'))
        events_data = [
            {"name": "Фестиваль «Самотлорские ночи»", "date": "15-17 июня 2026", "place": "Нижневартовск"},
            {"name": "День города Ханты-Мансийска", "date": "12 июля 2026", "place": "Ханты-Мансийск"},
            {"name": "Выставка «Югра туристическая»", "date": "20-22 августа 2026", "place": "Сургут"},
            {"name": "Гонки на оленьих упряжках", "date": "5-7 марта 2026", "place": "Ханты-Мансийск"},
        ]
        for event in events_data:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=70, padding=10)
            name_label = Label(text=f"🎪 {event['name']}", font_size='15sp', bold=True, size_hint_y=None, height=25, halign='left')
            name_label.bind(size=name_label.setter('text_size'))
            info_label = Label(text=f"📅 {event['date']}  📍 {event['place']}", font_size='12sp', size_hint_y=None, height=20, halign='left')
            info_label.bind(size=info_label.setter('text_size'))
            card.add_widget(name_label)
            card.add_widget(info_label)
            events_list.add_widget(card)
        scroll.add_widget(events_list)
        btn_back = Button(text="← Назад", size_hint=(1, 0.1), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(btn_back)
        self.clear_widgets()
        self.add_widget(layout)
    def go_back(self, instance): self.manager.current = 'main'


class ProfileScreen(Screen):
    def on_enter(self):
        self.display_profile()
    def display_profile(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        avatar = Label(text="👤", font_size='60sp', size_hint=(1, 0.2))
        title = Label(text="Личный кабинет", font_size='22sp', color=BRAND_GREEN, size_hint=(1, 0.1))
        info_label = Label(text="Здесь будет ваша статистика:\n\n✓ Посещённые маршруты\n✓ Избранные места\n✓ Отзывы и оценки\n✓ Настройки приложения", font_size='14sp', size_hint=(1, 0.4), halign='center', valign='top')
        info_label.bind(size=info_label.setter('text_size'))
        btn_back = Button(text="← Назад", size_hint=(1, 0.1), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(avatar)
        layout.add_widget(title)
        layout.add_widget(info_label)
        layout.add_widget(btn_back)
        self.clear_widgets()
        self.add_widget(layout)
    def go_back(self, instance): self.manager.current = 'main'


class WeatherScreen(Screen):
    def on_enter(self):
        self.display_weather()
    def display_weather(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        title = Label(text="🌤️ Погода в ХМАО-Югре", font_size='22sp', color=BRAND_GREEN, size_hint=(1, 0.15))
        weather_text = Label(text="Ханты-Мансийск\n\nТемпература: -5°C\nОблачно, снег\nВлажность: 85%\nВетер: 3 м/с\n\n⛄ Рекомендуем одеваться теплее!", font_size='16sp', size_hint=(1, 0.6), halign='center', valign='middle')
        weather_text.bind(size=weather_text.setter('text_size'))
        btn_back = Button(text="← Назад", size_hint=(1, 0.1), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(title)
        layout.add_widget(weather_text)
        layout.add_widget(btn_back)
        self.clear_widgets()
        self.add_widget(layout)
    def go_back(self, instance): self.manager.current = 'main'


class TourismApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(MapScreen(name='map'))
        sm.add_widget(RoutesScreen(name='routes'))
        sm.add_widget(EventsScreen(name='events'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(WeatherScreen(name='weather'))
        return sm


if __name__ == '__main__':
    TourismApp().run()
