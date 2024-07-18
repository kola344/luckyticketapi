from aiogram.fsm.state import State, StatesGroup

editor_tour_id = {}
editor_days_info = {}

class editor_days:
    def __init__(self, tour_id, day_id):
        self.tour_id = tour_id
        self.day_id = day_id

class tour_editorState(StatesGroup):
    edit_name = State()
    edit_description = State()
    edit_duration = State()
    edit_important_text = State()
    edit_card_image = State()
    edit_background_image = State()
    edit_day_info = State()

editor_departure = {}
class editor_dep:
    def __init__(self, tour_id, departure_id):
        self.tour_id = tour_id
        self.departure_id = departure_id
        self.variation_id = None

class departure_editorState(StatesGroup):
    edit_variation = State()
    edit_price = State()
    edit_departure_time = State()
    edit_arrival_time = State()
    edit_seats = State()
    edit_occupied_seats = State()
    edit_bus = State()


