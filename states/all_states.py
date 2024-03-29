from aiogram.dispatcher.filters.state import State, StatesGroup


    
class RegState(StatesGroup):
    phone = State()
    fullname = State()
    age = State()
    

class RegStateRu(StatesGroup):
    phone = State()
    fullname = State()
    age = State()
    
    
class TestState(StatesGroup):
    waiting_for_answer = State()
    
class TestStateRu(StatesGroup):
    waiting_for_answer = State()
    

class ApplicationState(StatesGroup):
    filial = State()
    
class ApplicationStateRu(StatesGroup):
    filial = State()

class ContactState(StatesGroup):
    answer = State()
    
class ContactStateRu(StatesGroup):
    answer = State()