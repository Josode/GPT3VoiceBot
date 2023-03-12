from tkinter import *
import time
import re
import os
import string

saved_username = ["vulgo temporario"]

# checks if username file exists, if not, makes one.
if not os.path.isfile("usernames.txt"):
    # doesnt exist, creates usernames.txt file
    print('"usernames.txt" Arquivo não existe. Criando novo arquivo.')
    with open ("usernames.txt", 'wb') as file:
        pass

else:
    # file exists, takes all existing usernames stored in file and adds them to saved_username list
    print('"usernames.txt" Arquivo encontrado.')
    with open("usernames.txt", 'r') as file:
        for line in file:
            saved_username.append(line.replace("\n", ""))
    pass


# checks if default_win_size file exists, if not, makes one.
if not os.path.isfile("default_win_size.txt"):
    # doesnt exist, creates default_win_size.txt file
    print('"default_win_size.txt" Arquivo não existe. Criando novo arquivo.')
    with open("default_win_size.txt", 'wb') as file:
        pass

    default_window_size = "500x200"

else:
    # file exists, takes existing window size and defines it
    print('"default_win_size.txt" Arquivo encontrado.')
    with open("default_win_size.txt", 'r') as file:
        size = file.readlines()
        default_window_size= ''.join(size)


class ChatInterface(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        # sets default bg for top level windows
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 10"

        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)
# Menu bar

    # File
        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="Arquivo", menu=file)
        file.add_command(label="Salvar Chat Log", command=self.save_chat)
        file.add_command(label="Limpar Chat", command=self.clear_chat)
        file.add_separator()
        file.add_command(label="Sair", command=self.client_exit)

    # Options
        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Opções", menu=options)

        # username
        username = Menu(options, tearoff=0)
        options.add_cascade(label="Usuario", menu=username)
        username.add_command(label="Alterar Usuário", command=lambda: self.change_username(height=80))
        username.add_command(label="Usuário Padrão", command=self.default_username)
        username.add_command(label="Ver Histórico do Usuário", command=self.view_username_history)
        username.add_command(label="Limpar Histórico do Usuário", command=self.clear_username_history)

        options.add_separator()

        # font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Fonte", menu=font)
        font.add_command(label="Padrão", command=self.font_change_default)
        font.add_command(label="Times", command=self.font_change_times)
        font.add_command(label="System", command=self.font_change_system)
        font.add_command(label="Helvetica", command=self.font_change_helvetica)
        font.add_command(label="Fixedsys", command=self.font_change_fixedsys)

        # color theme
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Tema", menu=color_theme)
        color_theme.add_command(label="Padrão", command=self.color_theme_default)
        color_theme.add_command(label="Escuro", command=self.color_theme_dark)
        color_theme.add_command(label="Cinza", command=self.color_theme_grey)
        color_theme.add_command(label="Azul", command=self.color_theme_dark_blue)
        color_theme.add_command(label="Rosa", command=self.color_theme_pink)
        color_theme.add_command(label="Turquesa", command=self.color_theme_turquoise)
        color_theme.add_command(label="Hacker", command=self.color_theme_hacker)

        # all to default
        options.add_command(label="Layout Padrão", command=self.default_format)

        options.add_separator()

        # change default window size
        # change default window size
        options.add_command(label="Alterar Padrão de Dimensões", command=self.change_default_window_size)

        # default window size
        options.add_command(label="Padrão de Dimensões", command=self.default_window_size)

    # Chat interface
        # frame containing text box with messages and scrollbar
        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # contains messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        # self.users_message = self.entry_field.get()

        # frame containing send button and emoji button
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        # send button
        self.send_button = Button(self.send_button_frame, text="Enviar", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message(None), activebackground="#FFFFFF",
                                  activeforeground="#000000")
        self.send_button.pack(side=LEFT, ipady=2)
        self.master.bind("<Return>", self.send_message_event)

        # emoticons
        self.emoji_button = Button(self.send_button_frame, text="☺", width=2, relief=GROOVE, bg='white',
                                   bd=1, command=self.emoji_options, activebackground="#FFFFFF",
                                   activeforeground="#000000")
        self.emoji_button.pack(side=RIGHT, padx=6, pady=6, ipady=2)

        self.last_sent_label(date="Nenhuma mensagem enviada.")

    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)

