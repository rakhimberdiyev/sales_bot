import asyncio
import random
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from keyboards.inline.all_inlines import langs, start_test_uz, application, filials
from keyboards.default.all_defaults import phone_uz, phone_ru
from keyboards.tests import test_uz
from loader import dp, db
from states.all_states import RegState, TestState, ApplicationState
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound

from utils.notify_admins import on_startup_notify, send_delayed_video


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    users = await db.select_all_telegram_ids(message.from_user.id)
    print("users: ", users)  
    if str(message.from_user.id) not in str(users):
        await db.add_user(message.from_user.id)
        print("Foydalanuvchi qo'shildi")
        await message.answer(f"Assalamu alaykum, {message.from_user.full_name}!\n\nMARS ITSchoolning sales botiga xush kelibsiz!\nTillardan birini tanlang\n\nДобро пожаловать вsales bot от Mars IT School!\nРаспознавание одного из языков:", reply_markup=langs)
    else:
        await message.answer(f"Assalamu alaykum, {message.from_user.full_name}!\n\nMARS ITSchoolning sales botiga xush kelibsiz!\nTillardan birini tanlang\n\nДобро пожаловать вsales bot от Mars IT School!\nРаспознавание одного из языков:", reply_markup=langs)
        
        
        
async def save_message_id(state: FSMContext, message: types.Message):
    async with state.proxy() as data:
        if 'message_ids' not in data:
            data['message_ids'] = []
        data['message_ids'].append(message.message_id)


@dp.callback_query_handler(text='uz', state=None)
async def uz_state_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    reply = await call.message.answer("Testni boshlash uchun iltimos, telefon raqamingizni kiriting📱\n\n", reply_markup=phone_uz)
    await save_message_id(state, reply)
    await RegState.phone.set()
    

@dp.message_handler(content_types=types.ContentType.CONTACT, state=RegState.phone)
async def uz_phone_state(message: types.Message, state=FSMContext):
    phone = message.contact.phone_number
        
    data = await state.update_data(
        {'phone': phone}
        )
    reply = await message.answer("Farzandingizning ism-familiyasi👨‍👨‍👧 \n\n", reply_markup=ReplyKeyboardRemove())
    await save_message_id(state, reply)
    await save_message_id(state, message)
    await RegState.next()
    
@dp.message_handler(state=RegState.fullname)
async def us_fullname_state(message: types.Message, state=FSMContext):
    fullname = message.text
    
    data = await state.update_data(
        {'full_name': fullname}
        )
    reply = await message.answer("Farzandingizning yoshi👫 \n\nMisol uchun 14\n")
    await save_message_id(state, reply)
    await save_message_id(state, message)
    await RegState.next()


@dp.message_handler(state=RegState.age)
async def us_fullname_state(message: types.Message, state=FSMContext):
    try:
        age = int(message.text)

        data = await state.update_data(
            {'age': age}
            )
        await save_message_id(state, message)
        
        
        data = await state.get_data()
        phone = data.get('phone')
        full_name = data.get('full_name')
        age = data.get('age')
        username = message.from_user.username
        telegram_id = message.from_user.id
        try:
            await db.update_user(phone, full_name, age, username, telegram_id)
            print(await db.select_all_users())
            print("update qilindi")
            await state.finish()
        except Exception as e:
            print(e)
            
        message_ids = data.get('message_ids', [])
        print(message_ids)
        for message_id in message_ids:
            try:
                await dp.bot.delete_message(message.from_user.id, message_id)
            except Exception as e:
                print(f"Xabarni o'chirishda xato: {e}")
        await message.answer("Ro’yxatdan o’tganingiz uchun raxmat! 😊")
        await message.answer(f"Telefon raqam: {phone}\n\nIsm familiya: {full_name}\n\nYosh: {age}")
        
        
        await message.answer_photo(photo="https://resources.biginterview.com/wp-content/uploads/2023/04/most-common-interview-questions.png", caption="Farzandingiz  qaysi yo’nalishda qobiliyati kuchli ekanligini bilishni xohlaysizmi?🤔\n\n", reply_markup=start_test_uz)

        
    except Exception as e:
        print(e)
        await message.answer("Itimos raqam kiriting:\n\nMisol uchun 14")

# @dp.callback_query_handler(text='start_test_uz', state=None)
# async def start_test_uz_handler(call: types.CallbackQuery):
#     n = 1
#     answers = []
#     for k, v in test_uz.items():
#         answer = f"{n}. {k}:"
#         inline_btn = InlineKeyboardMarkup(row_width=1)
#         for c, w in v.items():
#             btn = InlineKeyboardButton(text=c, callback_data=c)
#             inline_btn.add(btn)
        
