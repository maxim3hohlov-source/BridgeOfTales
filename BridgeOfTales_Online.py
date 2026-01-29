import customtkinter
import multiprocessing
import webview
from PIL import Image, ImageTk
import os
from tkinter import filedialog, messagebox
import json
import random
import sys
import tkinter
import threading
from tkinter import colorchooser
import asyncio
import websockets
import uuid
from threading import Thread
import queue
import logging
from datetime import datetime
import base64
import io
import hashlib
import tempfile

# ==================== НАСТРОЙКА ЛОГИРОВАНИЯ ====================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


CHUNK_SIZE = 65536  # 64KB - размер одного чанка
MAX_DIRECT_SIZE = 2 * 1024 * 1024  # 2MB - максимальный размер для прямой отправки
MAX_IMAGE_PIXELS = 8000 * 8000  # 64 мегапикселя


connection_status = "disconnected"
client_id = str(uuid.uuid4())[:8]
is_host = False
image_path = None


# ==================== ФУНКЦИИ ДЛЯ ИГРЫ ====================
def roll(text):
    """Бросок кубика"""
    text_str = str(text)
    dice_map = {
        "4": lambda: random.randint(1, 4),
        "6": lambda: random.randint(1, 6),
        "8": lambda: random.randint(1, 8),
        '10': lambda: random.randint(1, 10),
        "12": lambda: random.randint(1, 12),
        "20": lambda: random.randint(1, 20),
        "100": lambda: random.randint(1, 100),
    }
    return dice_map.get(text_str, lambda: random.randint(1, 20))()


def give_txt():
    """Случайная подсказка"""
    tips = [
        'Импровезируй! Порой результат может быть удивителен!',
        'Не забывай суммировать модификаторы определенных действий.',
        'Σ>―(〃°ω°〃)♡→',
        'Заговоры не тратят ячейки',
        'Порой, качественный отыгрыш может спасти ситуацию',
        'Не зли ДМ-а',
        '(✯◡✯)',
        'Каждая расса и класс имеют свои особенности.',
        '¯\_(ツ)_/¯',
        'Позиция на поле боя может решить исход сражения',
        'Не недооценивайте преимущество высоты (+2 к атаке)',
        'Используйте окружение: укрытия дают бонус к КД',
        'Держитесь вместе, но не слишком кучно - заклинания площади!',
        'Помните про возможности реакции: атака при возможности, щит и т.д.',
        'Проверка на восприятие может спасти от засады',
        'Иногда отступление - лучшая тактика',
        'Используйте помощь действием для сложных проверок',
        'Ваша предыстория - это не просто текст, а возможности',
        'Не все NPC должны быть врагами - дипломатия работает',
        'Иногда молчание говорит больше слов',
        'Запомните имена важных NPC - это имеет значение',
        'Ваши недостатки могут быть интереснее достоинств',
        'Истории у костра создают лучшие воспоминания',
        'Даже злодеи имеют мотивация',
        'Иногда стоит проиграть по-красивому',
        'Читайте описание заклинаний внимательно - там много деталей',
        'Эффекты разных школ магии могут комбинироваться',
        'Не все магические предметы требуют атрибуции',
        'Помните про концентрацию - только одно заклинание за раз',
        'Кантрипы - ваш лучший друг на низких уровнях',
        'Классовые способности обновляются после отдыха',
        'Мультиклассинг требует планирования',
        'Сила мага - в подготовленных заклинаниях',
        'ДМ тоже человек (вроде бы)',
        'Пицца решает все межсессионные конфликты',
        'Критический провал - это не конец, а начало истории',
        'Кубики имеют чувство юмора. Злое.',
        'Лучший план переживает первый контакт с врагом',
        'Если ДМ улыбается - готовьтесь',
        'ヽ(•‿•)ノ',
        '(╯°□°）╯︵ ┻━┻',
        '┬─┬ノ( º _ ºノ)',
        '٩(◕‿◕)۶', 'Ведите заметки - память не вечна',
        'Знайте свои бонусы к броскам заранее',
        'Подготовьте несколько действий на случай своего хода',
        'Помните про грузоподъемность и инвентарь',
        'Отдых - ваш главный ресурс',
        'Карты и схемы экономят время',
        'Синхронизируйте действия с союзниками',
        'Правила существуют, но ДМ имеет последнее слово',
        'Каждое приключение начинается с одного шага',
        'Сокровища - не только золото, но и воспоминания',
        'Настоячная магия - в воображении',
        'Самые опасные монстры часто внутри нас',
        'Доверие в группе важнее любого артефакта',
        'Иногда нужно потеряться, чтобы найти себя',
        '★~(◠‿◕✿)',
        '✨⚔️✨',
        '🎲 Судьба в ваших руках 🎲',
        'Гибкость важнее следования сценарию',
        'Дайте игрокам почувствовать себя героями',
        'Не бойтесь импровизировать',
        'Лучшие сюжеты рождаются за столом',
        'Помните про правило "Да, и..."',
        'Иногда нужно сказать "нет" ради сохранения баланса',
        'Игроки помнят эмоции, не детали квеста',
        'Перерывы спасают сессии',
    ]
    return random.choice(tips)


def mod(text):
    """Рассчет модификатора характеристики"""
    if text == '' or text is None:
        return ''

    try:
        score = int(text)
    except ValueError:
        return 'ERROR'

    if score == 1:
        return -5
    elif 2 <= score <= 3:
        return -4
    elif 4 <= score <= 5:
        return -3
    elif 6 <= score <= 7:
        return -2
    elif 8 <= score <= 9:
        return -1
    elif 10 <= score <= 11:
        return 0
    elif 12 <= score <= 13:
        return 1
    elif 14 <= score <= 15:
        return 2
    elif 16 <= score <= 17:
        return 3
    elif 18 <= score <= 19:
        return 4
    elif 20 <= score <= 21:
        return 5
    elif 22 <= score <= 23:
        return 6
    elif 24 <= score <= 25:
        return 7
    elif 26 <= score <= 27:
        return 8
    elif 28 <= score <= 29:
        return 9
    elif score == 30:
        return 10
    else:
        return 'ERROR'


def search(spell_name):
    """Поиск информации о заклинании"""
    search_window = customtkinter.CTk()
    search_window.geometry("800x400")
    search_window.title("Spell Details")
    search_window.resizable(False, False)
    customtkinter.set_appearance_mode("dark")

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(base_path, 'Base', 'Spells', f'{spell_name}.txt')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            spell_text = file.read()
    except FileNotFoundError:
        spell_text = f"Файл заклинания '{spell_name}.txt' не найден!\n\nПроверьте папку: Base/Spells/"
    except Exception as error:
        spell_text = f"Ошибка чтения файла заклинания: {str(error)}"

    text_field = customtkinter.CTkTextbox(search_window, width=800, height=400)
    text_field.pack(expand=True, fill="both", padx=10, pady=10)
    text_field.insert('0.0', spell_text)
    text_field.configure(state='disabled', wrap='word')

    close_button = customtkinter.CTkButton(search_window, text="Закрыть", command=search_window.destroy)
    close_button.pack(pady=10)

    search_window.mainloop()


def settings_main():
    """Окно настроек"""
    settings_window = customtkinter.CTk()
    settings_window.title('Настройки')
    settings_window.geometry('500x300')
    customtkinter.set_appearance_mode("dark")

    fullscreen_var = customtkinter.BooleanVar(value=False)

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    settings_path = os.path.join(base_path, 'settings.json')

    try:
        with open(settings_path, 'r', encoding='utf-8') as file:
            all_settings = json.load(file)
        fullscreen_value = all_settings.get("fullscreen", False)
        fullscreen_var.set(bool(fullscreen_value))
    except:
        fullscreen_var.set(False)

    fullscreen_checkbox = customtkinter.CTkCheckBox(
        settings_window,
        text='Полноэкранный режим (рекомендуется)',
        variable=fullscreen_var
    )
    fullscreen_checkbox.pack(side='left', anchor='nw', padx=20, pady=20)

    def save_settings():
        if fullscreen_checkbox.get() == 1:
            fullscreen = True
        else:
            fullscreen = False

        save_data = {"fullscreen": fullscreen}

        try:
            with open(settings_path, 'w', encoding='utf-8') as file:
                json.dump(save_data, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("Сохранено", "Настройки успешно сохранены!")
        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {str(error)}")

    save_button = customtkinter.CTkButton(
        settings_window,
        text='Применить',
        command=save_settings
    )
    save_button.pack(side='bottom', anchor='se', padx=20, pady=20)

    settings_window.mainloop()


# ==================== СЕРВЕР МУЛЬТИПЛЕЕРА ====================

# Глобальные переменные сервера
server_clients = set()
server_game_state = {
    'tokens': {},
    'chat_messages': [],
    'players': {},
    'current_map': None,
    'map_chunks': {}
}


async def server_register(websocket):
    """Регистрация нового клиента"""
    try:
        server_clients.add(websocket)
        logger.info(f"✅ Новый клиент подключен. Всего клиентов: {len(server_clients)}")

        init_message = json.dumps({
            'type': 'init',
            'data': server_game_state
        })

        await websocket.send(init_message)

    except Exception as e:
        logger.error(f"❌ Ошибка регистрации клиента: {str(e)}")
        try:
            server_clients.remove(websocket)
        except KeyError:
            pass
        raise


async def server_unregister(websocket):
    """Удаление клиента"""
    try:
        server_clients.remove(websocket)
        logger.info(f"🔴 Клиент отключен. Осталось клиентов: {len(server_clients)}")
    except KeyError:
        pass


async def server_broadcast(message, exclude=None):
    """Отправка сообщения всем клиентам, кроме исключенного"""
    if not server_clients:
        return

    tasks = []
    disconnected_clients = []

    for client in server_clients:
        if client == exclude:
            continue

        try:
            if hasattr(client, 'closed'):
                if client.closed:
                    disconnected_clients.append(client)
                    continue
            elif hasattr(client, 'state'):
                if client.state == websockets.protocol.State.CLOSED:
                    disconnected_clients.append(client)
                    continue

            task = asyncio.create_task(client.send(message))
            tasks.append(task)

        except websockets.exceptions.ConnectionClosed:
            disconnected_clients.append(client)
        except AttributeError as e:
            logger.debug(f"⚠️ Нестандартный объект соединения: {type(client)}")
            try:
                task = asyncio.create_task(client.send(message))
                tasks.append(task)
            except Exception as send_error:
                logger.error(f"❌ Ошибка отправки: {str(send_error)}")
                disconnected_clients.append(client)
        except Exception as e:
            logger.error(f"❌ Ошибка подготовки отправки клиенту: {str(e)}")
            disconnected_clients.append(client)

    for client in disconnected_clients:
        try:
            server_clients.remove(client)
            logger.info(f"🗑️ Удален отключенный клиент")
        except (KeyError, ValueError):
            pass

    if tasks:
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"❌ Ошибка широковещательной рассылки: {str(e)}")


async def assemble_and_broadcast_map(map_id, metadata):
    """Собирает карту из чанков и рассылает её"""
    try:
        # Собираем все чанки в правильном порядке
        chunks = server_game_state['map_chunks'][map_id]
        sorted_indices = sorted(map(int, chunks.keys()))

        # Объединяем чанки
        combined_base64 = ''
        for idx in sorted_indices:
            combined_base64 += chunks[str(idx)]

        # Сохраняем в текущую карту
        server_game_state['current_map'] = {
            'filename': metadata.get('filename'),
            'image_base64': combined_base64,
            'timestamp': datetime.now().isoformat(),
            'loaded_by': metadata.get('player'),
            'size': metadata.get('size', 0),
            'map_id': map_id
        }

        logger.info(f"🗺️ Карта собрана из чанков: {metadata.get('filename')} ({len(combined_base64)} байт)")

        # Рассылаем уведомление о готовности карты
        ready_message = json.dumps({
            'type': 'map_ready',
            'data': {
                'map_id': map_id,
                'metadata': metadata
            }
        })

        await server_broadcast(ready_message)

        # Очищаем чанки
        if map_id in server_game_state['map_chunks']:
            del server_game_state['map_chunks'][map_id]

    except Exception as e:
        logger.error(f"❌ Ошибка сборки карты: {str(e)}")


async def server_handle_message(websocket, message):
    """Обработка входящих сообщений"""
    try:
        data = json.loads(message)
        message_type = data.get('type')

        logger.info(f"📨 Получено сообщение типа: {message_type}")

        if message_type == 'token_update':
            token_data = data['data']
            token_id = token_data['id']

            if token_data['action'] == 'add':
                server_game_state['tokens'][token_id] = token_data
                logger.info(f"➕ Добавлен токен: {token_id}")
            elif token_data['action'] == 'update':
                if token_id in server_game_state['tokens']:
                    server_game_state['tokens'][token_id].update(token_data)
                    logger.info(f"🔄 Обновлен токен: {token_id}")
            elif token_data['action'] == 'remove':
                if token_id in server_game_state['tokens']:
                    del server_game_state['tokens'][token_id]
                    logger.info(f"➖ Удален токен: {token_id}")

            try:
                await server_broadcast(message, websocket)
            except Exception as e:
                logger.error(f"❌ Ошибка рассылки обновления токена: {str(e)}")

        elif message_type == 'chat_message':
            chat_data = data['data']
            chat_data['timestamp'] = datetime.now().isoformat()
            server_game_state['chat_messages'].append(chat_data)

            if len(server_game_state['chat_messages']) > 100:
                server_game_state['chat_messages'] = server_game_state['chat_messages'][-100:]

            logger.info(f"💬 Сообщение в чат от {chat_data.get('player', 'Неизвестно')}")
            try:
                await server_broadcast(message)
            except Exception as e:
                logger.error(f"❌ Ошибка рассылки сообщения чата: {str(e)}")

        elif message_type == 'roll_dice':
            roll_data = data['data']
            logger.info(
                f"🎲 Бросок кубика от {roll_data.get('player', 'Неизвестно')}: {roll_data.get('dice', '?')} = {roll_data.get('result', '?')}")
            try:
                await server_broadcast(message)
            except Exception as e:
                logger.error(f"❌ Ошибка рассылки броска кубика: {str(e)}")

        elif message_type == 'player_join':
            player_data = data['data']
            player_id = player_data['id']
            server_game_state['players'][player_id] = player_data
            logger.info(f"🟢 Игрок присоединился: {player_data.get('name', 'Неизвестно')}")
            try:
                await server_broadcast(message)
            except Exception as e:
                logger.error(f"❌ Ошибка рассылки присоединения игрока: {str(e)}")

        elif message_type == 'player_leave':
            player_id = data['data']['id']
            if player_id in server_game_state['players']:
                player_name = server_game_state['players'][player_id].get('name', 'Неизвестно')
                del server_game_state['players'][player_id]
                logger.info(f"🔴 Игрок покинул: {player_name}")
            try:
                await server_broadcast(message)
            except Exception as e:
                logger.error(f"❌ Ошибка рассылки выхода игрока: {str(e)}")

        elif message_type == 'map_update':
            map_data = data['data']
            map_action = map_data.get('action')

            if map_action == 'load':
                if 'image_base64' in map_data:
                    # Маленькая карта (прямая загрузка)
                    server_game_state['current_map'] = {
                        'filename': map_data.get('filename'),
                        'image_base64': map_data.get('image_base64'),
                        'timestamp': datetime.now().isoformat(),
                        'loaded_by': map_data.get('player'),
                        'size': map_data.get('size', 0)
                    }
                    logger.info(
                        f"🗺️ Загружена карта: {map_data.get('filename', 'Unknown')} ({map_data.get('size', 0)} байт)")
                else:
                    # Большая карта - ждем чанки
                    logger.info(f"🗺️ Начата загрузка большой карты: {map_data.get('filename', 'Unknown')}")

            elif map_action == 'clear':
                server_game_state.pop('current_map', None)
                # Очищаем чанки старых карт
                server_game_state['map_chunks'] = {}
                logger.info("🗺️ Карта очищена")

            try:
                await server_broadcast(message)
            except Exception as e:
                logger.error(f"❌ Ошибка рассылки обновления карты: {str(e)}")

        elif message_type == 'map_chunk':
            chunk_data = data['data']
            map_id = chunk_data['map_id']
            chunk_index = chunk_data['chunk_index']
            total_chunks = chunk_data['total_chunks']
            chunk_content = chunk_data['chunk']

            # Сохраняем чанк
            if map_id not in server_game_state['map_chunks']:
                server_game_state['map_chunks'][map_id] = {}

            server_game_state['map_chunks'][map_id][chunk_index] = chunk_content

            logger.info(f"🗺️ Получен чанк {chunk_index + 1}/{total_chunks} карты {map_id}")

            # Если получены все чанки, собираем карту
            if len(server_game_state['map_chunks'][map_id]) == total_chunks:
                await assemble_and_broadcast_map(map_id, chunk_data.get('metadata', {}))

            # Пересылаем чанк другим клиентам
            try:
                await server_broadcast(message, websocket)
            except Exception as e:
                logger.error(f"❌ Ошибка рассылки чанка карты: {str(e)}")

        elif message_type == 'map_ready':
            # Это сообщение отправляется после сборки карты
            map_data = data['data']
            map_id = map_data['map_id']

            # Уведомляем всех о готовности карты
            try:
                await server_broadcast(message)
            except Exception as e:
                logger.error(f"❌ Ошибка рассылки готовности карты: {str(e)}")

        else:
            logger.warning(f"⚠️ Неизвестный тип сообщения: {message_type}")

    except json.JSONDecodeError as e:
        logger.error(f"❌ Ошибка декодирования JSON: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Ошибка обработки сообщения: {str(e)}")