# File functions
    def client_exit(self):
        exit()

    def save_chat(self):
        # creates unique name for chat log file
        time_file = str(time.strftime('%X %x'))
        remove = ":/ "
        for var in remove:
            time_file = time_file.replace(var, "_")

        # gets current directory of program. creates "logs" folder to store chat logs.
        path = os.getcwd() + "\\logs\\"
        new_name = path + "log_" + time_file
        saved = "Chat salvo {}\n".format(new_name)

        # saves chat log file
        try:
            with open(new_name, 'w')as file:
                self.text_box.configure(state=NORMAL)
                log = self.text_box.get(1.0, END)
                file.write(log)
                self.text_box.insert(END, saved)
                self.text_box.see(END)
                self.text_box.configure(state=DISABLED)

        except UnicodeEncodeError:
            # displays error when trying to save chat with unicode. (fix in future)
            self.error_window("Não vai dar pra salvar não \nversion "
                              "contém caractéres >>zuados<<.", type="simple_error", height='100')

    # clears chat
    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.last_sent_label(date="Nenhuma mensagem enviada.")
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)
# creates top level window with error message
    def error_window(self, error_msg, type="simple_error", height='100', button_msg="Daora"):
        # try's to destroy change username window if its an error with username content
        try:
            self.change_username_window.destroy()
        except AttributeError:
            pass

        # makes top level with placement relative to root and specified error msg
        self.error_window_tl = Toplevel(bg=self.tl_bg)
        self.error_window_tl.focus_set()
        self.error_window_tl.grab_set()

        # gets main window width and height to position change username window
        half_root_width = root.winfo_x()
        half_root_height = root.winfo_y() + 60
        placement = '400x' + str(height) + '+' + str(int(half_root_width)) + '+' + str(int(half_root_height))
        self.error_window_tl.geometry(placement)

        too_long_frame = Frame(self.error_window_tl, bd=5, bg=self.tl_bg)
        too_long_frame.pack()

        self.error_scrollbar = Scrollbar(too_long_frame, bd=0)
        self.error_scrollbar.pack(fill=Y, side=RIGHT)

        error_text = Text(too_long_frame, font=self.font, bg=self.tl_bg, fg=self.tl_fg, wrap=WORD, relief=FLAT,
                          height=round(int(height)/30), yscrollcommand=self.error_scrollbar.set)
        error_text.pack(pady=6, padx=6)
        error_text.insert(INSERT, error_msg)
        error_text.configure(state=DISABLED)
        self.error_scrollbar.config(command=self.text_box.yview)

        button_frame = Frame(too_long_frame, width=12)
        button_frame.pack()

        okay_button = Button(button_frame, relief=GROOVE, bd=1, text=button_msg, font=self.font, bg=self.tl_bg,
                             fg=self.tl_fg, activebackground=self.tl_bg, width=5, height=1,
                             activeforeground=self.tl_fg, command=lambda: self.close_error_window(type))
        okay_button.pack(side=LEFT, padx=5)

        if type == "username_history_error":
            cancel_button = Button(button_frame, relief=GROOVE, bd=1, text="Cancelar", font=self.font, bg=self.tl_bg,
                             fg=self.tl_fg, activebackground=self.tl_bg, width=5, height=1,
                             activeforeground=self.tl_fg, command=lambda: self.close_error_window("simple_error"))
            cancel_button.pack(side=RIGHT, padx=5)

