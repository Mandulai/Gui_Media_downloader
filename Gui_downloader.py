# Графический интерфейс для загрузчика медиа файлов
# Версия: 1.0.1
# Дата: 2022-06-16
# Автор: --- неизвестен ---


from cgitb import text
from tkinter import * # Импортировать библиотеку tkinter
import tkinter as tk
import tkinter.ttk as ttk
import win32clipboard as clipboards 
import pafy
import os, sys, getpass


def get_text(dannie):# Функция ввода данных в текстовое поле
    tex = str(dannie)+'\n'
    vivod.insert(tk.END, tex)
    vivod.see(tk.END)


def clicked_btn_get(): # Функция при нажатии на кнопку 'Готово
    url_adress = url.get() # Получить данные из поля ввода
    if url_adress: # Если данные есть
        url_adress = url.get() # Получить данные из поля ввода
    else: # Если данных нет
        url.insert(0,'--Вы не ввели ссылку!--')  # Вставить в поле ввода сообщение 
        get_text('\n--Вы не ввели ссылку!--')
    if url_adress == '' or url_adress == '--Вы не ввели ссылку!--': # Если данные нет
        get_text('Нет URL!!!\n')
    else:
        get_text ('\nЕсть URL... '+url_adress)
        get_text ('Проверяем адрес..')
        if url_adress.find('youtube') == -1:
            get_text ('Не верный URL!\n')
        else:
            get_text ('Адрес корректный!...\n')
            get_text('Что качаем?..Видео...Аудио(по умолчанию)..\n')

        

def insert_btn_get():# Функция при нажатии на кнопку 'Вставить'
    url.delete(0, tk.END) # Очистить поле ввода
    clipboards.OpenClipboard() # Открыть буфер обмена
    url.insert(0, clipboards.GetClipboardData()) # Вставить в поле ввода данные из буфера обмена
    clipboards.CloseClipboard() # Закрыть буфер обмена    
    
    url_adress = url.get() # Получить данные из поля ввода
    if url_adress: # Если данные есть
        url_adress = url.get() # Получить данные из поля ввода
    else: # Если данных нет
        url.insert(0,'--Вы не ввели ссылку!--')  # Вставить в поле ввода сообщение 
        get_text('\n--Вы не ввели ссылку!--')
    if url_adress == '' or url_adress == '--Вы не ввели ссылку!--': # Если данные нет
        get_text('Нет URL!!!\n')
    else:
        get_text ('\nЕсть URL... '+url_adress)
        get_text ('Проверяем адрес..')
        if url_adress.find('youtube') == -1:
            get_text ('Не верный URL!\n')
        else:
            get_text ('Адрес корректный!...\n')
            get_text('Что качаем?..Видео...Аудио(по умолчанию)..\n')


def insert_btn_path():# Функция при нажатии на кнопку 'Изменить путь'
    path_default = path_window.get() # Получить данные из поля ввода
    get_text('Путь сохранения: '+ path_default)



def select_media():# Функция - открывает окно выбора типа медиа файла'
    path_window.delete(0, tk.END) # Очистить поле ввода
    if media_var.get() == 1:
        get_text('выбрано "Аудио"..')
        path_default = f'C:\\Users\\{user_name}\\Music\\YouTube'
        path_window.insert(0, path_default)
        get_text('Путь сохранения: '+ path_default+ '\n')
    elif media_var.get() == 0:
        get_text('выбрано "Видео"..')
        path_default = f'C:\\Users\\{user_name}\\Video\\YouTube'
        path_window.insert(0, path_default)
        get_text('Путь сохранения: '+ path_default+ '\n')