async def websocket_handler(websocket):
    """Главный обработчик WebSocket соединений"""
    try:
        await server_register(websocket)
    except Exception as e:
        logger.error(f"❌ Не удалось зарегистрировать клиента: {str(e)}")
        return

    try:
        async for message in websocket:
            try:
                await server_handle_message(websocket, message)
            except Exception as e:
                logger.error(f"❌ Ошибка при обработке сообщения: {str(e)}")
                continue

    except websockets.exceptions.ConnectionClosed:
        logger.info("🔌 Соединение закрыто клиентом")
    except Exception as e:
        logger.error(f"❌ Ошибка в обработчике соединения: {str(e)}")
    finally:
        await server_unregister(websocket)


async def main_server():
    """Основная функция запуска сервера"""
    server = await websockets.serve(
        websocket_handler,
        "0.0.0.0",
        8765,
        max_size=50 * 1024 * 1024,  # 50MB максимальный размер сообщения
        ping_interval=20,
        ping_timeout=60
    )

    logger.info("✅ Сервер запущен на ws://0.0.0.0:8765")
    logger.info("✅ Ожидание подключений...")
    logger.info("⚠️  Максимальный размер файла: 50MB")

    await server.wait_closed()


def start_server():
    """Запуск сервера в отдельном потоке"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main_server())
    except KeyboardInterrupt:
        logger.info("🛑 Сервер остановлен по запросу пользователя")
    except Exception as e:
        logger.error(f"❌ Ошибка запуска сервера: {e}")
    finally:
        loop.close()


# ==================== ЛИСТ ПЕРСОНАЖА (без изменений) ====================
def add_character_main():


    chwin = customtkinter.CTk()
    chwin.title("Add Character")
    chwin.geometry("1800x900")
    customtkinter.set_appearance_mode("dark")

    # Создаем меню
    menubar = customtkinter.CTkFrame(chwin, height=40)
    menubar.pack(fill="x", padx=5, pady=5)

    # Кнопки для сохранения/загрузки
    save_btn = customtkinter.CTkButton(menubar, text="Сохранить", command=lambda: save_data())
    save_btn.pack(side="left", padx=5)

    load_btn = customtkinter.CTkButton(menubar, text="Загрузить", command=lambda: load_data())
    load_btn.pack(side="left", padx=5)

    MainFrame2 = customtkinter.CTkScrollableFrame(chwin)
    MainFrame2.pack(fill="both", expand=True)

    MainFrame = customtkinter.CTkFrame(MainFrame2)
    MainFrame.pack(fill="both", expand=True)

    MainFrame.columnconfigure(0, weight=1)
    MainFrame.columnconfigure(1, weight=2)
    MainFrame.columnconfigure(2, weight=3)
    MainFrame.rowconfigure(0, weight=1)

    FrameColobarating1 = customtkinter.CTkFrame(MainFrame)
    FrameColobarating1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    FrameColobarating2 = customtkinter.CTkFrame(FrameColobarating1)
    FrameColobarating2.pack(padx=10, pady=10, expand=True, side='bottom', anchor="nw")

    MainFrame1 = customtkinter.CTkFrame(FrameColobarating1)
    MainFrame1.pack(padx=10, pady=10, anchor="nw")

    TopFrame = customtkinter.CTkFrame(MainFrame1)
    TopFrame.pack(padx=10, pady=10, expand=True, side='left')

    # Оглавление

    NameFrame = customtkinter.CTkFrame(TopFrame)
    NameFrame.pack(padx=10, pady=10)

    NameText = customtkinter.CTkLabel(NameFrame, text="Имя")
    NameText.pack(side='left', padx=5, pady=5)

    Name = customtkinter.CTkEntry(NameFrame, width=80)
    Name.pack(side="right", padx=5, pady=5)

    ExpFrame = customtkinter.CTkFrame(TopFrame)
    ExpFrame.pack(padx=10, pady=10, side='right')

    ExpText = customtkinter.CTkLabel(ExpFrame, text="Опыт")
    ExpText.pack(side='left', padx=5, pady=5)

    Exp = customtkinter.CTkEntry(ExpFrame, width=80)
    Exp.pack(side="right", padx=5, pady=5)

    TopFrame2 = customtkinter.CTkFrame(MainFrame1)
    TopFrame2.pack(padx=10, pady=10, side="right")

    MirFrame = customtkinter.CTkFrame(TopFrame2)
    MirFrame.pack(padx=10, pady=10)

    MirLab = customtkinter.CTkLabel(MirFrame, text="Мировозрение")
    MirLab.pack(side="left", padx=5, pady=5)

    Mir = customtkinter.CTkEntry(MirFrame, width=140)
    Mir.pack(side="right", padx=5, pady=5)

    HisFrame = customtkinter.CTkFrame(TopFrame2)
    HisFrame.pack(padx=10, pady=10)

    HisLab = customtkinter.CTkLabel(HisFrame, text='Предыстория')
    HisLab.pack(side="left", padx=5, pady=5)

    His = customtkinter.CTkEntry(HisFrame, width=150)
    His.pack(side="right", padx=5, pady=5)

    MessFrame1 = customtkinter.CTkFrame(MainFrame1)
    MessFrame1.pack(padx=10, pady=10, expand=True, side='right')

    ClassFrame = customtkinter.CTkFrame(MessFrame1)
    ClassFrame.pack(padx=10, pady=10, expand=True)

    ClassText = customtkinter.CTkLabel(ClassFrame, text='Класс')
    ClassText.pack(side='left', padx=5, pady=5)

    classificate = ['Бард', "Варвар", "Воин", "Волщебник", "Друид", "Жрец", "Изобретатель", "Колдун", "Монах",
                    "Паладин", "Плут", "Следопыт", "Чародей"]

    Class = customtkinter.CTkComboBox(ClassFrame, values=classificate)
    Class.pack(side="right", padx=5, pady=5)

    RaceFrame = customtkinter.CTkFrame(MessFrame1)
    RaceFrame.pack(padx=10, pady=10)

    RaceText = customtkinter.CTkLabel(RaceFrame, text='Раса')
    RaceText.pack(side='left', padx=5, pady=5)

    classificate1 = ["Аракокра", "Аасимар", "Автогном", "Астральный эльф", "Багбир", "Ведалкин", "Вердан",
                     "Гибрид Симиков", "Гит", "Гифф", "Гном", "Гоблин", "Гоблин", "Голиаф", "Грунг", "Дварф", "Дженази",
                     "Драконорожденный", "Зайцегон", "Калаштар", "Кендер", "Кенку", "Кентавр", "Кобольд", "Кованный",
                     "Лонин", "Локата", "Локсодон", "Людоящер", "Минотавр", "Орк", "Плазмоид", "Полуорк", "Полурослик",
                     "Полуэльф", "Сатир", "Совлин", "Табакси", "Тифлинг", "Тортл", "Три-крин", "Тритон", "Фирболг",
                     "Фэйри", "Хадози", "Хобгоблин", "Чейнджлинг", "Человек", "Шифтер", "Эльф", "Юань-ти"]

    Race = customtkinter.CTkComboBox(RaceFrame, values=classificate1, width=170, height=30)
    Race.pack(side="right", padx=5, pady=5)

    # Вдохновление и БВ
    FrameVDH = customtkinter.CTkFrame(FrameColobarating2)
    FrameVDH.pack(padx=10, pady=10, expand=True, side='right', anchor="ne")

    FrameVDH1 = customtkinter.CTkFrame(FrameVDH)
    FrameVDH1.pack(padx=5, pady=5, expand=True, side='top')

    EntryVDH = customtkinter.CTkEntry(FrameVDH1, width=50)
    EntryVDH.pack(side="left", padx=5, pady=5)

    LabelVDH = customtkinter.CTkLabel(FrameVDH1, text='Вдохновение', width=210)
    LabelVDH.pack(side="right", padx=5, pady=5)

    FrameVDH2 = customtkinter.CTkFrame(FrameVDH)
    FrameVDH2.pack(padx=5, pady=5, expand=True, side='top')

    EntreBV = customtkinter.CTkEntry(FrameVDH2, width=50)
    EntreBV.pack(side="left", padx=5, pady=5)

    LabelBV = customtkinter.CTkLabel(FrameVDH2, text='Бонус Владения', width=220)
    LabelBV.pack(side="right")

    FrameVDH3 = customtkinter.CTkFrame(FrameVDH)
    FrameVDH3.pack(padx=5, pady=5, expand=True, side='top')

    EntreM = customtkinter.CTkEntry(FrameVDH3, width=50)
    EntreM.pack(side="left", padx=5, pady=5)

    LabelM = customtkinter.CTkLabel(FrameVDH3, text='Пассивная мудрость(Восприятие)', width=220)
    LabelM.pack(side="right")

    # Статы

    FrameStat = customtkinter.CTkFrame(FrameColobarating2)
    FrameStat.pack(padx=10, pady=10, expand=True, side='left', anchor='nw')

    PowerFrame = customtkinter.CTkFrame(FrameStat)
    PowerFrame.pack(padx=10, pady=10, expand=True)

    StatePowerLabel = customtkinter.CTkLabel(PowerFrame, text='Сила', width=150)
    StatePowerLabel.pack()

    StatePowerEntry = customtkinter.CTkEntry(PowerFrame, width=50)
    StatePowerEntry.pack()

    modPower = ' '

    def updatePower():
        global modPower
        modPower = mod(StatePowerEntry.get())
        StatePowerLabelMod.configure(text=f'Модификатор = {modPower}')
        chwin.after(1000, updatePower)

    StatePowerLabelMod = customtkinter.CTkLabel(PowerFrame, text=f'Модификатор = {modPower}')
    StatePowerLabelMod.pack()

    LovFrame = customtkinter.CTkFrame(FrameStat)
    LovFrame.pack(padx=10, pady=10, expand=True)

    StateLovLabel = customtkinter.CTkLabel(LovFrame, text='Ловкость', width=150)
    StateLovLabel.pack()

    StateLovEntry = customtkinter.CTkEntry(LovFrame, width=50)
    StateLovEntry.pack()

    modLov = ''

    def updateLov():
        global modLov
        modLov = mod(StateLovEntry.get())
        StateLovLabelMod.configure(text=f'Модификатор = {modLov}')
        chwin.after(1000, updateLov)

    StateLovLabelMod = customtkinter.CTkLabel(LovFrame, text=f'Модификатор = {modLov}')
    StateLovLabelMod.pack()

    TELFrame = customtkinter.CTkFrame(FrameStat)
    TELFrame.pack(padx=10, pady=10, expand=True)

    StateTELLabel = customtkinter.CTkLabel(TELFrame, text='Телосложение', width=150)
    StateTELLabel.pack()

    StateTELEntry = customtkinter.CTkEntry(TELFrame, width=50)
    StateTELEntry.pack()

    modTEL = ''

    def updateTEL():
        global modTEL
        modTEL = mod(StateTELEntry.get())
        StateTELLabelMod.configure(text=f'Модификатор = {modTEL}')
        chwin.after(1000, updateTEL)

    StateTELLabelMod = customtkinter.CTkLabel(TELFrame, text=f'Модификатор = {modTEL}')
    StateTELLabelMod.pack()

    INTFrame = customtkinter.CTkFrame(FrameStat)
    INTFrame.pack(padx=10, pady=10, expand=True)

    StateINTLabel = customtkinter.CTkLabel(INTFrame, text='Интеллект', width=150)
    StateINTLabel.pack()

    StateINTEntry = customtkinter.CTkEntry(INTFrame, width=50)
    StateINTEntry.pack()

    modINT = ''

    def updateINT():
        global modINT
        modINT = mod(StateINTEntry.get())
        StateINTLabelMod.configure(text=f'Модификатор = {modINT}')
        chwin.after(1000, updateINT)

    StateINTLabelMod = customtkinter.CTkLabel(INTFrame, text=f'Модификатор = {modINT}')
    StateINTLabelMod.pack()

    MYDFrame = customtkinter.CTkFrame(FrameStat)
    MYDFrame.pack(padx=10, pady=10, expand=True)

    StateMYDLabel = customtkinter.CTkLabel(MYDFrame, text='Мудрость', width=150)
    StateMYDLabel.pack()

    StateMYDEntry = customtkinter.CTkEntry(MYDFrame, width=50)
    StateMYDEntry.pack()

    modMYD = ''

    def updateMYD():
        global modMYD
        modMYD = mod(StateMYDEntry.get())
        StateMYDLabelMod.configure(text=f'Модификатор = {modMYD}')
        chwin.after(1000, updateMYD)

    StateMYDLabelMod = customtkinter.CTkLabel(MYDFrame, text=f'Модификатор = {modMYD}')
    StateMYDLabelMod.pack()

    XARFrame = customtkinter.CTkFrame(FrameStat)
    XARFrame.pack(padx=10, pady=10, expand=True)

    StateXARLabel = customtkinter.CTkLabel(XARFrame, text='Харизма', width=150)
    StateXARLabel.pack()

    StateXAREntry = customtkinter.CTkEntry(XARFrame, width=50)
    StateXAREntry.pack()

    modXAR = ''

    def updateXAR():
        global modXAR
        modXAR = mod(StateXAREntry.get())
        StateXARLabelMod.configure(text=f'Модификатор = {modXAR}')
        chwin.after(1000, updateXAR)

    StateXARLabelMod = customtkinter.CTkLabel(XARFrame, text=f'Модификатор = {modXAR}')
    StateXARLabelMod.pack()


    def update_all():
        updatePower()
        updateLov()
        updateTEL()
        updateINT()
        updateMYD()
        updateXAR()

    # СпасБроски

    AbilityAndSpasFrame = customtkinter.CTkFrame(FrameColobarating2)
    AbilityAndSpasFrame.pack(padx=10, pady=10, expand=True, anchor='n')

    SpasFrame = customtkinter.CTkFrame(AbilityAndSpasFrame)
    SpasFrame.pack(padx=10, pady=10, expand=True)

    SpasLabel = customtkinter.CTkLabel(SpasFrame, text='Спасброски', width=150)
    SpasLabel.pack()

    PowerSpasFrame = customtkinter.CTkFrame(SpasFrame)
    PowerSpasFrame.pack(padx=5, pady=5, expand=True)

    PowerSpas = customtkinter.CTkCheckBox(PowerSpasFrame, onvalue='Сила', text='Сила', width=130)
    PowerSpas.pack(side='right')

    PowerSpasEntry = customtkinter.CTkEntry(PowerSpasFrame, width=40)
    PowerSpasEntry.pack(side='left')

    agilitySpasFrame = customtkinter.CTkFrame(SpasFrame)
    agilitySpasFrame.pack(padx=5, pady=5, expand=True)

    agilitySpas = customtkinter.CTkCheckBox(agilitySpasFrame, onvalue='Ловкость', text='Ловкость', width=130)
    agilitySpas.pack(side='right')

    agilitySpasEntry = customtkinter.CTkEntry(agilitySpasFrame, width=40)
    agilitySpasEntry.pack(side='left')

    TELSpasFrame = customtkinter.CTkFrame(SpasFrame)
    TELSpasFrame.pack(padx=5, pady=5, expand=True)

    TELSpas = customtkinter.CTkCheckBox(TELSpasFrame, onvalue='Teлосложение', text='Телосложение', width=130)
    TELSpas.pack(side='right')

    TELSpasEntry = customtkinter.CTkEntry(TELSpasFrame, width=40)
    TELSpasEntry.pack(side='left')

    IntSpasFrame = customtkinter.CTkFrame(SpasFrame)
    IntSpasFrame.pack(padx=5, pady=5, expand=True)

    IntSpas = customtkinter.CTkCheckBox(IntSpasFrame, onvalue='Интеллект', text='Интеллект', width=130)
    IntSpas.pack(side='right')

    IntSpasEntry = customtkinter.CTkEntry(IntSpasFrame, width=40)
    IntSpasEntry.pack(side='left')

    MydSpasFrame = customtkinter.CTkFrame(SpasFrame)
    MydSpasFrame.pack(padx=5, pady=5, expand=True)

    MydSpas = customtkinter.CTkCheckBox(MydSpasFrame, onvalue='Мудрость', text='Мудрость', width=130)
    MydSpas.pack(side='right')

    MydSpasEntry = customtkinter.CTkEntry(MydSpasFrame, width=40)
    MydSpasEntry.pack(side='left')

    XarSpasFrame = customtkinter.CTkFrame(SpasFrame)
    XarSpasFrame.pack(padx=5, pady=5, expand=True)

    XarSpas = customtkinter.CTkCheckBox(XarSpasFrame, onvalue='Харизма', text='Харизма', width=130)
    XarSpas.pack(side='right')

    XarSpasEntry = customtkinter.CTkEntry(XarSpasFrame, width=40)
    XarSpasEntry.pack(side='left')

    # Навыки

    AbilityFrame = customtkinter.CTkFrame(FrameVDH)
    AbilityFrame.pack(padx=5, pady=5, expand=True)

    AbilityLabel = customtkinter.CTkLabel(AbilityFrame, text='Навыки')
    AbilityLabel.pack()

    AcrSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    AcrSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')
    AcrSpasEntry = customtkinter.CTkEntry(AcrSpasFrame, width=40)
    AcrSpasEntry.pack(side='left')

    AcrSpas = customtkinter.CTkCheckBox(AcrSpasFrame, onvalue='Акробатика(Лов)', text='Акробатика(Лов)')
    AcrSpas.pack(side='left')

    AnalisSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    AnalisSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')
    AnalisSpasEntry = customtkinter.CTkEntry(AnalisSpasFrame, width=40)
    AnalisSpasEntry.pack(side='left')

    AnalisSpas = customtkinter.CTkCheckBox(AnalisSpasFrame, onvalue='Анализ(Инт)', text='Анализ(Инт)')
    AnalisSpas.pack(side='left')

    AtletSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    AtletSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')
    AtletSpasEntry = customtkinter.CTkEntry(AtletSpasFrame, width=40)
    AtletSpasEntry.pack(side='left')

    AtletSpas = customtkinter.CTkCheckBox(AtletSpasFrame, onvalue='Атлетика(Сил)', text='Атлетика(Сил)')
    AtletSpas.pack(side='left')

    VospSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    VospSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    VospSpasEntry = customtkinter.CTkEntry(VospSpasFrame, width=40)
    VospSpasEntry.pack(side='left')

    VospSpas = customtkinter.CTkCheckBox(VospSpasFrame, onvalue='Восприятие(Муд)', text='Восприятие(Муд)')
    VospSpas.pack(side='left')

    SurvivalSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    SurvivalSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    SurvivalSpasEntry = customtkinter.CTkEntry(SurvivalSpasFrame, width=40)
    SurvivalSpasEntry.pack(side='left')

    SurvivalSpas = customtkinter.CTkCheckBox(SurvivalSpasFrame, onvalue='Выживание(Муд)', text='Выживание(Муд)')
    SurvivalSpas.pack(side='left')

    PlaySpasFrame = customtkinter.CTkFrame(AbilityFrame)
    PlaySpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    PlaySpasEntry = customtkinter.CTkEntry(PlaySpasFrame, width=40)
    PlaySpasEntry.pack(side='left')

    PlaySpas = customtkinter.CTkCheckBox(PlaySpasFrame, onvalue='Выступление(Хар)', text='Выступление(Хар)')
    PlaySpas.pack(side='left')

    DanSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    DanSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')
    DanSpasEntry = customtkinter.CTkEntry(DanSpasFrame, width=40)
    DanSpasEntry.pack(side='left')

    DanSpas = customtkinter.CTkCheckBox(DanSpasFrame, onvalue='Запугивание(Хар)', text='Запугивание(Хар)')
    DanSpas.pack(side='left')

    HisSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    HisSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    HisSpasEntry = customtkinter.CTkEntry(HisSpasFrame, width=40)
    HisSpasEntry.pack(side='left')

    HisSpas = customtkinter.CTkCheckBox(HisSpasFrame, onvalue='История(Инт)', text='История(Инт)')
    HisSpas.pack(side='left')

    AgHSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    AgHSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    AgHSpasEntry = customtkinter.CTkEntry(AgHSpasFrame, width=40)
    AgHSpasEntry.pack(side='left')

    AgHSpas = customtkinter.CTkCheckBox(AgHSpasFrame, onvalue='Ловкость рук(Лов)', text='Ловкость рук(Лов)')
    AgHSpas.pack(side='left')

    MagicSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    MagicSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    MagicSpasEntry = customtkinter.CTkEntry(MagicSpasFrame, width=40)
    MagicSpasEntry.pack(side='left')

    MagicSpas = customtkinter.CTkCheckBox(MagicSpasFrame, onvalue='Магия(Инт)', text='Магия(Инт)')
    MagicSpas.pack(side='left')

    MedicineSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    MedicineSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    MedicineSpasEntry = customtkinter.CTkEntry(MedicineSpasFrame, width=40)
    MedicineSpasEntry.pack(side='left')

    MedicineSpas = customtkinter.CTkCheckBox(MedicineSpasFrame, onvalue='Медицина(Муд)', text='Медицина(Муд)')
    MedicineSpas.pack(side='left')

    ObmanSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    ObmanSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    ObmanSpasEntry = customtkinter.CTkEntry(ObmanSpasFrame, width=40)
    ObmanSpasEntry.pack(side='left')

    ObmanSpas = customtkinter.CTkCheckBox(ObmanSpasFrame, onvalue='Обман(Хар)', text='Обман(Хар)')
    ObmanSpas.pack(side='left')

    NatureSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    NatureSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    NatureSpasEntry = customtkinter.CTkEntry(NatureSpasFrame, width=40)
    NatureSpasEntry.pack(side='left')

    NatureSpas = customtkinter.CTkCheckBox(NatureSpasFrame, onvalue='Природа(Инт)', text='Природа(Инт)')
    NatureSpas.pack(side='left')

    PronicSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    PronicSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    PronicSpasEntry = customtkinter.CTkEntry(PronicSpasFrame, width=40)
    PronicSpasEntry.pack(side='left')

    PronicSpas = customtkinter.CTkCheckBox(PronicSpasFrame, onvalue='Проницательность(Муд)',
                                           text='Проницательность(Муд)')
    PronicSpas.pack(side='left')

    ReligSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    ReligSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')
    ReligSpasEntry = customtkinter.CTkEntry(ReligSpasFrame, width=40)
    ReligSpasEntry.pack(side='left')

    ReligSpas = customtkinter.CTkCheckBox(ReligSpasFrame, onvalue='Религия(Инт)', text='Религия(Инт)')
    ReligSpas.pack(side='left')

    ScretSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    ScretSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    ScretSpasEntry = customtkinter.CTkEntry(ScretSpasFrame, width=40)
    ScretSpasEntry.pack(side='left')

    ScretSpas = customtkinter.CTkCheckBox(ScretSpasFrame, onvalue='Скрытность(Лов)', text='Скрытность(Лов)')
    ScretSpas.pack(side='left')

    YbeSpasFrame = customtkinter.CTkFrame(AbilityFrame)
    YbeSpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    YbeSpasEntry = customtkinter.CTkEntry(YbeSpasFrame, width=40)
    YbeSpasEntry.pack(side='left')

    YbeSpas = customtkinter.CTkCheckBox(YbeSpasFrame, onvalue='Убеждение(Хар)', text='Убеждение(Хар)')
    YbeSpas.pack(side='left')

    YZASpasFrame = customtkinter.CTkFrame(AbilityFrame)
    YZASpasFrame.pack(padx=5, pady=5, expand=True, fill='x')

    YZASpasEntry = customtkinter.CTkEntry(YZASpasFrame, width=40)
    YZASpasEntry.pack(side='left')

    YZASpas = customtkinter.CTkCheckBox(YZASpasFrame, onvalue='Уход за животными(Муд)', text='Уход за животными(Муд)')
    YZASpas.pack(side='left')

    MidFrame = customtkinter.CTkFrame(MainFrame)
    MidFrame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    framecoloborating4 = customtkinter.CTkFrame(MidFrame)
    framecoloborating4.pack()

    StatBLockFrame = customtkinter.CTkFrame(framecoloborating4)
    StatBLockFrame.pack(padx=5, pady=5, expand=True, anchor='n')

    KZ = customtkinter.CTkFrame(StatBLockFrame)
    KZ.pack(padx=5, pady=5, expand=True, side='left')

    KZL = customtkinter.CTkLabel(KZ, text='Класс Защиты', width=150)
    KZL.pack(side='bottom')

    KZE = customtkinter.CTkEntry(KZ, width=40)
    KZE.pack(side='top')

    Init = customtkinter.CTkFrame(StatBLockFrame)
    Init.pack(padx=5, pady=5, expand=True, side='left')

    INITL = customtkinter.CTkLabel(Init, text='Инициатива', width=150)
    INITL.pack(side='bottom')

    InitE = customtkinter.CTkEntry(Init, width=40)
    InitE.pack(side='top')

    Speed = customtkinter.CTkFrame(StatBLockFrame)
    Speed.pack(padx=5, pady=5, expand=True, side='left')

    SpeedL = customtkinter.CTkLabel(Speed, text='Скорость', width=150)
    SpeedL.pack(side='bottom')

    SpeedE = customtkinter.CTkEntry(Speed, width=40)
    SpeedE.pack(side='top')

    HP = customtkinter.CTkFrame(framecoloborating4)
    HP.pack(padx=5, pady=5, expand=True, fill='x')

    TEkHP = customtkinter.CTkFrame(HP)
    TEkHP.pack(padx=5, pady=5, expand=True, side='left')

    ttekHPCol = customtkinter.CTkFrame(TEkHP)
    ttekHPCol.pack(padx=15, pady=15, expand=True, side='top')

    TekHPL = customtkinter.CTkLabel(ttekHPCol, text='Максимум Хитов', width=130)
    TekHPL.pack(side='left')

    TekHPE = customtkinter.CTkEntry(ttekHPCol, width=70)
    TekHPE.pack(side='right')

    TEKNP = customtkinter.CTkEntry(TEkHP, justify='center')
    TEKNP.pack(side='top', fill='x')

    TEKHPL = customtkinter.CTkLabel(TEkHP, text='Текущие хиты', width=100)
    TEKHPL.pack(side='bottom')

    TimeHP = customtkinter.CTkFrame(HP)
    TimeHP.pack(padx=15, pady=15, expand=True, side='right', fill='both')

    timeHPL = customtkinter.CTkLabel(TimeHP, text='Временные хиты', width=100)
    timeHPL.pack(side='bottom')

    timehpE = customtkinter.CTkEntry(TimeHP, justify='center')
    timehpE.pack(side='bottom', pady=15)

    framecoloborating5 = customtkinter.CTkFrame(framecoloborating4)
    framecoloborating5.pack(expand=True, fill='x', padx=5, pady=5)

    hitFrame = customtkinter.CTkFrame(framecoloborating5)
    hitFrame.pack(padx=5, pady=5, expand=True, side='left', fill='both')

    HitItog = customtkinter.CTkFrame(hitFrame)
    HitItog.pack(padx=5, pady=5, expand=True, side='top')

    Hitl = customtkinter.CTkLabel(HitItog, text='Итого:')
    Hitl.pack(side='left')

    Hite = customtkinter.CTkEntry(HitItog, justify='center')
    Hite.pack(side='right')

    HitE = customtkinter.CTkEntry(hitFrame, justify='center')
    HitE.pack(side='top')

    HitL = customtkinter.CTkLabel(hitFrame, text='Кость Хитов')
    HitL.pack(side='bottom')

    SpasDEath = customtkinter.CTkFrame(framecoloborating5)
    SpasDEath.pack(padx=5, pady=5, expand=True, side='right', fill='both')

    SpasDL = customtkinter.CTkLabel(SpasDEath, text='Спасброски от Смерти')
    SpasDL.pack(side='top')

    dopDeath = customtkinter.CTkFrame(SpasDEath)
    dopDeath.pack(padx=5, pady=5, expand=True, side='top')

    dopSuccess = customtkinter.CTkFrame(dopDeath)
    dopSuccess.pack(padx=5, pady=5, expand=True, side='top', fill='x')

    SuccessL = customtkinter.CTkLabel(dopSuccess, text='Успех')
    SuccessL.pack(side='left', padx=5)

    Success1 = customtkinter.CTkCheckBox(dopSuccess, text='▬', width=20)
    Success1.pack(side='left', padx=(0, 1))

    Success2 = customtkinter.CTkCheckBox(dopSuccess, text='▬', width=20)
    Success2.pack(side='left', padx=(1, 1))

    Success3 = customtkinter.CTkCheckBox(dopSuccess, text='', width=20)
    Success3.pack(side='left', padx=(1, 0))

    dopDeath1 = customtkinter.CTkFrame(dopDeath)
    dopDeath1.pack(padx=5, pady=5, expand=True, side='top', fill='x')

    DeathL = customtkinter.CTkLabel(dopDeath1, text='Провал')
    DeathL.pack(side='left', padx=5)

    Death1 = customtkinter.CTkCheckBox(dopDeath1, text='▬', width=20)
    Death1.pack(side='left', padx=(0, 1))

    Death2 = customtkinter.CTkCheckBox(dopDeath1, text='▬', width=20)
    Death2.pack(side='left', padx=(1, 1))

    Death3 = customtkinter.CTkCheckBox(dopDeath1, text='', width=20)
    Death3.pack(side='left', padx=(1, 0))

    framecoloborating6 = customtkinter.CTkFrame(framecoloborating4, height=3)
    framecoloborating6.pack(expand=True, fill='x', padx=5, pady=5)

    # Черты характера

    CHframe = customtkinter.CTkFrame(framecoloborating6)
    CHframe.pack(expand=True, padx=5, pady=5, side='left', anchor='nw', fill='both')

    CHL = customtkinter.CTkLabel(CHframe, text='Черты характера')
    CHL.pack(side='top')

    CHTB = customtkinter.CTkTextbox(CHframe)
    CHTB.pack(side='top', fill='x')



    Iframe = customtkinter.CTkFrame(framecoloborating6)
    Iframe.pack(expand=True, padx=5, pady=5, side='right', anchor='ne', fill='both')

    IL = customtkinter.CTkLabel(Iframe, text='Идеалы')
    IL.pack(side='top')

    ITB = customtkinter.CTkTextbox(Iframe)
    ITB.pack(side='top', fill='x')

    framecoloborating7 = customtkinter.CTkFrame(framecoloborating4, height=3)
    framecoloborating7.pack(expand=True, fill='x', padx=5, pady=5)



    Pframe = customtkinter.CTkFrame(framecoloborating6)
    Pframe.pack(expand=True, padx=5, pady=5, side='left', anchor='nw', fill='both')

    PL = customtkinter.CTkLabel(Pframe, text='Привязанности')
    PL.pack(side='top')

    PTB = customtkinter.CTkTextbox(Pframe)
    PTB.pack(side='top', fill='x')



    Sframe = customtkinter.CTkFrame(framecoloborating7)
    Sframe.pack(expand=True, padx=5, pady=5, side='right', anchor='ne', fill='both')

    SL = customtkinter.CTkLabel(Sframe, text='Слабости')
    SL.pack(side='top')

    STB = customtkinter.CTkTextbox(Sframe)
    STB.pack(side='top', fill='x')



    YOframe = customtkinter.CTkFrame(framecoloborating7)
    YOframe.pack(expand=True, padx=5, pady=5, side='right', anchor='nw', fill='both')

    YOL = customtkinter.CTkLabel(YOframe, text='Умения и Особенности')
    YOL.pack(side='top')

    YOTB = customtkinter.CTkTextbox(YOframe)
    YOTB.pack(side='top', fill='x')



    Luframe = customtkinter.CTkFrame(framecoloborating7)
    Luframe.pack(expand=True, padx=5, pady=5, side='right', anchor='nw', fill='both')

    LuL = customtkinter.CTkLabel(Luframe, text='Прочие Владения и языки')
    LuL.pack(side='top')

    LuTB = customtkinter.CTkTextbox(Luframe)
    LuTB.pack(side='top', fill='x')

    framecoloborating8 = customtkinter.CTkFrame(framecoloborating4, height=3)
    framecoloborating8.pack(expand=True, fill='x', padx=5, pady=5)



    SaMFrame = customtkinter.CTkFrame(framecoloborating4)
    SaMFrame.pack(expand=True, padx=5, pady=5, fill='both')

    Mframe = customtkinter.CTkFrame(SaMFrame)
    Mframe.pack(expand=True, padx=5, pady=(5, 0), fill='x')

    mmL = customtkinter.CTkLabel(Mframe, text='мм')
    mmL.pack(side='left', padx=5, pady=5)

    mmE = customtkinter.CTkEntry(Mframe, width=40)
    mmE.pack(side='left', padx=(1, 5), pady=5)

    smL = customtkinter.CTkLabel(Mframe, text='см')
    smL.pack(side='left', padx=5, pady=5)

    smE = customtkinter.CTkEntry(Mframe, width=40)
    smE.pack(side='left', padx=(1, 5), pady=5)

    gmL = customtkinter.CTkLabel(Mframe, text='зм')
    gmL.pack(side='left', padx=5, pady=5)

    gmE = customtkinter.CTkEntry(Mframe, width=40)
    gmE.pack(side='left', padx=(1, 5), pady=5)

    emL = customtkinter.CTkLabel(Mframe, text='эм')
    emL.pack(side='left', padx=5, pady=5)

    emE = customtkinter.CTkEntry(Mframe, width=40)
    emE.pack(side='left', padx=(1, 5), pady=5)

    pmL = customtkinter.CTkLabel(Mframe, text='пм')
    pmL.pack(side='left', padx=5, pady=5)

    pmE = customtkinter.CTkEntry(Mframe, width=40)
    pmE.pack(side='left', padx=(1, 5), pady=5)

    SL = customtkinter.CTkLabel(SaMFrame, text='Снаряжение')
    SL.pack(side='top', padx=5)

    STB = customtkinter.CTkTextbox(SaMFrame)
    STB.pack(side='top', fill='x')

    FFrame = customtkinter.CTkFrame(MainFrame)
    FFrame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

    AaSL = customtkinter.CTkLabel(FFrame, text='Атаки и Заклинания')
    AaSL.pack(side='top', padx=5, pady=5)

    AtackText = customtkinter.CTkTextbox(FFrame)
    AtackText.pack(side='top', fill='x')

    ActiveFrame = customtkinter.CTkScrollableFrame(FFrame)
    ActiveFrame.pack(expand=True, padx=5, pady=5, side='top', fill='both')

    classificate = ['Адское возмездие', 'Аура живучести', 'Аура очищения', 'Ашардалонова поступь', "Антипатия/симпатия",
                    'Аура жизни', 'Аура святости', 'Безмолвный образ',
                    'Божественное благоволение', 'Брешь в реальности', 'Быстрый колчан', 'Бесследное передвижение',
                    'Божественное оружие', 'Брызги кислоты', 'Благословение',
                    'Божественное слово', 'Быстрые друзья', 'Благословение удачи', 'Болезненное сияние',
                    'Быстрый гонец Гальдера', 'Ведьмин снаряд', 'Власть над погодой']
    spell_list = {
        'Адское возмездие': 'Hellish rebuke',
        'Аура живучести': 'Aura of vitality',
        'Аура очищения': 'Aura of purity',
        'Ашардалонова поступь': "Ashardalon's Stride",
        "Антипатия/симпатия": 'Antipathy&sympathy',
        'Аура жизни': 'Aura of life',
        'Аура святости': 'Holy aura',
        'Безмолвный образ': 'Silent image',
        'Божественное благоволение': 'Divine favor',
        'Брешь в реальности': 'Reality break',
        'Быстрый колчан': 'Swift quiver',
        'Бесследное передвижение': 'Pass without trace',
        'Божественное оружие': 'Spiritual weapon',
        'Брызги кислоты': 'Acid splash',
        'Благословение': 'Bless',
        'Божественное слово': 'Divine word',
        'Быстрые друзья': 'Fast friends',
        'Благословение удачи': "Fortune's favor",
        'Болезненное сияние': 'Sickening radiance',
        'Быстрый гонец Гальдера': "Galder's Speedy Courier",
        'Ведьмин снаряд': 'Witch bolt',
        'Власть над погодой': 'Control weather'
    }

    FrameSpells = customtkinter.CTkFrame(FFrame)
    FrameSpells.pack(fill='both', expand=True, padx=5, pady=5)

    Search_AbilityFrame = customtkinter.CTkScrollableFrame(FrameSpells)
    Search_AbilityFrame.pack(side='bottom', expand=True, fill='both')

    frames = {}

    def Info(text):
        search(text)

    def move_to_active_frame(spell, source_frame):
        children = source_frame.winfo_children()

        for child in children:
            child.pack_forget()

        new_spell_name = customtkinter.CTkLabel(ActiveFrame, text=spell)
        new_spell_name.pack()

        new_info_btn = customtkinter.CTkButton(
            ActiveFrame,
            text="ⓘ",
            command=lambda s=spell_list[spell]: Info(s)
        )
        new_info_btn.pack()

        return_btn = customtkinter.CTkButton(
            ActiveFrame,
            text="-",
            command=lambda s=spell, sf=source_frame: return_to_source(s, sf)
        )
        return_btn.pack()

    def return_to_source(spell, source_frame):
        active_children = ActiveFrame.winfo_children()
        for widget in active_children[-3:]:
            widget.destroy()

        Spell_name = customtkinter.CTkLabel(source_frame, text=spell)
        Spell_name.pack()

        Info_btn = customtkinter.CTkButton(
            source_frame,
            text="ⓘ",
            command=lambda s=spell_list[spell]: Info(s)
        )
        Info_btn.pack()

        Add_btn = customtkinter.CTkButton(
            source_frame,
            text="+",
            command=lambda s=spell, sf=source_frame: move_to_active_frame(s, sf)
        )
        Add_btn.pack()

    for i, spell in enumerate(classificate):
        frame_name = f"frame_{i}"
        frames[frame_name] = customtkinter.CTkFrame(Search_AbilityFrame)
        frames[frame_name].pack(pady=10, fill='x')

        Spell_name = customtkinter.CTkLabel(frames[frame_name], text=spell)
        Spell_name.pack()

        Info_btn = customtkinter.CTkButton(
            frames[frame_name],
            text="ⓘ",
            command=lambda s=spell_list[spell]: Info(s)
        )
        Info_btn.pack()

        Add_btn = customtkinter.CTkButton(
            frames[frame_name],
            text="+",
            command=lambda s=spell, f=frames[frame_name]: move_to_active_frame(s, f)
        )
        Add_btn.pack()


    def collect_widget_data():
        data = {}

        # Базовые поля
        data['name'] = Name.get()
        data['exp'] = Exp.get()
        data['mir'] = Mir.get()
        data['his'] = His.get()
        data['class'] = Class.get()
        data['race'] = Race.get()

        # Статистики
        data['power'] = StatePowerEntry.get()
        data['lov'] = StateLovEntry.get()
        data['tel'] = StateTELEntry.get()
        data['int'] = StateINTEntry.get()
        data['myd'] = StateMYDEntry.get()
        data['xar'] = StateXAREntry.get()

        # Спасброски
        data['power_spas'] = PowerSpas.get()
        data['power_spas_entry'] = PowerSpasEntry.get()
        data['agility_spas'] = agilitySpas.get()
        data['agility_spas_entry'] = agilitySpasEntry.get()
        data['tel_spas'] = TELSpas.get()
        data['tel_spas_entry'] = TELSpasEntry.get()
        data['int_spas'] = IntSpas.get()
        data['int_spas_entry'] = IntSpasEntry.get()
        data['myd_spas'] = MydSpas.get()
        data['myd_spas_entry'] = MydSpasEntry.get()
        data['xar_spas'] = XarSpas.get()
        data['xar_spas_entry'] = XarSpasEntry.get()

        # Навыки
        data['acr_spas'] = AcrSpas.get()
        data['acr_spas_entry'] = AcrSpasEntry.get()
        data['analis_spas'] = AnalisSpas.get()
        data['analis_spas_entry'] = AnalisSpasEntry.get()
        data['atlet_spas'] = AtletSpas.get()
        data['atlet_spas_entry'] = AtletSpasEntry.get()
        data['vosp_spas'] = VospSpas.get()
        data['vosp_spas_entry'] = VospSpasEntry.get()
        data['survival_spas'] = SurvivalSpas.get()
        data['survival_spas_entry'] = SurvivalSpasEntry.get()
        data['play_spas'] = PlaySpas.get()
        data['play_spas_entry'] = PlaySpasEntry.get()
        data['dan_spas'] = DanSpas.get()
        data['dan_spas_entry'] = DanSpasEntry.get()
        data['his_spas'] = HisSpas.get()
        data['his_spas_entry'] = HisSpasEntry.get()
        data['agh_spas'] = AgHSpas.get()
        data['agh_spas_entry'] = AgHSpasEntry.get()
        data['magic_spas'] = MagicSpas.get()
        data['magic_spas_entry'] = MagicSpasEntry.get()
        data['medicine_spas'] = MedicineSpas.get()
        data['medicine_spas_entry'] = MedicineSpasEntry.get()
        data['obman_spas'] = ObmanSpas.get()
        data['obman_spas_entry'] = ObmanSpasEntry.get()
        data['nature_spas'] = NatureSpas.get()
        data['nature_spas_entry'] = NatureSpasEntry.get()
        data['pronic_spas'] = PronicSpas.get()
        data['pronic_spas_entry'] = PronicSpasEntry.get()
        data['relig_spas'] = ReligSpas.get()
        data['relig_spas_entry'] = ReligSpasEntry.get()
        data['scret_spas'] = ScretSpas.get()
        data['scret_spas_entry'] = ScretSpasEntry.get()
        data['ybe_spas'] = YbeSpas.get()
        data['ybe_spas_entry'] = YbeSpasEntry.get()
        data['yza_spas'] = YZASpas.get()
        data['yza_spas_entry'] = YZASpasEntry.get()

        # Боевые характеристики
        data['kz'] = KZE.get()
        data['init'] = InitE.get()
        data['speed'] = SpeedE.get()
        data['max_hp'] = TekHPE.get()
        data['current_hp'] = TEKNP.get()
        data['temp_hp'] = timehpE.get()
        data['hit_dice'] = HitE.get()
        data['hit_dice_total'] = Hite.get()

        # Спасброски от смерти
        data['death_success1'] = Success1.get()
        data['death_success2'] = Success2.get()
        data['death_success3'] = Success3.get()
        data['death_fail1'] = Death1.get()
        data['death_fail2'] = Death2.get()
        data['death_fail3'] = Death3.get()

        # Текстовые поля
        data['character_traits'] = CHTB.get("1.0", "end-1c")
        data['ideals'] = ITB.get("1.0", "end-1c")
        data['attachments'] = PTB.get("1.0", "end-1c")
        data['weaknesses'] = STB.get("1.0", "end-1c")
        data['abilities'] = YOTB.get("1.0", "end-1c")
        data['languages'] = LuTB.get("1.0", "end-1c")
        data['equipment'] = STB.get("1.0", "end-1c")
        data['attacks'] = AtackText.get("1.0", "end-1c")


        data['mm'] = mmE.get()
        data['sm'] = smE.get()
        data['gm'] = gmE.get()
        data['em'] = emE.get()
        data['pm'] = pmE.get()


        data['inspiration'] = EntryVDH.get()
        data['proficiency'] = EntreBV.get()
        data['passive_wisdom'] = EntreM.get()


        active_spells = []
        for widget in ActiveFrame.winfo_children():
            if isinstance(widget, customtkinter.CTkLabel):
                active_spells.append(widget.cget("text"))
        data['active_spells'] = active_spells

        return data


    def load_widget_data(data):

        Name.delete(0, "end")
        Name.insert(0, data.get('name', ''))
        Exp.delete(0, "end")
        Exp.insert(0, data.get('exp', ''))
        Mir.delete(0, "end")
        Mir.insert(0, data.get('mir', ''))
        His.delete(0, "end")
        His.insert(0, data.get('his', ''))
        Class.set(data.get('class', ''))
        Race.set(data.get('race', ''))


        StatePowerEntry.delete(0, "end")
        StatePowerEntry.insert(0, data.get('power', ''))
        StateLovEntry.delete(0, "end")
        StateLovEntry.insert(0, data.get('lov', ''))
        StateTELEntry.delete(0, "end")
        StateTELEntry.insert(0, data.get('tel', ''))
        StateINTEntry.delete(0, "end")
        StateINTEntry.insert(0, data.get('int', ''))
        StateMYDEntry.delete(0, "end")
        StateMYDEntry.insert(0, data.get('myd', ''))
        StateXAREntry.delete(0, "end")
        StateXAREntry.insert(0, data.get('xar', ''))


        update_all()

        # Спасброски
        PowerSpasEntry.delete(0, "end")
        PowerSpasEntry.insert(0, data.get('power_spas_entry', ''))
        if data.get('power_spas'):
            PowerSpas.select()
        else:
            PowerSpas.deselect()

        agilitySpasEntry.delete(0, "end")
        agilitySpasEntry.insert(0, data.get('agility_spas_entry', ''))
        if data.get('agility_spas'):
            agilitySpas.select()
        else:
            agilitySpas.deselect()

        TELSpasEntry.delete(0, "end")
        TELSpasEntry.insert(0, data.get('tel_spas_entry', ''))
        if data.get('tel_spas'):
            TELSpas.select()
        else:
            TELSpas.deselect()

        IntSpasEntry.delete(0, "end")
        IntSpasEntry.insert(0, data.get('int_spas_entry', ''))
        if data.get('int_spas'):
            IntSpas.select()
        else:
            IntSpas.deselect()

        MydSpasEntry.delete(0, "end")
        MydSpasEntry.insert(0, data.get('myd_spas_entry', ''))
        if data.get('myd_spas'):
            MydSpas.select()
        else:
            MydSpas.deselect()

        XarSpasEntry.delete(0, "end")
        XarSpasEntry.insert(0, data.get('xar_spas_entry', ''))
        if data.get('xar_spas'):
            XarSpas.select()
        else:
            XarSpas.deselect()

        # Навыки
        AcrSpasEntry.delete(0, "end")
        AcrSpasEntry.insert(0, data.get('acr_spas_entry', ''))
        if data.get('acr_spas'):
            AcrSpas.select()
        else:
            AcrSpas.deselect()

        AnalisSpasEntry.delete(0, "end")
        AnalisSpasEntry.insert(0, data.get('analis_spas_entry', ''))
        if data.get('analis_spas'):
            AnalisSpas.select()
        else:
            AnalisSpas.deselect()

        AtletSpasEntry.delete(0, "end")
        AtletSpasEntry.insert(0, data.get('atlet_spas_entry', ''))
        if data.get('atlet_spas'):
            AtletSpas.select()
        else:
            AtletSpas.deselect()

        VospSpasEntry.delete(0, "end")
        VospSpasEntry.insert(0, data.get('vosp_spas_entry', ''))
        if data.get('vosp_spas'):
            VospSpas.select()
        else:
            VospSpas.deselect()

        SurvivalSpasEntry.delete(0, "end")
        SurvivalSpasEntry.insert(0, data.get('survival_spas_entry', ''))
        if data.get('survival_spas'):
            SurvivalSpas.select()
        else:
            SurvivalSpas.deselect()

        PlaySpasEntry.delete(0, "end")
        PlaySpasEntry.insert(0, data.get('play_spas_entry', ''))
        if data.get('play_spas'):
            PlaySpas.select()
        else:
            PlaySpas.deselect()

        DanSpasEntry.delete(0, "end")
        DanSpasEntry.insert(0, data.get('dan_spas_entry', ''))
        if data.get('dan_spas'):
            DanSpas.select()
        else:
            DanSpas.deselect()

        HisSpasEntry.delete(0, "end")
        HisSpasEntry.insert(0, data.get('his_spas_entry', ''))
        if data.get('his_spas'):
            HisSpas.select()
        else:
            HisSpas.deselect()

        AgHSpasEntry.delete(0, "end")
        AgHSpasEntry.insert(0, data.get('agh_spas_entry', ''))
        if data.get('agh_spas'):
            AgHSpas.select()
        else:
            AgHSpas.deselect()

        MagicSpasEntry.delete(0, "end")
        MagicSpasEntry.insert(0, data.get('magic_spas_entry', ''))
        if data.get('magic_spas'):
            MagicSpas.select()
        else:
            MagicSpas.deselect()

        MedicineSpasEntry.delete(0, "end")
        MedicineSpasEntry.insert(0, data.get('medicine_spas_entry', ''))
        if data.get('medicine_spas'):
            MedicineSpas.select()
        else:
            MedicineSpas.deselect()

        ObmanSpasEntry.delete(0, "end")
        ObmanSpasEntry.insert(0, data.get('obman_spas_entry', ''))
        if data.get('obman_spas'):
            ObmanSpas.select()
        else:
            ObmanSpas.deselect()

        NatureSpasEntry.delete(0, "end")
        NatureSpasEntry.insert(0, data.get('nature_spas_entry', ''))
        if data.get('nature_spas'):
            NatureSpas.select()
        else:
            NatureSpas.deselect()

        PronicSpasEntry.delete(0, "end")
        PronicSpasEntry.insert(0, data.get('pronic_spas_entry', ''))
        if data.get('pronic_spas'):
            PronicSpas.select()
        else:
            PronicSpas.deselect()

        ReligSpasEntry.delete(0, "end")
        ReligSpasEntry.insert(0, data.get('relig_spas_entry', ''))
        if data.get('relig_spas'):
            ReligSpas.select()
        else:
            ReligSpas.deselect()

        ScretSpasEntry.delete(0, "end")
        ScretSpasEntry.insert(0, data.get('scret_spas_entry', ''))
        if data.get('scret_spas'):
            ScretSpas.select()
        else:
            ScretSpas.deselect()

        YbeSpasEntry.delete(0, "end")
        YbeSpasEntry.insert(0, data.get('ybe_spas_entry', ''))
        if data.get('ybe_spas'):
            YbeSpas.select()
        else:
            YbeSpas.deselect()

        YZASpasEntry.delete(0, "end")
        YZASpasEntry.insert(0, data.get('yza_spas_entry', ''))
        if data.get('yza_spas'):
            YZASpas.select()
        else:
            YZASpas.deselect()

        # Боевые характеристики
        KZE.delete(0, "end")
        KZE.insert(0, data.get('kz', ''))
        InitE.delete(0, "end")
        InitE.insert(0, data.get('init', ''))
        SpeedE.delete(0, "end")
        SpeedE.insert(0, data.get('speed', ''))
        TekHPE.delete(0, "end")
        TekHPE.insert(0, data.get('max_hp', ''))
        TEKNP.delete(0, "end")
        TEKNP.insert(0, data.get('current_hp', ''))
        timehpE.delete(0, "end")
        timehpE.insert(0, data.get('temp_hp', ''))
        HitE.delete(0, "end")
        HitE.insert(0, data.get('hit_dice', ''))
        Hite.delete(0, "end")
        Hite.insert(0, data.get('hit_dice_total', ''))

        # Спасброски от смерти
        if data.get('death_success1'):
            Success1.select()
        else:
            Success1.deselect()

        if data.get('death_success2'):
            Success2.select()
        else:
            Success2.deselect()

        if data.get('death_success3'):
            Success3.select()
        else:
            Success3.deselect()

        if data.get('death_fail1'):
            Death1.select()
        else:
            Death1.deselect()

        if data.get('death_fail2'):
            Death2.select()
        else:
            Death2.deselect()

        if data.get('death_fail3'):
            Death3.select()
        else:
            Death3.deselect()

        # Текстовые поля
        CHTB.delete("1.0", "end")
        CHTB.insert("1.0", data.get('character_traits', ''))
        ITB.delete("1.0", "end")
        ITB.insert("1.0", data.get('ideals', ''))
        PTB.delete("1.0", "end")
        PTB.insert("1.0", data.get('attachments', ''))
        STB.delete("1.0", "end")
        STB.insert("1.0", data.get('weaknesses', ''))
        YOTB.delete("1.0", "end")
        YOTB.insert("1.0", data.get('abilities', ''))
        LuTB.delete("1.0", "end")
        LuTB.insert("1.0", data.get('languages', ''))
        STB.delete("1.0", "end")
        STB.insert("1.0", data.get('equipment', ''))
        AtackText.delete("1.0", "end")
        AtackText.insert("1.0", data.get('attacks', ''))

        # Деньги
        mmE.delete(0, "end")
        mmE.insert(0, data.get('mm', ''))
        smE.delete(0, "end")
        smE.insert(0, data.get('sm', ''))
        gmE.delete(0, "end")
        gmE.insert(0, data.get('gm', ''))
        emE.delete(0, "end")
        emE.insert(0, data.get('em', ''))
        pmE.delete(0, "end")
        pmE.insert(0, data.get('pm', ''))

        # Вдохновение и бонусы
        EntryVDH.delete(0, "end")
        EntryVDH.insert(0, data.get('inspiration', ''))
        EntreBV.delete(0, "end")
        EntreBV.insert(0, data.get('proficiency', ''))
        EntreM.delete(0, "end")
        EntreM.insert(0, data.get('passive_wisdom', ''))


        for widget in ActiveFrame.winfo_children():
            widget.destroy()


        for spell_name in data.get('active_spells', []):
            if spell_name in spell_list:

                for frame_key, frame in frames.items():
                    children = frame.winfo_children()
                    if children and isinstance(children[0], customtkinter.CTkLabel):
                        if children[0].cget("text") == spell_name:
                            move_to_active_frame(spell_name, frame)


    def save_data():
        data = collect_widget_data()


        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"{data.get('name', 'character')}.json"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Успех", f"Данные сохранены в файл:\n{filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")


    def load_data():
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)


                if messagebox.askyesno("Подтверждение",
                                       f"Загрузить данные персонажа '{data.get('name', 'Без имени')}'?\n"
                                       "Текущие данные будут потеряны."):
                    load_widget_data(data)
                    messagebox.showinfo("Успех", f"Данные загружены из файла:\n{filename}")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")


    def on_closing():
        if messagebox.askyesno("Выход", "Сохранить данные перед выходом?"):
            save_data()
        chwin.destroy()

    chwin.protocol("WM_DELETE_WINDOW", on_closing)


    def quick_save():
        data = collect_widget_data()
        filename = f"{data.get('name', 'character')}_quicksave.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Быстрое сохранение", f"Данные сохранены в файл:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")


    def quick_load():
        filename = filedialog.askopenfilename(
            initialdir=".",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Выберите файл для быстрой загрузки"
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if messagebox.askyesno("Быстрая загрузка",
                                       f"Загрузить данные персонажа '{data.get('name', 'Без имени')}'?"):
                    load_widget_data(data)
                    messagebox.showinfo("Успех", f"Данные загружены из файла:\n{filename}")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")

    quick_save_btn = customtkinter.CTkButton(menubar, text="Быстрое сохранение", command=quick_save)
    quick_save_btn.pack(side="left", padx=5)

    quick_load_btn = customtkinter.CTkButton(menubar, text="Быстрая загрузка", command=quick_load)
    quick_load_btn.pack(side="left", padx=5)

    update_all()
    chwin.mainloop()


def Add():
    add_character_main()


# ==================== СЕТЕВОЙ МЕНЕДЖЕР (КЛИЕНТ) ====================

class NetworkManager:
    def __init__(self, player_name=None):
        self.ws = None
        self.connected = False
        self.message_queue = queue.Queue()
        self.game_board_ref = None
        self.chat_callback = None
        self.token_callback = None
        self.map_callback = None
        self.loop = None
        self.background_thread = None
        self.pending_maps = {}  # Ожидающие сборки карты

        if player_name and player_name.strip():
            self.player_name = player_name.strip()
        else:
            self.player_name = f"Игрок_{client_id[:4]}"

        logger.info(f"🌐 Сетевой менеджер инициализирован для {self.player_name}")

    def update_player_name(self, new_name):
        """Обновление имени игрока"""
        if new_name and new_name.strip():
            self.player_name = new_name.strip()
            logger.info(f"🔄 Имя игрока обновлено: {self.player_name}")
            return True
        return False

    def start_background_loop(self):
        """Запуск фонового event loop для асинхронных операций"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def connect_async(self, host="localhost", port=8765):
        """Асинхронное подключение к серверу"""
        try:
            uri = f"ws://{host}:{port}"
            logger.info(f"🔗 Попытка подключения к {uri}")

            self.ws = await asyncio.wait_for(
                websockets.connect(uri, ping_interval=20, ping_timeout=10, max_size=50 * 1024 * 1024),
                timeout=10
            )

            self.connected = True
            logger.info("✅ Успешное подключение к серверу")

            # Отправляем информацию о игроке
            await self.send({
                'type': 'player_join',
                'data': {
                    'id': client_id,
                    'name': self.player_name,
                    'color': "#FF4444"
                }
            })

            # Запускаем прием сообщений
            asyncio.create_task(self.receive_messages())

            return True
        except asyncio.TimeoutError:
            logger.error("⏱️ Таймаут подключения к серверу")
            return False
        except ConnectionRefusedError:
            logger.error("❌ Сервер недоступен")
            return False
        except Exception as e:
            logger.error(f"❌ Ошибка подключения: {e}")
            return False

    def connect(self, host="localhost", port=8765):
        """Синхронное подключение к серверу"""
        try:
            if not self.loop or not self.loop.is_running():
                self.background_thread = Thread(target=self.start_background_loop, daemon=True)
                self.background_thread.start()

                import time
                for _ in range(10):
                    if self.loop and self.loop.is_running():
                        break
                    time.sleep(0.1)
                else:
                    logger.error("❌ Не удалось запустить event loop")
                    return False

            future = asyncio.run_coroutine_threadsafe(
                self.connect_async(host, port),
                self.loop
            )

            result = future.result(timeout=15)
            return result

        except Exception as e:
            logger.error(f"❌ Ошибка при подключении: {e}")
            return False

    async def send(self, data):
        """Асинхронная отправка сообщения"""
        if self.connected and self.ws:
            try:
                await self.ws.send(json.dumps(data))
            except Exception as e:
                logger.error(f"❌ Ошибка отправки сообщения: {e}")
                self.connected = False

    def send_sync(self, data):
        """Синхронная отправка сообщения"""
        if self.connected and self.loop and self.loop.is_running():
            try:
                asyncio.run_coroutine_threadsafe(self.send(data), self.loop)
            except Exception as e:
                logger.error(f"❌ Ошибка синхронной отправки: {e}")

    async def send_large_data(self, data_type, data_bytes, metadata=None):
        """Отправка больших данных чанками"""
        try:
            if not self.connected or not self.ws:
                return False

            # Генерируем уникальный ID для этой передачи
            transfer_id = str(uuid.uuid4())

            # Конвертируем данные в base64
            base64_data = base64.b64encode(data_bytes).decode('utf-8')

            # Разбиваем на чанки
            chunks = []
            for i in range(0, len(base64_data), CHUNK_SIZE):
                chunk = base64_data[i:i + CHUNK_SIZE]
                chunks.append(chunk)

            total_chunks = len(chunks)
            logger.info(f"📦 Разбито на {total_chunks} чанков по {CHUNK_SIZE} байт")

            # Отправляем метаданные
            await self.send({
                'type': 'map_update',
                'data': {
                    'action': 'load',
                    'filename': metadata.get('filename'),
                    'player': self.player_name,
                    'size': len(data_bytes),
                    'chunked': True,
                    'total_chunks': total_chunks,
                    'map_id': transfer_id
                }
            })

            # Отправляем чанки
            for i, chunk in enumerate(chunks):
                await self.send({
                    'type': 'map_chunk',
                    'data': {
                        'map_id': transfer_id,
                        'chunk_index': i,
                        'total_chunks': total_chunks,
                        'chunk': chunk,
                        'metadata': metadata
                    }
                })

                # Логируем прогресс каждые 10 чанков
                if (i + 1) % 10 == 0:
                    logger.info(f"📦 Отправлено {i + 1}/{total_chunks} чанков")

            # Отправляем подтверждение завершения
            await self.send({
                'type': 'map_ready',
                'data': {
                    'map_id': transfer_id,
                    'metadata': metadata
                }
            })

            logger.info(f"✅ {data_type} успешно отправлен ({len(base64_data)} байт)")
            return True

        except Exception as e:
            logger.error(f"❌ Ошибка отправки больших данных: {e}")
            return False

    def send_large_data_sync(self, data_type, data_bytes, metadata=None):
        """Синхронная отправка больших данных"""
        if not self.connected or not self.loop or not self.loop.is_running():
            return False

        try:
            future = asyncio.run_coroutine_threadsafe(
                self.send_large_data(data_type, data_bytes, metadata),
                self.loop
            )
            return future.result(timeout=60)  # 60 секунд таймаут
        except Exception as e:
            logger.error(f"❌ Ошибка синхронной отправки больших данных: {e}")
            return False

    async def receive_messages(self):
        """Прием сообщений от сервера"""
        try:
            async for message in self.ws:
                await self.handle_message(message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("🔌 Соединение с сервером закрыто")
            self.connected = False
        except Exception as e:
            logger.error(f"❌ Ошибка приема сообщений: {e}")
            self.connected = False

    async def handle_message(self, message):
        """Обработка входящих сообщений"""
        try:
            data = json.loads(message)
            message_type = data['type']

            if message_type == 'init':
                if self.game_board_ref and 'tokens' in data['data']:
                    for token_id, token_data in data['data']['tokens'].items():
                        self.game_board_ref.add_token_from_network(token_data)

                if 'current_map' in data['data'] and data['data']['current_map']:
                    map_data = data['data']['current_map']
                    if self.map_callback:
                        self.map_callback({
                            'action': 'load',
                            'filename': map_data.get('filename'),
                            'image_base64': map_data.get('image_base64'),
                            'player': map_data.get('loaded_by'),
                            'size': map_data.get('size', 0)
                        })

            elif message_type == 'token_update':
                if self.token_callback:
                    self.token_callback(data['data'])

            elif message_type == 'chat_message':
                if self.chat_callback:
                    self.chat_callback(data['data'])

            elif message_type == 'roll_dice':
                if self.chat_callback:
                    roll_data = data['data']
                    self.chat_callback({
                        'player': '🎲',
                        'message': f"{roll_data['player']}: d{roll_data['dice']} = {roll_data['result']}",
                        'is_system': True
                    })

            elif message_type == 'player_join':
                if self.chat_callback:
                    player = data['data']['name']
                    if player != self.player_name:
                        self.chat_callback({
                            'player': '🟢',
                            'message': f"{player} присоединился",
                            'is_system': True
                        })

            elif message_type == 'player_leave':
                if self.chat_callback:
                    player = data['data']['name']
                    self.chat_callback({
                        'player': '🔴',
                        'message': f"{player} покинул игру",
                        'is_system': True
                    })

            elif message_type == 'map_update':
                if self.map_callback:
                    self.map_callback(data['data'])

            elif message_type == 'map_chunk':
                chunk_data = data['data']
                map_id = chunk_data['map_id']
                chunk_index = chunk_data['chunk_index']
                chunk_content = chunk_data['chunk']

                # Сохраняем чанк
                if map_id not in self.pending_maps:
                    self.pending_maps[map_id] = {
                        'chunks': {},
                        'total_chunks': chunk_data.get('total_chunks', 0),
                        'metadata': chunk_data.get('metadata', {})
                    }

                self.pending_maps[map_id]['chunks'][chunk_index] = chunk_content

                # Проверяем, собраны ли все чанки
                pending = self.pending_maps[map_id]
                if len(pending['chunks']) >= pending['total_chunks']:
                    await self.assemble_map(map_id)

            elif message_type == 'map_ready':
                if self.map_callback:
                    self.map_callback(data['data'])

        except Exception as e:
            logger.error(f"❌ Ошибка обработки сообщения: {e}")

    async def assemble_map(self, map_id):
        """Сборка карты из чанков"""
        try:
            if map_id not in self.pending_maps:
                return

            pending = self.pending_maps[map_id]

            # Собираем чанки в правильном порядке
            sorted_indices = sorted(pending['chunks'].keys())
            combined_base64 = ''

            for idx in sorted_indices:
                combined_base64 += pending['chunks'][idx]

            # Вызываем callback
            if self.map_callback:
                self.map_callback({
                    'action': 'load',
                    'filename': pending['metadata'].get('filename'),
                    'image_base64': combined_base64,
                    'player': pending['metadata'].get('player'),
                    'size': pending['metadata'].get('size', 0)
                })

            logger.info(
                f"🗺️ Карта собрана из чанков: {pending['metadata'].get('filename')} ({len(combined_base64)} байт)")

            # Очищаем из ожидающих
            del self.pending_maps[map_id]

        except Exception as e:
            logger.error(f"❌ Ошибка сборки карты: {e}")
            if map_id in self.pending_maps:
                del self.pending_maps[map_id]


# ==================== ИГРОВОЕ ПОЛЕ С СЕТЕВОЙ ПОДДЕРЖКОЙ ====================
class AdvancedGameBoard(customtkinter.CTkFrame):
    """Игровое поле с поддержкой мультиплеера"""

    def __init__(self, parent, network_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.network_manager = network_manager

        # Callback'и будут установлены позже в update_ui_with_player_name
        # если network_manager передан

        self.canvas = tkinter.Canvas(self, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.grid_size = 50
        self.grid_color = "#333333"
        self.grid_width = 1

        self.original_image = None
        self.map_image = None
        self.canvas_map_id = None
        self.map_position = None
        self.map_dimensions = None
        self.current_map_filename = None
        self.current_map_base64 = None
        self.load_map_image()

        self.token_colors = ["#ff4444", "#44ff44", "#4444ff", "#ffff44",
                             "#ff44ff", "#44ffff", "#ff8844", "#8844ff"]
        self.current_color_index = 0
        self.selected_color = self.token_colors[0]

        self.create_color_palette()

        self.tokens = {}
        self.current_token_id = 0

        # Прогресс-бар для загрузки карт
        self.progress_frame = customtkinter.CTkFrame(self, height=40)
        self.progress_frame.place(relx=0.5, rely=0.95, anchor="center")
        self.progress_frame.pack_forget()  # Скрываем по умолчанию

        self.progress_label = customtkinter.CTkLabel(
            self.progress_frame,
            text="Загрузка карты...",
            font=("Arial", 12)
        )
        self.progress_label.pack(pady=(5, 0))

        self.progress_bar = customtkinter.CTkProgressBar(
            self.progress_frame,
            width=300,
            height=20
        )
        self.progress_bar.pack(pady=(0, 5))
        self.progress_bar.set(0)

        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind("<Button-1>", self.place_token)
        self.canvas.bind("<Button-3>", self.remove_token)
        self.canvas.bind("<Button-2>", self.change_token_color)

    def create_color_palette(self):
        """Создание панели выбора цвета"""
        self.palette_frame = customtkinter.CTkFrame(self, height=50)
        self.palette_frame.place(relx=0.5, rely=0.02, anchor="n")

        self.color_buttons = []

        self.color_preview = customtkinter.CTkLabel(
            self.palette_frame,
            text="Цвет:",
            font=("Arial", 12)
        )
        self.color_preview.pack(side='left', padx=(10, 5))

        self.color_display = customtkinter.CTkLabel(
            self.palette_frame,
            text="     ",
            fg_color=self.selected_color,
            width=30,
            height=30,
            corner_radius=15
        )
        self.color_display.pack(side='left', padx=5)

        for color in self.token_colors:
            self.add_color_button(color)

        custom_btn = customtkinter.CTkButton(
            self.palette_frame,
            text="🎨",
            width=30,
            height=30,
            command=self.choose_custom_color,
            font=("Arial", 14)
        )
        custom_btn.pack(side='left', padx=(10, 5))

        prev_btn = customtkinter.CTkButton(
            self.palette_frame,
            text="←",
            width=30,
            height=30,
            command=self.previous_color,
            font=("Arial", 14)
        )
        prev_btn.pack(side='left', padx=(10, 0))

        next_btn = customtkinter.CTkButton(
            self.palette_frame,
            text="→",
            width=30,
            height=30,
            command=self.next_color,
            font=("Arial", 14)
        )
        next_btn.pack(side='left', padx=(0, 10))

        self.color_info = customtkinter.CTkLabel(
            self.palette_frame,
            text=f"Цвет {self.current_color_index + 1}/{len(self.token_colors)}",
            font=("Arial", 10)
        )
        self.color_info.pack(side='left', padx=10)

    def add_color_button(self, color):
        """Добавление кнопки цвета в палитру"""
        color_btn = customtkinter.CTkButton(
            self.palette_frame,
            text="",
            width=25,
            height=25,
            fg_color=color,
            hover_color=color,
            command=lambda c=color: self.select_color(c)
        )
        color_btn.pack(side='left', padx=2)
        self.color_buttons.append(color_btn)

    def select_color(self, color):
        """Выбор цвета"""
        self.selected_color = color
        self.current_color_index = self.token_colors.index(color)
        self.update_color_display()

    def choose_custom_color(self):
        """Выбор произвольного цвета"""
        color_code = colorchooser.askcolor(
            title="Выберите цвет метки",
            initialcolor=self.selected_color
        )
        if color_code and color_code[0]:
            new_color = color_code[1]

            if new_color not in self.token_colors:
                self.token_colors.append(new_color)
                self.add_color_button(new_color)

            self.selected_color = new_color
            self.current_color_index = self.token_colors.index(new_color)
            self.update_color_display()

    def change_token_color(self, event):
        """Изменение цвета существующего токена"""
        item = self.canvas.find_closest(event.x, event.y)
        if item and "token" in self.canvas.gettags(item[0]):
            new_color = colorchooser.askcolor(
                title="Изменить цвет метки",
                initialcolor=self.selected_color
            )
            if new_color and new_color[0]:
                color_hex = new_color[1]
                self.canvas.itemconfig(item[0], fill=color_hex)

                if color_hex not in self.token_colors:
                    self.token_colors.append(color_hex)
                    self.add_color_button(color_hex)

                for token_id, token_info in self.tokens.items():
                    if token_info["id"] == item[0]:
                        self.tokens[token_id]["color"] = color_hex

                        if self.network_manager and self.network_manager.connected:
                            self.network_manager.send_sync({
                                'type': 'token_update',
                                'data': {
                                    'id': token_id,
                                    'color': color_hex,
                                    'action': 'update'
                                }
                            })
                        break

    def update_color_display(self):
        """Обновление отображения текущего цвета"""
        self.color_display.configure(fg_color=self.selected_color)
        self.color_info.configure(
            text=f"Цвет {self.current_color_index + 1}/{len(self.token_colors)}"
        )

    def next_color(self):
        """Следующий цвет в палитре"""
        self.current_color_index = (self.current_color_index + 1) % len(self.token_colors)
        self.selected_color = self.token_colors[self.current_color_index]
        self.update_color_display()

    def previous_color(self):
        """Предыдущий цвет в палитре"""
        self.current_color_index = (self.current_color_index - 1) % len(self.token_colors)
        self.selected_color = self.token_colors[self.current_color_index]
        self.update_color_display()

    def load_map_image(self):
        """Загрузка изображения карты"""
        global image_path
        try:
            if image_path and os.path.exists(image_path):
                self.original_image = Image.open(image_path)
                self.current_map_filename = os.path.basename(image_path)
                self.after(100, self.resize_image)
            else:
                logger.info("Карта не выбрана, отображаем пустое поле")
                self.draw_grid()
        except Exception as e:
            logger.error(f"Ошибка загрузки карты: {e}")
            self.draw_grid()

    def optimize_image_for_transfer(self, img_path, max_dimension=4096):
        """Оптимизирует изображение для передачи по сети"""
        try:
            img = Image.open(img_path)

            # Проверяем размеры
            if img.width > max_dimension or img.height > max_dimension:
                # Масштабируем
                ratio = min(max_dimension / img.width, max_dimension / img.height)
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)

                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                logger.info(f"Изображение масштабировано до {new_width}x{new_height}")

            # Конвертируем в RGB если нужно
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            # Сохраняем во временный файл с оптимизацией
            temp_path = os.path.join(tempfile.gettempdir(), f"optimized_{uuid.uuid4().hex}.jpg")
            img.save(temp_path, 'JPEG', quality=85, optimize=True)

            return temp_path

        except Exception as e:
            logger.error(f"Ошибка оптимизации изображения: {e}")
            return img_path

    def send_map_to_network(self, img_path):
        """Отправка карты в сеть"""
        try:
            if not self.network_manager or not self.network_manager.connected:
                logger.warning("Не подключен к серверу, не могу отправить карту")
                return False

            # Оптимизируем изображение если нужно
            optimized_path = self.optimize_image_for_transfer(img_path)
            should_delete_temp = optimized_path != img_path

            try:
                # Читаем файл
                with open(optimized_path, "rb") as image_file:
                    image_bytes = image_file.read()

                filename = os.path.basename(img_path)
                filesize = len(image_bytes)

                # Определяем способ отправки
                if filesize <= MAX_DIRECT_SIZE:
                    # Маленькая карта - отправляем напрямую
                    base64_string = base64.b64encode(image_bytes).decode('utf-8')

                    self.network_manager.send_sync({
                        'type': 'map_update',
                        'data': {
                            'action': 'load',
                            'filename': filename,
                            'image_base64': base64_string,
                            'player': self.network_manager.player_name,
                            'size': filesize
                        }
                    })

                    logger.info(f"Карта отправлена напрямую: {filename} ({filesize} байт)")

                else:
                    # Большая карта - используем чанкировку
                    logger.info(f"Карта большая ({filesize} байт), начинаю чанкировку...")

                    # Отправляем чанки
                    success = self.network_manager.send_large_data_sync(
                        'map',
                        image_bytes,
                        {
                            'filename': filename,
                            'player': self.network_manager.player_name,
                            'size': filesize,
                            'chunked': True
                        }
                    )

                    if not success:
                        logger.error("Ошибка отправки чанкованной карты")
                        return False

                return True

            finally:
                # Удаляем временный файл если он был создан
                if should_delete_temp and os.path.exists(optimized_path):
                    os.remove(optimized_path)

        except Exception as e:
            logger.error(f"Ошибка отправки карты в сеть: {e}")
            return False

    def load_map_from_base64(self, base64_string, filename):
        """Загрузка карты из base64 строки"""
        try:
            # Проверяем размер данных
            if len(base64_string) > 100 * 1024 * 1024:  # 100MB
                logger.error("Слишком большая карта для загрузки")
                messagebox.showerror("Ошибка", "Карта слишком большая для загрузки в память")
                return False

            # Декодируем base64 в байты
            image_bytes = base64.b64decode(base64_string)

            # Проверяем, что это валидное изображение
            try:
                image = Image.open(io.BytesIO(image_bytes))
                image.verify()  # Проверяем целостность
            except:
                logger.error("Некорректное изображение")
                return False

            # Создаем изображение заново после verify
            image = Image.open(io.BytesIO(image_bytes))

            # Ограничиваем максимальный размер в пикселях
            if image.width * image.height > MAX_IMAGE_PIXELS:
                # Масштабируем
                ratio = (MAX_IMAGE_PIXELS / (image.width * image.height)) ** 0.5
                new_width = int(image.width * ratio)
                new_height = int(image.height * ratio)

                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                logger.info(f"Карта масштабирована до {new_width}x{new_height}")

            self.original_image = image
            self.current_map_filename = filename
            self.current_map_base64 = base64_string

            # Обновляем отображение
            self.after(100, self.resize_image)

            logger.info(f"Карта загружена: {filename} ({len(base64_string)} байт)")
            return True

        except MemoryError:
            logger.error("Недостаточно памяти для загрузки карты")
            messagebox.showerror("Ошибка", "Недостаточно памяти для загрузки этой карты")
            return False
        except Exception as e:
            logger.error(f"Ошибка загрузки карты из base64: {e}")
            return False

    def on_canvas_configure(self, event=None):
        """Обработчик изменения размера холста"""
        if self.original_image:
            self.resize_image()
        else:
            self.draw_grid()

    def resize_image(self):
        """Изменение размера изображения карты"""
        if not self.original_image:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        original_width, original_height = self.original_image.size
        width_ratio = canvas_width / original_width
        height_ratio = canvas_height / original_height

        scale_ratio = min(width_ratio, height_ratio)
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)

        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.map_image = ImageTk.PhotoImage(resized_image)

        if self.canvas_map_id:
            self.canvas.delete(self.canvas_map_id)

        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.canvas_map_id = self.canvas.create_image(x, y, anchor="nw", image=self.map_image, tags="map")

        self.map_position = (x, y)
        self.map_dimensions = (new_width, new_height)

        self.draw_fixed_grid()

    def draw_fixed_grid(self):
        """Отрисовка сетки поверх карты"""
        self.canvas.delete("grid")

        if not self.map_position or not self.map_dimensions:
            return

        map_x, map_y = self.map_position
        map_width, map_height = self.map_dimensions

        if map_width <= 0 or map_height <= 0:
            return

        num_cells_x = int(map_width / self.grid_size) + 1
        num_cells_y = int(map_height / self.grid_size) + 1

        for i in range(num_cells_x + 1):
            x = map_x + (i * self.grid_size)
            if x <= map_x + map_width:
                self.canvas.create_line(
                    x, map_y,
                    x, map_y + map_height,
                    fill=self.grid_color,
                    width=self.grid_width,
                    tags="grid"
                )

        for i in range(num_cells_y + 1):
            y = map_y + (i * self.grid_size)
            if y <= map_y + map_height:
                self.canvas.create_line(
                    map_x, y,
                    map_x + map_width, y,
                    fill=self.grid_color,
                    width=self.grid_width,
                    tags="grid"
                )

    def draw_grid(self, event=None):
        """Отрисовка сетки на пустом поле"""
        self.canvas.delete("grid")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width > 20 and height > 20:
            num_cells_x = int(width / self.grid_size) + 1
            num_cells_y = int(height / self.grid_size) + 1

            for i in range(num_cells_x + 1):
                x = i * self.grid_size
                self.canvas.create_line(
                    x, 0,
                    x, height,
                    fill=self.grid_color,
                    width=self.grid_width,
                    tags="grid"
                )

            for i in range(num_cells_y + 1):
                y = i * self.grid_size
                self.canvas.create_line(
                    0, y,
                    width, y,
                    fill=self.grid_color,
                    width=self.grid_width,
                    tags="grid"
                )

    def handle_network_token(self, token_data):
        """Обработка токенов из сети"""
        try:
            action = token_data.get('action')
            token_id = token_data.get('id')

            if action == 'add':
                self.add_token_from_network(token_data)
            elif action == 'update':
                self.update_token_from_network(token_data)
            elif action == 'remove':
                self.remove_token_from_network(token_id)
        except Exception as e:
            logger.error(f"Ошибка обработки сетевого токена: {e}")

    def handle_network_map(self, map_data):
        """Обработка обновлений карты из сети"""
        try:
            action = map_data.get('action')

            if action == 'load':
                # Проверяем, чанкованная ли это карта
                if map_data.get('chunked', False):
                    # Для чанкованных карт ждем отдельного сообщения
                    filename = map_data.get('filename')
                    player = map_data.get('player', 'Неизвестно')

                    # Уведомляем о начале загрузки большой карты
                    if self.network_manager and self.network_manager.chat_callback:
                        size_mb = map_data.get('size', 0) / (1024 * 1024)
                        self.network_manager.chat_callback({
                            'player': '🗺️',
                            'message': f"{player} загружает карту: {filename} ({size_mb:.1f} MB)",
                            'is_system': True
                        })

                elif 'image_base64' in map_data:
                    # Прямая загрузка
                    filename = map_data.get('filename')
                    image_base64 = map_data.get('image_base64')
                    player = map_data.get('player', 'Неизвестно')

                    if image_base64:
                        self.load_map_from_base64(image_base64, filename)

                        # Уведомляем в чат
                        if self.network_manager and self.network_manager.chat_callback:
                            size_kb = len(image_base64) / 1024
                            self.network_manager.chat_callback({
                                'player': '🗺️',
                                'message': f"{player}: {filename} ({size_kb:.1f} KB)",
                                'is_system': True
                            })

            elif action == 'ready':
                # Карта собрана из чанков, можно показать уведомление
                metadata = map_data.get('metadata', {})
                filename = metadata.get('filename')
                player = metadata.get('player', 'Неизвестно')

                if self.network_manager and self.network_manager.chat_callback:
                    self.network_manager.chat_callback({
                        'player': '🗺️',
                        'message': f"{player}: {filename} (загрузка завершена)",
                        'is_system': True
                    })

            elif action == 'clear':
                self.clear_map()

                if self.network_manager and self.network_manager.chat_callback:
                    player = map_data.get('player', 'Неизвестно')
                    self.network_manager.chat_callback({
                        'player': '🗺️',
                        'message': f"{player} очистил карту",
                        'is_system': True
                    })

        except Exception as e:
            logger.error(f"Ошибка обработки сетевой карты: {e}")

    def add_token_from_network(self, token_data):
        """Добавление токена из сети"""
        try:
            token_id = token_data['id']

            if token_id in self.tokens:
                return

            x = token_data['x']
            y = token_data['y']
            color = token_data.get('color', '#ff4444')

            token = self.canvas.create_oval(
                x - 15, y - 15,
                x + 15, y + 15,
                fill=color,
                outline="#ffffff",
                width=2,
                tags=("token", token_id, "network")
            )

            self.tokens[token_id] = {
                "id": token,
                "x": x,
                "y": y,
                "color": color,
                "is_network": True
            }

            logger.info(f"Добавлен сетевой токен: {token_id}")

        except Exception as e:
            logger.error(f"Ошибка добавления токена из сети: {e}")

    def update_token_from_network(self, token_data):
        """Обновление токена из сети"""
        try:
            token_id = token_data['id']
            x = token_data.get('x')
            y = token_data.get('y')
            color = token_data.get('color')

            if token_id in self.tokens:
                token_info = self.tokens[token_id]

                if x is not None and y is not None:
                    self.canvas.coords(token_info["id"],
                                       x - 15, y - 15,
                                       x + 15, y + 15)
                    token_info["x"] = x
                    token_info["y"] = y

                if color is not None:
                    self.canvas.itemconfig(token_info["id"], fill=color)
                    token_info["color"] = color

        except Exception as e:
            logger.error(f"Ошибка обновления токена из сети: {e}")

    def remove_token_from_network(self, token_id):
        """Удаление токена из сети"""
        try:
            if token_id in self.tokens:
                token_info = self.tokens[token_id]
                if token_info.get('is_network', False):
                    self.canvas.delete(token_info["id"])
                    del self.tokens[token_id]
                    logger.info(f"Удален сетевой токен: {token_id}")

        except Exception as e:
            logger.error(f"Ошибка удаления токена из сети: {e}")

    def place_token(self, event):
        """Размещение токена на поле"""
        try:
            if self.map_position:
                map_x, map_y = self.map_position
                map_width, map_height = self.map_dimensions

                if (map_x <= event.x <= map_x + map_width and
                        map_y <= event.y <= map_y + map_height):

                    token_id = f"token_{self.current_token_id}"
                    radius = 15

                    token = self.canvas.create_oval(
                        event.x - radius, event.y - radius,
                        event.x + radius, event.y + radius,
                        fill=self.selected_color,
                        outline="#ffffff",
                        width=2,
                        tags=("token", token_id)
                    )

                    grid_x = int((event.x - map_x) / self.grid_size)
                    grid_y = int((event.y - map_y) / self.grid_size)

                    self.tokens[token_id] = {
                        "id": token,
                        "x": event.x,
                        "y": event.y,
                        "grid_x": grid_x,
                        "grid_y": grid_y,
                        "color": self.selected_color,
                        "is_network": False
                    }
                    self.current_token_id += 1

                    self.canvas.tag_bind(token, "<Button1-Motion>", lambda e, t=token: self.move_token(e, t))

                    if self.network_manager and self.network_manager.connected:
                        self.network_manager.send_sync({
                            'type': 'token_update',
                            'data': {
                                'id': token_id,
                                'x': event.x,
                                'y': event.y,
                                'color': self.selected_color,
                                'action': 'add'
                            }
                        })

                    logger.info(f"Размещен токен: {token_id} на ({event.x}, {event.y})")

        except Exception as e:
            logger.error(f"Ошибка размещения токена: {e}")

    def move_token(self, event, token):
        """Перемещение токена"""
        try:
            if self.map_position:
                map_x, map_y = self.map_position
                map_width, map_height = self.map_dimensions

                if (map_x <= event.x <= map_x + map_width and
                        map_y <= event.y <= map_y + map_height):

                    grid_x = int((event.x - map_x) / self.grid_size)
                    grid_y = int((event.y - map_y) / self.grid_size)

                    use_snapping = True
                    if use_snapping:
                        snapped_x = map_x + (grid_x * self.grid_size) + (self.grid_size // 2)
                        snapped_y = map_y + (grid_y * self.grid_size) + (self.grid_size // 2)
                        final_x, final_y = snapped_x, snapped_y
                    else:
                        final_x, final_y = event.x, event.y

                    self.canvas.coords(token,
                                       final_x - 15, final_y - 15,
                                       final_x + 15, final_y + 15)

                    token_id = None
                    for tid, token_info in self.tokens.items():
                        if token_info["id"] == token:
                            token_id = tid
                            self.tokens[token_id]["x"] = final_x
                            self.tokens[token_id]["y"] = final_y
                            self.tokens[token_id]["grid_x"] = grid_x
                            self.tokens[token_id]["grid_y"] = grid_y
                            break

                    if token_id and self.network_manager and self.network_manager.connected:
                        if not self.tokens[token_id].get('is_network', False):
                            self.network_manager.send_sync({
                                'type': 'token_update',
                                'data': {
                                    'id': token_id,
                                    'x': final_x,
                                    'y': final_y,
                                    'action': 'update'
                                }
                            })

        except Exception as e:
            logger.error(f"Ошибка перемещения токена: {e}")

    def remove_token(self, event):
        """Удаление токена"""
        try:
            item = self.canvas.find_closest(event.x, event.y)
            if item and "token" in self.canvas.gettags(item[0]):
                token_id = None
                for tid, token_info in self.tokens.items():
                    if token_info["id"] == item[0]:
                        token_id = tid
                        break

                self.canvas.delete(item[0])

                if token_id in self.tokens:
                    if not self.tokens[token_id].get('is_network', False):
                        if self.network_manager and self.network_manager.connected:
                            self.network_manager.send_sync({
                                'type': 'token_update',
                                'data': {
                                    'id': token_id,
                                    'action': 'remove'
                                }
                            })

                    del self.tokens[token_id]
                    logger.info(f"Удален токен: {token_id}")

        except Exception as e:
            logger.error(f"Ошибка удаления токена: {e}")

    def update_map_image(self):
        """Обновление изображения карты"""
        self.load_map_image()

    def clear_board(self):
        """Очистка игрового поля"""
        for token_info in list(self.tokens.values()):
            self.canvas.delete(token_info["id"])
        self.tokens.clear()
        self.current_token_id = 0
        logger.info("Игровое поле очищено")

    def clear_map(self):
        """Очистка карты"""
        if self.canvas_map_id:
            self.canvas.delete(self.canvas_map_id)
            self.canvas_map_id = None

        self.original_image = None
        self.map_image = None
        self.map_position = None
        self.map_dimensions = None
        self.current_map_filename = None
        self.current_map_base64 = None
        self.draw_grid()

    def load_map_with_progress(self, new_image_path):
        """Загрузка карты с отображением прогресса"""

        def load_task():
            try:
                # Показываем прогресс-бар
                self.progress_frame.pack()
                self.progress_label.configure(text="Подготовка карты...")
                self.progress_bar.set(0.1)
                self.update_idletasks()

                # Отправляем карту в сеть
                success = self.send_map_to_network(new_image_path)

                if success:
                    # Обновляем локально - используем глобальную переменную
                    global image_path
                    image_path = new_image_path

                    self.after(200, self.update_map_image)

                    # Плавно скрываем прогресс-бар
                    self.progress_bar.set(1.0)
                    self.progress_label.configure(text="Карта загружена!")
                    self.after(1000, self.hide_progress)
                else:
                    self.progress_label.configure(text="Ошибка загрузки!")
                    self.after(2000, self.hide_progress)

            except Exception as e:
                logger.error(f"Ошибка загрузки карты: {e}")
                self.hide_progress()

        # Запускаем в отдельном потоке
        load_thread = Thread(target=load_task, daemon=True)
        load_thread.start()

    def hide_progress(self):
        """Скрытие прогресс-бара"""
        self.progress_frame.pack_forget()
        self.progress_bar.set(0)


# ==================== СЕТЕВАЯ ПАНЕЛЬ UI ====================
class NetworkFrame(customtkinter.CTkFrame):
    """Панель управления сетевым подключением"""

    def __init__(self, parent, network_manager, chat_frame):
        super().__init__(parent)
        self.network_manager = network_manager
        self.chat_frame = chat_frame
        self.setup_ui()

    def setup_ui(self):
        """Настройка интерфейса панели"""
        title_label = customtkinter.CTkLabel(self, text="Мультиплеер", font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 5))

        # Фрейм для ввода имени
        name_frame = customtkinter.CTkFrame(self)
        name_frame.pack(pady=5, padx=10, fill="x")

        name_label = customtkinter.CTkLabel(name_frame, text="Имя игрока:", font=("Arial", 12))
        name_label.pack(anchor="w", padx=5)

        self.name_entry = customtkinter.CTkEntry(
            name_frame,
            placeholder_text="Введите ваше имя",
            height=35,
            font=("Arial", 12)
        )
        self.name_entry.pack(fill="x", padx=5, pady=(0, 5))

        if self.network_manager.player_name:
            self.name_entry.insert(0, self.network_manager.player_name)

        self.update_name_btn = customtkinter.CTkButton(
            name_frame,
            text="✏️ Обновить имя",
            command=self.update_player_name,
            height=30,
            font=("Arial", 10)
        )
        self.update_name_btn.pack(fill="x", padx=5, pady=(0, 5))

        self.status_label = customtkinter.CTkLabel(self, text="❌ Отключено", text_color="red", font=("Arial", 12))
        self.status_label.pack(pady=5)

        btn_frame = customtkinter.CTkFrame(self)
        btn_frame.pack(pady=10, padx=10, fill="x")

        self.host_btn = customtkinter.CTkButton(
            btn_frame,
            text="🎮 Хост",
            command=self.start_host,
            width=120,
            height=35,
            font=("Arial", 12)
        )
        self.host_btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        self.connect_btn = customtkinter.CTkButton(
            btn_frame,
            text="🔌 Подключиться",
            command=self.connect_to_host,
            width=120,
            height=35,
            font=("Arial", 12)
        )
        self.connect_btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        server_frame = customtkinter.CTkFrame(self)
        server_frame.pack(pady=10, padx=10, fill="x")

        server_label = customtkinter.CTkLabel(server_frame, text="Адрес сервера:", font=("Arial", 12))
        server_label.pack(anchor="w", padx=5)

        self.host_entry = customtkinter.CTkEntry(
            server_frame,
            placeholder_text="localhost:8765",
            height=35,
            font=("Arial", 12)
        )
        self.host_entry.pack(fill="x", padx=5, pady=(0, 5))
        self.host_entry.insert(0, "localhost:8765")

        hint_label = customtkinter.CTkLabel(
            self,
            text="Для игры в локальной сети используйте IP-адрес хоста",
            font=("Arial", 10),
            text_color="gray",
            wraplength=250
        )
        hint_label.pack(pady=(5, 10))

    def update_player_name(self):
        """Обновление имени игрока"""
        new_name = self.name_entry.get().strip()
        if new_name:
            success = self.network_manager.update_player_name(new_name)
            if success:
                self.chat_frame.add_message("Система", f"Имя изменено на: {new_name}", True)
                messagebox.showinfo("Имя обновлено", f"Ваше имя изменено на: {new_name}")
            else:
                messagebox.showerror("Ошибка", "Имя не может быть пустым")
        else:
            messagebox.showwarning("Внимание", "Введите имя игрока")

    def start_host(self):
        """Запуск сервера"""
        global is_host
        try:
            is_host = True
            self.status_label.configure(text="🔄 Запуск сервера...", text_color="orange")

            self.host_btn.configure(state="disabled")
            self.connect_btn.configure(state="disabled")

            server_thread = Thread(target=start_server, daemon=True)
            server_thread.start()

            import time
            for i in range(5):
                time.sleep(1)
                self.status_label.configure(text=f"🔄 Запуск сервера... {i + 1}/5", text_color="orange")

            self.connect_to_host()

        except Exception as e:
            logger.error(f"Ошибка запуска сервера: {e}")
            self.status_label.configure(text="❌ Ошибка запуска", text_color="red")
            self.host_btn.configure(state="normal")
            self.connect_btn.configure(state="normal")

    def connect_to_host(self):
        """Подключение к серверу"""

        def connect_task():
            try:
                host_port = self.host_entry.get().split(":")
                host = host_port[0].strip()
                port = int(host_port[1]) if len(host_port) > 1 else 8765

                self.status_label.configure(text="🔄 Подключение...", text_color="orange")

                success = self.network_manager.connect(host, port)

                if success:
                    self.status_label.configure(text="✅ Подключено", text_color="green")
                    self.host_btn.configure(state="disabled")
                    self.connect_btn.configure(state="disabled")

                    self.chat_frame.add_message("Система", f"Вы подключились как: {self.network_manager.player_name}",
                                                True)
                else:
                    self.status_label.configure(text="❌ Ошибка подключения", text_color="red")
                    self.host_btn.configure(state="normal")
                    self.connect_btn.configure(state="normal")

            except Exception as e:
                logger.error(f"Ошибка в задаче подключения: {e}")
                self.status_label.configure(text="❌ Ошибка", text_color="red")
                self.host_btn.configure(state="normal")
                self.connect_btn.configure(state="normal")

        connect_thread = Thread(target=connect_task, daemon=True)
        connect_thread.start()


# ==================== ОКНО ЧАТА ====================
class ChatFrame(customtkinter.CTkFrame):
    """Фрейм чата для общения"""

    def __init__(self, parent, network_manager):
        super().__init__(parent)
        self.network_manager = network_manager
        self.setup_ui()

    def setup_ui(self):
        """Настройка интерфейса чата"""
        title_label = customtkinter.CTkLabel(self, text="💬 Чат", font=("Arial", 14, "bold"))
        title_label.pack(pady=(10, 5))

        self.chat_display = customtkinter.CTkTextbox(self, height=200)
        self.chat_display.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        self.chat_display.configure(state="disabled")

        # Настройка тегов только с цветами (без font)
        self.chat_display.tag_config("system", foreground="gray")
        self.chat_display.tag_config("roll", foreground="orange")
        self.chat_display.tag_config("map", foreground="blue")
        self.chat_display.tag_config("join", foreground="green")
        self.chat_display.tag_config("leave", foreground="red")
        self.chat_display.tag_config("normal", foreground="white")

        input_frame = customtkinter.CTkFrame(self)
        input_frame.pack(padx=10, pady=(0, 10), fill="x")

        self.chat_input = customtkinter.CTkEntry(
            input_frame,
            placeholder_text="Введите сообщение...",
            height=35
        )
        self.chat_input.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.chat_input.bind("<Return>", self.send_message)

        self.chat_send_btn = customtkinter.CTkButton(
            input_frame,
            text="➤",
            width=50,
            height=35,
            command=self.send_message
        )
        self.chat_send_btn.pack(side="right")

    def add_message(self, player, message, is_system=False, message_type="normal"):
        """Добавление сообщения в чат"""
        self.chat_display.configure(state="normal")

        tag = "normal"
        if is_system:
            tag = message_type

        if player == "Система":
            self.chat_display.insert("end", f"{message}\n", tag)
        else:
            self.chat_display.insert("end", f"{player}: {message}\n", tag)

        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def send_message(self, event=None):
        """Отправка сообщения"""
        message = self.chat_input.get().strip()
        if message:
            if self.network_manager and self.network_manager.connected:
                self.network_manager.send_sync({
                    'type': 'chat_message',
                    'data': {
                        'player': self.network_manager.player_name,
                        'message': message
                    }
                })

            self.chat_input.delete(0, "end")


# ==================== ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ ====================
class BridgeOfTalesApp(customtkinter.CTk):
    """Главное окно приложения Bridge of Tales"""

    def __init__(self):
        super().__init__()

        # Настройка главного окна
        self.title("Bridge of Tales beta 1.0.2")
        self.geometry("1600x900")
        self.minsize(1200, 700)

        # Загружаем настройки
        self.load_settings()

        # Инициализируем переменные
        self.player_name = None
        self.network_manager = None

        # Настройка интерфейса
        self.setup_ui()

        # Запрашиваем имя игрока с небольшой задержкой
        self.after(100, self.get_player_name)

        # Обновление подсказок
        self.after(200, self.update_tips)

    def load_settings(self):
        """Загрузка настроек из файла"""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        settings_path = os.path.join(base_path, 'settings.json')

        try:
            with open(settings_path, 'r') as f:
                all_settings = json.load(f)
            fullscreen = all_settings.get("fullscreen", False)
            if fullscreen:
                self.attributes('-fullscreen', True)
        except Exception as e:
            logger.error(f"Ошибка загрузки настроек: {e}")

    def get_player_name(self):
        """Запрос имени игрока"""
        # Простой диалог для ввода имени
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Имя игрока")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Центрируем окно
        dialog.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f'400x200+{x}+{y}')

        # Виджеты
        label = customtkinter.CTkLabel(dialog, text="Введите ваше имя:", font=("Arial", 16))
        label.pack(pady=20)

        name_entry = customtkinter.CTkEntry(dialog, width=300, height=40, font=("Arial", 14))
        name_entry.pack(pady=10)
        name_entry.focus_set()

        result = [None]  # Используем список для передачи значения

        def on_ok():
            name = name_entry.get().strip()
            if name:
                result[0] = name
            dialog.destroy()

        def on_cancel():
            result[0] = f"Игрок_{client_id[:4]}"
            dialog.destroy()

        # Кнопки
        btn_frame = customtkinter.CTkFrame(dialog)
        btn_frame.pack(pady=20)

        ok_btn = customtkinter.CTkButton(btn_frame, text="OK", command=on_ok, width=100, height=35)
        ok_btn.pack(side="left", padx=10)

        cancel_btn = customtkinter.CTkButton(btn_frame, text="Отмена", command=on_cancel, width=100, height=35)
        cancel_btn.pack(side="right", padx=10)

        # Обработка Enter
        def on_enter(event):
            on_ok()

        name_entry.bind("<Return>", on_enter)

        # Ждем закрытия окна
        self.wait_window(dialog)

        # Устанавливаем имя
        self.player_name = result[0] if result[0] else f"Игрок_{client_id[:4]}"

        # Обновляем интерфейс
        self.update_ui_with_player_name()

    def update_ui_with_player_name(self):
        """Обновление интерфейса после получения имени игрока"""
        # Обновляем заголовок окна
        self.title(f"Bridge of Tales Online")

        # Обновляем заголовок в центре
        if hasattr(self, 'center_title'):
            self.center_title.configure(text=f"🎭 Bridge of Tales")

        # Создаем сетевой менеджер
        self.network_manager = NetworkManager(self.player_name)

        # Обновляем игровое поле с сетевым менеджером
        if hasattr(self, 'game_board'):
            self.game_board.network_manager = self.network_manager
            self.network_manager.game_board_ref = self.game_board
            self.network_manager.token_callback = self.game_board.handle_network_token
            self.network_manager.map_callback = self.game_board.handle_network_map

        # Обновляем отображение имени в левой панели
        if hasattr(self, 'player_name_label'):
            self.player_name_label.configure(text=f"👤 {self.player_name}")

        # Настраиваем правую панель
        self.setup_right_panel()

        # Настраиваем callback для сетевого менеджера
        self.network_manager.chat_callback = self.handle_chat_message

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Левая панель (инструменты)
        self.left_panel = customtkinter.CTkFrame(self, width=300)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.left_panel.grid_propagate(False)

        # Центральная панель (игровое поле)
        self.center_panel = customtkinter.CTkFrame(self)
        self.center_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Правая панель будет создана позже
        self.right_panel = None

        # Настройка панелей
        self.setup_left_panel()
        self.setup_center_panel()

    def setup_left_panel(self):
        """Настройка левой панели (инструменты)"""
        title_label = customtkinter.CTkLabel(
            self.left_panel,
            text="🎲 Инструменты",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(15, 10))

        # Отображение имени игрока
        self.player_name_label = customtkinter.CTkLabel(
            self.left_panel,
            text="👤 Загрузка...",
            font=("Arial", 12),
            text_color="lightblue"
        )
        self.player_name_label.pack(pady=(0, 10))

        dice_frame = customtkinter.CTkFrame(self.left_panel)
        dice_frame.pack(pady=10, padx=10, fill="x")

        dice_label = customtkinter.CTkLabel(dice_frame, text="Бросок кубика:", font=("Arial", 14))
        dice_label.pack(anchor="w", padx=5, pady=(5, 0))

        dice_inner_frame = customtkinter.CTkFrame(dice_frame)
        dice_inner_frame.pack(pady=5, padx=5, fill="x")

        self.variable_dice = customtkinter.CTkComboBox(
            dice_inner_frame,
            values=["4", "6", "8", "10", "12", "20", "100"],
            width=80,
            height=35
        )
        self.variable_dice.pack(side="left", padx=(0, 5))
        self.variable_dice.set("20")

        btn_trow = customtkinter.CTkButton(
            dice_inner_frame,
            text="🎲 Бросить",
            command=self.roll_dice,
            height=35
        )
        btn_trow.pack(side="left", padx=(0, 5))

        self.roll_result = customtkinter.CTkLabel(
            dice_inner_frame,
            text="= ?",
            font=("Arial", 16, "bold"),
            width=50
        )
        self.roll_result.pack(side="left")

        notes_label = customtkinter.CTkLabel(self.left_panel, text="📝 Заметки:", font=("Arial", 14))
        notes_label.pack(anchor="w", padx=15, pady=(15, 0))

        self.text_notes = customtkinter.CTkTextbox(self.left_panel, height=300)
        self.text_notes.pack(pady=10, padx=10, fill="both", expand=True)
        self.text_notes.bind("<Control-BackSpace>", self.clear_text)

        buttons_frame = customtkinter.CTkFrame(self.left_panel)
        buttons_frame.pack(pady=10, padx=10, fill="x")

        self.btn_load_map = customtkinter.CTkButton(
            buttons_frame,
            text="🗺️ Загрузить карту",
            command=self.load_map,
            height=35
        )
        self.btn_load_map.pack(pady=5, fill="x")

        self.btn_character = customtkinter.CTkButton(
            buttons_frame,
            text="👤 Персонаж",
            command=self.open_character_sheet,
            height=35
        )
        self.btn_character.pack(pady=5, fill="x")

        self.btn_settings = customtkinter.CTkButton(
            buttons_frame,
            text="⚙️ Настройки",
            command=self.open_settings,
            height=35
        )
        self.btn_settings.pack(pady=5, fill="x")

        self.btn_browser = customtkinter.CTkButton(
            buttons_frame,
            text="🌐 DND.su",
            command=self.open_browser,
            height=35
        )
        self.btn_browser.pack(pady=5, fill="x")

        self.btn_quit = customtkinter.CTkButton(
            buttons_frame,
            text="🚪 Выход",
            command=self.quit_app,
            height=35,
            fg_color="#d9534f",
            hover_color="#c9302c"
        )
        self.btn_quit.pack(pady=5, fill="x")

    def setup_center_panel(self):
        """Настройка центральной панели (игровое поле)"""
        self.center_title = customtkinter.CTkLabel(
            self.center_panel,
            text="🎭 Bridge of Tales",
            font=("Arial", 24, "bold")
        )
        self.center_title.pack(pady=(10, 5))

        self.tip_label = customtkinter.CTkLabel(
            self.center_panel,
            text=give_txt(),
            font=("Arial", 12),
            text_color="gray",
            wraplength=800
        )
        self.tip_label.pack(pady=(0, 10))

        # Создаем игровое поле БЕЗ network_manager (он еще не создан)
        self.game_board = AdvancedGameBoard(self.center_panel)
        self.game_board.pack(padx=10, pady=10, fill="both", expand=True)

        control_frame = customtkinter.CTkFrame(self.center_panel)
        control_frame.pack(pady=(0, 10), padx=10, fill="x")

        self.btn_clear_board = customtkinter.CTkButton(
            control_frame,
            text="🧹 Очистить поле",
            command=self.clear_game_board,
            width=120
        )
        self.btn_clear_board.pack(side="left", padx=5)

        self.btn_clear_map = customtkinter.CTkButton(
            control_frame,
            text="🗑️ Очистить карту",
            command=self.clear_map,
            width=120,
            fg_color="#f0ad4e",
            hover_color="#ec971f"
        )
        self.btn_clear_map.pack(side="left", padx=5)

    def setup_right_panel(self):
        """Настройка правой панели (сеть и чат)"""
        # Удаляем старую правую панель если есть
        if self.right_panel:
            self.right_panel.destroy()

        # Создаем новую правую панель
        self.right_panel = customtkinter.CTkFrame(self, width=350)
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.right_panel.grid_propagate(False)

        # Сначала создаем чат
        self.chat_frame = ChatFrame(self.right_panel, self.network_manager)
        self.chat_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Затем создаем сетевую панель с ссылкой на чат
        self.network_frame = NetworkFrame(self.right_panel, self.network_manager, self.chat_frame)
        self.network_frame.pack(pady=(15, 10), padx=10, fill="x")

    def handle_chat_message(self, message_data):
        """Обработка входящих сообщений чата"""
        player = message_data.get('player', '')
        message = message_data.get('message', '')
        is_system = message_data.get('is_system', False)

        message_type = "normal"

        if is_system:
            if player == '🎲':
                message_type = "roll"
            elif player == '🗺️':
                message_type = "map"
            elif player == '🟢':
                message_type = "join"
            elif player == '🔴':
                message_type = "leave"
            else:
                message_type = "system"

        self.chat_frame.add_message(player, message, is_system, message_type)

    def roll_dice(self):
        """Бросок кубика"""
        dice_type = self.variable_dice.get()
        result = roll(dice_type)

        self.roll_result.configure(text=f"= {result}")

        if self.network_manager and self.network_manager.connected:
            self.network_manager.send_sync({
                'type': 'roll_dice',
                'data': {
                    'player': self.network_manager.player_name,
                    'dice': dice_type,
                    'result': result
                }
            })

    def clear_text(self, event=None):
        """Очистка текстового поля"""
        text = self.text_notes.get("1.0", "end-1c")
        words = text.split(" ")
        if words:
            words.pop()
        self.text_notes.delete("1.0", "end")
        self.text_notes.insert("1.0", " ".join(words))
        return "break"

    def load_map(self):
        """Загрузка карты"""
        global image_path
        new_image_path = filedialog.askopenfilename(
            title="Выберите карту",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("Все файлы", "*.*")
            ]
        )

        if new_image_path:
            # Проверяем размер файла
            filesize = os.path.getsize(new_image_path)
            max_size_mb = 50  # Максимальный размер 50MB

            if filesize > max_size_mb * 1024 * 1024:
                if not messagebox.askyesno(
                        "Большой файл",
                        f"Файл очень большой ({filesize / (1024 * 1024):.1f} MB).\n"
                        f"Загрузка может занять некоторое время.\n"
                        "Продолжить?"
                ):
                    return

            # Загружаем с прогрессом - передаем путь как параметр
            self.game_board.load_map_with_progress(new_image_path)

    def clear_map(self):
        """Очистка карты"""
        self.game_board.clear_map()

        if self.network_manager and self.network_manager.connected:
            self.network_manager.send_sync({
                'type': 'map_update',
                'data': {
                    'action': 'clear',
                    'player': self.network_manager.player_name
                }
            })

            self.chat_frame.add_message(
                "🗺️",
                "Карта очищена",
                True,
                "map"
            )

    def open_character_sheet(self):
        """Открытие листа персонажа"""
        thread = threading.Thread(target=Add, daemon=True)
        thread.start()

    def open_settings(self):
        """Открытие настроек"""
        settings_main()

    def open_browser(self):
        """Открытие браузера DND.su"""
        webview.create_window('DND.su', 'https://dnd.su/', width=1024, height=768)
        webview.start()

    def clear_game_board(self):
        """Очистка игрового поля"""
        self.game_board.clear_board()
        self.chat_frame.add_message("Система", "Игровое поле очищено", True)

    def update_tips(self):
        """Обновление подсказок"""
        self.tip_label.configure(text=give_txt())
        self.after(10000, self.update_tips)

    def quit_app(self):
        """Выход из приложения"""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.destroy()


# ==================== ТОЧКА ВХОДА ====================
if __name__ == '__main__':
    if not os.path.exists("Base/Spells"):
        os.makedirs("Base/Spells", exist_ok=True)

    if not os.path.exists("settings.json"):
        with open("settings.json", "w", encoding='utf-8') as f:
            json.dump({"fullscreen": False}, f, indent=4, ensure_ascii=False)

    try:
        import websockets
    except ImportError:
        print("❌ Ошибка: библиотека websockets не установлена!")
        sys.exit(1)

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    app = BridgeOfTalesApp()
    app.mainloop()