# Send Message

    # allows user to hit enter instead of button to change username
    def change_username_main_event(self, event):
        saved_username.append(self.username_entry.get())
        self.change_username_main(username=saved_username[-1])

        # gets passed username from input

    def change_username_main(self, username, default=False):

        # takes saved_username list and writes all usernames into text file
        def write_usernames():
            with open('usernames.txt', 'w') as filer:
                for item in saved_username:
                    filer.write(item + "\n")

        # ensures username contains only letters and numbers
        found = False
        for char in username:
            if char in string.punctuation:
                found = True

        if found is True:
            saved_username.remove(username)
            self.error_window("Seu nome de usuário deve ter apenas letras e/ou números.", type="username_error",
                              height='100')
        # username length limiter (limits to 20 characters or less and greater than 1 character)
        elif len(username) > 20:
            saved_username.remove(username)
            self.error_window("Seu nome de usuário deve ter até 20 caractéres ou menos.", type="username_error", height='100')

        elif len(username) < 2:
            saved_username.remove(username)
            self.error_window("Seu nome de usuário deve ter mais de 2 caractéres, imbecil.", type="username_error", height='100')

        # detects if user entered already current username
        elif len(saved_username) >= 2 and username == saved_username[-2]:
            self.error_window("Este é seu nome de usuário atual, idiota!", type="username_error", height='100')

        # used to detect when user wants default username.
        else:
            # closes change username window, adds username to list, and displays notification
            self.close_username_window()
            write_usernames()
            self.send_message_insert("Usuário alterado para " + '"' + username + '".')

    # allows "enter" key for sending msg
    def send_message_event(self, event):
        user_name = saved_username[-1]
        self.send_message(user_name)

    # joins username with message into publishable format
    def send_message(self, username):

        user_input = self.entry_field.get()

        username = saved_username[-1] + ": "
        message = (username, user_input)
        readable_msg = ''.join(message)
        readable_msg.strip('{')
        readable_msg.strip('}')

        # clears entry field, passes formatted msg to send_message_insert
        if user_input != '':
            self.entry_field.delete(0, END)
            self.send_message_insert(readable_msg)

    # inserts user input into text box
    def send_message_insert(self, message):
        # tries to close emoji window if its open. If not, passes
        try:
            self.close_emoji()

        except AttributeError:
            pass

        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, message + '\n')
        self.last_sent_label(str(time.strftime( "Última mensagem enviada: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
        self.text_box.see(END)
        self.text_box.configure(state=DISABLED)

    # closes change username window
    def close_username_window(self):
        self.change_username_window.destroy()

    # decides type of error when i create an error window ( re-open change username window or not)
    def close_error_window(self, type):
        if type == "username_error":
            self.error_window_tl.destroy()
            self.change_username(height=80)
        elif type == "dimension_error":
            self.error_window_tl.destroy()
            self.change_username(type="window_size", label='Entre "width x height" \n'
                                                           "ex: 500x500", height=125)
        elif type == "simple_error":
            self.error_window_tl.destroy()
        elif type == "username_history_error":
            self.error_window_tl.destroy()
            self.clear_username_history_confirmed()
        else:
            print("Parabéns Idiota!!! Erro desconhecido.")

# enter emoticons
    def emoji_options(self):
        # makes top level window positioned to the right and at the bottom of root window
        self.emoji_selection_window = Toplevel(bg=self.tl_bg, )
        self.emoji_selection_window.bind("<Return>", self.send_message_event)
        selection_frame = Frame(self.emoji_selection_window, bd=4, bg=self.tl_bg)
        selection_frame.grid()
        self.emoji_selection_window.focus_set()
        self.emoji_selection_window.grab_set()

        close_frame = Frame(self.emoji_selection_window)
        close_frame.grid(sticky=S)
        close_button = Button(close_frame, text="Fechar", font="Verdana 9", relief=GROOVE, bg=self.tl_bg,
                              fg=self.tl_fg, activebackground=self.tl_bg,
                              activeforeground=self.tl_fg, command=self.close_emoji)
        close_button.grid(sticky=S)

        root_width = root.winfo_width()
        root_pos_x = root.winfo_x()
        root_pos_y = root.winfo_y()
        selection_width_x = self.emoji_selection_window.winfo_reqwidth()
        selection_height_y = self.emoji_selection_window.winfo_reqheight()

        position = '180x320' + '+' + str(root_pos_x+root_width) + '+' + str(root_pos_y)
        self.emoji_selection_window.geometry(position)
        self.emoji_selection_window.minsize(180, 320)
        self.emoji_selection_window.maxsize(180, 320)

        emoticon_1 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☺",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("☺"), relief=GROOVE, bd=0)
        emoticon_1.grid(column=1, row=0, ipadx=5, ipady=5)
        emoticon_2 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☻",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("☻"), relief=GROOVE, bd=0)
        emoticon_2.grid(column=2, row=0, ipadx=5, ipady=5)
        emoticon_3 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☹",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("☹"), relief=GROOVE, bd=0)
        emoticon_3.grid(column=3, row=0, ipadx=5, ipady=5)
        emoticon_4 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="♡",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("♡"), relief=GROOVE, bd=0)
        emoticon_4.grid(column=4, row=0, ipadx=5, ipady=5)

        emoticon_5 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="♥",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("♥"), relief=GROOVE, bd=0)
        emoticon_5.grid(column=1, row=1, ipadx=5, ipady=5)
        emoticon_6 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="♪",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("♪"), relief=GROOVE, bd=0)
        emoticon_6.grid(column=2, row=1, ipadx=5, ipady=5)
        emoticon_7 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❀",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("❀"), relief=GROOVE, bd=0)
        emoticon_7.grid(column=3, row=1, ipadx=5, ipady=5)
        emoticon_8 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❁",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("❁"), relief=GROOVE, bd=0)
        emoticon_8.grid(column=4, row=1, ipadx=5, ipady=5)

        emoticon_9 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✼",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("✼"), relief=GROOVE, bd=0)
        emoticon_9.grid(column=1, row=2, ipadx=5, ipady=5)
        emoticon_10 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☀",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☀"), relief=GROOVE, bd=0)
        emoticon_10.grid(column=2, row=2, ipadx=5, ipady=5)
        emoticon_11 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✌",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✌"), relief=GROOVE, bd=0)
        emoticon_11.grid(column=3, row=2, ipadx=5, ipady=5)
        emoticon_12 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✊",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✊"), relief=GROOVE, bd=0)
        emoticon_12.grid(column=4, row=2, ipadx=5, ipady=5)

        emoticon_13 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✋",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✋"), relief=GROOVE, bd=0)
        emoticon_13.grid(column=1, row=3, ipadx=5, ipady=5)
        emoticon_14 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☃",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☃"), relief=GROOVE, bd=0)
        emoticon_14.grid(column=2, row=3, ipadx=5, ipady=5)
        emoticon_15 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❄",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❄"), relief=GROOVE, bd=0)
        emoticon_15.grid(column=3, row=3, ipadx=5, ipady=5)
        emoticon_16 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☕",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☕"), relief=GROOVE, bd=0)
        emoticon_16.grid(column=4, row=3, ipadx=5, ipady=5)

        emoticon_17 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☂",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☂"), relief=GROOVE, bd=0)
        emoticon_17.grid(column=1, row=4, ipadx=5, ipady=5)
        emoticon_18 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="★",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("★"), relief=GROOVE, bd=0)
        emoticon_18.grid(column=2, row=4, ipadx=5, ipady=5)
        emoticon_19 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❎",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❎"), relief=GROOVE, bd=0)
        emoticon_19.grid(column=3, row=4, ipadx=5, ipady=5)
        emoticon_20 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❓",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❓"), relief=GROOVE, bd=0)
        emoticon_20.grid(column=4, row=4, ipadx=5, ipady=5)

        emoticon_21 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❗",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❗"), relief=GROOVE, bd=0)
        emoticon_21.grid(column=1, row=5, ipadx=5, ipady=5)
        emoticon_22 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✔",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✔"), relief=GROOVE, bd=0)
        emoticon_22.grid(column=2, row=5, ipadx=5, ipady=5)
        emoticon_23 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✏",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✏"), relief=GROOVE, bd=0)
        emoticon_23.grid(column=3, row=5, ipadx=5, ipady=5)
        emoticon_24 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✨",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✨"), relief=GROOVE, bd=0)
        emoticon_24.grid(column=4, row=5, ipadx=5, ipady=5)

    def send_emoji(self, emoticon):
        self.entry_field.insert(END, emoticon)
        # following line would close emoji toplevel windwo, only allowing 1 emoji per opening of window
        # self.close_emoji()

    def close_emoji(self):
        self.emoji_selection_window.destroy()


