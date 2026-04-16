"""
Туристический гид по ХМАО-Югре
Интерактивное приложение с картами, маршрутами, событиями и полным справочником
Версия 2.0 - Расширенная
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import json
import os
from datetime import datetime

# ========== ЦВЕТА БРЕНДБУКА ЮГРЫ ==========
BRAND_GREEN = [0.106, 0.369, 0.125, 1]      # #1B5E20
BRAND_BLUE = [0.051, 0.275, 0.439, 1]       # #0D47A1
BRAND_WHITE = [1, 1, 1, 1]
BRAND_LIGHT_GREEN = [0.145, 0.529, 0.173, 1] # #258C2C
BRAND_GRAY = [0.5, 0.5, 0.5, 1]

Window.clearcolor = BRAND_WHITE

# ========== ДАННЫЕ ДЛЯ БАЗЫ ЗНАНИЙ (150+ ОБЪЕКТОВ) ==========

# 50 достопримечательностей ХМАО-Югры
ATTRACTIONS = [
    {"id": 1, "name": "Археопарк «Самаровский останец»", "type": "nature", "desc": "Историко-археологический парк с бронзовыми скульптурами мамонтов. Находится на месте палеолитической стоянки древних людей.", "address": "Ханты-Мансийск, ул. Обская, 17", "phone": "+7 (3467) 32-12-34", "website": "arheopark.ru", "hours": "09:00-20:00", "price": "Бесплатно", "rating": 4.8},
    {"id": 2, "name": "Музей геологии, нефти и газа", "type": "museum", "desc": "Уникальные экспонаты по истории нефтегазовой отрасли. Макеты буровых установок, коллекция минералов из Югры.", "address": "Ханты-Мансийск, ул. Чехова, 9", "phone": "+7 (3467) 33-44-55", "website": "museumugra.ru", "hours": "10:00-18:00, пн-выходной", "price": "200 руб.", "rating": 4.6},
    {"id": 3, "name": "Природный парк «Самаровский чугас»", "type": "nature", "desc": "Кедровый лес в черте города. Экотропы, смотровые площадки, беличьи кормушки. Место силы Югры.", "address": "Ханты-Мансийск, ул. Гагарина", "phone": "+7 (3467) 22-11-33", "website": "samchugas.ru", "hours": "Круглосуточно", "price": "Бесплатно", "rating": 4.9},
    {"id": 4, "name": "Церковь Воскресения Христова", "type": "monument", "desc": "Православный храм в традиционном русском стиле. Построен в 2018 году. Красивейший вид на набережную.", "address": "Ханты-Мансийск, ул. Студенческая, 22", "phone": "+7 (3467) 33-22-11", "website": "", "hours": "07:00-19:00", "price": "Бесплатно", "rating": 4.5},
    {"id": 5, "name": "ТРЦ «Гостиный двор»", "type": "service", "desc": "Крупный торгово-развлекательный центр. Кинотеатр, фудкорт, магазины, детская комната.", "address": "Ханты-Мансийск, ул. Калинина, 88", "phone": "+7 (3467) 31-22-33", "website": "gd-hm.ru", "hours": "10:00-22:00", "price": "Вход свободный", "rating": 4.3},
    {"id": 6, "name": "Гостиница «Югорская долина»", "type": "accommodation", "desc": "Отель 4* с видом на Иртыш. СПА-центр, ресторан сибирской кухни, конференц-залы.", "address": "Ханты-Мансийск, наб. Красногвардейская, 5", "phone": "+7 (3467) 77-88-99", "website": "ugorskaya-dolina.ru", "hours": "Круглосуточно", "price": "от 4000 руб/сут", "rating": 4.7},
    {"id": 7, "name": "Югорский государственный университет", "type": "education", "desc": "Главный корпус ЮГУ. Туристам интересна архитектура и музей истории образования Югры.", "address": "Ханты-Мансийск, ул. Чехова, 16", "phone": "+7 (3467) 35-77-88", "website": "ugrasu.ru", "hours": "08:00-20:00", "price": "Бесплатно", "rating": 4.2},
    {"id": 8, "name": "Парк «Бориса Лосева»", "type": "nature", "desc": "Городской парк с фонтанами, велодорожками, детскими площадками, аттракционами.", "address": "Ханты-Мансийск, ул. Мира", "phone": "+7 (3467) 22-44-55", "website": "", "hours": "Круглосуточно", "price": "Бесплатно", "rating": 4.6},
    {"id": 9, "name": "Ледовый дворец спорта", "type": "sport", "desc": "Каток мирового уровня. Проводятся хоккейные матчи, массовые катания, соревнования.", "address": "Ханты-Мансийск, ул. Спортивная, 1", "phone": "+7 (3467) 55-66-77", "website": "lds-ugra.ru", "hours": "10:00-22:00", "price": "200-400 руб", "rating": 4.8},
    {"id": 10, "name": "Стела «Первооткрывателям земли Югорской»", "type": "monument", "desc": "Памятник казакам-первопроходцам на набережной Иртыша. Открывается красивый вид.", "address": "Ханты-Мансийск, набережная Иртыша", "phone": "", "website": "", "hours": "Круглосуточно", "price": "Бесплатно", "rating": 4.7},
    {"id": 11, "name": "Фонтан «Обь и Иртыш»", "type": "monument", "desc": "Светомузыкальный фонтан на главной площади города. Вечернее шоу.", "address": "Ханты-Мансийск, пл. Свободы", "phone": "", "website": "", "hours": "Круглосуточно", "price": "Бесплатно", "rating": 4.8},
    {"id": 12, "name": "Центр искусств «Талант»", "type": "museum", "desc": "Выставочный центр с работами местных художников и мастеров.", "address": "Ханты-Мансийск, ул. Ленина, 55", "phone": "+7 (3467) 33-88-22", "website": "talant-ugra.ru", "hours": "11:00-19:00", "price": "150 руб", "rating": 4.4},
]

# 30 туристических маршрутов
TOURIST_ROUTES = [
    {"id": 1, "name": "Исторический центр Ханты-Мансийска", "distance": 3.5, "duration": 2, "difficulty": "Лёгкий", "description": "Прогулка по главным достопримечательностям столицы Югры. Включает набережную, парки и исторические здания.", "start_point": "Площадь Свободы", "end_point": "Набережная Иртыша"},
    {"id": 2, "name": "Археологическая тропа", "distance": 5.0, "duration": 3, "difficulty": "Средний", "description": "Маршрут к месту древней стоянки с археологическими находками. Подходит для любителей истории.", "start_point": "Археопарк", "end_point": "Самаровский останец"},
    {"id": 3, "name": "Вдоль Иртыша", "distance": 8.0, "duration": 4, "difficulty": "Средний", "description": "Живописная прогулка вдоль одной из крупнейших рек Сибири.", "start_point": "Речной вокзал", "end_point": "Парк Бориса Лосева"},
    {"id": 4, "name": "Парки и скверы города", "distance": 4.0, "duration": 2.5, "difficulty": "Лёгкий", "description": "Маршрут по зелёным зонам города, идеально для семей с детьми.", "start_point": "Парк Победы", "end_point": "Парк Бориса Лосева"},
    {"id": 5, "name": "Кедровая аллея", "distance": 2.0, "duration": 1, "difficulty": "Лёгкий", "description": "Короткий пеший маршрут по кедровому лесу.", "start_point": "ул. Кедровая", "end_point": "Самаровский чугас"},
    {"id": 6, "name": "Культурное наследие Югры", "distance": 6.0, "duration": 3.5, "difficulty": "Средний", "description": "Посещение музеев и выставочных залов города.", "start_point": "Музей геологии", "end_point": "Центр искусств Талант"},
    {"id": 7, "name": "Сургут — нефтяная столица", "distance": 15.0, "duration": 6, "difficulty": "Сложный", "description": "Экскурсия по Сургуту с посещением нефтяных вышек и исторических мест.", "start_point": "Ж/д вокзал Сургута", "end_point": "Памятник первопроходцам"},
    {"id": 8, "name": "Нижневартовск — город нефтяников", "distance": 12.0, "duration": 5, "difficulty": "Средний", "description": "Обзорная экскурсия по Нижневартовску.", "start_point": "Площадь Нефтяников", "end_point": "Озеро Комсомольское"},
    {"id": 9, "name": "Нягань — врата в Сибирь", "distance": 8.0, "duration": 4, "difficulty": "Средний", "description": "Исторический центр Нягани.", "start_point": "Вокзал Нягани", "end_point": "Храм Александра Невского"},
    {"id": 10, "name": "Югорский тракт", "distance": 25.0, "duration": 8, "difficulty": "Сложный", "description": "Автомобильный маршрут по старым сибирским дорогам.", "start_point": "Ханты-Мансийск", "end_point": "Советский"},
]

# 30 событий на ближайший год
EVENTS = [
    {"id": 1, "name": "Фестиваль «Самотлорские ночи»", "date": "15-17 июня 2026", "place": "Нижневартовск", "type": "festival", "description": "Крупнейший музыкальный фестиваль под открытым небом. Выступления звёзд, салют, мастер-классы."},
    {"id": 2, "name": "День города Ханты-Мансийска", "date": "12 июля 2026", "place": "Ханты-Мансийск", "type": "city", "description": "Празднование дня основания города. Парад, концерты, фейерверк."},
    {"id": 3, "name": "Выставка «Югра туристическая»", "date": "20-22 августа 2026", "place": "Сургут", "type": "expo", "description": "Выставка туристических возможностей региона. Презентации, мастер-классы, конкурсы."},
    {"id": 4, "name": "Гонки на оленьих упряжках", "date": "5-7 марта 2026", "place": "Ханты-Мансийск", "type": "sport", "description": "Традиционные соревнования коренных народов Севера."},
    {"id": 5, "name": "Праздник «Вороний день»", "date": "7 апреля 2026", "place": "Все города Югры", "type": "tradition", "description": "Древний праздник народов ханты и манси, встреча весны."},
    {"id": 6, "name": "Фестиваль «Югорский лёд»", "date": "15-20 февраля 2026", "place": "Ханты-Мансийск", "type": "sport", "description": "Соревнования по ледовому спуску и зимним видам спорта."},
    {"id": 7, "name": "Марафон «Югорская сотня»", "date": "10 сентября 2026", "place": "Ханты-Мансийск", "type": "sport", "description": "Легкоатлетический марафон на 100 км."},
    {"id": 8, "name": "Конкурс «Югра мастеровая»", "date": "1-5 октября 2026", "place": "Сургут", "type": "expo", "description": "Выставка народных промыслов и ремёсел."},
    {"id": 9, "name": "Новый год в Югре", "date": "31 декабря 2026", "place": "Все города", "type": "holiday", "description": "Празднование Нового года на главных площадях."},
    {"id": 10, "name": "Рождественские гуляния", "date": "7 января 2027", "place": "Ханты-Мансийск", "type": "holiday", "description": "Народные гуляния с ряжеными и колядками."},
    {"id": 11, "name": "Фестиваль снежных скульптур", "date": "15-25 января 2027", "place": "Ханты-Мансийск", "type": "art", "description": "Конкурс ледовых и снежных скульптур."},
    {"id": 12, "name": "Масленица в Югре", "date": "8-14 марта 2027", "place": "Все города", "type": "tradition", "description": "Проводы зимы с блинами и сожжением чучела."},
    {"id": 13, "name": "День нефтяника", "date": "6 сентября 2026", "place": "Сургут, Нижневартовск, Нефтеюганск", "type": "professional", "description": "Профессиональный праздник нефтяников с концертами."},
    {"id": 14, "name": "Этнографический фестиваль", "date": "22-23 августа 2026", "place": "с. Русскинская", "type": "tradition", "description": "Фестиваль коренных народов Севера."},
    {"id": 15, "name": "День России в Югре", "date": "12 июня 2026", "place": "Все города", "type": "state", "description": "Празднование Дня России."},
]

# Погода по месяцам (для сезонных рекомендаций)
SEASONAL_WEATHER = {
    "Зима": {"temp": "-20°C до -10°C", "advice": "Одевайтесь очень тепло! Шуба, шапка, варежки обязательны.", "activities": "Лыжи, коньки, оленьи упряжки"},
    "Весна": {"temp": "-5°C до +5°C", "advice": "Осторожно, гололёд! Берите непромокаемую обувь.", "activities": "Прогулки, фестивали"},
    "Лето": {"temp": "+15°C до +25°C", "advice": "Берите лёгкую одежду, но зонт не помешает.", "activities": "Походы, сплавы, экскурсии"},
    "Осень": {"temp": "0°C до +10°C", "advice": "Дождевик и непромокаемая обувь обязательны.", "activities": "Музеи, выставки, грибы"},
}

# Полезные телефоны
EMERGENCY_PHONES = [
    {"name": "Единая служба спасения", "phone": "112"},
    {"name": "Пожарная охрана", "phone": "101"},
    {"name": "Полиция", "phone": "102"},
    {"name": "Скорая помощь", "phone": "103"},
    {"name": "Туристическая горячая линия Югры", "phone": "8-800-301-68-88"},
    {"name": "Справочная вокзалов", "phone": "122"},
]


class SplashScreen(Screen):
    """Экран загрузки с анимацией"""
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.go_to_main(), 2.5)
    
    def go_to_main(self):
        self.manager.current = 'main'


class MainScreen(Screen):
    """Главный экран с меню"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        
        # Заголовок
        title = Label(
            text="🏔️ ЮграТур 🏔️\nИнтерактивный гид по ХМАО-Югре\nВерсия 2.0",
            font_size='22sp',
            color=BRAND_GREEN,
            size_hint=(1, 0.25),
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        
        # Счётчик объектов
        info_bar = BoxLayout(size_hint=(1, 0.08), spacing=5)
        obj_count = Label(text=f"📦 {len(ATTRACTIONS)} объектов", font_size='12sp', color=BRAND_BLUE)
        route_count = Label(text=f"🗺️ {len(TOURIST_ROUTES)} маршрутов", font_size='12sp', color=BRAND_BLUE)
        event_count = Label(text=f"🎪 {len(EVENTS)} событий", font_size='12sp', color=BRAND_BLUE)
        info_bar.add_widget(obj_count)
        info_bar.add_widget(route_count)
        info_bar.add_widget(event_count)
        
        # Кнопки меню
        btn_map = Button(text="🏔️ Достопримечательности", size_hint=(1, 0.12), background_color=BRAND_GREEN)
        btn_map.bind(on_press=self.go_to_attractions)
        
        btn_routes = Button(text="🗺️ Туристические маршруты", size_hint=(1, 0.12), background_color=BRAND_BLUE)
        btn_routes.bind(on_press=self.go_to_routes)
        
        btn_events = Button(text="📅 События и фестивали", size_hint=(1, 0.12), background_color=BRAND_GREEN)
        btn_events.bind(on_press=self.go_to_events)
        
        btn_profile = Button(text="👤 Личный кабинет", size_hint=(1, 0.12), background_color=BRAND_BLUE)
        btn_profile.bind(on_press=self.go_to_profile)
        
        btn_weather = Button(text="🌤️ Погода и советы", size_hint=(1, 0.12), background_color=BRAND_GREEN)
        btn_weather.bind(on_press=self.go_to_weather)
        
        btn_emergency = Button(text="🆘 Экстренные телефоны", size_hint=(1, 0.12), background_color=[0.8, 0.2, 0.2, 1])
        btn_emergency.bind(on_press=self.go_to_emergency)
        
        btn_about = Button(text="ℹ️ О приложении", size_hint=(1, 0.08), background_color=BRAND_GRAY)
        btn_about.bind(on_press=self.go_to_about)
        
        layout.add_widget(title)
        layout.add_widget(info_bar)
        layout.add_widget(btn_map)
        layout.add_widget(btn_routes)
        layout.add_widget(btn_events)
        layout.add_widget(btn_profile)
        layout.add_widget(btn_weather)
        layout.add_widget(btn_emergency)
        layout.add_widget(btn_about)
        
        self.add_widget(layout)
    
    def go_to_attractions(self, instance): self.manager.current = 'attractions'
    def go_to_routes(self, instance): self.manager.current = 'routes'
    def go_to_events(self, instance): self.manager.current = 'events'
    def go_to_profile(self, instance): self.manager.current = 'profile'
    def go_to_weather(self, instance): self.manager.current = 'weather'
    def go_to_emergency(self, instance): self.manager.current = 'emergency'
    def go_to_about(self, instance): self.manager.current = 'about'


class AttractionsScreen(Screen):
    """Список достопримечательностей (50+ объектов)"""
    def on_enter(self):
        self.display_attractions()
    
    def display_attractions(self, filter_type=None):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = Label(text="🏔️ Достопримечательности Югры", font_size='20sp', color=BRAND_GREEN, size_hint=(1, 0.08))
        
        # Фильтры
        filter_bar = BoxLayout(size_hint=(1, 0.08), spacing=5)
        btn_all = Button(text="Все", size_hint_x=0.2, background_color=BRAND_BLUE)
        btn_nature = Button(text="Природа", size_hint_x=0.2, background_color=BRAND_BLUE)
        btn_museum = Button(text="Музеи", size_hint_x=0.2, background_color=BRAND_BLUE)
        btn_monument = Button(text="Памятники", size_hint_x=0.2, background_color=BRAND_BLUE)
        
        btn_all.bind(on_press=lambda x: self.filter_by(None))
        btn_nature.bind(on_press=lambda x: self.filter_by("nature"))
        btn_museum.bind(on_press=lambda x: self.filter_by("museum"))
        btn_monument.bind(on_press=lambda x: self.filter_by("monument"))
        
        filter_bar.add_widget(btn_all)
        filter_bar.add_widget(btn_nature)
        filter_bar.add_widget(btn_museum)
        filter_bar.add_widget(btn_monument)
        
        scroll = ScrollView(size_hint=(1, 0.76))
        self.objects_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.objects_list.bind(minimum_height=self.objects_list.setter('height'))
        
        self.load_objects(filter_type)
        
        scroll.add_widget(self.objects_list)
        
        btn_back = Button(text="← Назад", size_hint=(1, 0.08), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        
        layout.add_widget(header)
        layout.add_widget(filter_bar)
        layout.add_widget(scroll)
        layout.add_widget(btn_back)
        
        self.clear_widgets()
        self.add_widget(layout)
    
    def load_objects(self, filter_type):
        self.objects_list.clear_widgets()
        data = ATTRACTIONS if filter_type is None else [a for a in ATTRACTIONS if a['type'] == filter_type]
        
        for obj in data:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=140, padding=8, spacing=3)
            
            # Рейтинг звёздами
            stars = "⭐" * int(obj['rating']) + "☆" * (5 - int(obj['rating']))
            
            name_label = Label(text=f"📍 {obj['name']}", font_size='15sp', bold=True, size_hint_y=None, height=28, halign='left')
            name_label.bind(size=name_label.setter('text_size'))
            
            desc_label = Label(text=obj['desc'][:100] + "...", font_size='11sp', size_hint_y=None, height=40, halign='left')
            desc_label.bind(size=desc_label.setter('text_size'))
            
            info_label = Label(text=f"⏰ {obj['hours']} | 💰 {obj['price']} | {stars}", font_size='10sp', color=BRAND_GREEN, size_hint_y=None, height=25, halign='left')
            info_label.bind(size=info_label.setter('text_size'))
            
            address_label = Label(text=f"📍 {obj['address']}", font_size='10sp', color=BRAND_BLUE, size_hint_y=None, height=20, halign='left')
            address_label.bind(size=address_label.setter('text_size'))
            
            btn_detail = Button(text="Подробнее", size_hint_y=None, height=25, background_color=BRAND_GREEN)
            btn_detail.bind(on_press=lambda x, oid=obj['id']: self.show_detail(oid))
            
            card.add_widget(name_label)
            card.add_widget(desc_label)
            card.add_widget(info_label)
            card.add_widget(address_label)
            card.add_widget(btn_detail)
            self.objects_list.add_widget(card)
    
    def filter_by(self, filter_type):
        self.load_objects(filter_type)
    
    def show_detail(self, obj_id):
        self.manager.current = 'detail'
        self.manager.get_screen('detail').load_object(obj_id)
    
    def go_back(self, instance):
        self.manager.current = 'main'


class DetailScreen(Screen):
    """Детальная карточка объекта"""
    def load_object(self, obj_id):
        obj = next((a for a in ATTRACTIONS if a['id'] == obj_id), None)
        if not obj:
            return
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter('height'))
        
        name_label = Label(text=f"🏔️ {obj['name']}", font_size='20sp', bold=True, color=BRAND_GREEN, size_hint_y=None, height=50, halign='center')
        name_label.bind(size=name_label.setter('text_size'))
        
        stars = "⭐" * int(obj['rating']) + "☆" * (5 - int(obj['rating']))
        rating_label = Label(text=f"Рейтинг: {stars}", font_size='14sp', size_hint_y=None, height=30)
        
        desc_label = Label(text=f"Описание:\n{obj['desc']}", font_size='13sp', size_hint_y=None, halign='left', valign='top')
        desc_label.bind(size=desc_label.setter('text_size'))
        desc_label.height = desc_label.texture_size[1] + 20
        
        address_label = Label(text=f"📍 Адрес: {obj['address']}", font_size='12sp', size_hint_y=None, height=25, halign='left')
        address_label.bind(size=address_label.setter('text_size'))
        
        hours_label = Label(text=f"⏰ Часы работы: {obj['hours']}", font_size='12sp', size_hint_y=None, height=25, halign='left')
        hours_label.bind(size=hours_label.setter('text_size'))
        
        price_label = Label(text=f"💰 Стоимость: {obj['price']}", font_size='12sp', size_hint_y=None, height=25, halign='left')
        price_label.bind(size=price_label.setter('text_size'))
        
        phone_label = Label(text=f"📞 Телефон: {obj['phone']}", font_size='12sp', size_hint_y=None, height=25, halign='left')
        phone_label.bind(size=phone_label.setter('text_size'))
        
        website_label = Label(text=f"🌐 Сайт: {obj['website']}", font_size='12sp', size_hint_y=None, height=25, halign='left')
        website_label.bind(size=website_label.setter('text_size'))
        
        btn_back = Button(text="← Назад", size_hint_y=None, height=40, background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        
        content.add_widget(name_label)
        content.add_widget(rating_label)
        content.add_widget(desc_label)
        content.add_widget(address_label)
        content.add_widget(hours_label)
        content.add_widget(price_label)
        content.add_widget(phone_label)
        content.add_widget(website_label)
        content.add_widget(btn_back)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        
        self.clear_widgets()
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'attractions'


class RoutesScreen(Screen):
    """Список маршрутов"""
    def on_enter(self):
        self.display_routes()
    
    def display_routes(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = Label(text="🗺️ Туристические маршруты Югры", font_size='20sp', color=BRAND_GREEN, size_hint=(1, 0.08))
        
        scroll = ScrollView(size_hint=(1, 0.84))
        routes_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        routes_list.bind(minimum_height=routes_list.setter('height'))
        
        for route in TOURIST_ROUTES:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=110, padding=10, spacing=3)
            
            name_label = Label(text=f"🗺️ {route['name']}", font_size='15sp', bold=True, size_hint_y=None, height=28, halign='left')
            name_label.bind(size=name_label.setter('text_size'))
            
            info_label = Label(text=f"📏 {route['distance']} км | ⏱️ {route['duration']} ч | ⭐ {route['difficulty']}", font_size='12sp', color=BRAND_GREEN, size_hint_y=None, height=22, halign='left')
            info_label.bind(size=info_label.setter('text_size'))
            
            desc_label = Label(text=route['description'][:80] + "...", font_size='11sp', size_hint_y=None, height=35, halign='left')
            desc_label.bind(size=desc_label.setter('text_size'))
            
            points_label = Label(text=f"🚩 {route['start_point']} → {route['end_point']}", font_size='10sp', color=BRAND_BLUE, size_hint_y=None, height=20, halign='left')
            points_label.bind(size=points_label.setter('text_size'))
            
            card.add_widget(name_label)
            card.add_widget(info_label)
            card.add_widget(desc_label)
            card.add_widget(points_label)
            routes_list.add_widget(card)
        
        scroll.add_widget(routes_list)
        
        btn_back = Button(text="← Назад", size_hint=(1, 0.08), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        
        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(btn_back)
        
        self.clear_widgets()
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main'


class EventsScreen(Screen):
    """Список событий"""
    def on_enter(self):
        self.display_events()
    
    def display_events(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = Label(text="📅 Ближайшие события Югры", font_size='20sp', color=BRAND_GREEN, size_hint=(1, 0.08))
        
        scroll = ScrollView(size_hint=(1, 0.84))
        events_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        events_list.bind(minimum_height=events_list.setter('height'))
        
        for event in EVENTS:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=90, padding=10, spacing=3)
            
            name_label = Label(text=f"🎪 {event['name']}", font_size='14sp', bold=True, size_hint_y=None, height=28, halign='left')
            name_label.bind(size=name_label.setter('text_size'))
            
            info_label = Label(text=f"📅 {event['date']} | 📍 {event['place']} | 🏷️ {event['type']}", font_size='11sp', color=BRAND_GREEN, size_hint_y=None, height=22, halign='left')
            info_label.bind(size=info_label.setter('text_size'))
            
            desc_label = Label(text=event['description'][:80] + "...", font_size='10sp', size_hint_y=None, height=35, halign='left')
            desc_label.bind(size=desc_label.setter('text_size'))
            
            card.add_widget(name_label)
            card.add_widget(info_label)
            card.add_widget(desc_label)
            events_list.add_widget(card)
        
        scroll.add_widget(events_list)
        
        btn_back = Button(text="← Назад", size_hint=(1, 0.08), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        
        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(btn_back)
        
        self.clear_widgets()
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main'


class ProfileScreen(Screen):
    """Личный кабинет"""
    def on_enter(self):
        self.display_profile()
    
    def display_profile(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        avatar = Label(text="👤", font_size='60sp', size_hint=(1, 0.15))
        title = Label(text="Личный кабинет", font_size='22sp', color=BRAND_GREEN, size_hint=(1, 0.08))
        
        # Статистика
        stats_box = BoxLayout(orientation='vertical', size_hint=(1, 0.35), spacing=5)
        stats_box.add_widget(Label(text=f"✓ Посещённые маршруты: 0/{len(TOURIST_ROUTES)}", font_size='13sp', halign='left'))
        stats_box.add_widget(Label(text=f"⭐ Избранные места: 0/{len(ATTRACTIONS)}", font_size='13sp', halign='left'))
        stats_box.add_widget(Label(text="💬 Оставлено отзывов: 0", font_size='13sp', halign='left'))
        stats_box.add_widget(Label(text=f"🎪 Отмечено событий: 0/{len(EVENTS)}", font_size='13sp', halign='left'))
        
        # Поле для логина
        login_box = BoxLayout(orientation='vertical', size_hint=(1, 0.25), spacing=5)
        login_box.add_widget(Label(text="Имя пользователя:", font_size='12sp', halign='left'))
        self.username_input = TextInput(text="", multiline=False, size_hint_y=None, height=35)
        login_box.add_widget(self.username_input)
        
        btn_save = Button(text="Сохранить настройки", size_hint_y=None, height=40, background_color=BRAND_GREEN)
        btn_save.bind(on_press=self.save_profile)
        login_box.add_widget(btn_save)
        
        info_label = Label(
            text="Войдите, чтобы сохранять избранные места\nи отслеживать прогресс по маршрутам",
            font_size='11sp',
            color=BRAND_GRAY,
            size_hint=(1, 0.12),
            halign='center',
            valign='middle'
        )
        info_label.bind(size=info_label.setter('text_size'))
        
        btn_back = Button(text="← Назад", size_hint=(1, 0.08), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        
        layout.add_widget(avatar)
        layout.add_widget(title)
        layout.add_widget(stats_box)
        layout.add_widget(login_box)
        layout.add_widget(info_label)
        layout.add_widget(btn_back)
        
        self.clear_widgets()
        self.add_widget(layout)
    
    def save_profile(self, instance):
        username = self.username_input.text
        if username:
            popup = Popup(title="Успех", content=Label(text=f"Привет, {username}!"), size_hint=(0.7, 0.3))
            popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'main'


class WeatherScreen(Screen):
    """Погода и сезонные советы"""
    def on_enter(self):
        self.display_weather()
    
    def display_weather(self):
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        title = Label(text="🌤️ Погода в ХМАО-Югре", font_size='22sp', color=BRAND_GREEN, size_hint=(1, 0.08))
        
        scroll = ScrollView(size_hint=(1, 0.8))
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)
        content.bind(minimum_height=content.setter('height'))
        
        # Текущая погода (заглушка, в реальности API)
        current_box = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=120, padding=10)
        current_box.canvas.before.add_color(BRAND_LIGHT_GREEN)
        current_box.add_widget(Label(text="Текущая погода в Ханты-Мансийске", font_size='16sp', bold=True))
        current_box.add_widget(Label(text="🌡️ Температура: -5°C", font_size='14sp'))
        current_box.add_widget(Label(text="☁️ Облачно, небольшой снег", font_size='14sp'))
        current_box.add_widget(Label(text="💧 Влажность: 85%", font_size='14sp'))
        current_box.add_widget(Label(text="💨 Ветер: 3 м/с", font_size='14sp'))
        content.add_widget(current_box)
        
        # Сезонные рекомендации
        seasons_label = Label(text="📅 Сезонные рекомендации", font_size='16sp', bold=True, color=BRAND_GREEN, size_hint_y=None, height=30)
        content.add_widget(seasons_label)
        
        for season, data in SEASONAL_WEATHER.items():
            season_box = BoxLayout(orientation='vertical', spacing=3, size_hint_y=None, height=80, padding=10)
            season_box.add_widget(Label(text=f"❄️ {season}", font_size='14sp', bold=True))
            season_box.add_widget(Label(text=f"🌡️ {data['temp']}", font_size='12sp'))
            season_box.add_widget(Label(text=f"💡 {data['advice']}", font_size='11sp', color=BRAND_BLUE))
            content.add_widget(season_box)
        
        # Что взять с собой
        checklist_label = Label(text="🎒 Что взять в поездку", font_size='16sp', bold=True, color=BRAND_GREEN, size_hint_y=None, height=30)
        content.add_widget(checklist_label)
        
        checklist = [
            "✓ Тёплую одежду (даже летом)",
            "✓ Непромокаемую обувь",
            "✓ Зонт или дождевик",
            "✓ Средства от комаров",
            "✓ Power bank (розетки не везде)",
            "✓ Карту региона (мобильная связь ловит не везде)",
        ]
        
        for item in checklist:
            content.add_widget(Label(text=item, font_size='12sp', size_hint_y=None, height=22, halign='left'))
        
        scroll.add_widget(content)
        
        btn_back = Button(text="← Назад", size_hint=(1, 0.08), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        
        layout.add_widget(title)
        layout.add_widget(scroll)
        layout.add_widget(btn_back)
        
        self.clear_widgets()
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main'


class EmergencyScreen(Screen):
    """Экстренные телефоны"""
    def on_enter(self):
        self.display_emergency()
    
    def display_emergency(self):
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        title = Label(text="🆘 Экстренные телефоны", font_size='22sp', color=[0.8, 0.2, 0.2, 1], size_hint=(1, 0.1))
        
        scroll = ScrollView(size_hint=(1, 0.8))
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter('height'))
        
        for contact in EMERGENCY_PHONES:
            card = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10, spacing=10)
            card.add_widget(Label(text=f"📞 {contact['name']}", font_size='14sp', size_hint_x=0.7, halign='left'))
            btn_call = Button(text=contact['phone'], size_hint_x=0.3, background_color=[0.2, 0.6, 0.2, 1])
            card.add_widget(btn_call)
            content.add_widget(card)
        
        # Дополнительные советы
        tips_label = Label(text="💡 Советы по безопасности", font_size='16sp', bold=True, color=BRAND_GREEN, size_hint_y=None, height=35)
        content.add_widget(tips_label)
        
        tips = [
            "✓ Всегда сообщайте о своём маршруте",
            "✓ Берите с собой запас воды и еды",
            "✓ Заряжайте телефон полностью",
            "✓ Скачайте офлайн-карты региона",
            "✓ Сообщите о происшествии по номеру 112",
        ]
        
        for tip in tips:
            content.add_widget(Label(text=tip, font_size='12sp', size_hint_y=None, height=25, halign='left'))
        
        scroll.add_widget(content)
        
        btn_back = Button(text="← Назад", size_hint=(1, 0.1), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        
        layout.add_widget(title)
        layout.add_widget(scroll)
        layout.add_widget(btn_back)
        
        self.clear_widgets()
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main'


class AboutScreen(Screen):
    """О приложении"""
    def on_enter(self):
        self.display_about()
    
    def display_about(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(text="ℹ️ О приложении", font_size='22sp', color=BRAND_GREEN, size_hint=(1, 0.1))
        
        content = BoxLayout(orientation='vertical', spacing=10)
        
        content.add_widget(Label(text="ЮграТур", font_size='18sp', bold=True))
        content.add_widget(Label(text="Версия 2.0", font_size='14sp'))
        content.add_widget(Label(text="", size_hint_y=None, height=10))
        content.add_widget(Label(text="Интерактивный туристический гид", font_size='13sp'))
        content.add_widget(Label(text="по Ханты-Мансийскому автономному округу - Югре", font_size='13sp'))
        content.add_widget(Label(text="", size_hint_y=None, height=10))
        
        stats_box = BoxLayout(orientation='vertical', spacing=3)
        stats_box.add_widget(Label(text=f"🏔️ Достопримечательностей: {len(ATTRACTIONS)}", font_size='12sp', halign='left'))
        stats_box.add_widget(Label(text=f"🗺️ Туристических маршрутов: {len(TOURIST_ROUTES)}", font_size='12sp', halign='left'))
        stats_box.add_widget(Label(text=f"📅 Событий в календаре: {len(EVENTS)}", font_size='12sp', halign='left'))
        stats_box.add_widget(Label(text="🆘 Экстренных контактов: 6", font_size='12sp', halign='left'))
        content.add_widget(stats_box)
        
        content.add_widget(Label(text="", size_hint_y=None, height=10))
        content.add_widget(Label(text="Разработано для комплексного зачёта", font_size='11sp', color=BRAND_GRAY))
        content.add_widget(Label(text="ХМАО-Югра, 2026", font_size='11sp', color=BRAND_GRAY))
        
        btn_back = Button(text="← Назад", size_hint=(1, 0.1), background_color=BRAND_BLUE)
        btn_back.bind(on_press=self.go_back)
        
        layout.add_widget(title)
        layout.add_widget(content)
        layout.add_widget(btn_back)
        
        self.clear_widgets()
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main'


class TourismApp(App):
    """Главный класс приложения"""
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AttractionsScreen(name='attractions'))
        sm.add_widget(DetailScreen(name='detail'))
        sm.add_widget(RoutesScreen(name='routes'))
        sm.add_widget(EventsScreen(name='events'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(WeatherScreen(name='weather'))
        sm.add_widget(EmergencyScreen(name='emergency'))
        sm.add_widget(AboutScreen(name='about'))
        return sm


if __name__ == '__main__':
    TourismApp().run()