def window_vibor_potoka(streams, name_potoka):# Функция - открывает окно выбора потока 
    
    def select_potok(): # функция при выборе потока
        f = streams[int(potok_check.get())-1]
        get_text('\nВыбран поток: '+ str(f)+'\n')


    get_text('--------------------')
    get_text('Имя трека: '+ name_potoka)
    get_text('--------------------')
    get_text('Введите номер: ')

    vibor_potoka = tk.Toplevel(win)
    vibor_potoka.title(name_potoka)
    vibor_potoka.geometry()
    vibor_potoka.configure(background='#2C3A55')
    Label(vibor_potoka, text="Выберите поток...", font='Verdana 12', bg='#2C3A55', fg='white')\
        .grid(row=0, column=0, padx=5, pady=10, sticky=W)

    counter = 1
    row = 1
    potok_check = IntVar()
    potok_check.set(4)

    for vibor in streams: # Создаем радиокнопки для выбора потока
        bitrate = vibor.bitrate.split('.')
        size = round(vibor.get_filesize() / 1000000, 2) 
        get_text(f'{counter}: {vibor.mediatype}: {vibor.extension}: {size} Mb: {bitrate[0]} kbps ')
        text_btn_potoka = (f'{counter}: {vibor.mediatype}: {vibor.extension}: {size} Mb: {bitrate[0]} kbps ')
        radBtn_vibor_potoka = Radiobutton(vibor_potoka, value=counter, variable=potok_check, text=text_btn_potoka,\
            command= select_potok, bg='#2C3A55', fg='Black')
        radBtn_vibor_potoka.grid(row=row, sticky=W, padx=5, pady=4)
        row += 1
        counter += 1
    
    streams_index = None
    def result_and_exit(): 
        nonlocal streams_index
        streams_index = potok_check.get()
        vibor_potoka.destroy()
        download (streams, path_window.get(), streams_index,media_var.get())
        return

    btn_Vibor_potoka = Button(vibor_potoka, text='Скачать', command=lambda: result_and_exit(), bg='#2C3A55', fg='white')
    btn_Vibor_potoka.grid(row=row, column=0, padx=5, pady=10)
    
    vibor_potoka.wait_window # Ожидание закрытия окна выбора потока
    vibor_potoka.mainloop()
   

def load_streams(vibor_media_type,url_adress, path_save): # Функция при нажатии на кнопку 'Выбрать поток'
    global v
    v = pafy.new(url_adress) # Создаем обьект PAFY
    # выбираем поток в зависимости от выбора пользователя
    if int(vibor_media_type) == 0: 
        streams = v.streams
    elif int(vibor_media_type) == 1:
        streams = v.audiostreams
    else:
        get_text('Хрень какая то...')
        sys.exit() # В случае отсутствия выбора закрываем программу

    window_vibor_potoka(streams, v.title) # Открываем окно выбора потока
    # print("Exxyyyy")

def download(streams, path_save, streams_index,vibor_media_type): # Функция закачки потока
    try:
        def zagruzka_progress(total, recvd, ratio, rate, eta): # Функция прогресса загрузки
            progress_bar['value'] = round(ratio*100) # Выводим процент загрузки
            win.update()

        # Создаем список с вариантами потоков  
        variants = {} 
        streams
        counter = 1     
        for vibor in streams:
            variants[counter] = vibor
            counter += 1
        get_text('Качаем поток...'+str(streams_index))
 
        # Проверяем качали ли мы уже этот файл
        media_ext = str(variants[streams_index]) # Берем выбранный поток
        media_extension = media_ext.split('@')[0].split(':')[1] # Выдираем расширение
        file_name = str(v.title) # Узнаем имя трека
        file_name = file_name.replace("/", "_") # Заменяем спец символы
        media_files = f'{file_name}.{media_extension}' # получем имя файла + расширение
        path_file = f'{path_save}\{media_files}' # получаем путь + имя файла + расширение
        audio_path_save =f'{path_save}\{file_name}.mp3' # получаем тоже самое для сохраненного аудио файла
                
        if os.path.exists(path_file) or os.path.exists(audio_path_save) == True: # Проверяем есть ли уже файл в папке
            get_text('Отбой!..Мы качали уже этот файл...')
        else: # Качаем файл
            # progress_label.grid(row=3, column=0, padx=4) # Пишем надпись прогресса
            # progress_bar.grid(row=3, column=1, columnspan=1, sticky='W') # Открываем прогресс бар
            media_file_output = streams[streams_index - 1].download(filepath=f'{path_save}'\
                , quiet=True, callback=zagruzka_progress)

            # Переименовываем аудиодорожку в MP3
            if int(vibor_media_type) == 1: 
                audio_extension = str(variants[streams_index])
                audio_extension = audio_extension.split('@')[0].split(':')[1]
                file_name = str(v.title) # Узнаем имя трека
                file_name = file_name.replace("/", "_") # Заменяем спец символы
                music_file = f'{file_name}.{audio_extension}'
                base = os.path.splitext(music_file)[0]
                os.chdir(path=path_save)
                os.rename(music_file, base + ".mp3")
            get_text('Скачивание успешно завершено! \n')
            progress_bar['value'] = 0
            # progress_label.grid_remove()
            # progress_bar.grid_remove()
            win.update()

    except FileExistsError: # В случае если файл уже существует
        get_text('Ооопс....Мы качали уже этот файл!')
        path_del = (f"{path_save}\{music_file}")
        get_text(f"Удаляю заготовку...{music_file}")
        os.remove(path=path_del)
    
    except Exception as err: # В случае ошибки
        get_text("Ооопс....Проверьте данные!!!")
        get_text('Ошибка....'+ str(err))
        
       

