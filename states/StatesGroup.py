from aiogram.dispatcher.filters.state import StatesGroup, State


class FacultyState(StatesGroup):
    get_titles = State()


class DirectionState(StatesGroup):
    get_titles = State()


class RegisterUser(StatesGroup):
    get_phone = State()
    get_language = State()
    #


class Registration_ru(StatesGroup):
    get_full_name = State()
    get_faculty = State()
    get_direction = State()
    get_group_name = State()
    get_programming_language = State()
    finish = State()


class Registration_uz(StatesGroup):
    get_full_name = State()
    get_faculty = State()
    get_direction = State()
    get_group_name = State()
    get_programming_language = State()
    finish = State()


class Chat(StatesGroup):
    get_public_msg = State()
    get_private_msg_to_user = State()
    get_private_msg_to_admin = State()
    get_message_to_answer = State()
    get_public_msg_to_edit = State()
    get_private_msg_to_edit = State()
    get_id_to_search = State()
    edit_public_msgs = State()
    edit_private_msg = State()
    videos_lessons = State()
    add_example1 = State()
    add_example2 = State()
    add_example3 = State()




class ChatUz(StatesGroup):
    get_public_msg = State()
    get_private_msg_to_user = State()
    get_private_msg_to_admin = State()
    get_message_to_answer = State()
    get_public_msg_to_edit = State()
    get_private_msg_to_edit = State()
    get_id_to_search = State()
    edit_public_msgs = State()
    edit_private_msg = State()
    choose_programming_language = State()
    examples_uz = State()
    examples_ru = State()



class ChannelState(StatesGroup):
    get_title = State()
    get_id = State()

class VideoLesson(StatesGroup):
    get_title = State()
    get_url = State()
    get_programming_language = State()
    check_url = State()

class ExamplesState(StatesGroup):
    get_programming_language = State()
    get_programming_language_uz = State()
    see_list = State()


class APIToken(StatesGroup):
    get_password = State()
    get_username = State()
    finish = State()

class CarCreate(StatesGroup):
    get_vin = State()
    get_color = State()
    get_brand = State()
    get_car_type = State()
    finish = State()



