import logging
from aiogram import Dispatcher, Bot, executor, types
import time

logging.basicConfig(filename="logging.log", level=logging.INFO)

check_list = ["+", "-", "/", "*"]
number_list = []
calc_list = []


def iscalc(text):
    global check_list
    if text in check_list:
        return 1
    else:
        return 0


def isnumber(numb):
    global check_list
    if numb in check_list:
        return 1
    elif isinstance(complex(numb), complex) and complex(numb).imag != 0:
        return 1
    elif numb.isdigit:
        return 1
    elif numb in check_list:
        return 1
    else:
        return 0


def return_number(numb):
    if isinstance(complex(numb), complex) and complex(numb).imag != 0:
        return complex(numb)
    else:
        return float(numb)


def calculator(numb1, action, numb2):
    newnumb1 = return_number(numb1)
    newnumb2 = return_number(numb2)
    if action == "/" and newnumb2 == 0:
        return "Делить на ноль нельзя"
    else:
        operation = {
            '+': newnumb1+newnumb2,
            '-': newnumb1-newnumb2,
            '*': newnumb1*newnumb2,
            '/': newnumb1/newnumb2
        }
    return operation[action]


TOKEN = ""
MSG = "Добро пожаловать в калькулятор!"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
user_id = ""


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    global user_id
    global check_list
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_name = message.from_user.first_name
    logging.info(f"{user_id=} {user_full_name=} , {time.asctime()} ")
    await message.reply(f"Привет, {user_full_name}")

    await bot.send_message(user_id, MSG.format(user_name))
    await bot.send_message(user_id, "Введите число (если оно комплексное, то в формате a+bj)")

    @dp.message_handler(lambda message: not isnumber(message.text.replace(" ", "")))
    async def check_empty(message: types.Message):
        return await message.reply("Это не число и не действие\n Введите число (если оно комплексное, то в формате a+bj)")

    @dp.message_handler(lambda message: iscalc(message.text))
    async def calc_handler1(message: types.Message):
        global user_id
        global calc_list
        calc = message.text
        if calc_list == []:
            calc_list.append(calc)
            await bot.send_message(user_id, "Введите второе число(если оно комплексное, то в формате a+bj)")
        else:
            await bot.send_message(user_id, "Действие (+, -, *,/) уже введено, введите число")

    @dp.message_handler(lambda message: isnumber(message.text.replace(" ", "")))
    async def numbers_handler(message: types.Message):
        global user_id
        global number_list
        global calc_list
        number = return_number(message.text.replace(" ", ""))
        if len(number_list) < 2:
            number_list.append(number)
        else:
            await bot.send_message(user_id, "Уже введено два числа,введите действие")

        if len(number_list) == 1:
            await bot.send_message(user_id, "Введите действие (+, -, *,/) с первым числом")
        else:
            await bot.send_message(user_id, f"Результат вычислений {number_list[0]} {calc_list[0]} {number_list[1]} равен {calculator(number_list[0],calc_list[0],number_list[1])}")
            await bot.send_message(user_id, "Нажмите /start")
            number_list = []
            calc_list = []


if __name__ == "__main__":
    executor.start_polling(dp)