#         await call.message.answer(answer, reply_markup=inline_btn)
        
#         n += 1
        
#     @dp.callback_query_handler()
#     async def answer_handler(call: types.CallbackQuery):
#         answer = call.data
#         answers.append(k[answer])
        

@dp.callback_query_handler(text='start_test_uz', state=None)
async def start_test_uz_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(TestState.waiting_for_answer)
    await state.update_data(current_question_index=0, answers=[])
    await call.message.delete()
    await send_question(call.message, state, answers=None, id=call.from_user.id)

async def send_question(message: types.Message, state: FSMContext, answers: list, id):
    user_data = await state.get_data()
    current_question_index = user_data.get("current_question_index", 0)
    questions = list(test_uz.keys())
    
    if current_question_index < len(questions):
        question = questions[current_question_index]
        options = test_uz[question]
        
        markup = InlineKeyboardMarkup()
        for option, value in options.items():
            callback_data = f"answer_{current_question_index}_{value}"
            markup.add(InlineKeyboardButton(option, callback_data=callback_data))
        
        await message.answer(f"{current_question_index+1}-savol \n\n{question}\n\n", reply_markup=markup)
    else:
        # await message.answer("Test yakunlandi. Raxmat!")
        await db.update_user_test_step(id)
        await state.finish()
        print(answers)
        design = 0
        front=0
        back=0
        full=0
        for i in answers:
            for v in i.values():
                if v == 'Dizayn':
                    design += 1
                elif v == 'Frontend' or v == 'Frontend/Fullstack':
                    front += 1
                elif v == 'Backend':
                    back += 1
                elif v == 'Fullstack' or v == 'Frontend/Fullstack':
                    full += 1
        results = [design, front, back, full]
        print(results)
        max_res = max(results)
        course_index = results.index(max_res)
        max_course = ''
        if course_index == 0:
            max_course = 'Dizayn'
        elif course_index == 1:
            max_course = 'Frontend' 
        elif course_index == 2:
            max_course = 'Backend'
        elif course_index == 3:
            max_course = 'Fullstack' 
        result = f"{max_course}:{max_res}ta"
        await db.update_user_result(result, id)
        print(result, message.from_user.id)
        prot = random.randint(75, 86) 
        await message.answer(f"Tabriklaymiz🤩Siz psixologik testdan o’tdingiz va natijalari bilan tanishing:\n\nSizning test natijalarinizdan kelib chiqqan holda farzandingizni bizning {max_course} kursimizga {prot}% to'g'ri kelishini aniqladik✅\n\nVa shuni inobatga olgan holda farzandingizga {max_course} kursimiz uchun 15% lik chegirma bermoqchimiz🤗\n\nSinov darsiga yozilish uchun quyidagi tugmani bosing", reply_markup=application)
        
        
        
        

@dp.callback_query_handler(text_contains='answer_', state=TestState.waiting_for_answer)
async def handle_answer(call: types.CallbackQuery, state: FSMContext):
    answer_data = call.data.split('_')
    question_index = int(answer_data[1])
    answer_value = answer_data[2]
    
    user_data = await state.get_data()
    answers = user_data.get("answers", [])
    answers.append({question_index: answer_value})
    
    await state.update_data(answers=answers, current_question_index=question_index + 1)
    
    # await asyncio.sleep(1)  # 1 soniya kutish
    try:
        await call.message.delete()
    except MessageToDeleteNotFound:
        pass
    
    await send_question(call.message, state, answers, id=call.from_user.id)

    # print(answers[-1])   

@dp.callback_query_handler(text='application')
async def application_handler(call: types.CallbackQuery, state=None):
    await call.message.delete()
    await call.message.answer("Sizga qulay bo’lgan filialni tanlang📍", reply_markup=filials)
    await ApplicationState.filial.set()

@dp.callback_query_handler(text=['yunusobod', 'tinchlik', 'chilonzor', 'sergeli'],state=ApplicationState.filial)
async def application_handler(call: types.CallbackQuery, state:FSMContext):
    filial = call.data
    await db.update_user_finish_step(filial, call.from_user.id)
    user = await db.select_finished_user(call.from_user.id)
    print(call.from_user.id)
    user = str(user)
    print(type(user))
    await call.message.delete()
    await call.message.answer("Arizangiz qabul qilindi ✅ \n\nBiz tez orada sizga aloqaga chiqamiz📞")
    await state.finish()
    await on_startup_notify(dp, user)
    await send_delayed_video(dp, call.from_user.id)
    

# @dp.message_handler(content_types=types.ContentType.VIDEO)
# async def video_handler(message: types.Message):
#     # video = message.video
#     video = message
#     print(video)
#     print("video keldi")
#     await message.answer(f"{video}")