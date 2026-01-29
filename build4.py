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




def roll(text):


    text_str = str(text)
    if text_str == "4":
        return roll4()
    elif text_str == "6":
        return roll6()
    elif text_str == "8":
        return roll8()
    elif text_str == "10":
        return roll10()
    elif text_str == "12":
        return roll12()
    elif text_str == "20":
        return roll20()
    elif text_str == "100":
        return roll100()
    else:
        return roll20()


def roll4():

    return random.randint(1, 4)


def roll6():

    return random.randint(1, 6)


def roll8():

    return random.randint(1, 8)

def roll10():

    return random.randint(1, 10)


def roll12():

    return random.randint(1, 12)


def roll20():

    return random.randint(1, 20)


def roll100():

    return random.randint(1, 100)




def give_txt():

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
        'Даже злодеи имеют мотивацию',
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
        'Настоящая магия - в воображении',
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

    if text == '' or text is None:
        return ''


    try:
        score = int(text)
    except ValueError:
        return 'ERROR'


    if score == 1:
        return -5
    elif score >= 2 and score <= 3:
        return -4
    elif score >= 4 and score <= 5:
        return -3
    elif score >= 6 and score <= 7:
        return -2
    elif score >= 8 and score <= 9:
        return -1
    elif score >= 10 and score <= 11:
        return 0
    elif score >= 12 and score <= 13:
        return 1
    elif score >= 14 and score <= 15:
        return 2
    elif score >= 16 and score <= 17:
        return 3
    elif score >= 18 and score <= 19:
        return 4
    elif score >= 20 and score <= 21:
        return 5
    elif score >= 22 and score <= 23:
        return 6
    elif score >= 24 and score <= 25:
        return 7
    elif score >= 26 and score <= 27:
        return 8
    elif score >= 28 and score <= 29:
        return 9
    elif score == 30:
        return 10
    else:
        return 'ERROR'




def search(spell_name):

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
        spell_text = f"Spell file '{spell_name}.txt' not found!\n\nCheck folder: Base/Spells/"
    except Exception as error:
        spell_text = f"Error reading spell file: {str(error)}"


    text_field = customtkinter.CTkTextbox(search_window, width=800, height=400)
    text_field.pack(expand=True, fill="both", padx=10, pady=10)
    text_field.insert('0.0', spell_text)
    text_field.configure(state='disabled', wrap='word')


    close_button = customtkinter.CTkButton(search_window, text="Close", command=search_window.destroy)
    close_button.pack(pady=10)

    search_window.mainloop()




