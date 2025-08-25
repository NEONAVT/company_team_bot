from aiogram.filters import CommandStart, Command
from aiogram import types, Router, F
from aiogram.types import CallbackQuery
from settings import settings
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from users.services import users_service

router = Router()


class AdminStates(StatesGroup):
    waiting_for_username = State()


@router.message(CommandStart())
async def start(message: types.Message):
    user = await users_service.get_user(message.chat.id)

    if not user:
        user = await users_service.register_guest(
            chat_id=message.chat.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )

    await show_main_menu(message, chat_id=message.chat.id)


async def show_main_menu(message: types.Message, chat_id: int):
    user = await users_service.get_user(chat_id)
    display_name = user.first_name or user.username or "Пользователь"

    kb = []

    if user.role == settings.GUEST_ROLE:
        kb = [[types.InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await message.answer(
            f"Привет, {display_name}\n"
            f"Для регистрации получи ключ доступа у руководства и воспользуйся кнопкой ниже",
            reply_markup=keyboard
        )

    elif user.role == settings.USER_ROLE:
        kb = [
            [types.InlineKeyboardButton(text="Меню", callback_data="menu")],
            [
                types.InlineKeyboardButton(text="Наша история", callback_data="bio"),
                types.InlineKeyboardButton(text="Наши ценности", callback_data="corp_cult")
            ]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await message.answer(
            f"{display_name}, воспользуйся кнопками ниже для навигации.",
            reply_markup=keyboard
        )

    elif user.role == settings.OWNER_ROLE:
        kb = [
            [types.InlineKeyboardButton(text="Меню", callback_data="menu")],
            [
                types.InlineKeyboardButton(text="Наша история", callback_data="bio"),
                types.InlineKeyboardButton(text="Наши ценности", callback_data="corp_cult")
            ],
            [types.InlineKeyboardButton(text="Менеджмент", callback_data="management")]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await message.answer(
            f"{display_name}, воспользуйся кнопками ниже для навигации.",
            reply_markup=keyboard
        )


@router.callback_query(F.data == "register")
async def register_user(callback: CallbackQuery):
    update_user = await users_service.update_user(callback.message.chat.id)
    if update_user:
        kb = [
            [types.InlineKeyboardButton(text="В начало", callback_data="main")]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await callback.message.edit_text(
            f"Спасибо! Вы зарегистрированы как {update_user.role}\n"
            f"Твой статус: {update_user.role}",
            reply_markup=keyboard
        )
    else:
        await callback.answer("Ошибка при регистрации")


@router.callback_query(F.data == "main")
async def show_main(callback: CallbackQuery):
    await callback.answer()
    await show_main_menu(callback.message, chat_id=callback.message.chat.id)


@router.callback_query(F.data == "management")
async def grant_admin_permissions(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Введите логин сотрудника в телеграм (например, @ivan_ivanov)"
    )
    await state.set_state(AdminStates.waiting_for_username)


@router.message(AdminStates.waiting_for_username)
async def process_admin_permissions(message: types.Message, state: FSMContext):
    username = message.text.strip().lstrip("@")
    user = await users_service.grant_admin_permissions(username=username)

    kb = [
        [types.InlineKeyboardButton(text="В начало", callback_data="main")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

    if user:
        await message.answer(
            f"Пользователь @{username} получил права администратора",
            reply_markup=keyboard
        )
    else:
        await message.answer(
            f"Пользователь @{username} не найден",
            reply_markup=keyboard
        )

    await state.clear()