# =========== ТЕЛО ПРОГРАММЫ ================
user_name = getpass.getuser() # Получить имя пользователя
path_default = (f'C:\\Users\\{user_name}\\Music\\YouTube')
vibor_media_type = 0
url_adress =  ' '

win = tk.Tk()
win.title('Кому-то нужны наркотики, кому-то алкоголь. А мне и музыки хватает. (Курт Кобейн)')
win.geometry("600x450")
win.resizable(width=False, height=False)
win.configure(bg='#2C3A55')

#=== Кнопки и виджеты интерфейса ===
Label(win).grid(row=5, column=5) # Пустая строка1
vivod = tk.Text(win, height=16, width=79, bg='#0E1720', fg='grey', font=('Verdana', 8))
vivod.grid(column=0, row=6, columnspan=5) #
path = os.path.dirname(__file__) # Получить путь к файлу
win.image = PhotoImage(file=(f'{path}/Background.png')) # Загрузить изображение
bg_logo = Label(win, image=win.image, bd=0)\
    .grid(row=0, column=0, columnspan=4, rowspan=2) # Вывести фон 

Label(win, text='Вставьте URL ...', font=('Verdana', 10), fg='white', bg='#2C3A55')\
    .grid(row=2, column=0, pady=8) # Метка для ввода ссылки
url = tk.Entry(win, width=45, font=('Verdana', 10)) # Поле для ввода ссылки
url.grid(row=2, column=1) # Поле для ввода ссылки
url.focus() # Поле ввода ссылки получает фокус

progress_label = Label(win, text='Прогресс ...', font=('Verdana', 10), fg='white', bg='#2C3A55')
progress_label.grid(row=3, column=0, padx=4) # Метка для ввода ссылки
progress_bar = ttk.Progressbar(win, orient='horizontal', length=200, mode='determinate', maximum=100, value=0)
progress_bar.grid(row=3, column=1, columnspan=1, sticky='W') 

Button(win, text='Очистить', font=('Verdana', 10), bg='#2C3A55',fg='#ccc', command=lambda:url.delete(0, tk.END))\
    .grid(row=3, column=2, padx=4) # Кнопка 'Очистить'
Button(win, text='Вставить', font=('Verdana', 10), bg='#2C3A55',fg='#ccc', command=insert_btn_get)\
    .grid(row=2, column=2, ipadx=1, padx=4) # Кнопка 'Вставить'

media_var = IntVar()
media_var.set(1)
Label(win, text=' Выберите тип медиа:', font=('Verdana', 10), fg='white', bg='#2C3A55')\
    .grid(row=8, column=0, columnspan=2, pady=2, sticky=W) # Метка для выбора типа медиа файла
audio_btn = tk.Radiobutton(win, text='Аудио', variable=media_var, value=1, bg='#2C3A55', selectcolor='white', command=select_media)
audio_btn.grid(row=8,column=1, pady=2)
video_btn = tk.Radiobutton(win, text='Видео', variable=media_var, value=0, bg='#2C3A55', selectcolor='white', command=select_media)
video_btn.grid(row=8,column=2, pady=2)

Label(win, text='Сохраняем в:', font=('Verdana', 10), fg='white', bg='#2C3A55')\
    .grid(row=9, column=0, pady=1, columnspan=1) # Метка для ввода пути сохранения
path_window = tk.Entry(win,  width=45, font=('Verdana', 10),fg='grey', bg='#2C3A55') # Поле для ввода пути сохранения
path_window.insert(0, path_default) # Вставить путь по умолчанию
path_window.grid(row=9, column=1, columnspan=1,pady=8) # Поле для ввода пути сохранения
Button(win, text='Изменить', width=8, font=('Verdana', 10), bg='#2C3A55', fg='#ccc', command=insert_btn_path)\
    .grid(row=9, column=2, ipadx=1, padx=15, sticky='w') # Кнопка 'Изменить'

download_button = tk.Button(win, text='Выбрать поток..', width=44, font=('Verdana', 10), bg='#2C3A55',fg='#ccc',\
    command=lambda: load_streams(media_var.get(), url.get(), path_window.get())).grid(row=10, column=1) # Кнопка 'Скачать'
    
get_text('Качаем видео или аудио с YouTube....')
get_text('Введите URL...')


win.mainloop() # Запуск окна
# Конец программы