def settings_main():

    settings_window = customtkinter.CTk()
    settings_window.title('Настройки')
    settings_window.geometry('500x500')
    customtkinter.set_appearance_mode("dark")


    fullscreen_var = customtkinter.BooleanVar(value=False)


    fullscreen_checkbox = customtkinter.CTkCheckBox(
        settings_window,
        text='Полноэкранный режим(рекомендуется)',
        variable=fullscreen_var
    )
    fullscreen_checkbox.pack(side='left', anchor='nw', padx=20, pady=20)


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

    def save_settings():

        if fullscreen_checkbox.get() == 1:
            fullscreen = True
        else:
            fullscreen = False

        save_data = {"fullscreen": fullscreen}

        try:
            with open(settings_path, 'w', encoding='utf-8') as file:
                json.dump(save_data, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("Saved", "Settings successfully saved!")
        except Exception as error:
            messagebox.showerror("Error", f"Failed to save settings: {str(error)}")


    save_button = customtkinter.CTkButton(
        settings_window,
        text='Применить',
        command=save_settings
    )
    save_button.pack(side='bottom', anchor='se', padx=20, pady=20)

    settings_window.mainloop()




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





customtkinter.set_appearance_mode("dark")
image_path = None


def open_browser():
    webview.create_window('DND.su', 'https://dnd.su/', width=1024, height=768)
    webview.start()


class AdvancedGameBoard(customtkinter.CTkFrame):


    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        import tkinter as tk
        from tkinter import colorchooser

        self.canvas = tk.Canvas(self, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.grid_size = 50
        self.grid_color = "#333333"
        self.grid_width = 1

        self.original_image = None
        self.map_image = None
        self.canvas_map_id = None
        self.map_position = None
        self.map_dimensions = None
        self.load_map_image()

        self.token_colors = ["#ff4444", "#44ff44", "#4444ff", "#ffff44",
                             "#ff44ff", "#44ffff", "#ff8844", "#8844ff"]
        self.current_color_index = 0
        self.selected_color = self.token_colors[0]

        self.create_color_palette()

        self.tokens = {}
        self.current_token_id = 0

        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind("<Button-1>", self.place_token)
        self.canvas.bind("<Button-3>", self.remove_token)
        self.canvas.bind("<Button-2>", self.change_token_color)

    def create_color_palette(self):
        self.palette_frame = customtkinter.CTkFrame(self, height=50)
        self.palette_frame.place(relx=0.5, rely=0.02, anchor="n")

        self.color_buttons = []

        self.color_preview = customtkinter.CTkLabel(
            self.palette_frame,
            text="Цвет:",
            font=("Arial", 12)
        )
        self.color_preview.pack(side="left", padx=(10, 5))

        self.color_display = customtkinter.CTkLabel(
            self.palette_frame,
            text="     ",
            fg_color=self.selected_color,
            width=30,
            height=30,
            corner_radius=15
        )
        self.color_display.pack(side="left", padx=5)

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
        custom_btn.pack(side="left", padx=(10, 5))

        prev_btn = customtkinter.CTkButton(
            self.palette_frame,
            text="←",
            width=30,
            height=30,
            command=self.previous_color,
            font=("Arial", 14)
        )
        prev_btn.pack(side="left", padx=(10, 0))

        next_btn = customtkinter.CTkButton(
            self.palette_frame,
            text="→",
            width=30,
            height=30,
            command=self.next_color,
            font=("Arial", 14)
        )
        next_btn.pack(side="left", padx=(0, 10))

        self.color_info = customtkinter.CTkLabel(
            self.palette_frame,
            text=f"Цвет {self.current_color_index + 1}/{len(self.token_colors)}",
            font=("Arial", 10)
        )
        self.color_info.pack(side="left", padx=10)

    def add_color_button(self, color):
        color_btn = customtkinter.CTkButton(
            self.palette_frame,
            text="",
            width=25,
            height=25,
            fg_color=color,
            hover_color=color,
            command=lambda c=color: self.select_color(c)
        )
        color_btn.pack(side="left", padx=2)
        self.color_buttons.append(color_btn)

    def select_color(self, color):
        self.selected_color = color
        self.current_color_index = self.token_colors.index(color)
        self.update_color_display()

    def choose_custom_color(self):
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
                        break

    def update_color_display(self):
        self.color_display.configure(fg_color=self.selected_color)
        self.color_info.configure(
            text=f"Цвет {self.current_color_index + 1}/{len(self.token_colors)}"
        )

    def next_color(self):
        self.current_color_index = (self.current_color_index + 1) % len(self.token_colors)
        self.selected_color = self.token_colors[self.current_color_index]
        self.update_color_display()

    def previous_color(self):
        self.current_color_index = (self.current_color_index - 1) % len(self.token_colors)
        self.selected_color = self.token_colors[self.current_color_index]
        self.update_color_display()

    def load_map_image(self):
        global image_path
        try:
            if image_path and os.path.exists(image_path):
                self.original_image = Image.open(image_path)
                self.after(100, self.resize_image)
            else:
                print("Map file not selected or not found")
                self.draw_grid()
        except Exception as e:
            print(f"Failed to load map: {e}")
            self.draw_grid()

    def on_canvas_configure(self, event=None):
        if self.original_image:
            self.resize_image()
        else:
            self.draw_grid()

    def resize_image(self):
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

    def place_token(self, event):
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
                    "color": self.selected_color
                }
                self.current_token_id += 1

                self.canvas.tag_bind(token, "<Button1-Motion>", lambda e, t=token: self.move_token(e, t))

    def move_token(self, event, token):
        if self.map_position:
            map_x, map_y = self.map_position
            map_width, map_height = self.map_dimensions

            if (map_x <= event.x <= map_x + map_width and
                    map_y <= event.y <= map_y + map_height):

                grid_x = int((event.x - map_x) / self.grid_size)
                grid_y = int((event.y - map_y) / self.grid_size)

                snapped_x = map_x + (grid_x * self.grid_size) + (self.grid_size // 2)
                snapped_y = map_y + (grid_y * self.grid_size) + (self.grid_size // 2)

                use_snapping = False

                if use_snapping:
                    final_x, final_y = snapped_x, snapped_y
                else:
                    final_x, final_y = event.x, event.y

                self.canvas.coords(token,
                                   final_x - 15, final_y - 15,
                                   final_x + 15, final_y + 15)

                for token_id, token_info in self.tokens.items():
                    if token_info["id"] == token:
                        self.tokens[token_id]["x"] = final_x
                        self.tokens[token_id]["y"] = final_y
                        self.tokens[token_id]["grid_x"] = grid_x
                        self.tokens[token_id]["grid_y"] = grid_y
                        break

    def remove_token(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item and "token" in self.canvas.gettags(item[0]):
            self.canvas.delete(item[0])
            for token_id, token_info in list(self.tokens.items()):
                if token_info["id"] == item[0]:
                    del self.tokens[token_id]
                    break

    def update_map_image(self):
        self.load_map_image()



class Prototype(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title("Bridge of Tales build 4")
        self.geometry("1400x800")

        self.after(100, self.update_setting)

        self.panel_frame = customtkinter.CTkFrame(self, width=300)
        self.panel_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.panel_info_frame = customtkinter.CTkFrame(self, width=300)
        self.panel_info_frame.pack(side="right", fill="y", padx=10, pady=10)

        self.central_frame = customtkinter.CTkFrame(self)
        self.central_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.content_for_dice()
        self.Text_for_texting()
        self.Right_panel()
        self.setup_game_board()

    def update_setting(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        settings_path = os.path.join(base_path, 'settings.json')

        try:
            with open(settings_path, 'r') as f:
                all_settings = json.load(f)
            size = all_settings.get("fullscreen", False)
            self.attributes('-fullscreen', size)
        except:
            pass

        self.after(1000, self.update_setting)

    def setup_game_board(self):
        title_label = customtkinter.CTkLabel(self.central_frame, text="Bridge of Tales", font=("Arial", 18))
        title_label.pack(pady=5)

        self.game_board = AdvancedGameBoard(self.central_frame)
        self.game_board.pack(fill="both", expand=True, padx=10, pady=10)

        self.setup_board_controls()

    def setup_board_controls(self):
        control_frame = customtkinter.CTkFrame(self.central_frame)
        control_frame.pack(fill="x", padx=10, pady=5)

        clear_btn = customtkinter.CTkButton(
            control_frame, text="Очистить", command=self.clear_board, width=120)
        clear_btn.pack(side="left", padx=5)

        self.info_label = customtkinter.CTkLabel(
            control_frame, text=give_txt(),
            font=("Arial", 12), text_color="gray")
        self.info_label.pack(side="left", padx=20)

        self.after(5000, self.update_info_label)

    def update_info_label(self):
        if hasattr(self, 'info_label'):
            self.info_label.configure(text=give_txt())
        self.after(5000, self.update_info_label)

    def clear_board(self):
        for token_info in self.game_board.tokens.values():
            self.game_board.canvas.delete(token_info["id"])
        self.game_board.tokens.clear()
        self.game_board.current_token_id = 0

    def content_for_dice(self):
        self.dice_frame = customtkinter.CTkFrame(self.panel_frame, width=150)
        self.dice_frame.pack(padx=10, pady=10)

        btn_trow = customtkinter.CTkButton(self.dice_frame, command=self.trow, text="Бросить")
        btn_trow.pack(padx=10, pady=10, side="left")

        self.variable_dice = customtkinter.CTkComboBox(self.dice_frame, values=["4", "6", "8", '10', "12", "20", "100"])
        self.variable_dice.pack(side="left")
        self.variable_dice.set("20")

        self.RollResult = customtkinter.CTkLabel(self.dice_frame, text='= ', width=30)
        self.RollResult.pack(side="right", padx=10)

    def Right_panel(self):
        self.btn_web = customtkinter.CTkButton(self.panel_info_frame, command=self.browser, text="OpenDND4")
        self.btn_web.pack(padx=10, pady=10, side="top")

        self.Characters_Frame = customtkinter.CTkFrame(self.panel_info_frame, width=150)
        self.Characters_Frame.pack(padx=10, pady=10)

        Add_btn = customtkinter.CTkButton(self.Characters_Frame, text="Персонаж", command=self.add_character)
        Add_btn.pack(padx=10, pady=10, side="left")

        Quitbtn = customtkinter.CTkButton(self.panel_info_frame, command=self.quit, text='Выход')
        Quitbtn.pack(padx=10, pady=10, side="bottom")

    def add_character(self):
        thread = threading.Thread(target=Add, daemon=True)
        thread.start()

    def browser(self):
        thread = threading.Thread(target=open_browser(), daemon=True)
        thread.start()


    def Text_for_texting(self):
        self.TextTable = customtkinter.CTkTextbox(self.panel_frame, width=300, height=600)
        self.TextTable.pack(padx=10, pady=10)
        self.TextTable.bind("<Control-BackSpace>", self.clear_text)

        self.btn_Search_Img = customtkinter.CTkButton(self.panel_frame, command=self.add_img, text='Загрузить карту')
        self.btn_Search_Img.pack(padx=10, pady=10, side="bottom")

        self.Button_Set = customtkinter.CTkButton(self.panel_frame, command=self.setting, text='Настройки')
        self.Button_Set.pack(padx=10, pady=10, side="bottom")

    def setting(self):
        settings_main()

    def add_img(self):
        global image_path
        new_image_path = filedialog.askopenfilename(
            title="Select Map",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )

        if new_image_path:
            image_path = new_image_path
            self.game_board.update_map_image()

    def clear_text(self, event=None):
        All_inn = self.TextTable.get("1.0", "end-1c")
        All_out = All_inn.split(" ")
        All_out.reverse()
        if All_out:
            All_out.pop(0)
        All_out.reverse()
        self.TextTable.delete("1.0", "end")
        self.TextTable.insert("1.0", " ".join(All_out))
        return "break"

    def trow(self):
        g = self.variable_dice.get()
        G = roll(g)
        self.RollResult.configure(text=f'= {G}')




if __name__ == '__main__':
    if not os.path.exists("../Job_With_Test/Base/Spells"):
        os.makedirs("../Job_With_Test/Base/Spells", exist_ok=True)



    if not os.path.exists("../Job_With_Test/settings.json"):
        with open("../Job_With_Test/settings.json", "w") as f:
            json.dump({"fullscreen": False}, f)



    win = Prototype()
    win.mainloop()