from aiogram.dispatcher.filters.state import State, StatesGroup


    
class RegState(StatesGroup):
    phone = State()
    fullname = State()
    age = State()
    
    
class TestState(StatesGroup):
    waiting_for_answer = State()
    

class ApplicationState(StatesGroup):
    filial = State()