# Font options
    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

    def font_change_times(self):
        self.text_box.config(font="Times")
        self.entry_field.config(font="Times")
        self.font = "Times"

    def font_change_system(self):
        self.text_box.config(font="System")
        self.entry_field.config(font="System")
        self.font = "System"

    def font_change_helvetica(self):
        self.text_box.config(font="helvetica 10")
        self.entry_field.config(font="helvetica 10")
        self.font = "helvetica 10"

    def font_change_fixedsys(self):
        self.text_box.config(font="fixedsys")
        self.entry_field.config(font="fixedsys")
        self.font = "fixedsys"

# Color theme options
    # Default
    def color_theme_default(self):
        self.master.config(bg="#EEEEEE")
        self.text_frame.config(bg="#EEEEEE")
        self.entry_frame.config(bg="#EEEEEE")
        self.text_box.config(bg="#FFFFFF", fg="#000000")
        self.entry_field.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#EEEEEE")
        self.send_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.emoji_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.sent_label.config(bg="#EEEEEE", fg="#000000")

        self.tl_bg = "#FFFFFF"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"

    # Dark
    def color_theme_dark(self):
        self.master.config(bg="#2a2b2d")
        self.text_frame.config(bg="#2a2b2d")
        self.text_box.config(bg="#212121", fg="#FFFFFF")
        self.entry_frame.config(bg="#2a2b2d")
        self.entry_field.config(bg="#212121", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#2a2b2d")
        self.send_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#2a2b2d", fg="#FFFFFF")

        self.tl_bg = "#212121"
        self.tl_bg2 = "#2a2b2d"
        self.tl_fg = "#FFFFFF"

    # Grey
    def color_theme_grey(self):
        self.master.config(bg="#444444")
        self.text_frame.config(bg="#444444")
        self.text_box.config(bg="#4f4f4f", fg="#ffffff")
        self.entry_frame.config(bg="#444444")
        self.entry_field.config(bg="#4f4f4f", fg="#ffffff", insertbackground="#ffffff")
        self.send_button_frame.config(bg="#444444")
        self.send_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        self.emoji_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        self.sent_label.config(bg="#444444", fg="#ffffff")

        self.tl_bg = "#4f4f4f"
        self.tl_bg2 = "#444444"
        self.tl_fg = "#ffffff"

    # Blue
    def color_theme_dark_blue(self):
        self.master.config(bg="#263b54")
        self.text_frame.config(bg="#263b54")
        self.text_box.config(bg="#1c2e44", fg="#FFFFFF")
        self.entry_frame.config(bg="#263b54")
        self.entry_field.config(bg="#1c2e44", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#263b54")
        self.send_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#263b54", fg="#FFFFFF")

        self.tl_bg = "#1c2e44"
        self.tl_bg2 = "#263b54"
        self.tl_fg = "#FFFFFF"

    # Pink
    def color_theme_pink(self):
        self.master.config(bg="#ffc1f2")
        self.text_frame.config(bg="#ffc1f2")
        self.text_box.config(bg="#ffe8fa", fg="#000000")
        self.entry_frame.config(bg="#ffc1f2")
        self.entry_field.config(bg="#ffe8fa", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#ffc1f2")
        self.send_button.config(bg="#ffe8fa", fg="#000000", activebackground="#ffe8fa", activeforeground="#000000")
        self.emoji_button.config(bg="#ffe8fa", fg="#000000", activebackground="#ffe8fa", activeforeground="#000000")
        self.sent_label.config(bg="#ffc1f2", fg="#000000")

        self.tl_bg = "#ffe8fa"
        self.tl_bg2 = "#ffc1f2"
        self.tl_fg = "#000000"

    # Turquoise
    def color_theme_turquoise(self):
        self.master.config(bg="#003333")
        self.text_frame.config(bg="#003333")
        self.text_box.config(bg="#669999", fg="#FFFFFF")
        self.entry_frame.config(bg="#003333")
        self.entry_field.config(bg="#669999", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#003333")
        self.send_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#003333", fg="#FFFFFF")

        self.tl_bg = "#669999"
        self.tl_bg2 = "#003333"
        self.tl_fg = "#FFFFFF"

    # Hacker
    def color_theme_hacker(self):
        self.master.config(bg="#0F0F0F")
        self.text_frame.config(bg="#0F0F0F")
        self.entry_frame.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#33FF33")
        self.entry_field.config(bg="#0F0F0F", fg="#33FF33", insertbackground="#33FF33")
        self.send_button_frame.config(bg="#0F0F0F")
        self.send_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#0F0F0F", fg="#33FF33")

        self.tl_bg = "#0F0F0F"
        self.tl_bg2 = "#0F0F0F"
        self.tl_fg = "#33FF33"

    # Default font and color theme
    def default_format(self):
        self.font_change_default()
        self.color_theme_default()

# Change Username or window size window
    def change_username(self, type="username", label=None, height=None):
        self.change_username_window = Toplevel()

        if type == "username":
            self.change_username_window.bind("<Return>", self.change_username_main_event)
        elif type == "window_size":
            self.change_username_window.bind("<Return>", self.change_window_size_event)

        self.change_username_window.configure(bg=self.tl_bg)
        self.change_username_window.focus_set()
        self.change_username_window.grab_set()

        # gets main window width and height to position change username window
        half_root_width = root.winfo_x()+100
        half_root_height = root.winfo_y()+60
        placement = '180x' + str(height) + '+' + str(int(half_root_width)) + '+' + str(int(half_root_height))
        self.change_username_window.geometry(placement)

        # frame for entry field
        enter_username_frame = Frame(self.change_username_window, bg=self.tl_bg)
        enter_username_frame.pack(pady=5)

        if label:
            self.window_label = Label(enter_username_frame, text=label, fg=self.tl_fg)
            self.window_label.pack(pady=4, padx=4)

        self.username_entry = Entry(enter_username_frame, width=22, bg=self.tl_bg, fg=self.tl_fg, bd=1,
                      insertbackground=self.tl_fg)
        self.username_entry.pack(pady=3, padx=10)

        # Frame for Change button and cancel button
        buttons_frame = Frame(self.change_username_window, bg=self.tl_bg)
        buttons_frame.pack()

    # implement username/ size
        if type == "username":
            username_command = lambda: self.change_username_main(self.username_entry.get())
        elif type == "window_size":
            username_command = lambda: self.change_window_size_main(self.username_entry.get())

        change_button = Button(buttons_frame, relief=GROOVE, text="Alterar", width=8, bg=self.tl_bg, bd=1,
                               fg=self.tl_fg, activebackground=self.tl_bg, activeforeground=self.tl_fg,
                               command=username_command)
        change_button.pack(side=LEFT, padx=4, pady=3)


    # cancel
        cancel_button = Button(buttons_frame, relief=GROOVE, text="Cancelar", width=8, bg=self.tl_bg, bd=1,
                               fg=self.tl_fg, command=self.close_username_window,
                               activebackground=self.tl_bg, activeforeground=self.tl_fg)
        cancel_button.pack(side=RIGHT, padx=4, pady=3)

# Use default username ("You")
    def default_username(self):
        saved_username.append("You")
        self.send_message_insert("Usuário local alterado.")

# promps user to Clear username history (deletes usernames.txt file and clears saved_username list)
    def clear_username_history(self):
        self.error_window(error_msg="Tem certeza de que deseja limpar o histórico?\n", button_msg="Limpar",
                          type="username_history_error", height="120")

    def clear_username_history_confirmed(self):
         os.remove("usernames.txt")
         saved_username.clear()
         saved_username.append("Você")

         self.send_message_insert("Histórico limpo.")

# opens window showing username history (possible temp feature)
    def view_username_history(self):
        with open("usernames.txt", 'r') as usernames:
            view_usernames = str(usernames.readlines())

        view_usernames = re.sub("[\[\]']", "", view_usernames)
        view_usernames = view_usernames.replace("\\n", "")

        self.error_window(error_msg="Histórico de Usuário: \n\n" + view_usernames, type="simple_error",
                          button_msg="Fechar", height='150')

# Change Default Window Size
    # called from options, creates window to input dimensions
    def change_default_window_size(self):
        self.change_username(type="window_size", label='Defina "largura x altura" \n'
                                                       "ex: 500x500", height=125)

    # event window, also gets input and checks if it's valid to use as dimensions
    def change_window_size_event(self, event):
        dimensions_get = self.username_entry.get()

        listed = list(dimensions_get)
        try:
            x_index = listed.index("x")

            # formats height and width into seperate int's
            num_1 = int(''.join(listed[0:x_index]))
            num_2 = int(''.join(listed[x_index + 1:]))

        except ValueError or UnboundLocalError:
            self.error_window(
                error_msg="Dimensões específicadas são inválidas. \nTente usar o formato do exemplo: ",
                type="dimension_error", height='125')
            self.close_username_window()

        # checks that its not too big or too small
        try:
            if num_1 > 3840 or num_2 > 2160 or num_1 < 360 or num_2 < 200:
                self.error_window(error_msg="Dimensões específicadas são inválidas.\n"
                                            "Máximo é 3840 x 2160. \n"
                                            "Mínimo é 360 x 200.",
                                  type="dimension_error", height="140")
            else:
                self.change_window_size_main(dimensions_get)
        except:
            pass

    # change size and saves new default into txt file to remember across sessions
    def change_window_size_main(self, window_size):
        window_size = window_size.lower().replace(" ", "")

        root.geometry(window_size)

        with open("default_win_size.txt", 'w') as file:
            print("Novas dimensões de janela: " + window_size)
            file.write(window_size)

        self.close_username_window()

        self.send_message_insert("Dimensão padrão de janela alterada para: " + window_size + ".")

# return to default window size
    def default_window_size(self):

        # gets custom default win size from file
        with open("default_win_size.txt", 'r') as file:
            size = file.readlines()
            default_window_size = ''.join(size)

        root.geometry(default_window_size)
        print(default_window_size)

        # scrolls to very bottom of textbox
        def see_end():
            self.text_box.configure(state=NORMAL)
            self.text_box.see(END)
            self.text_box.configure(state=DISABLED)
        root.after(10, see_end)

root = Tk()
root.title("Chat do Sexo GRÁTIS!!!")
root.wm_attributes("-topmost", True)
root.geometry(default_window_size)
print(default_window_size)
root.minsize(360,200)

a = ChatInterface(root)

root.mainloop()
