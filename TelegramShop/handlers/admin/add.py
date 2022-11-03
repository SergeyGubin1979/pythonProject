from aiogram.dispatcher import FSMContext
from aiogram.types import (Message, CallbackQuery,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           ContentType, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.callback_data import CallbackData
from keyboards.default.markups import *
from states import ProductState, CategoryState
from aiogram.types.chat import ChatActions
from handlers.user.menu import settings
from loader import dp, db, bot
from filters import IsAdmin
from hashlib import md5

category_cb = CallbackData('category', 'id', 'action')
product_cb = CallbackData('product', 'id', 'action')

add_product = '➕ Добавить товар'
delete_category = '🗑️ Удалить категорию'

@dp.message_handler(IsAdmin(), text=settings)
async def process_settings(message: Message):

    markup = InlineKeyboardMarkup()

    for idx, title in db.fetchall('SELECT * FROM categories'):

        markup.add(InlineKeyboardButton(
            title, callback_data=category_cb.new(id=idx, action='view')))

    markup.add(InlineKeyboardButton(
        '+ Добавить категорию', callback_data='add_category'))

    await message.answer('Настройка категорий:', reply_markup=markup)

@dp.callback_query_handler(IsAdmin(), category_cb.filter(action='view'))
async def category_callback_handler(query: CallbackQuery, callback_data: dict, state:FSMContext):

    category_idx = callback_data['id']

    products = db.fetchall('''SELECT * FROM products product
    WHERE product.tag = (SELECT title FROM categories WHERE idx=?''',
                           (category_idx,))

    await query.message.delete()
    await query.answer('Все добавленные товары в эту категроию')
    await state.update_data(category_index=category_idx)
    await show_products(query.message, products, category_idx)

#category
@dp.callback_query_handler(IsAdmin(), text='add_category')
async def add_category_callback_handler(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer('Название категории?')
    await CategoryState.title.set()

@dp.message_handler(IsAdmin(), state=CategoryState.title)
async def set_category_title_handler(message: Message, state: FSMContext):

    category = message.text
    idx = md5(category.encode('utf-8')).hexdigest()
    db.query('INSERT INTO categories VALUES (?, ?)',(idx, category))

    await state.finish()
    await process_settings(message)

@dp.message_handler(IsAdmin(), text=delete_category)
async def delete_category_handler(message: Message, state: FSMContext):

    async with state.proxy() as data:
        if 'category_index' in data.keys():
            idx = data['category_index']

            db.query(
                'DELETE FROM products WHERE tag IN(SELECT title FROM categories WHERE idx=?',(idx,))
            db.query('DELETE FROM categories WHERE idx=?',(idx,))

            await message.answer('Готово!', reply_markup=ReplyKeyboardRemove())
            await process_settings(message)
#add product
@db.message_handler(IsAdmin(), text=add_product)
async def process_add_product(message: Message):

    await ProductState.title.set()

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(cancel_message)

    await message.answer('Название?', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(IsAdmin(), text=cancel_message, state=ProductState.title)
async def process_concel(message: Message, state: FSMContext):

    await message.answer('Ok, отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()

    await process_settings(message)

@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.title)
async def process_title_back(message: Message, state: FSMContext):
    await process_add_product(message)

@dp.message_handler(IsAdmin(), state=ProductState.title)
async def process_title(message:Message, state: FSMContext):

    async with state.proxy() as data:
        data['title'] = message.text
    await ProductState.next()
    await message.answer('Описание?', reply_markup=back_markup())

@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.body)
async def process_body_back(message: Message,state: FSMContext):

    await ProductState.title.set()

    async with state.proxy() as data:

        await message.answer(f"Изменить название с <b>{data['title']}</b>?", reply_markup=back_markup())

@dp.message_handler(IsAdmin(), state=ProductState.body)
async def process_body(message:Message, state: FSMContext):
    async with state.proxy() as data:
        data['body'] = message.text

    await ProductState.next()
    await message.answer('Фото?', reply_markup=back_markup())

@dp.message_handler(IsAdmin(), content_types=ContentType.PHOTO, state=ProductState.image)
async def process_image_photo(message: Message, state: FSMContext):

    fileID = message.photo[-1].file_id
    file_info = await bot.get_file(fileID)
    download_file = (await bot.download_file(file_info.file_path)).read()

    async with state.proxy() as data:
        data['image'] = download_file

    await ProductState.next()
    await message.answer('Цена?', reply_markup=back_markup)



