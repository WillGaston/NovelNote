import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd # module can be found at the following link: https://pandas.pydata.org/docs/
import csv
import os
import sys
import subprocess
import traceback
import textwrap
import customtkinter # module can be found at the following link: https://github.com/TomSchimansky/CustomTkinter
from ctypes import windll, byref, sizeof, c_int
from tkinter import PhotoImage
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from uuid import uuid4
import matplotlib.pyplot as plt # module can be found at the following link: https://matplotlib.org/
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sys import platform
from CTkMessagebox import CTkMessagebox # module can be found at the following link: https://github.com/Akascape/CTkMessagebox




""" all subsequent iterations of the following code was created with the assistance of samples from the following website: https://stackoverflow.com/questions/75825190/how-to-put-iconbitmap-on-a-customtkinter-toplevel
if platform.startswith("win"):
    self.after(200, lambda: self.iconbitmap("icon.ico"))

all subsequent iterations of the following code was created with the assistance of samples from the following video: https://www.youtube.com/watch?v=36PpT4Z22Os&t=580s
change the color of the window topbar and topbar text:
HWND = windll.user32.GetParent(self.winfo_id())
title_bar_color = 655376
title_text_color = 16777215
windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int)) """

        


""" Initial variables """

username=""
stats_frame = None


""" custom tkinter initialization """

customtkinter.set_appearance_mode("Dark")
customtkinter.deactivate_automatic_dpi_awareness()




""" Global functions to be called modularly """



""" Insert library csv contents in library treeview """
def insert_library():
    
    """ create a dataframe using the csv file and remove the contents of the treeview """
    df = pd.read_csv("Novel_Note_Library.csv")
    library_frame_treeview.delete(*library_frame_treeview.get_children())
    
    """ loop through the dataframe and, if the username column matches the username, insert each row of dataframe to treeview """
    for i in df.index:
        if df.at[i, "username"] == username:
            library_frame_treeview.insert("", i, values=(df.at[i, "id"],
                                                        df.at[i, "novel_title"],
                                                        df.at[i, "chapter_count"],
                                                        df.at[i, "novel_type"],
                                                        df.at[i, "genre"],
                                                        df.at[i, "status"],
                                                        df.at[i, "rating"]))
    
""" Insert quote csv contents in quote treeview """    
def insert_quotes(): 
    
    """ create a dataframe using the csv file and remove the contents of the treeview """
    df = pd.read_csv('Novel_Note_Quotes.csv', encoding='ISO-8859-3')
    quotes_frame_treeview.delete(*quotes_frame_treeview.get_children())
    
    """ loop through the dataframe and, if the username column matches the username, insert each row of dataframe to treeview """
    for i in df.index:
        if df.at[i, "username"] == username:
            quotes_frame_treeview.insert("", i, values=(df.at[i, "id"],
                                                        df.at[i, "novel"],
                                                        df.at[i, "character"],
                                                        df.at[i, "quote"],))   

""" Insert topnovel csv contents in topnovel treeview """   
def insert_topnovel():
    
    """ create a dataframe using the csv file and remove the contents of the treeview """
    df = pd.read_csv("Novel_Note_Top_Novels.csv")
    home_frame_treeview_novel.delete(*home_frame_treeview_novel.get_children())
    
    """ loop through the dataframe and check if the contents of the username column matches contents of username variable """
    for i in df.index:
        if df.at[i, "username"] == username:
            """ loop through the dataframe and create a tuple of values which are then inserted into the treeview """
            for j in range(1, 11):
                novel_number = "novel_" + str(j)
                novel_value = df.at[i, novel_number]
                if pd.notna(novel_value):  #checks if the value is a number
                    values = tuple([novel_value])
                    home_frame_treeview_novel.insert("", "end", values=values)
 
""" Insert topcharacter csv contents in topcharacter treeview """ 
def insert_topcharacter():
    
    """ create a dataframe using the csv file and remove the contents of the treeview """
    df = pd.read_csv("Novel_Note_Top_Characters.csv")
    home_frame_treeview_character.delete(*home_frame_treeview_character.get_children())
    
    """ loop through the dataframe and check if the contents of the username column matches contents of username variable """
    for i in df.index:
        if df.at[i, "username"] == username:
            """ loop through the dataframe and create a tuple of values which are then inserted into the treeview """
            for j in range(1, 11):
                character_number = "character_" + str(j)
                character_value = df.at[i, character_number]
                if pd.notna(character_value): #checks if the value is a number
                    values = tuple([character_value])
                    home_frame_treeview_character.insert("", "end", values=values)

""" Insert 5 newest library csv entries for a user into library treeview """ 
def insert_recent():
    
    """ create a dataframe using the csv file and remove the contents of the treeview """
    file_path = "Novel_Note_Library.csv"
    df = pd.read_csv(file_path)
    home_frame_treeview_recent.delete(*home_frame_treeview_recent.get_children())

    """ create a dataframe which is made up only of the user's entries, then reverse the dataframe """
    mask = df['username'] == username
    filtered_df = df[mask]
    df_reversed = filtered_df.loc[::-1]

    """ insert the first 5 entries from previous dataframe into treeview """
    data_rows = df_reversed.head(6)
    for i, row in data_rows.iterrows():
        home_frame_treeview_recent.insert("", i, values=(row["id"],
                                                        row["novel_title"],
                                                        row["chapter_count"],
                                                        row["novel_type"],
                                                        row["genre"],
                                                        row["status"],
                                                        row["rating"]))   

""" generate stats data/charts and populate them in the stats_frame of the main application window """
def initialize_stats():
    global stats_frame
    
    """ create an initial dataframe using the csv file then create a second dataframe from only the entries wherein the contents of the username column matches contents of username variable  """
    df = pd.read_csv("Novel_Note_Library.csv")
    df_user = df[df['username'] == username]
    
    """ create a variable totalling the chapter count column integers into a variabel (from previous dataframe) """
    chapter_total = df_user['chapter_count'].sum()
    
    """ create dataframes totalling unique data entries from the user dataframe then create a column to record the count of each entry """
    df_genre_count = df_user.groupby('genre').size().reset_index(name='count')
    df_status_count = df_user.groupby('status').size().reset_index(name='count')
    df_type_count = df_user.groupby('novel_type').size().reset_index(name='count')
      
    """ sort the genre dataframe in descending order (by count) and take only the top ten   """
    df_genre_count = df_genre_count.sort_values(by='count', ascending=False)
    top_genres = df_genre_count.head(10)['genre'].tolist()
    
    """ combine the remaining entries into a seperate 'genre' called other which sums the occurence of each remaining entry """
    df_genre_count['modified_genre'] = df_genre_count['genre']
    df_genre_count.loc[~df_genre_count['modified_genre'].isin(top_genres), 'modified_genre'] = 'Other'
    other_count = df_genre_count.loc[df_genre_count['modified_genre'] == 'Other', 'count'].sum()
    df_genre_count = df_genre_count[df_genre_count['modified_genre'] != 'Other']
    df_genre_count = pd.concat([df_genre_count, pd.DataFrame({'modified_genre': ['Other'], 'count': [other_count]})])
    
    """ window labels """
    stats_chaptercount_label = customtkinter.CTkLabel(stats_frame, text="Total Chapter Count:", font=("Tahoma", 20, "bold"))
    stats_chaptercount_label.place(relx=0.15, rely=0.9, anchor="n")
    stats_chaptercount_sum = customtkinter.CTkLabel(stats_frame, text=chapter_total,  font=("Tahoma", 20))
    stats_chaptercount_sum.place(relx=0.32,rely=0.9,anchor="n")

    """ create variables to hold the contents of dataframe """
    values_genre = df_genre_count['count']
    names_genre = df_genre_count['modified_genre']
        
    """ create a pie chart for the genre count detailing the breakdown of genres as a percentage of the whole """
    fig, ax = plt.subplots(constrained_layout=True)
    labels = [f"{name} ({value}), {percent:.1f}%" for name, value, percent in zip(names_genre, values_genre, values_genre / sum(values_genre) * 100)]
    pie = ax.pie(values_genre, labels=labels, autopct='', wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'},
                        textprops={'size': 'small'}, pctdistance=0.8)
    texts = pie[1]
    
    """ make the labels the same colour as the pie chart sections """
    for i, patch in enumerate(pie[0]):
            texts[i].set_color(patch.get_facecolor())
            
    """ scaling, placement, title, etc """
    plt.setp(texts, fontweight=600)
    ax.set_title("Genre Breakdown")
    ax.set_aspect(1)
    ax.set_position([0.0, 0.0, 1.0, 0.82])

    """ create a canvas within the stats frame and place the pie chart inside """
    piechart_canvas = FigureCanvasTkAgg(fig, master=stats_frame)
    piechart_canvas.draw()  # Required to update the canvas before placing it
    piechart_canvas.get_tk_widget().place(relx=0.5, rely=0.4, anchor="c")
    piechart_canvas.get_tk_widget().configure(width=850, height=480)
        
    """ create variables to hold the contents of dataframe """   
    values_status = df_status_count['count']
    names_status = df_status_count['status']
    
    """ create a horizontal bar chart which shows the number of novels of different status types (eg. currently or planning to read) """
    fig2, ax2 =plt.subplots()
    bar_height = 0.8
    ax2.barh(names_status, values_status, height=bar_height)
    
    """ scaling, placement, title, etc """
    ax2.set_xlabel('Count')
    ax2.set_ylabel('Status')
    ax2.set_title('Status Breakdown')
    ax2.tick_params(axis='x', rotation=45)
    ax2.set_aspect(10)

    """ create a canvas within the stats frame and place the bar chart inside """
    barchart_status_canvas = FigureCanvasTkAgg(fig2, master=stats_frame)
    barchart_status_canvas.draw()  # Required to update the canvas before placing it
    barchart_status_canvas.get_tk_widget().place(relx=0.5, rely=0.4, anchor="c")
    barchart_status_canvas.get_tk_widget().configure(width=850, height=480)
      
    """ create variables to hold the contents of dataframe """  
    values_type = df_type_count['count']
    names_type = df_type_count['novel_type']
     
    """ create a horizontal bar chart which shows the number of novels of different types (eg. english or korean) """   
    fig3, ax3 =plt.subplots()
    bar_height = 0.6
    ax3.barh(names_type, values_type, height=bar_height)
    
    """ scaling, placement, title, etc """
    ax3.set_xlabel('Count')
    ax3.set_ylabel('Type')
    ax3.set_title('Type Breakdown')
    ax3.tick_params(axis='x', rotation=45)
    ax3.set_aspect(7)
    
    """ create a canvas within the stats frame and place the bar chart inside """
    barchart_type_canvas = FigureCanvasTkAgg(fig3, master=stats_frame)
    barchart_type_canvas.draw()  # Required to update the canvas before placing it
    barchart_type_canvas.get_tk_widget().place(relx=0.5, rely=0.4, anchor="c")
    barchart_type_canvas.get_tk_widget().configure(width=850, height=480)
        
    """ window labels """
    stats_choosechart_label = customtkinter.CTkLabel(stats_frame, text="Select Chart:", font=("Tahoma", 20, "bold"))
    stats_choosechart_label.place(relx=0.55, rely=0.9, anchor="n")
    
    """ function which allows the user to choose which chart is displayed on the window """
    def choose_chart(piechart_canvas, barchart_status_canvas, barchart_type_canvas):
        """ take the content of the stats combobox, the selected canvas will appear, the others will disappear """
        selected_chart = stats_choosechart_select.get()
        if selected_chart == "Genre Breakdown":
            piechart_canvas.get_tk_widget().place(relx=0.5, rely=0.4, anchor="c")
            barchart_status_canvas.get_tk_widget().place_forget()
            barchart_type_canvas.get_tk_widget().place_forget()
        elif selected_chart == "Status Breakdown":
            piechart_canvas.get_tk_widget().place_forget()
            barchart_status_canvas.get_tk_widget().place(relx=0.5, rely=0.4, anchor="c")
            barchart_type_canvas.get_tk_widget().place_forget()
        elif selected_chart == "Type Breakdown":
            piechart_canvas.get_tk_widget().place_forget()
            barchart_status_canvas.get_tk_widget().place_forget()
            barchart_type_canvas.get_tk_widget().place(relx=0.5, rely=0.4, anchor="c")
        
    """ A combobox bound the the choose chart function, selection in the combobox will change canvas content """
    stats_choosechart_select = ttk.Combobox(stats_frame,  values=["Genre Breakdown", "Status Breakdown", "Type Breakdown"])
    stats_choosechart_select.place(relx=0.73, rely=0.91, relwidth=0.2, anchor="n")
    stats_choosechart_select.current(2)
    stats_choosechart_select.bind('<<ComboboxSelected>>', lambda event: choose_chart(piechart_canvas, barchart_status_canvas, barchart_type_canvas))
    
""" display entry error when an entry from treeview is not selected (for edit function) """
def entry_error():
    CTkMessagebox(title="Entry Warning", message="You Must Select An Entry", icon="warning", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")

""" display entry error when there are no values for all inputs"""
def field_error():
    CTkMessagebox(title="Field Warning", message="You Must Input Values For All Fields.", icon="warning", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")




""" Top level windows """



""" Window providing login and registration functionality """
class LoginWindow(customtkinter.CTkToplevel):
    def __init__(self, frames):
        super().__init__()
        
        self.frames = frames
        
        """ create and style window """
        self.current_frame = None
        self.title("Novel Note")
        self.geometry(f"{400}x{500}")
        self.configure(fg_color="#0A0410")
        self.resizable(False,False)
        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("icon.ico"))
        
        """ change the color of the window topbar and topbar text """
        HWND = windll.user32.GetParent(self.winfo_id())
        title_bar_color = 655376
        title_text_color = 16777215
        windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
        windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
        
        """ create and place the login frame on the login window """
        self.login_frame = customtkinter.CTkFrame (self, height=470, width=376, fg_color="#0E0B13")
        self.login_frame.grid(column=0, row=0,padx=(12,12), pady=(15,15), sticky="n")
        
        login_title_label=customtkinter.CTkLabel(self.login_frame, text="Login", font=("Tahoma", 30,  "bold") )
        login_title_label.place(relx=0.1, rely=0.15, anchor="w")

        """ find the login image from the root directory and assign it as a variable """
        login_img = Image.open("login.png")
        self.login_photo = ImageTk.PhotoImage(login_img)
        
        """ create a label and populate it with the previously declared image """
        login_image_label = Label(self.login_frame, image=self.login_photo)
        login_image_label.image = self.login_photo
        login_image_label.place(relx=0.09, rely=0.2, anchor="w")
        
        """ make the label background transparent and bring the image label above the text label """
        login_image_label.config(bg=self.login_frame.cget("fg_color"), highlightthickness=0)
        login_title_label.lift()
        
        """ populate the login frame with username/password entry fields/labels """
        login_username_label=customtkinter.CTkLabel(self.login_frame, text="Username:", font=("Tahoma", 20,  "bold"))
        login_username_label.place(relx=0.1, rely=0.3, anchor="w")
        login_password_label=customtkinter.CTkLabel(self.login_frame, text="Password:", font=("Tahoma", 20,  "bold"))
        login_password_label.place(relx=0.1, rely=0.5, anchor="w")
        login_account_label=customtkinter.CTkLabel(self.login_frame, text="Don't have an account?")
        login_account_label.place(relx=0.41, rely=0.75, anchor="c")
        login_username_entry=customtkinter.CTkEntry(self.login_frame, width=300, fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Username...")
        login_username_entry.place(relx=0.1, rely=0.4, anchor="w")
        login_password_entry=customtkinter.CTkEntry(self.login_frame, width=300, fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Password...")
        login_password_entry.place(relx=0.1, rely=0.6, anchor="w")
        
        """ create the button which switches to the register frame """
        login_toregister_button = customtkinter.CTkButton(self.login_frame, text="REGISTER", width=50, fg_color="transparent", hover_color="#0E0B13", command=self.register_button_event)
        login_toregister_button.place(relx=0.585, rely=0.75, anchor="w")
        
        """ function to log in to main application """
        def login_account():
            
            """ assign username as a global variable to fill the roll as an identifier throughout the program """
            global username
            username = login_username_entry.get()
            password = login_password_entry.get()

            """ check if both the username and password entries are full, if no then an error window pops up """
            if not all([username, password]):
                field_error()
                return

            """ check if the entered username/password matches any in the user csv, if no then an error window pops up """
            with open("Novel_Note_User_List.csv", mode="r") as f:
                reader = csv.reader(f)
                next(reader)
                user_list = list(reader)
                if [username, password] not in user_list:
                    CTkMessagebox(title="Field Warning", message="Invalid Username or Password", icon="warning", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                    return
                
            """ if the user successfully enters correct credentials, then the frame class/window will begin """
            self.frames.deiconify()

            
            """ call global functions to populate frame window with user specific content """
            
            insert_topnovel()
                        
            insert_topcharacter()

            insert_quotes()
                    
            insert_library()
                    
            insert_recent()
            
            initialize_stats()
            
        """ create the button that initiates the login_account function """
        login_startframes_button = customtkinter.CTkButton(self.login_frame, text="LOGIN", fg_color="#1F044C", border_width=2,border_color="#574379", hover_color="#170830", width=200, command=login_account)
        login_startframes_button.place(relx=0.5, rely=0.85, anchor="c")
        
        """ Create the register frame on top of the self window """
        self.register_frame = customtkinter.CTkFrame (self, height=470, width=376, fg_color="#0E0B13")
        self.register_frame.grid(column=0, row=0,padx=(12,12), pady=(15,15), sticky="n")
        
        """ label """
        register_title_label=customtkinter.CTkLabel(self.register_frame, text="Register", font=("Tahoma", 30,  "bold") )
        register_title_label.place(relx=0.1, rely=0.15, anchor="w")
        
        """ find the login image from the root directory and assign it as a variable """
        register_img = Image.open("login.png")
        self.register_photo = ImageTk.PhotoImage(register_img)
        
        """ create a label and populate it with the previously declared image """
        register_image_label = Label(self.register_frame, image=self.register_photo)
        register_image_label.image = self.register_photo  # keep a reference to the photo
        register_image_label.place(relx=0.09, rely=0.2, anchor="w")
        
        """ make the label background transparent and bring the image label above the text label """
        register_image_label.config(bg=self.register_frame.cget("fg_color"), highlightthickness=0)
        register_title_label.lift()
        
        """ populate the register frame with username/password entry fields/labels """
        register_username_label=customtkinter.CTkLabel(self.register_frame, text="Username:", font=("Tahoma", 20,  "bold"))
        register_username_label.place(relx=0.1, rely=0.3, anchor="w")
        register_username_label=customtkinter.CTkLabel(self.register_frame, text="Password:", font=("Tahoma", 20,  "bold"))
        register_username_label.place(relx=0.1, rely=0.5, anchor="w")
        register_account_label=customtkinter.CTkLabel(self.register_frame, text="Already have an account?")
        register_account_label.place(relx=0.41, rely=0.75, anchor="c")
        register_username_entry=customtkinter.CTkEntry(self.register_frame, width=300, fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Username...")
        register_username_entry.place(relx=0.1, rely=0.4, anchor="w")
        register_password_entry=customtkinter.CTkEntry(self.register_frame, width=300, fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Password...")
        register_password_entry.place(relx=0.1, rely=0.6, anchor="w")
        register_tologin_button = customtkinter.CTkButton(self.register_frame, text="LOGIN", width=50, fg_color="transparent", hover_color="#0E0B13", command=self.login_button_event)
        register_tologin_button.place(relx=0.6, rely=0.75, anchor="w")
        
        """ function to register a new user """
        def register_account():
            
            """ take username/password from entry fields """
            username = register_username_entry.get()
            password = register_password_entry.get()
            
            """ check if both the username and password entries are full, if no then an error window pops up """
            if not all([username, password]):
                field_error()
                return

            """ check if the entered username exists in the csv by creating a list of the user column and comparing the entered username to each row """
            with open("Novel_Note_User_List.csv", mode="r") as f:
                reader = csv.reader(f)
                existing_usernames = [row[0] for row in reader]
                if username in existing_usernames:
                    CTkMessagebox(title="Field Warning", message="Username Already Exists", icon="warning", cancel_button="cross", fg_color="#0E0B13", 
                                  bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                    return

            """ if the username does not exist in the user csv, then the entered username and password are written to the user csv """
            with open("Novel_Note_User_List.csv", mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([username, password])
                self.select_frame_by_name("login")

            """ if registration is complete, creates a popup window which once clicked will switch to the login frame """
            CTkMessagebox(title="Registration Successful", message="Your account has been created successfully. Please Login", icon="check", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            self.select_frame_by_name("login")
            
        """ create the button that initiates the register_account function """
        register_startframes_button = customtkinter.CTkButton(self.register_frame, text="REGISTER", fg_color="#1F044C", border_width=2,border_color="#574379", hover_color="#170830", width=200, command=register_account)
        register_startframes_button.place(relx=0.5, rely=0.85, anchor="c")
        
        
        """ selects the default frame as the login frame """
        self.select_frame_by_name("login")
    
    
    
    """ if the name is login, then the login frame appears on the window and all others disappear
    if the name is register, then the register frame appears on the window and all others disappear """
    """ this function was created using the help of the following example https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/image_example.py """
    def select_frame_by_name(self, name):
        if name == "login":
            self.login_frame.grid(column=0, row=0,padx=(12,12), pady=(15,15), sticky="n")
        else:
            self.login_frame.grid_forget()
        if name == "register":
            self.register_frame.grid(column=0, row=0,padx=(12,12), pady=(15,15), sticky="n")
        else:
            self.register_frame.grid_forget()
    
    """ assigns the name used in the select_frame_by_name function to login """
    def login_button_event(self):
        self.select_frame_by_name("login")
    """ assigns the name used in the select_frame_by_name function to register """
    def register_button_event(self):
        self.select_frame_by_name("register")

""" Window providing functionality to add quote to library """    
class AddQuoteEntry(customtkinter.CTkToplevel):
    
        """global variable username to be used as an identifier """
        global username
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Add Entry")
            self.geometry("400x400")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the addquoteentry window as the foremost window """
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ create the novel,character, quote entry boxes """
            novel_entry_quotes = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_quotes.place(relx=0.5, rely=0.31, relwidth=0.8, anchor="c")
            character_entry_quotes = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_quotes.place(relx=0.5, rely=0.48,relwidth=0.8,  anchor="c")
            quote_entry_quotes = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Quote...")
            quote_entry_quotes.place(relx=0.5, rely=0.65,relwidth=0.8, anchor="c")
            
            """ function which saves the quote to csv """
            def add_quote():
                
                """ create variables from the entered data """
                novel = novel_entry_quotes.get()
                character = character_entry_quotes.get()
                quote = quote_entry_quotes.get()
                id = str(uuid4())

                """ Check if any of the fields is empty, if yes display error message """
                if not all([novel, character, quote]):
                    field_error()
                    return

                """ write to row/entry to the csv """
                with open("Novel_Note_Quotes.csv", mode="a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([id, username, novel, character, quote])

                """ place row in treeview and destroy the window """
                insert_quotes()   
                self.destroy()
              
            """ validation to save """
            def confirm_add():
                
                """ create message box whith options yes and no """
                msg = CTkMessagebox(title="Confirm Entry", message="Are you sure you would like to save this entry?", icon="warning", option_2 = "Yes", option_1 = "No", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                
                """ if option from messagebox is yes, begin save entry function, if no do nothing """
                if msg.get() == "Yes":
                    add_quote()
                else:
                    msg.destroy()  
                
            """ destroy the window """     
            def close():
                self.destroy()        
            
            """ create a messagebox """
            def help():
                CTkMessagebox(title="Add Quote - Help", message="To add a quote you must first type in the entry fields." + "\n" + "\n" + "-To save the quote to your library you must then select the 'Save Entry' button once all fields are full", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            
            """ create and place labels/buttons """
            save_button = customtkinter.CTkButton(self, text="Save Entry", width=100, fg_color="#638619", border_width=2, border_color="#2B3418", hover_color="#4B5D24", command=confirm_add)
            save_button.place(relx=0.33, rely=0.9, anchor="c")
            cancel_button = customtkinter.CTkButton(self, text="Cancel", width=100, fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command=close)
            cancel_button.place(relx=0.66, rely=0.9, anchor="c")
            quotes_novel_label = customtkinter.CTkLabel(self, text="Novel Title:", font=("Tahoma", 20,  "bold"))
            quotes_novel_label.place(relx=0.1,rely=0.2)
            quotes_character_label = customtkinter.CTkLabel(self, text="Character Name:", font=("Tahoma", 20,  "bold"))
            quotes_character_label.place(relx=0.1,rely=0.37)
            quotes_quote_label = customtkinter.CTkLabel(self, text="Quote:", font=("Tahoma", 20,  "bold"))
            quotes_quote_label.place(relx=0.1,rely=0.54)
            quotes_title_label = customtkinter.CTkLabel(self, text="Add Entry:", font=("Tahoma", 30,  "bold"))
            quotes_title_label.place(relx=0.1,rely=0.045)
            quotes_help_button = customtkinter.CTkButton(self,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=help)
            quotes_help_button.place(relx=0.88, rely=0.03, relwidth=0.1)        

""" Window providing functionality to edit quote in library """  
class EditQuoteEntry(customtkinter.CTkToplevel):
    
        """ global variable username to be used as an identifier """
        global username
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Edit Entry")
            self.geometry("400x400")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
             
            """ sets the editquoteentry window as the foremost window """   
            self.lift()
            self.attributes("-topmost", True)
            
            """ call the selected_quote variable (a row of the quote treeview) """
            global selected_quote
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
        
            """ create a variable from the items in selected_quote """
            values = quotes_frame_treeview.item(selected_quote, 'values')
            
            """ entry fields """
            novel_entry_quotes = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white")
            novel_entry_quotes.place(relx=0.5, rely=0.31, relwidth=0.8, anchor="c")
            character_entry_quotes = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white")
            character_entry_quotes.place(relx=0.5, rely=0.48,relwidth=0.8,  anchor="c")
            quote_entry_quotes = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white")
            quote_entry_quotes.place(relx=0.5, rely=0.65,relwidth=0.8, anchor="c")
            
            """ insert the selected_quote data into entry fields """
            novel_entry_quotes.insert(0, values[1])
            character_entry_quotes.insert(0, values[2])
            quote_entry_quotes.insert(0, values[3])

            """ edit then save quote """
            def edit_quote():
                
                """ create varaiables from the input data """
                novel = novel_entry_quotes.get()
                character = character_entry_quotes.get()
                quote = quote_entry_quotes.get()
                id = str(uuid4())
                
                """ Check if any of the fields is empty, if yes display error message """
                if not all([novel, character, quote]):
                    field_error()
                    return
                
                """ Read CSV file into a list of dictionaries """
                with open('Novel_Note_Quotes.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    data = [row for row in reader]
                    
                """ Find the index of the selected row """
                del_index = None
                for i, row in enumerate(data):
                    if row['id'] == values[0]:
                        del_index = i
                        break
                if del_index is not None:
                    
                    """ Remove the selected row from the list of dictionaries """
                    del data[del_index]
                    
                    """ Write the updated data back to the CSV file (will not include the selected entry) """
                    with open('Novel_Note_Quotes.csv', 'w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)

                """ write the entered data to the csv """
                with open("Novel_Note_Quotes.csv", mode="a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([id,username, novel, character, quote])
                 
                """ call function  """  
                insert_quotes()
                
                """ destroy the window """     
                self.destroy()
                            
            """ validation to save """
            def confirm_edit():    
                """ create message box whith options yes and no """
                msg = CTkMessagebox(title="Confirm Entry", message="Are you sure you would like to save this entry?", icon="warning", option_2 = "Yes", option_1 = "No", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                
                """ if option from messagebox is yes, begin save entry function, if no do nothing """
                if msg.get() == "Yes":
                    edit_quote()
                else:
                    msg.destroy()      
                
            """ destroy the window """ 
            def close():
                self.destroy()

            """ remove the selected quote """
            def delete_quote():
                
                """ Read CSV file into a list of dictionaries """
                with open('Novel_Note_Quotes.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    data = [row for row in reader]
                    
                """ Find the index of the selected row """
                del_index = None
                for i, row in enumerate(data):
                    if row['id'] == values[0]:
                        del_index = i
                        break
                if del_index is not None:
                    
                    """ Remove the selected row from the list """
                    del data[del_index]
                    
                    """ write the updated list back to csv (will not include removed row) """
                    with open('Novel_Note_Quotes.csv', 'w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                    
                    insert_quotes()
                    
                    """ destroy the window """ 
                    self.destroy()
            
            """ validation to delete """
            def confirm_delete():
                
                """ create message box whith options yes and no """
                msg = CTkMessagebox(title="Confirm Deletion", message="Are you sure you would like to delete this entry?", icon="warning", option_2 = "Yes", option_1 = "No", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                
                """ if option from messagebox is yes, begin save entry function, if no do nothing """
                if msg.get() == "Yes":
                    delete_quote()
                else:
                    msg.destroy()  
            
            """ create a messagebox """        
            def help():
                CTkMessagebox(title="Edit Quote - Help", message="To edit a quote you must first type in the entry fields." + "\n" + "\n" + "-To save the updated quote to your library you must then select the 'Save Entry' button once all fields are full" + "\n" + "-To remove the entry from your library, press the 'Delete' button.", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            
            """ create and place labels/buttons """        
            save_button = customtkinter.CTkButton(self, text="Save Entry", width=75, fg_color="#638619", border_width=2, border_color="#2B3418", hover_color="#4B5D24", command=confirm_edit)
            save_button.place(relx=0.25, rely=0.9, anchor="c")
            delete_button = customtkinter.CTkButton(self, text="Delete", width=75, fg_color="#C62020", border_width=2, border_color="#7C1414", hover_color="#951818", command=confirm_delete)
            delete_button.place(relx=0.5, rely=0.9, anchor="c")
            cancel_button = customtkinter.CTkButton(self, text="Cancel", width=75, fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command=close)
            cancel_button.place(relx=0.75, rely=0.9, anchor="c")
            quotes_novel_label = customtkinter.CTkLabel(self, text="Novel Title:", font=("Tahoma", 20,  "bold"))
            quotes_novel_label.place(relx=0.1,rely=0.2)
            quotes_character_label = customtkinter.CTkLabel(self, text="Character Name:", font=("Tahoma", 20,  "bold"))
            quotes_character_label.place(relx=0.1,rely=0.37)
            quotes_quote_label = customtkinter.CTkLabel(self, text="Quote:", font=("Tahoma", 20,  "bold"))
            quotes_quote_label.place(relx=0.1,rely=0.54)
            quotes_new_label = customtkinter.CTkLabel(self, text="Edit Entry:", font=("Tahoma", 30,  "bold"))
            quotes_new_label.place(relx=0.1,rely=0.045)
            quotes_help_button = customtkinter.CTkButton(self,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=help)
            quotes_help_button.place(relx=0.88, rely=0.03, relwidth=0.1)

""" Window providing functionality to add novel to library """  
class AddLibraryEntry(customtkinter.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Add Entry")
            self.geometry("350x550")
            self.configure(fg_color="#0A0410")  
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the addlibraryentry window as the foremost window """    
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ entry fields/selection menus """
            novel_title_entry_library = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_title_entry_library.place(relx=0.5, rely=0.21, relwidth=0.8, anchor="n")
            chapter_count_entry_library = customtkinter.CTkEntry(self, fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Chapter Count...")
            chapter_count_entry_library.place(relx=0.5, rely=0.33, relwidth=0.8, anchor="n")
            novel_type_entry_library = customtkinter.CTkOptionMenu(self, fg_color="#1F1037", button_color="#35284A", button_hover_color="#170830", dropdown_fg_color="#110425", dropdown_hover_color="#1F1037", values=["Manhwa", "Manhua", "Manga", "English Novel", "Chinese Novel", "Korean Novel", "Japanese Novel"])
            novel_type_entry_library.place(relx=0.5, rely=0.45, relwidth=0.8, anchor="n")
            genre_entry_library = customtkinter.CTkOptionMenu(self, fg_color="#1F1037", button_color="#35284A", button_hover_color="#170830", dropdown_fg_color="#110425", dropdown_hover_color="#1F1037", values=["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Historical", "Horror", "Isekai", "Korean Dungeon", "Murim", "Mystery", "Otome Isekai", "Romance", "Sports", "Thriller", "Xianxia", "Xuanhuan"])
            genre_entry_library.place(relx=0.5, rely=0.57, relwidth=0.8, anchor="n")
            status_entry_library = customtkinter.CTkOptionMenu(self, fg_color="#1F1037", button_color="#35284A", button_hover_color="#170830", dropdown_fg_color="#110425", dropdown_hover_color="#1F1037", values=["Currently Reading", "Plan to Read", "Completed", "On Hold", "Dropped"])
            status_entry_library.place(relx=0.5, rely=0.69, relwidth=0.8, anchor="n")
            rating_entry_library = customtkinter.CTkEntry(self, justify=CENTER,fg_color="#170830", border_color="#574379", text_color="white")
            rating_entry_library.insert(0, float("1")) 
            rating_entry_library.configure(state="disabled")
            rating_entry_library.place(relx=0.5, rely=0.81, relwidth=0.8, anchor="n")

            """ saves entry to csv """
            def add_novel():
                
                """ create variables of entered data """
                novel_title = novel_title_entry_library.get()
                chapter_count = chapter_count_entry_library.get()
                novel_type = novel_type_entry_library.get()
                genre = genre_entry_library.get()
                status = status_entry_library.get()
                rating = rating_entry_library.get()
                id = str(uuid4())

                """ Check if any of the fields is empty, if yes display error """
                if not all([novel_title, chapter_count, novel_type, genre, status, rating]):
                    field_error()
                    return
                
                """ Check if chapter count is a number """
                if not chapter_count.isdigit():
                    CTkMessagebox(title="Field Warning", message="Chapter Count Must Be A Number.", icon="warning", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                    return

                """ write entry to csv """
                with open("Novel_Note_Library.csv", mode="a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([id, username, novel_title, chapter_count, novel_type, genre, status, rating])

                """ call functions """
                insert_library()
                initialize_stats() 
                insert_recent()
                
                """ destroy the window """
                self.destroy()
            
            """ validation to save """
            def confirm_add():
                
                """ create message box whith options yes and no """
                msg = CTkMessagebox(title="Confirm Entry", message="Are you sure you would like to save this entry?", icon="warning", option_2 = "Yes", option_1 = "No", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                
                """ if option from messagebox is yes, begin save entry function, if no do nothing """
                if msg.get() == "Yes":
                    add_novel()
                else:
                    msg.destroy()  
            
            """ destroy the window """
            def close():
                self.destroy()
            
            """ create a messagebox """
            def help():
                CTkMessagebox(title="Add Novel - Help", message="To add a novel you must first type in the entry fields and select suitable options by clicking on the entry boxes." + "\n" + "\n" + "-To save the novel to your library you must then select the 'Save Entry' button once all fields are full", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            
            """ button/labels """
            button_library_cancel = customtkinter.CTkButton(self, text="Cancel", width=100, fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command=close)
            button_library_cancel.place(relx=0.66, rely=0.9, anchor="n")
            button_library_save = customtkinter.CTkButton(self, text="Save Entry", width=100, fg_color="#638619", border_width=2, border_color="#2B3418", hover_color="#4B5D24", command=confirm_add)
            button_library_save.place(relx=0.33, rely=0.9, anchor="n")
            library_help_button = customtkinter.CTkButton(self,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=help)
            library_help_button.place(relx=0.88, rely=0.03, relwidth=0.1)
            library_title_label = customtkinter.CTkLabel(self,text="Novel Title:", font=("Tahoma", 20,  "bold"))
            library_title_label.place(relx=0.1,rely=0.15)
            library_chapter_count_label =customtkinter.CTkLabel(self, text="Chapter Count:", font=("Tahoma", 20,  "bold"))
            library_chapter_count_label.place(relx=0.1,rely=0.27)
            library_novel_type_label = customtkinter.CTkLabel(self, text="Novel Type:",font=("Tahoma", 20,  "bold"))
            library_novel_type_label.place(relx=0.1,rely=0.39)
            library_genre_label = customtkinter.CTkLabel(self, text="Genre:",font=("Tahoma", 20,  "bold"))
            library_genre_label.place(relx=0.1,rely=0.51)
            library_library_status_label = customtkinter.CTkLabel(self, text="Library Status:", font=("Tahoma", 20,  "bold"))
            library_library_status_label.place(relx=0.1,rely=0.63)
            library_rating_label = customtkinter.CTkLabel(self, text="Rating:",font=("Tahoma", 20,  "bold"))
            library_rating_label.place(relx=0.1,rely=0.75)
            library_title_label = customtkinter.CTkLabel(self,text="Add Entry:",font=("Tahoma", 30,  "bold"))
            library_title_label.place(relx=0.1,rely=0.045)   
            
            """ increases rating entrybox values by 1 (0-10)"""
            def add_1_0():
                value = float(rating_entry_library.get())
                if value < 10:
                    value += 1
                    rating_entry_library.configure(state="normal")
                    rating_entry_library.delete(0, 'end')
                    rating_entry_library.insert(0, value)
                    rating_entry_library.configure(state="disabled")
            
            """ decreases rating entrybox values by 1 (0-10) """
            def subtract_1_0():
                value = float(rating_entry_library.get())
                if value > 0:
                    value -= 1
                    rating_entry_library.configure(state="normal")
                    rating_entry_library.delete(0, 'end')
                    rating_entry_library.insert(0, value)
                    rating_entry_library.configure(state="disabled")

            """ buttons to decrease/increase rating """
            library_addone_button = customtkinter.CTkButton(rating_entry_library, text="+", width=2, fg_color="#1F044C", border_width=2,border_color="#574379", hover_color="#170830", command=add_1_0)
            library_addone_button.place(relx=1,rely=0.5, anchor="e")
            library_subtractone_button = customtkinter.CTkButton(rating_entry_library, text="-", width=2, fg_color="#1F044C", border_width=2,border_color="#574379", hover_color="#170830", command=subtract_1_0)
            library_subtractone_button.place(relx=0.0,rely=0.5, anchor="w")    

""" Window providing functionality to edit quote in library """  
class EditLibraryEntry(customtkinter.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Edit Entry")
            self.geometry("350x550")
            self.configure(fg_color="#0A0410")  
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the editlibraryentry window as the foremost window """ 
            self.lift()
            self.attributes("-topmost", True)
            
            """ selected_library variable (a row of the library treeview) """
            global selected_library
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ create a variable from the items in selected_library """
            values = library_frame_treeview.item(selected_library, 'values')
            
            """ entry fields/selection menus """
            novel_title_entry_library = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_title_entry_library.place(relx=0.5, rely=0.21, relwidth=0.8, anchor="n")
            chapter_count_entry_library = customtkinter.CTkEntry(self, fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Chapter Count...")
            chapter_count_entry_library.place(relx=0.5, rely=0.33, relwidth=0.8, anchor="n")
            novel_type_entry_library = customtkinter.CTkOptionMenu(self, fg_color="#1F1037", button_color="#35284A", button_hover_color="#170830", dropdown_fg_color="#110425", dropdown_hover_color="#1F1037", values=["Manhwa", "Manhua", "Manga", "English Novel", "Chinese Novel", "Korean Novel", "Japanese Novel"])
            novel_type_entry_library.place(relx=0.5, rely=0.45, relwidth=0.8, anchor="n")
            genre_entry_library = customtkinter.CTkOptionMenu(self, fg_color="#1F1037", button_color="#35284A", button_hover_color="#170830", dropdown_fg_color="#110425", dropdown_hover_color="#1F1037", values=["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Historical", "Horror", "Isekai", "Korean Dungeon", "Murim", "Mystery", "Otome Isekai", "Romance", "Sports", "Thriller", "Xianxia", "Xuanhuan"])
            genre_entry_library.place(relx=0.5, rely=0.57, relwidth=0.8, anchor="n")
            status_entry_library = customtkinter.CTkOptionMenu(self, fg_color="#1F1037", button_color="#35284A", button_hover_color="#170830", dropdown_fg_color="#110425", dropdown_hover_color="#1F1037", values=["Currently Reading", "Plan to Read", "Completed", "On Hold", "Dropped"])
            status_entry_library.place(relx=0.5, rely=0.69, relwidth=0.8, anchor="n")
            rating_entry_library = customtkinter.CTkEntry(self, justify=CENTER,fg_color="#170830", border_color="#574379", text_color="white")
            rating_entry_library.place(relx=0.5, rely=0.81, relwidth=0.8, anchor="n")
            
            """ insert the selected_library data into entry fields/selection menus """
            novel_title_entry_library.insert(0, values[1])
            chapter_count_entry_library.insert(0, values[2])
            novel_type_entry_library.set(values[3])
            genre_entry_library.set(values[4])
            status_entry_library.set(values[5])
            rating_entry_library.insert(0, values[6])
            
            rating_entry_library.configure(state="disabled")
            
            """ edit then save novel """
            def edit_novel():
                
                """ create varaiables from the input data """
                novel_title = novel_title_entry_library.get()
                chapter_count = chapter_count_entry_library.get()
                novel_type = novel_type_entry_library.get()
                genre = genre_entry_library.get()
                status = status_entry_library.get()
                rating = rating_entry_library.get()
                id = str(uuid4())
                
                """ Check if any of the fields is empty, if yes display error message """
                if not all([novel_title, chapter_count, novel_type, genre, status, rating]):
                    field_error()
                    return
                
                """ Check if chapter count is a number """
                if not chapter_count.isdigit():
                    CTkMessagebox(title="Field Warning", message="Chapter Count Must Be A Number.", icon="warning", cancel_button="cross",
                                  fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", 
                                  button_hover_color="#4B5D24")
                    return
                
                """ Read CSV file into a list of dictionaries """
                with open('Novel_Note_Library.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    data = [row for row in reader]
                    
                """ Find the index of the selected row """
                del_index = None
                for i, row in enumerate(data):
                    if row['id'] == values[0]:
                        del_index = i
                        break
                if del_index is not None:
                    
                    """ Remove the selected row from the list of dictionaries """
                    del data[del_index]
                    
                    """ Write the updated data back to the CSV file (will not include the selected entry) """
                    with open('Novel_Note_Library.csv', 'w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)

                """ write the entered data to the csv """
                with open("Novel_Note_Library.csv", mode="a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([id, username, novel_title, chapter_count, novel_type, genre, status, rating])

                """ call functions """ 
                insert_library()
                initialize_stats() 
                
                """ destroy the window """     
                self.destroy()
            
            """ validation to save """
            def confirm_edit():
                
                """ create message box whith options yes and no """
                msg = CTkMessagebox(title="Confirm Entry", message="Are you sure you would like to save these entries?", icon="warning", option_2 = "Yes", option_1 = "No", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                
                """ if option from messagebox is yes, begin save entry function, if no do nothing """
                if msg.get() == "Yes":
                    edit_novel()
                else:
                    msg.destroy()  
            
            """ destroy the window """ 
            def close():
                self.destroy()

            """ create a messagebox """ 
            def help():
                CTkMessagebox(title="Edit Novel - Help", message="To edit a novel you must first type in the entry fields and select suitable options." + "\n" + "\n" + "-To save the updated novel to your library you must then select the 'Save Entry' button once all fields are full" + "\n" + "-To remove the novel from your library, press the 'Delete' button.", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            
            """ remove the selected novel """
            def delete_novel():
                
                """ Read CSV file into a list of dictionaries """
                with open('Novel_Note_Library.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    data = [row for row in reader]
                    

                """ Find the index of the selected row """
                del_index = None
                for i, row in enumerate(data):
                    if row['id'] == values[0]:
                        del_index = i
                        break
                if del_index is not None:
                        
                    """ Remove the selected row from the list """
                    del data[del_index]
                        
                    """ write the updated list back to csv (will not include removed row) """
                    with open('Novel_Note_Library.csv', 'w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                        
                    """ call function """
                    initialize_stats() 
                    insert_library()
                        
                    """ destroy the window """
                    self.destroy()


            """ validation to delete """
            def confirm_delete():
                
                """ create message box whith options yes and no """
                msg = CTkMessagebox(title="Confirm Deletion", message="Are you sure you would like to delete this entry?", icon="warning", option_2 = "Yes", option_1 = "No", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                
                """ if option from messagebox is yes, begin save entry function, if no do nothing """
                if msg.get() == "Yes":
                    delete_novel()
                else:
                    msg.destroy()   
            
            """ buttons/labels """
            library_delete_button = customtkinter.CTkButton(self, text="Delete", width=75, fg_color="#C62020", border_width=2, border_color="#7C1414", hover_color="#951818", command=confirm_delete)
            library_delete_button.place(relx=0.5, rely=0.9, anchor="n")
            button_library_cancel = customtkinter.CTkButton(self, text="Cancel", width=75, fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command=close)
            button_library_cancel.place(relx=0.75, rely=0.9, anchor="n")
            button_library_save = customtkinter.CTkButton(self, text="Save Entry", width=75, fg_color="#638619", border_width=2, border_color="#2B3418", hover_color="#4B5D24", command=confirm_edit)
            button_library_save.place(relx=0.25, rely=0.9, anchor="n")
            library_help_button = customtkinter.CTkButton(self,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=help)
            library_help_button.place(relx=0.88, rely=0.03, relwidth=0.1)
            library_title_label = customtkinter.CTkLabel(self,text="Novel Title:", font=("Tahoma", 20,  "bold"))
            library_title_label.place(relx=0.1,rely=0.15)
            library_chapter_count_label =customtkinter.CTkLabel(self, text="Chapter Count:", font=("Tahoma", 20,  "bold"))
            library_chapter_count_label.place(relx=0.1,rely=0.27)
            library_novel_type_label = customtkinter.CTkLabel(self, text="Novel Type:",font=("Tahoma", 20,  "bold"))
            library_novel_type_label.place(relx=0.1,rely=0.39)
            library_genre_label = customtkinter.CTkLabel(self, text="Genre:",font=("Tahoma", 20,  "bold"))
            library_genre_label.place(relx=0.1,rely=0.51)
            library_library_status_label = customtkinter.CTkLabel(self, text="Library Status:", font=("Tahoma", 20,  "bold"))
            library_library_status_label.place(relx=0.1,rely=0.63)
            library_rating_label = customtkinter.CTkLabel(self, text="Rating:",font=("Tahoma", 20,  "bold"))
            library_rating_label.place(relx=0.1,rely=0.75)
            library_title_label = customtkinter.CTkLabel(self,text="Edit Entry:",font=("Tahoma", 30,  "bold"))
            library_title_label.place(relx=0.1,rely=0.045)   
            
            """ increases rating entrybox values by 1 (0-10)"""
            def add_1_0():
                value = float(rating_entry_library.get())
                if value < 10:
                    value += 1
                    rating_entry_library.configure(state="normal")
                    rating_entry_library.delete(0, 'end')
                    rating_entry_library.insert(0, value)
                    rating_entry_library.configure(state="disabled")
            
            """ decreases rating entrybox values by 1 (0-10) """
            def subtract_1_0():
                value = float(rating_entry_library.get())
                if value > 0:
                    value -= 1
                    rating_entry_library.configure(state="normal")
                    rating_entry_library.delete(0, 'end')
                    rating_entry_library.insert(0, value)
                    rating_entry_library.configure(state="disabled")

            """ buttons to decrease/increase rating """
            library_addone_button = customtkinter.CTkButton(rating_entry_library, text="+", width=2, fg_color="#1F044C", border_width=2,border_color="#574379", hover_color="#170830", command=add_1_0)
            library_addone_button.place(relx=1,rely=0.5, anchor="e")
            library_subtractone_button = customtkinter.CTkButton(rating_entry_library, text="-", width=2, fg_color="#1F044C", border_width=2,border_color="#574379", hover_color="#170830", command=subtract_1_0)
            library_subtractone_button.place(relx=0.0,rely=0.5, anchor="w") 

""" Window providing functionality filter novel library """  
class FilterLibrary(customtkinter.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Filter Library")
            self.geometry("400x300")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False) 
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the filter window as the foremost window """ 
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ comboboxes bound the filter functions (used to access filter options) """
            self.combo_chaptercount = ttk.Combobox(self, values=["Any", "Ascending", "Descending"])
            self.combo_chaptercount.current(0)
            self.combo_chaptercount.place(relx=0.5,rely=0.29, anchor=NW)
            self.combo_chaptercount.bind('<<ComboboxSelected>>', self.filter_library_chaptercount)
            self.combo_noveltype = ttk.Combobox(self, values=["All","Manhwa", "Manhua", "Manga", "English Novel", "Chinese Novel", "Korean Novel", "Japanese Novel"])
            self.combo_noveltype.current(0)
            self.combo_noveltype.place(relx=0.05,rely=0.29, anchor=NW)
            self.combo_noveltype.bind('<<ComboboxSelected>>', self.filter_library_rating, self.filter_library_chaptercount)
            self.combo_genre = ttk.Combobox(self, state="readonly", values=["All","Action", "Adventure", "Comedy", "Drama", "Fantasy", "Historical", "Horror", "Isekai", "Korean Dungeon", "Murim", "Mystery", "Otome Isekai", "Romance", "Sports", "Thriller", "Xianxia", "Xuanhuan"])
            self.combo_genre.current(0)
            self.combo_genre.place(relx=0.05,rely=0.51, anchor=NW)
            self.combo_genre.bind('<<ComboboxSelected>>', self.filter_library_rating, self.filter_library_chaptercount)
            self.combo_librarystatus = ttk.Combobox(self, values=["All","Currently Reading", "Plan to Read", "Completed", "On Hold", "Dropped"])
            self.combo_librarystatus.current(0)
            self.combo_librarystatus.place(relx=0.05,rely=0.73, anchor=NW)
            self.combo_librarystatus.bind('<<ComboboxSelected>>', self.filter_library_rating, self.filter_library_chaptercount)
            self.combo_rating = ttk.Combobox(self, values=["Any", "Ascending", "Descending"])
            self.combo_rating.current(0)
            self.combo_rating.place(relx=0.5,rely=0.51, anchor=NW)
            self.combo_rating.bind('<<ComboboxSelected>>', self.filter_library_rating)
            
            """ labels """
            heading = customtkinter.CTkLabel(self, text="Filter & Refine", font=("Tahoma",25,  "bold"))
            heading.place(relx=0.05,rely=0.05, anchor=NW)
            chaptercount = customtkinter.CTkLabel(self, text="Chapter Count:", font=("Tahoma",18,  "bold"))
            chaptercount.place(relx=0.5,rely=0.18, anchor=NW)
            rating = customtkinter.CTkLabel(self, text="Rating:", font=("Tahoma",18,  "bold"))
            rating.place(relx=0.5,rely=0.4, anchor=NW)
            noveltype = customtkinter.CTkLabel(self, text="Novel Type:", font=("Tahoma",18,  "bold"))
            noveltype.place(relx=0.05,rely=0.18, anchor=NW)
            genre = customtkinter.CTkLabel(self, text="Genre:", font=("Tahoma",18,  "bold"))
            genre.place(relx=0.05,rely=0.4, anchor=NW)
            librarystatus = customtkinter.CTkLabel(self, text="Library Status:", font=("Tahoma",18,  "bold"))
            librarystatus.place(relx=0.05,rely=0.62, anchor=NW)
            
            """ create message box """
            def help():
                CTkMessagebox(title="Filter Novel - Help", message="To filter the library you must select suitable restrictions by clicking on the entry boxes." + "\n" + "\n" + "-If a restriction does not work properly, reset each option and isolate the restriction.", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            
            """ help button """
            filter_help_button = customtkinter.CTkButton(self,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=help)
            filter_help_button.place(relx=0.88, rely=0.03, relwidth=0.1)
        
        """ filter function when rating is selected   """  
        def filter_library_rating(self, event):
            
            """ if the rating selection is ascending/descending make chaptercount selection to default """
            if self.combo_rating.get() in ["Ascending", "Descending"]:
                self.combo_chaptercount.current(0)

            """ get selected values from comboboxes, assign them as variables """
            selected_noveltype = self.combo_noveltype.get()
            selected_genre = self.combo_genre.get()
            selected_librarystatus = self.combo_librarystatus.get()

            """ remove contents of treeview """
            library_frame_treeview.delete(*library_frame_treeview.get_children())

            """ read the csv file as an iterable """
            with open("Novel_Note_Library.csv") as csvfile:
                reader = csv.reader(csvfile)
                
                """ skip the first row"""
                next(reader)
                    
                """ get the selected sort order from the rating combobox """
                sort_order = self.combo_rating.get()
                
                """ define the sorting key based on the selected sort order and column """
                sort_key = lambda row: (float(row[7]), -float(row[7]))[sort_order == "Descending"]

                """ read the rows, filter and sort them, then insert them into the treeview """
                rows = [row for row in reader if (selected_noveltype == 'All' or row[4] == selected_noveltype) and \
                            (selected_genre == 'All' or row[5] == selected_genre) and \
                            (selected_librarystatus == 'All' or row[6] == selected_librarystatus)]
                
                sorted_rows = sorted(rows, key=sort_key)
                
                """ insert sorted rows into treeview """
                i = 0
                for row in sorted_rows:
                    if row[1] == username:
                        values = (row[0],
                                row[2],
                                row[3],
                                row[4],
                                row[5],
                                row[6],
                                row[7])
                        library_frame_treeview.insert("", i, values=values)
                        i += 1

        """ filter function when chaptercount is selected   """
        def filter_library_chaptercount(self, event):

            """ if the chaptercount selection is ascending/descending make rating selection to default """
            if self.combo_chaptercount.get() in ["Ascending", "Descending"]:
                self.combo_rating.current(0)
                
            """ get selected values from comboboxes, assign them as variables """
            selected_noveltype = self.combo_noveltype.get()
            selected_genre = self.combo_genre.get()
            selected_librarystatus = self.combo_librarystatus.get()
            
            """ remove contents of treeview """
            library_frame_treeview.delete(*library_frame_treeview.get_children())
            
            """ read the csv file as an iterable """
            with open("Novel_Note_Library.csv") as csvfile:
                reader = csv.reader(csvfile)
                
                """ skip the first row if both selections are 'All' """
                if selected_noveltype == 'All' and selected_genre == 'All' and selected_librarystatus == 'All':
                    next(reader)
                    
                """ get the selected sort order from the chaptercount combobox """
                sort_order = self.combo_chaptercount.get()
                
                """ define the sorting key based on the selected sort order and column """
                sort_key = lambda row: float(row[3]) if sort_order == "Ascending" else -float(row[3])
                
                """ read the rows, filter and sort them, then insert them into the treeview """
                rows = [row for row in reader if (selected_noveltype == 'All' or row[4] == selected_noveltype) and \
                            (selected_genre == 'All' or row[5] == selected_genre) and \
                            (selected_librarystatus == 'All' or row[6] == selected_librarystatus)]
                sorted_rows = sorted(rows, key=sort_key)
                i = 0
                for row in sorted_rows:
                    if row[1] == username:
                        values = (row[0],
                                row[2],
                                row[3],
                                row[4],
                                row[5],
                                row[6],
                                row[7])
                        library_frame_treeview.insert("", i, values=values)
                        i += 1

""" Window providing functionality to add/edit topnovel rankings """  
class TopNovelsEntry(customtkinter.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Top Novels")
            self.geometry("800x480")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the topnovel window as the foremost window """ 
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ entry fields/labels """
            novel_entry_1 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_1.place(relx=0.28, rely=0.25, relwidth=0.4, anchor="c")
            novel_entry_2 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_2.place(relx=0.28, rely=0.4, relwidth=0.4, anchor="c")
            novel_entry_3 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_3.place(relx=0.28, rely=0.55, relwidth=0.4, anchor="c")
            novel_entry_4 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_4.place(relx=0.28, rely=0.7, relwidth=0.4, anchor="c")
            novel_entry_5 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_5.place(relx=0.28, rely=0.85, relwidth=0.4, anchor="c")
            novel_entry_6 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_6.place(relx=0.72, rely=0.25, relwidth=0.4, anchor="c")
            novel_entry_7 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_7.place(relx=0.72, rely=0.4, relwidth=0.4, anchor="c")
            novel_entry_8 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_8.place(relx=0.72, rely=0.55, relwidth=0.4, anchor="c")
            novel_entry_9 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_9.place(relx=0.72, rely=0.7, relwidth=0.4, anchor="c")
            novel_entry_10 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_entry_10.place(relx=0.72, rely=0.85, relwidth=0.4, anchor="c")
            novel_label_1 = customtkinter.CTkLabel(self, text="Rank 1:", font=("Tahoma", 15,  "bold"))
            novel_label_1.place(relx=0.1,rely=0.14 ,anchor="nw")
            novel_label_2 = customtkinter.CTkLabel(self, text="Rank 2:", font=("Tahoma", 15,  "bold"))
            novel_label_2.place(relx=0.1,rely=0.29 ,anchor="nw")
            novel_label_3 = customtkinter.CTkLabel(self, text="Rank 3:", font=("Tahoma", 15,  "bold"))
            novel_label_3.place(relx=0.1,rely=0.44 ,anchor="nw")
            novel_label_4 = customtkinter.CTkLabel(self, text="Rank 4:", font=("Tahoma", 15,  "bold"))
            novel_label_4.place(relx=0.1,rely=0.59 ,anchor="nw")
            novel_label_5 = customtkinter.CTkLabel(self, text="Rank 5:", font=("Tahoma", 15,  "bold"))
            novel_label_5.place(relx=0.1,rely=0.74 ,anchor="nw")
            novel_label_6 = customtkinter.CTkLabel(self, text="Rank 6:", font=("Tahoma", 15,  "bold"))
            novel_label_6.place(relx=0.55,rely=0.14 ,anchor="nw")
            novel_label_7 = customtkinter.CTkLabel(self, text="Rank 7:", font=("Tahoma", 15,  "bold"))
            novel_label_7.place(relx=0.55,rely=0.29 ,anchor="nw")
            novel_label_8 = customtkinter.CTkLabel(self, text="Rank 8:", font=("Tahoma", 15,  "bold"))
            novel_label_8.place(relx=0.55,rely=0.44 ,anchor="nw")
            novel_label_9 = customtkinter.CTkLabel(self, text="Rank 9:", font=("Tahoma", 15,  "bold"))
            novel_label_9.place(relx=0.55,rely=0.59 ,anchor="nw")
            novel_label_10 = customtkinter.CTkLabel(self, text="Rank 10:", font=("Tahoma", 15,  "bold"))
            novel_label_10.place(relx=0.55,rely=0.74 ,anchor="nw")
            enter_topnovels = customtkinter.CTkLabel(self, text="Enter Top Novels:", font=("Tahoma", 25,  "bold"))
            enter_topnovels.place(relx=0.1,rely=0.045)
            
            """ save the entry to csv """
            def save_entry():
                
                """ reads the csv to dataframe """
                df = pd.read_csv("Novel_Note_Top_Novels.csv")

                """ removes rows from the dataframe where the username does not match """
                df = df[df['username'] != username]

                """ assign values of entry fields to variables """
                novel_1 = novel_entry_1.get()
                novel_2 = novel_entry_2.get()
                novel_3 = novel_entry_3.get()
                novel_4 = novel_entry_4.get()
                novel_5 = novel_entry_5.get()
                novel_6 = novel_entry_6.get()
                novel_7 = novel_entry_7.get()
                novel_8 = novel_entry_8.get()
                novel_9 = novel_entry_9.get()
                novel_10 = novel_entry_10.get()

                """ Create a new row as a list (from entry field values) """
                new_entry = [username, novel_1, novel_2, novel_3, novel_4, novel_5, novel_6, novel_7, novel_8, novel_9, novel_10]

                """ Add the new row to the Data Frame """
                df.loc[len(df)] = new_entry

                """ Save the updated DataFrame to the CSV file """
                df.to_csv("Novel_Note_Top_Novels.csv", index=False)
                
                """ call function """
                insert_topnovel()
                 
                """ destroy window  """          
                self.destroy()
            
            """ validation to save """
            def edit_topnovel():
                
                """ create message box whith options yes and no """
                msg = CTkMessagebox(title="Confirm Entry", message="Are you sure you would like to save these entries?", icon="warning", option_2 = "Yes", option_1 = "No", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                
                """ if option from messagebox is yes, begin save entry function, if no do nothing """
                if msg.get() == "Yes":
                    save_entry()
                else:
                    msg.destroy()
            
            """ create message box """
            def help():
                CTkMessagebox(title="Top Novel - Help", message="To add your top novels you must first type in the entry fields." + "\n" + "\n" + "-To save the entries to your ranking you must then select the 'Save Entry' button and follow the on screen prompts", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            
            """ destroy window """
            def close():
                self.destroy()
            
            """ buttons which call functions above """
            topnovel_help_button = customtkinter.CTkButton(self,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=help)
            topnovel_help_button.place(relx=0.88, rely=0.03, relwidth=0.05)       
            save_button = customtkinter.CTkButton(self, text="Save Entries", width=75, fg_color="#638619", border_width=2, border_color="#2B3418", hover_color="#4B5D24", command= edit_topnovel)
            save_button.place(relx=0.33, rely=0.94, anchor="c")
            cancel_button = customtkinter.CTkButton(self, text="Cancel", width=75, fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command=close)
            cancel_button.place(relx=0.66, rely=0.94, anchor="c")

""" Window providing functionality to add/edit topcharacter rankings """             
class TopCharactersEntry(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Top Characters")
            self.geometry("800x480")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the topcharacter window as the foremost window """
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ entry fields/labels """
            character_entry_1 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_1.place(relx=0.28, rely=0.25, relwidth=0.4, anchor="c")
            character_entry_2 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_2.place(relx=0.28, rely=0.4, relwidth=0.4, anchor="c")
            character_entry_3 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_3.place(relx=0.28, rely=0.55, relwidth=0.4, anchor="c")
            character_entry_4 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_4.place(relx=0.28, rely=0.7, relwidth=0.4, anchor="c")
            character_entry_5 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_5.place(relx=0.28, rely=0.85, relwidth=0.4, anchor="c")
            character_entry_6 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_6.place(relx=0.72, rely=0.25, relwidth=0.4, anchor="c")
            character_entry_7 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_7.place(relx=0.72, rely=0.4, relwidth=0.4, anchor="c")
            character_entry_8 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_8.place(relx=0.72, rely=0.55, relwidth=0.4, anchor="c")
            character_entry_9 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_9.place(relx=0.72, rely=0.7, relwidth=0.4, anchor="c")
            character_entry_10 = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Character Name...")
            character_entry_10.place(relx=0.72, rely=0.85, relwidth=0.4, anchor="c")
            character_label_1 = customtkinter.CTkLabel(self, text="Rank 1:", font=("Tahoma", 15,  "bold"))
            character_label_1.place(relx=0.1,rely=0.14 ,anchor="nw")
            character_label_2 = customtkinter.CTkLabel(self, text="Rank 2:", font=("Tahoma", 15,  "bold"))
            character_label_2.place(relx=0.1,rely=0.29 ,anchor="nw")
            character_label_3 = customtkinter.CTkLabel(self, text="Rank 3:", font=("Tahoma", 15,  "bold"))
            character_label_3.place(relx=0.1,rely=0.44 ,anchor="nw")
            character_label_4 = customtkinter.CTkLabel(self, text="Rank 4:", font=("Tahoma", 15,  "bold"))
            character_label_4.place(relx=0.1,rely=0.59 ,anchor="nw")
            character_label_5 = customtkinter.CTkLabel(self, text="Rank 5:", font=("Tahoma", 15,  "bold"))
            character_label_5.place(relx=0.1,rely=0.74 ,anchor="nw")
            character_label_6 = customtkinter.CTkLabel(self, text="Rank 6:", font=("Tahoma", 15,  "bold"))
            character_label_6.place(relx=0.55,rely=0.14 ,anchor="nw")
            character_label_7 = customtkinter.CTkLabel(self, text="Rank 7:", font=("Tahoma", 15,  "bold"))
            character_label_7.place(relx=0.55,rely=0.29 ,anchor="nw")
            character_label_8 = customtkinter.CTkLabel(self, text="Rank 8:", font=("Tahoma", 15,  "bold"))
            character_label_8.place(relx=0.55,rely=0.44 ,anchor="nw")
            character_label_9 = customtkinter.CTkLabel(self, text="Rank 9:", font=("Tahoma", 15,  "bold"))
            character_label_9.place(relx=0.55,rely=0.59 ,anchor="nw")
            character_label_10 = customtkinter.CTkLabel(self, text="Rank 10:", font=("Tahoma", 15,  "bold"))
            character_label_10.place(relx=0.55,rely=0.74 ,anchor="nw")
            enter_topcharacters = customtkinter.CTkLabel(self, text="Enter Top Characters:", font=("Tahoma", 25,  "bold"))
            enter_topcharacters.place(relx=0.1,rely=0.045)
            
            """ save the entry to csv """
            def save_entry():
                
                """ reads the csv to dataframe """
                df = pd.read_csv("Novel_Note_Top_Characters.csv")
    
                """ removes rows from the dataframe where the username does not match """
                df = df[df['username'] != username]
                
                """ assign values of entry fields to variables """
                character_1 = character_entry_1.get()
                character_2 = character_entry_2.get()
                character_3 = character_entry_3.get()
                character_4 = character_entry_4.get()
                character_5 = character_entry_5.get()
                character_6 = character_entry_6.get()
                character_7 = character_entry_7.get()
                character_8 = character_entry_8.get()
                character_9 = character_entry_9.get()
                character_10 = character_entry_10.get()

                """ Create a new row as a list (from entry field values) """
                new_entry = [username, character_1, character_2, character_3, character_4, character_5, character_6, character_7, character_8, character_9, character_10]

                """ Add the new row to the Data Frame """
                df.loc[len(df)] = new_entry

                """ Save the updated DataFrame to the CSV file """
                df.to_csv("Novel_Note_Top_Characters.csv", index=False)

                """ call function """
                insert_topcharacter()
                           
                """ destroy window  """ 
                self.destroy()
            
            """ validation to save """
            def edit_topcharacter():
                
                """ create message box whith options yes and no """
                msg = CTkMessagebox(title="Confirm Entry", message="Are you sure you would like to save these entries?", icon="warning", option_2 = "Yes", option_1 = "No", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                
                """ if option from messagebox is yes, begin save entry function, if no do nothing """
                if msg.get() == "Yes":
                    save_entry()
                else:
                    msg.destroy()   
            
            """ create message box """ 
            def help():
                CTkMessagebox(title="Top Character - Help", message="To add your top characters you must first type in the entry fields." + "\n" + "\n" + "-To save the entries to your ranking you must then select the 'Save Entry' button and follow the on screen prompts", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            
            """ destroy window  """
            def close():
                self.destroy()
             
            """ buttons which call functions above """            
            topcharacter_help_button = customtkinter.CTkButton(self,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=help)
            topcharacter_help_button.place(relx=0.88, rely=0.03, relwidth=0.05)             
            save_button = customtkinter.CTkButton(self, text="Save Entries", width=75, fg_color="#638619", border_width=2, border_color="#2B3418", hover_color="#4B5D24", command= edit_topcharacter)
            save_button.place(relx=0.33, rely=0.94, anchor="c")
            cancel_button = customtkinter.CTkButton(self, text="Cancel", width=75, fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command=close)
            cancel_button.place(relx=0.66, rely=0.94, anchor="c")

""" Window providing functionality to view quote"""
class ViewQuotesEntry(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("View Quote")
            self.geometry("500x500")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the view quote window as the foremost window """
            self.lift()
            self.attributes("-topmost", True)
            
            """ selected_quote_view variable (a row of the quote treeview) """
            global selected_quote_view
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ create a variable from the items in selected_quote_view """
            values = quotes_frame_treeview.item(selected_quote_view, 'values')
            
            """ labels/textboxes (selected data is inserted)"""
            title_quotes = customtkinter.CTkLabel(self, text="Quote:", font=("Tahoma", 20,  "bold"))
            title_quotes.place(relx=0.05, rely=0.05, anchor="nw")
            novel_title_quotes = customtkinter.CTkLabel(self, text="Novel Title:", font=("Tahoma", 15,  "bold"))
            novel_title_quotes.place(relx=0.05, rely=0.15, anchor="nw")
            novel_text_quotes = customtkinter.CTkTextbox(self, width=420, height=40, corner_radius=0, activate_scrollbars=True, wrap='char')
            novel_text_quotes.place(relx=0.08, rely=0.21, anchor="nw")
            novel_text_quotes.insert("0.0", values[1])
            character_title_quotes = customtkinter.CTkLabel(self, text="Character's Name:", font=("Tahoma", 15,  "bold"))
            character_title_quotes.place(relx=0.05, rely=0.30, anchor="nw")
            character_text_quotes = customtkinter.CTkTextbox(self, width=420, height=40, corner_radius=0, activate_scrollbars=True, wrap='char')
            character_text_quotes.place(relx=0.08, rely=0.36, anchor="nw")
            character_text_quotes.insert("0.0", values[2])
            quotes_title_quotes = customtkinter.CTkLabel(self, text="Quote:", font=("Tahoma", 15,  "bold"))
            quotes_title_quotes.place(relx=0.05, rely=0.45, anchor="nw")
            quote_text_quotes = customtkinter.CTkTextbox(self, width=420, height=200, corner_radius=0, activate_scrollbars=True, wrap='char')
            quote_text_quotes.place(relx=0.08, rely=0.51, anchor="nw")
            quote_text_quotes.insert("0.0", values[3])
            
            """ create message box """
            def help():
                CTkMessagebox(title="View Quote - Help", message="This screen allows you to simply view your quote entries" + "\n" + "-Any changes to the contents of each textbox will not be reflected in the library.", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            
            """ button calling help function """
            quotes_help_button = customtkinter.CTkButton(self,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=help)
            quotes_help_button.place(relx=0.88, rely=0.03, relwidth=0.1)

""" Window providing functionality to view novel"""
class ViewLibraryEntry(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("View Entry")
            self.geometry("500x500")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the view library window as the foremost window """
            self.lift()
            self.attributes("-topmost", True)
            
            """selected_library_view variable (a row of the library treeview) """
            global selected_library_view
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ create a variable from the items in selected_library_view """
            values = library_frame_treeview.item(selected_library_view, 'values')
            
            """ labels/textboxes (selected data is inserted)"""
            title_library = customtkinter.CTkLabel(self, text="Novel Entry:", font=("Tahoma", 20,  "bold"))
            title_library.place(relx=0.05, rely=0.05, anchor="nw")
            library_novel_title_label = customtkinter.CTkLabel(self, text="Novel Title:", font=("Tahoma", 15,  "bold"))
            library_novel_title_label.place(relx=0.05, rely=0.15, anchor="nw")
            library_novel_title = customtkinter.CTkTextbox(self, width=420, height=40, corner_radius=0, activate_scrollbars=True, wrap='char')
            library_novel_title.place(relx=0.08, rely=0.21, anchor="nw")
            library_novel_title.insert("0.0", values[1])
            library_chapter_count_label = customtkinter.CTkLabel(self, text="Chapter Count:", font=("Tahoma", 15,  "bold"))
            library_chapter_count_label.place(relx=0.05, rely=0.3, anchor="nw")
            library_chapter_count = customtkinter.CTkTextbox(self, width=420, height=20, corner_radius=0, activate_scrollbars=True, wrap='char')
            library_chapter_count.place(relx=0.08, rely=0.36, anchor="nw")
            library_chapter_count.insert("0.0", values[2])
            library_novel_type_label = customtkinter.CTkLabel(self, text="Novel Type:", font=("Tahoma", 15,  "bold"))
            library_novel_type_label.place(relx=0.05, rely=0.42, anchor="nw")
            library_novel_type = customtkinter.CTkTextbox(self, width=420, height=20, corner_radius=0, activate_scrollbars=True, wrap='char')
            library_novel_type.place(relx=0.08, rely=0.48, anchor="nw")
            library_novel_type.insert("0.0", values[3])
            library_genre_label = customtkinter.CTkLabel(self, text="Genre:", font=("Tahoma", 15,  "bold"))
            library_genre_label.place(relx=0.05, rely=0.54, anchor="nw")
            library_genre = customtkinter.CTkTextbox(self, width=420, height=20, corner_radius=0, activate_scrollbars=True, wrap='char')
            library_genre.place(relx=0.08, rely=0.6, anchor="nw")
            library_genre.insert("0.0", values[4])
            library_status_label = customtkinter.CTkLabel(self, text="Library Staus:", font=("Tahoma", 15,  "bold"))
            library_status_label.place(relx=0.05, rely=0.67, anchor="nw")
            library_status = customtkinter.CTkTextbox(self, width=420, height=20, corner_radius=0, activate_scrollbars=True, wrap='char')
            library_status.place(relx=0.08, rely=0.72, anchor="nw")
            library_status.insert("0.0", values[5])
            library_rating_label = customtkinter.CTkLabel(self, text="Rating:", font=("Tahoma", 15,  "bold"))
            library_rating_label.place(relx=0.05, rely=0.78, anchor="nw")
            library_rating = customtkinter.CTkTextbox(self, width=420, height=20, corner_radius=0, activate_scrollbars=True, wrap='char')
            library_rating.place(relx=0.08, rely=0.84, anchor="nw")
            library_rating.insert("0.0", values[6] + " / 10.0")
            
            """ create message box """
            def help():
                CTkMessagebox(title="View Novel - Help", message="This screen allows you to simply view your novel entries" + "\n" + "-Any changes to the contents of each textbox will not be reflected in the library.", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            
            """ button calling help function """
            library_help_button = customtkinter.CTkButton(self,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=help)
            library_help_button.place(relx=0.88, rely=0.03, relwidth=0.1)

""" Window providing functionality to add novel to library (from premade list) """ 
class AddPremadeEntry(customtkinter.CTkToplevel):
        global username
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Add Entry")
            self.geometry("350x550")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)  
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the addpremadeentry window as the foremost window """
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ selected_premade variable (a row of the premadelibrary treeview) """
            global selected_premade
            values = search_frame_treeview.item(selected_premade, 'values')
            
            """ entry fields/option menus """
            novel_title_entry_library = customtkinter.CTkEntry(self,fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Novel Title...")
            novel_title_entry_library.place(relx=0.5, rely=0.21, relwidth=0.8, anchor="n")
            chapter_count_entry_library = customtkinter.CTkEntry(self, fg_color="#170830", border_color="#574379", text_color="white", placeholder_text_color="white", placeholder_text="Enter Chapter Count...")
            chapter_count_entry_library.place(relx=0.5, rely=0.33, relwidth=0.8, anchor="n")
            novel_type_entry_library = customtkinter.CTkOptionMenu(self, fg_color="#1F1037", button_color="#35284A", button_hover_color="#170830", dropdown_fg_color="#110425", dropdown_hover_color="#1F1037", values=["Manhwa", "Manhua", "Manga", "English Novel", "Chinese Novel", "Korean Novel", "Japanese Novel"])
            novel_type_entry_library.place(relx=0.5, rely=0.45, relwidth=0.8, anchor="n")
            genre_entry_library = customtkinter.CTkOptionMenu(self, fg_color="#1F1037", button_color="#35284A", button_hover_color="#170830", dropdown_fg_color="#110425", dropdown_hover_color="#1F1037", values=["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Historical", "Horror", "Isekai", "Korean Dungeon", "Murim", "Mystery", "Otome Isekai", "Romance", "Sports", "Thriller", "Xianxia", "Xuanhuan"])
            genre_entry_library.place(relx=0.5, rely=0.57, relwidth=0.8, anchor="n")
            status_entry_library = customtkinter.CTkOptionMenu(self, fg_color="#1F1037", button_color="#35284A", button_hover_color="#170830", dropdown_fg_color="#110425", dropdown_hover_color="#1F1037", values=["Currently Reading", "Plan to Read", "Completed", "On Hold", "Dropped"])
            status_entry_library.place(relx=0.5, rely=0.69, relwidth=0.8, anchor="n")
            rating_entry_library = customtkinter.CTkEntry(self, justify=CENTER,fg_color="#170830", border_color="#574379", text_color="white")
            rating_entry_library.insert(0, float("1")) 
            rating_entry_library.configure(state="disabled")
            rating_entry_library.place(relx=0.5, rely=0.81, relwidth=0.8, anchor="n")
            novel_title_entry_library.insert(0, values[0])

            """ saves entry to csv """
            def add_novel():

                """ create variables of entered data """
                novel_title = novel_title_entry_library.get()
                chapter_count = chapter_count_entry_library.get()
                novel_type = novel_type_entry_library.get()
                genre = genre_entry_library.get()
                status = status_entry_library.get()
                rating = rating_entry_library.get()
                id = str(uuid4())

                """ Check if any of the fields is empty, if yes display error """
                if not all([novel_title, chapter_count, novel_type, genre, status, rating]):
                    field_error()
                    return

                """ write entry to csv """
                with open("Novel_Note_Library.csv", mode="a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([id, username, novel_title, chapter_count, novel_type, genre, status, rating])

                """ call functions """
                insert_library()
                initialize_stats()
                
                """ destroy the window """
                self.destroy()
            
            """ validation to save """
            def confirm_add():
                
                """ create message box whith options yes and no """
                msg = CTkMessagebox(title="Confirm Entry", message="Are you sure you would like to save these entries?", icon="warning", option_2 = "Yes", option_1 = "No", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
                
                """ if option from messagebox is yes, begin save entry function, if no do nothing """
                if msg.get() == "Yes":
                    add_novel()
                else:
                    msg.destroy() 
            
            """ destroy the window """
            def close():
                self.destroy()
                
            """ create message box """
            def help():
                CTkMessagebox(title="Add Novel - Help", message="To add a novel you must first type in the entry fields and select suitable options by clicking on the entry boxes." + "\n" + "\n" + "-To save the novel to your library you must then select the 'Save Entry' button once all fields are full", cancel_button="cross",fg_color="#0E0B13", bg_color="#0A0410", border_color="white", button_width=100, button_color="#638619", button_hover_color="#4B5D24")
            
            """ buttons/labels """
            button_library_cancel = customtkinter.CTkButton(self, text="Cancel", width=100, fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command=close)
            button_library_cancel.place(relx=0.66, rely=0.9, anchor="n")
            button_library_save = customtkinter.CTkButton(self, text="Save Entry", width=100, fg_color="#638619", border_width=2, border_color="#2B3418", hover_color="#4B5D24", command=confirm_add)
            button_library_save.place(relx=0.33, rely=0.9, anchor="n")
            library_help_button = customtkinter.CTkButton(self,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=help)
            library_help_button.place(relx=0.88, rely=0.03, relwidth=0.1)
            library_title_label = customtkinter.CTkLabel(self,text="Novel Title:", font=("Tahoma", 20,  "bold"))
            library_title_label.place(relx=0.1,rely=0.15)
            library_chapter_count_label =customtkinter.CTkLabel(self, text="Chapter Count:", font=("Tahoma", 20,  "bold"))
            library_chapter_count_label.place(relx=0.1,rely=0.27)
            library_novel_type_label = customtkinter.CTkLabel(self, text="Novel Type:",font=("Tahoma", 20,  "bold"))
            library_novel_type_label.place(relx=0.1,rely=0.39)
            library_genre_label = customtkinter.CTkLabel(self, text="Genre:",font=("Tahoma", 20,  "bold"))
            library_genre_label.place(relx=0.1,rely=0.51)
            library_library_status_label = customtkinter.CTkLabel(self, text="Library Status:", font=("Tahoma", 20,  "bold"))
            library_library_status_label.place(relx=0.1,rely=0.63)
            library_rating_label = customtkinter.CTkLabel(self, text="Rating:",font=("Tahoma", 20,  "bold"))
            library_rating_label.place(relx=0.1,rely=0.75)
            library_title_label = customtkinter.CTkLabel(self,text="Add Entry:",font=("Tahoma", 30,  "bold"))
            library_title_label.place(relx=0.1,rely=0.045)   
            
            """ increases rating entrybox values by 1 (0-10)"""
            def add_1_0():
                value = float(rating_entry_library.get())
                if value < 10:
                    value += 1
                    rating_entry_library.configure(state="normal")
                    rating_entry_library.delete(0, 'end')
                    rating_entry_library.insert(0, value)
                    rating_entry_library.configure(state="disabled")
            
            """ decreases rating entrybox values by 1 (0-10) """
            def subtract_1_0():
                value = float(rating_entry_library.get())
                if value > 0:
                    value -= 1
                    rating_entry_library.configure(state="normal")
                    rating_entry_library.delete(0, 'end')
                    rating_entry_library.insert(0, value)
                    rating_entry_library.configure(state="disabled")

            """ buttons to decrease/increase rating """
            library_addone_button = customtkinter.CTkButton(rating_entry_library, text="+", width=2, fg_color="#1F044C", border_width=2,border_color="#574379", hover_color="#170830", command=add_1_0)
            library_addone_button.place(relx=1,rely=0.5, anchor="e")
            library_subtractone_button = customtkinter.CTkButton(rating_entry_library, text="-", width=2, fg_color="#1F044C", border_width=2,border_color="#574379", hover_color="#170830", command=subtract_1_0)
            library_subtractone_button.place(relx=0.0,rely=0.5, anchor="w")   

""" Window providing functionality to view user and logout""" 
class Profile(customtkinter.CTkToplevel):
    def __init__(self,frames_instance, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Profile")
            self.geometry("350x100")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the profile window as the foremost window """
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ assign instance of Frames class as local variable """
            self.frames_instance = frames_instance
            
            """ label/button """
            username_label = customtkinter.CTkLabel(self, text="Username: " + username, font=("Tahoma", 20,  "bold"))
            username_label.place(relx=0.05, rely=0.3, anchor="w")
            logout_button = customtkinter.CTkButton(self, text="Logout", width=75, fg_color="#C62020", border_width=2, border_color="#7C1414", hover_color="#951818", command=self.restart)
            logout_button.place(relx=0.5, rely=0.8, anchor="c")    
      
    """ the following function was found at the webiste at this link: https://stackoverflow.com/questions/48267348/how-to-unconditionally-re-run-a-python-program-based-on-button-click      """ 
    def restart(self):
            frames.destroy()
            command = '"{}" "{}" "{}"'.format(
                sys.executable,             # Python interpreter
                __file__,                   # argv[0] - this file
                os.path.basename(__file__), # argv[1] - this file without path
            )
            try:
                subprocess.Popen(command)
            except Exception:
                traceback.print_exc()
                sys.exit('fatal error occurred rerunning script')
            else:
                self.quit()        

""" Window displaying quote screen help """
class MainQuoteHelp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Help - Quote")
            self.geometry("450x400")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the mainquotehelp window as the foremost window """  
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ labels """
            title1 = customtkinter.CTkLabel(self, text="Welcome to Novel Note's Quotes Page")
            title1.place(relx=0.05, rely=0.1, anchor="w")
            title2 = customtkinter.CTkLabel(self, text="Getting Started:")
            title2.place(relx=0.05, rely=0.2, anchor="w")
            title3 = customtkinter.CTkLabel(self, text="1) At the top of the tab is a search bar with the text 'Search Quotes...'." + "\n" + "     Type in here to filter the below quotes by the search text", justify="left")
            title3.place(relx=0.05, rely=0.3, anchor="w")
            title4 = customtkinter.CTkLabel(self, text="2) To the right of the search bar are 4 buttons. 'Add Entry', 'Edit Entry'," + "\n" + "     'View Entry' and '?'" + "\n" + "     - Pressing any of these buttons will open a window associated with" + "\n" + "      the buttons title", justify="left")
            title4.place(relx=0.05, rely=0.45, anchor="w")
            title5 = customtkinter.CTkLabel(self, text="3) Below the buttons and search bar is a table featuring your quote" + "\n" + "     entries. You may simply preview the quotes, or select a row of the" + "\n" + "     table (a single entry). Once a row is selected you may press the edit" + "\n" + "      or view buttons to acces their functions.", justify="left")
            title5.place(relx=0.05, rely=0.63, anchor="w")

""" Window displaying library screen help """
class MainLibraryHelp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Help - Library")
            self.geometry("450x400")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
             
            """ sets the mainlibraryhelp window as the foremost window """   
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ labels """
            title1 = customtkinter.CTkLabel(self, text="Welcome to Novel Note's Library Page")
            title1.place(relx=0.05, rely=0.1, anchor="w")
            title2 = customtkinter.CTkLabel(self, text="Getting Started:")
            title2.place(relx=0.05, rely=0.2, anchor="w")
            title3 = customtkinter.CTkLabel(self, text="1) At the top of the tab is a search bar with the text 'Search Library...'." + "\n" + "     Type in here to filter the below novels by the search text", justify="left")
            title3.place(relx=0.05, rely=0.3, anchor="w")
            title4 = customtkinter.CTkLabel(self, text="2) To the right of the search bar are 5 buttons. 'Filter' 'Add Entry', " + "\n" + "     'Edit Entry', 'View Entry' and '?'" + "\n" + "     - Pressing any of these buttons will open a window associated with" + "\n" + "      the buttons title", justify="left")
            title4.place(relx=0.05, rely=0.45, anchor="w")
            title5 = customtkinter.CTkLabel(self, text="3) Below the buttons and search bar is a table featuring your novel" + "\n" + "     entries. You may simply preview the library, or select a row of the" + "\n" + "     table (a single entry). Once a row is selected you may press the edit" + "\n" + "      or view buttons to acces their functions.", justify="left")
            title5.place(relx=0.05, rely=0.63, anchor="w")

""" Window displaying stats screen help """
class MainStatsHelp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Help - Stats")
            self.geometry("450x400")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
                
            """ sets the mainstatshelp window as the foremost window """    
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ labels """
            title1 = customtkinter.CTkLabel(self, text="Welcome to Novel Note's Stats Page")
            title1.place(relx=0.05, rely=0.1, anchor="w")
            title2 = customtkinter.CTkLabel(self, text="Getting Started:")
            title2.place(relx=0.05, rely=0.2, anchor="w")
            title3 = customtkinter.CTkLabel(self, text="1) At the centre of the tab is a box holding charts which detail your  " + "\n" + "     account's statistics." + "\n" + "\n" + "      -You can switch the chart type through the drop down box towards" + "\n" + "       the bottom right of the screen.", justify="left")
            title3.place(relx=0.05, rely=0.3, anchor="nw")

""" Window displaying home screen help """
class MainHomeHelp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Help - Home")
            self.geometry("450x400")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the mainhomehelp window as the foremost window """    
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ labels """
            title1 = customtkinter.CTkLabel(self, text="Welcome to Novel Note's Home Page")
            title1.place(relx=0.05, rely=0.1, anchor="w")
            title2 = customtkinter.CTkLabel(self, text="Getting Started:")
            title2.place(relx=0.05, rely=0.2, anchor="w")
            title3 = customtkinter.CTkLabel(self, text="1) You are currently on the home page of Novel Note. At the top of the" + "\n" + "     application is a taskbar with buttons." + "\n" + "\n" + "      -Pressing a button will navigate you to the associated tab." + "\n" + "\n" + "      -Typing in the search bar will navigate you to a premade library from" + "\n" + "       which you can add novels.", justify="left")
            title3.place(relx=0.05, rely=0.3, anchor="nw")
            title4 = customtkinter.CTkLabel(self, text="2) The top of the tab houses a table which shows the 5 most recent" + "\n" + "      entries to your novel library", justify="left")
            title4.place(relx=0.05, rely=0.6, anchor="nw")
            title5 = customtkinter.CTkLabel(self, text="3) Below are two tables showing your ten favourite novels and characters" + "\n" + "\n" + "       -Pressing on the 'Edit Entries' buttons will allows you to change" + "\n" + "        what is included in these top ten.", justify="left")
            title5.place(relx=0.05, rely=0.6, anchor="nw")

""" Window displaying search screen help """
class MainSearchHelp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            """ create/style window """
            self.title("Help - Search")
            self.geometry("450x400")
            self.configure(fg_color="#0A0410")
            self.resizable(False,False)
            if platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap("icon.ico"))
            
            """ sets the mainsearchhelp window as the foremost window """    
            self.lift()
            self.attributes("-topmost", True)
            
            """ Change the colour of the control bar/text of the window """
            HWND = windll.user32.GetParent(self.winfo_id())
            title_bar_color = 655376
            title_text_color = 16777215
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
            
            """ labels """
            title1 = customtkinter.CTkLabel(self, text="Welcome to Novel Note's Search Page")
            title1.place(relx=0.05, rely=0.1, anchor="w")
            title2 = customtkinter.CTkLabel(self, text="Getting Started:")
            title2.place(relx=0.05, rely=0.2, anchor="w")
            title3 = customtkinter.CTkLabel(self, text="1) At the top of the screen is a search bar with the text 'Search Novel...'." + "\n" + "     Type in here to filter the below novels by the search text", justify="left")
            title3.place(relx=0.05, rely=0.3, anchor="w")
            title4 = customtkinter.CTkLabel(self, text="2) To the top right of the tab are 2 buttons. 'Add Entry' and '?'. " + "\n" + "     - Pressing any of these buttons will open a window associated with" + "\n" + "      the buttons title", justify="left")
            title4.place(relx=0.05, rely=0.45, anchor="w")




""" Primary window """



class Frames(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        global username, search_frame_treeview, home_frame_treeview_recent, home_frame_treeview_character, home_frame_treeview_novel, quotes_frame_treeview, library_frame_treeview, stats_frame, toplevel_window
        
        """ create window """
        self.title("Novel Note")
        self.geometry(f"{900}x{600}")
        self.configure(fg_color="#0A0410")
        self.resizable(False,False)
        self.iconbitmap("icon.ico")
        self.withdraw
        
        """ change the color of the window topbar and topbar text """
        HWND = windll.user32.GetParent(self.winfo_id())
        title_bar_color = 655376
        title_text_color = 16777215
        windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int))
        windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(title_text_color)), sizeof(c_int))
         
        
        """ Search Functions """
         
         
        """ search premade library by entered text """
        def on_entry_change(*args):
            
            """  once text is entered switch frame to search frame """
            self.select_frame_by_name("search")
            
            """ open csv file as iterable and create search_text variable from entered text """
            search_text = search_entry.get().lower()
            with open("Premade_List_2.csv", newline='', encoding='utf8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  #Skip the first row (header of the csv)
                
                """ create a matching_rows varaiable filled with rows from iterable including search text (if no search text then include all rows). include rows only if they match username """
                if search_text:
                    matching_rows = [row for row in reader if any(search_text in str(cell).lower() for cell in row)]
                else:
                    matching_rows = [row for row in reader]
                    
            """ remove contents of treeview, then insert matching_rows into treeview """
            for i in search_frame_treeview.get_children():
                search_frame_treeview.delete(i)
            for row in matching_rows:
                updated_row=[row[0]]
                search_frame_treeview.insert("", "end", values=updated_row)
        
        """ search quotes library by entered text """
        def search_quotes_treeview(event):
            
            """ open csv file as iterable and create search_text variable from entered text """
            search_text = quotes_search_bar.get().lower()
            with open("Novel_Note_Quotes.csv", newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the first row (header of csv)
                
                """ create a matching_rows varaiable filled with rows from iterable including search text (if no search text then include all rows). include rows only if they match username """
                if search_text:
                    matching_rows = [row for row in reader if any(search_text in str(cell).lower() for cell in row[2:]) and row[1] == username]
                else: 
                    matching_rows = [row for row in reader if row[1]==username]
                    
            """ remove contents of treeview, then insert matching_rows into treeview """
            for i in quotes_frame_treeview.get_children():
                quotes_frame_treeview.delete(i)
            for row in matching_rows:
                updated_row=[row[0], row[2], row[3], row[4]]
                quotes_frame_treeview.insert("", "end", values=updated_row)
        
        """ search novel library by entered text """
        def search_library_treeview(event):
            
            """ open csv file as iterable and create search_text variable from entered text """
            search_text = library_search_bar.get().lower()
            with open("Novel_Note_Library.csv", newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  #Skip the first row (header of csv)
                
                """ create a matching_rows varaiable filled with rows from iterable including search text (if no search text then include all rows). include rows only if they match username """
                if search_text:
                    matching_rows = [row for row in reader if any(search_text in str(cell).lower() for cell in row[2:]) and row[1] == username]
                else:
                    matching_rows = [row for row in reader if row[1]==username]
                    
            """ remove contents of treeview, then insert matching_rows into treeview """
            for i in library_frame_treeview.get_children():
                library_frame_treeview.delete(i)
            for row in matching_rows:
                updated_row=[row[0], row[2], row[3], row[4], row[5], row[6], row[7]]
                library_frame_treeview.insert("", "end", values=updated_row)
        
        
        """ Topbar Frame """
        
        
        """ create and place topbar frame onto window """    
        self.topbar_frame = customtkinter.CTkFrame (self, width=900, height=500, fg_color="#0E0B13")
        self.topbar_frame.grid(row=0, column=0, columnspan=6, rowspan=1, sticky="n", pady=(0,10))
        
        """ import logo image """
        logo_img = Image.open("Novel_Note_Logo(white).png")
        logo_img_resized = logo_img.resize((80, 15), Image.ANTIALIAS)
        logo_img_final = ImageTk.PhotoImage(logo_img_resized)
        
        """ create and place frame buttons onto topbar frame """
        home_button = customtkinter.CTkButton(self.topbar_frame, width=100, height= 35, text="", image=logo_img_final, border_width=2,border_color="#574379", hover_color="#170830",fg_color="#1F044C", command=self.home_button_event)
        home_button.grid(row=0, column=0, padx=(100,5), pady=10)
        quotes_button = customtkinter.CTkButton(self.topbar_frame, width=100, height= 35, text="Quotes", fg_color="#1F044C",border_width=2,border_color="#574379",hover_color="#170830", command=self.quotes_button_event)
        quotes_button.grid(row=0, column=1, padx=5, pady=10)
        library_button = customtkinter.CTkButton(self.topbar_frame, width=100, height= 35, text="Library", fg_color="#1F044C",border_width=2,border_color="#574379",hover_color="#170830", command=self.library_button_event)
        library_button.grid(row=0, column=2, padx=5, pady=10)
        stats_button = customtkinter.CTkButton(self.topbar_frame, width=100, height= 35, text="Stats", fg_color="#1F044C",border_width=2,border_color="#574379",hover_color="#170830", command=self.stats_button_event)
        stats_button.grid(row=0, column=3, padx=5, pady=10)
        search_entry = customtkinter.CTkEntry(self.topbar_frame, width=200, height= 35,fg_color="#170830", border_color="#574379", text_color="white",placeholder_text_color="white", placeholder_text="Search Novel...")
        search_entry.grid(row=0,column=4, padx=5, pady=10)
        profile_button = customtkinter.CTkButton(self.topbar_frame, width=50, height= 35, fg_color="#1F044C",border_width=2,border_color="#574379",hover_color="#170830", text="Profile", command=self.open_Profile)
        profile_button.grid(row=0, column=5, pady=10, padx=(5,100))
        
        """ when text is entered in search entry box call the on_entry_change function  """ 
        search_entry.bind("<KeyRelease>", on_entry_change, '+')


        """ Home Frame  """       
        
        
        """ create and place home frame onto window """
        self.home_frame = customtkinter.CTkFrame(self, height=525, width=880, fg_color="#0E0B13")
        self.home_frame.grid(row=1, column=1, columnspan=6, rowspan=1, sticky="nsew", padx=(10, 10), pady=(0, 10))

        """ create styling for recent treeview """
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", background="#CEC9D2", foreground="black", fieldbackground="#F3F2F2", relief="sunken", rowheight=50)
        style.map('Treeview', background=[('selected', '#575B59')])

        """ create and place recent treeview onto home frame """
        home_frame_treeview_recent = ttk.Treeview(self.home_frame, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", style="Treeview")
        home_frame_treeview_recent.place(relx=0.5, rely=0.1, relwidth=0.95, relheight=0.3, anchor="n")
        home_frame_treeview_recent.bind('<Motion>', 'break')
        home_frame_treeview_recent.heading("1",text="")
        home_frame_treeview_recent.column("1",width=0, stretch=0)
        home_frame_treeview_recent.heading("2",text="Title")
        home_frame_treeview_recent.column("2",width=200)
        home_frame_treeview_recent.heading("3",text="Chapter Count")
        home_frame_treeview_recent.column("3",width=90)
        home_frame_treeview_recent.heading("4",text="Novel Type")
        home_frame_treeview_recent.column("4",width=130)
        home_frame_treeview_recent.heading("5",text="Genre")
        home_frame_treeview_recent.column("5",width=150)
        home_frame_treeview_recent.heading("6",text="Library Status")
        home_frame_treeview_recent.column("6",width=185)
        home_frame_treeview_recent.heading("7",text="Rating")
        home_frame_treeview_recent.column("7",width=75)

        """ create and place topnovel treeview onto home frame """
        home_frame_treeview_novel = ttk.Treeview(self.home_frame, columns=(1), show="headings")
        home_frame_treeview_novel.place(relx=0.48, rely=0.5, relwidth=0.36, relheight=0.46, anchor="ne")
        home_frame_treeview_novel.heading("1", text="Novel Title")
        home_frame_treeview_novel.column("1", width="200")

        """ create and place topnovel label treeview onto home frame """
        home_frame_treeview_novel_label=ttk.Treeview(self.home_frame, columns=(1),show="headings")
        home_frame_treeview_novel_label.place(relx= 0.02,rely=0.5 ,relwidth=0.1 ,relheight=0.46, anchor="nw")
        home_frame_treeview_novel_label.heading("1",text="Rank")
        home_frame_treeview_novel_label.column("1",width="25")
        
        """ place numbers 1-10 in each row of topnovel label treeview """
        numbers = list(range(1, 11))
        for index, number in enumerate(numbers):
            home_frame_treeview_novel_label.insert('', 'end', text=index, values=(number))

        """ create and place topcharacter treeview onto home frame """
        home_frame_treeview_character=ttk.Treeview(self.home_frame, columns=(1),show="headings", style="My.Treeview")
        home_frame_treeview_character.place(relx=0.98,rely=0.5,relwidth=0.36,relheight=0.46, anchor="ne")
        home_frame_treeview_character.heading("1",text="Novel Title")
        home_frame_treeview_character.column("1",width="200")
        
        """ create and place topcharacter label treeview onto home frame """
        home_frame_treeview_character_label=ttk.Treeview(self.home_frame, columns=(1),show="headings", style="My.Treeview")
        home_frame_treeview_character_label.place(relx= 0.52,rely=0.5 ,relwidth=0.1 ,relheight=0.46, anchor="nw")
        home_frame_treeview_character_label.heading("1",text="Rank")
        home_frame_treeview_character_label.column("1",width="25")
        
        """ place numbers 1-10 in each row of topcharacter label treeview """
        numbers = list(range(1, 11))
        for index, number in enumerate(numbers):
            home_frame_treeview_character_label.insert('', 'end', text=index, values=(number))
        
        """ create and place labels and help/edit buttons onto home frame """
        home_recent_title = customtkinter.CTkLabel(self.home_frame, text="Recent Entries:", font=("Tahoma", 20,  "bold"))
        home_recent_title.place(relx=0.05, rely=0.03, anchor='nw')
        home_recent_novels = customtkinter.CTkLabel(self.home_frame, text="Top Novels:", font=("Tahoma", 20,  "bold"))
        home_recent_novels.place(relx=0.05, rely=0.43, anchor='nw')
        home_recent_characters = customtkinter.CTkLabel(self.home_frame, text="Top Characters:", font=("Tahoma", 20,  "bold"))
        home_recent_characters.place(relx=0.55, rely=0.43, anchor='nw')
        home_topnovels_button = customtkinter.CTkButton(self.home_frame,text="Edit Entries", fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command= self.open_TopNovelsEntry)
        home_topnovels_button.place(relx=0.48, rely=0.49, relwidth=0.086, anchor="se")
        home_topcharacters_button = customtkinter.CTkButton(self.home_frame,text="Edit Entries", fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command= self.open_TopCharactersEntry)
        home_topcharacters_button.place(relx=0.98, rely=0.49, relwidth=0.086, anchor="se")
        home_help_button = customtkinter.CTkButton(self.home_frame,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=self.open_MainHomeHelp)
        home_help_button.place(relx=0.925, rely=0.03, relwidth=0.043)
        
        
        """ Quotes Frame """
        
        
        """ create and place quotes frame onto window """
        self.quotes_frame = customtkinter.CTkFrame(self, height = 525, width = 880, fg_color="#0E0B13")
        self.quotes_frame.grid(row=1, column=1,columnspan=6,rowspan=1, sticky="nsew", padx=(10,10), pady=(0,10))

        """ create and place quote treeview onto frame """
        quotes_frame_treeview=ttk.Treeview(self.quotes_frame,columns=(1,2,3,4),show="headings",style="my.Treeview")
        quotes_frame_treeview.place(relx=0.025,rely=0.15,relwidth=0.95,relheight=0.80)
        quotes_frame_treeview.bind('<Motion>', 'break')
        quotes_frame_treeview.heading("1",text="")
        quotes_frame_treeview.column("1",stretch=0,width=0)
        quotes_frame_treeview.heading("2",text="Novel")
        quotes_frame_treeview.column("2",width=200)
        quotes_frame_treeview.heading("3",text="Character")
        quotes_frame_treeview.column("3",width=200)
        quotes_frame_treeview.heading("4", text="Quote Preview")
        quotes_frame_treeview.column("4", width=455)

        """ create and place quote search bar onto quotes frame. bind character entry to search function """
        quotes_search_bar = customtkinter.CTkEntry(self.quotes_frame, fg_color="#170830", border_color="#574379", text_color="white",placeholder_text_color="white", placeholder_text="Search Quotes...", width=688)
        quotes_search_bar.bind("<KeyRelease>", search_quotes_treeview)
        quotes_search_bar.place(relx=0.025,rely=0.045,relwidth=0.61)

        """ create and place buttons onto quotes frame """
        quotes_addentry_button = customtkinter.CTkButton(self.quotes_frame,text="Add Entry", fg_color="#638619", border_width=2, border_color="#2B3418", hover_color="#4B5D24", command= self.open_AddQuoteEntry)
        quotes_addentry_button.place(relx=0.64,rely=0.045, relwidth=0.086)
        quotes_editentry_button = customtkinter.CTkButton(self.quotes_frame,text="Edit Entry", fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command= self.open_EditQuoteEntry)
        quotes_editentry_button.place(relx=0.735,rely=0.045, relwidth=0.086)
        quotes_viewentry_button = customtkinter.CTkButton(self.quotes_frame,text="View Entry", fg_color="#2B80AD", border_width=2, border_color="#164057", hover_color="#216082", command= self.open_ViewQuoteEntry)
        quotes_viewentry_button.place(relx=0.83,rely=0.045, relwidth=0.086)
        quotes_help_button = customtkinter.CTkButton(self.quotes_frame,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=self.open_MainQuoteHelp)
        quotes_help_button.place(relx=0.925, rely=0.045, relwidth=0.043)

        
        """ Library Frame """
        
        
        """ create and place library frame onto window """
        self.library_frame = customtkinter.CTkFrame(self, height = 525, width = 880, fg_color="#0E0B13")
        self.library_frame.grid(row=1, column=1,columnspan=6,rowspan=1, sticky="nsew", padx=(10,10), pady=(0,10))

        """ create and place library treeview onto frame """
        library_frame_treeview=ttk.Treeview(self.library_frame,columns=(1,2,3,4,5,6,7),show="headings",style="My.Treeview")
        library_frame_treeview.place(relx=0.025,rely=0.15,relwidth=0.95,relheight=0.80)
        library_frame_treeview.bind('<Motion>', 'break')
        library_frame_treeview.heading("1",text="")
        library_frame_treeview.column("1",width=0, stretch=0)
        library_frame_treeview.heading("2",text="Title")
        library_frame_treeview.column("2",width=200)
        library_frame_treeview.heading("3",text="Chapter Count")
        library_frame_treeview.column("3",width=90)
        library_frame_treeview.heading("4",text="Novel Type")
        library_frame_treeview.column("4",width=130)
        library_frame_treeview.heading("5",text="Genre")
        library_frame_treeview.column("5",width=150)
        library_frame_treeview.heading("6",text="Library Status")
        library_frame_treeview.column("6",width=185)
        library_frame_treeview.heading("7",text="Rating")
        library_frame_treeview.column("7",width=75)

        """ create and place library search bar onto library frame. bind character entry to search function """
        library_search_bar = customtkinter.CTkEntry(self.library_frame,fg_color="#170830", border_color="#574379", text_color="white",placeholder_text_color="white", placeholder_text="Search Library...",width=680)
        library_search_bar.bind("<KeyRelease>", search_library_treeview)
        library_search_bar.place(relx=0.025,rely=0.045,relwidth=0.55)
        
        """ create and place buttons onto library frame """
        library_addentry_button = customtkinter.CTkButton(self.library_frame,text="Add Entry", fg_color="#638619", border_width=2, border_color="#2B3418", hover_color="#4B5D24", command= self.open_AddLibraryEntry)
        library_addentry_button.place(relx=0.64,rely=0.045, relwidth=0.086)
        library_editentry_button = customtkinter.CTkButton(self.library_frame,text="Edit Entry",fg_color="#575B59", border_width=2, border_color="#3A3D3B", hover_color="#494C4A", command= self.open_EditLibraryEntry)
        library_editentry_button.place(relx=0.735,rely=0.045, relwidth=0.086)
        library_viewentry_button = customtkinter.CTkButton(self.library_frame,text="View Entry", fg_color="#2B80AD", border_width=2, border_color="#164057", hover_color="#216082", command= self.open_ViewLibraryEntry)
        library_viewentry_button.place(relx=0.83,rely=0.045, relwidth=0.086)
        library_filterentry_button = customtkinter.CTkButton(self.library_frame,text="Filter", fg_color="#9A4120", border_width=2, border_color="#691C00", hover_color="#933310", command = self.open_FilterLibrary)
        library_filterentry_button.place(relx=0.582,rely=0.045, relwidth=0.05)
        library_help_button = customtkinter.CTkButton(self.library_frame,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command= self.open_MainLibraryHelp)
        library_help_button.place(relx=0.925, rely=0.045, relwidth=0.043)
        
        
        """ Stats Frame """
        
        
        """ create and place stats frame onto window. Content of frame is injected through insert stats function """
        stats_frame = customtkinter.CTkFrame(self, height=525, width=880, fg_color="#0E0B13")
        stats_frame.grid(row=1, column=1, columnspan=6, rowspan=1, sticky="nsew", padx=(10, 10), pady=(0, 10))
           
        """ help button """
        stats_help_button = customtkinter.CTkButton(stats_frame,text="?", fg_color="yellow", border_width=2, border_color="#ff8000", text_color="black", hover_color="#ffaa00", command=self.open_MainStatsHelp)
        stats_help_button.place(relx=0.925, rely=0.9, relwidth=0.043, anchor="n")
        
        """ Search Frame """
        
        
        """ create and place search frame onto window """
        self.search_frame = customtkinter.CTkFrame(self, height=525, width=880, fg_color="#0E0B13")
        self.search_frame.grid(row=1, column=1, columnspan=6, rowspan=1, sticky="nsew", padx=(10, 10), pady=(0, 10))

        """ create and place search treeview onto frame """
        search_frame_treeview=ttk.Treeview(self.search_frame,columns=(1),show="headings",style="My.Treeview")
        search_frame_treeview.place(relx=0.025,rely=0.1,relwidth=0.95,relheight=0.80)
        search_frame_treeview.heading("1",text="Novel Title")
        search_frame_treeview.column("1")
            
        """ create and place buttons onto library frame """
        search_addentry_button = customtkinter.CTkButton(self.search_frame,text="Add Entry", fg_color="#638619", border_width=2, border_color="#2B3418", hover_color="#4B5D24", command= self.open_AddPremadeEntry)
        search_addentry_button.place(relx=0.83,rely=0.025, relwidth=0.086)
        search_help_button = customtkinter.CTkButton(self.search_frame,text="?", fg_color="#FFEE32", border_width=2, text_color="black", border_color="#ff8000", hover_color="#ffaa00", font=("Tahoma", 13), command=self.open_MainSearchHelp)
        search_help_button.place(relx=0.925, rely=0.025, relwidth=0.043)

        
        """ Misc Functions """
        
        
        """ Initialize the frames wiondow to have no child/toplevel windows """
        self.toplevel_window = None
        
        """ start the window on the home frame """
        self.select_frame_by_name("home")
        
    """ Open the add quote entry toplevel window """ 
    def open_AddQuoteEntry(self):
        self.toplevel_window = AddQuoteEntry(self) 
    
    """ Open the edit quote entry toplevel window after it is checked that a quote is selected. If a quote is not selected display the error messagebox """      
    def open_EditQuoteEntry(self):
        global selected_quote
        selected_quote = quotes_frame_treeview.focus()
        if selected_quote:
            self.toplevel_window = EditQuoteEntry(self) 
        else:
            entry_error()
    
    """ Open the add library entry toplevel window """ 
    def open_AddLibraryEntry(self):
        self.toplevel_window = AddLibraryEntry(self)
        
    """ Open the edit library entry toplevel window after it is checked that a novel is selected. If a novel is not selected display the error messagebox """ 
    def open_EditLibraryEntry(self): 
        global selected_library 
        selected_library = library_frame_treeview.focus()
        if selected_library:
            self.toplevel_window = EditLibraryEntry(self)
        else:
            entry_error()
    
    """ Open the filter library toplevel window """
    def open_FilterLibrary(self):
        self.toplevel_window = FilterLibrary(self)

    """ Open the top novel entry toplevel window """
    def open_TopNovelsEntry(self):
        self.toplevel_window = TopNovelsEntry(self)
    
    """ Open the top character entry toplevel window """    
    def open_TopCharactersEntry(self):
        self.toplevel_window = TopCharactersEntry(self)

    """ Open the view quote toplevel window after it is checked that a quote is selected. If a quote is not selected display the error messagebox """ 
    def open_ViewQuoteEntry(self):
        global selected_quote_view
        selected_quote_view = quotes_frame_treeview.focus()
        if selected_quote_view:
           self.toplevel_window = ViewQuotesEntry(self)
        else:
            entry_error()
    
    """ Open the view library entry toplevel window after it is checked that a novel is selected. If a novel is not selected display the error messagebox """   
    def open_ViewLibraryEntry(self):  
        global selected_library_view 
        selected_library_view = library_frame_treeview.focus()
        if selected_library_view:
            self.toplevel_window = ViewLibraryEntry(self)
        else:
            entry_error()        
    
    """ Open the add premade library entry toplevel window after it is checked that a novel is selected. If a novel is not selected display the error messagebox """   
    def open_AddPremadeEntry(self):
        global selected_premade
        selected_premade = search_frame_treeview.focus()
        if selected_premade:
            self.toplevel_window = AddPremadeEntry(self)
        else:
            entry_error()
    
    """ Open the main quote help toplevel window """ 
    def open_MainQuoteHelp(self):
        self.toplevel_window = MainQuoteHelp(self)
    
    """ Open the main library help toplevel window """ 
    def open_MainLibraryHelp(self):
        self.toplevel_window = MainLibraryHelp(self)
    
    """ Open the main stats help toplevel window """     
    def open_MainStatsHelp(self):
        self.toplevel_window = MainStatsHelp(self)
    
    """ Open the main home help toplevel window """ 
    def open_MainHomeHelp(self):
        self.toplevel_window = MainHomeHelp(self)
    
    """ Open the main search help toplevel window """ 
    def open_MainSearchHelp(self):
        self.toplevel_window = MainSearchHelp(self)
        
    """ open the profile toplevel window """
    def open_Profile(self):
        self.toplevel_window = Profile(self)
    
    
    """ Frame Selection Functions """
    
    
    """ show the frame whos name is selected. If the frame is not selected, remove it from the window """
    """ this function was created using the help of the following example https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/image_example.py """
    def select_frame_by_name(Top, name):
        if name == "home":
            Top.home_frame.grid(row=1, column=1,rowspan=1, sticky="nsew", padx=(10,10), pady=(0,10))
        else:
            Top.home_frame.grid_forget()
        if name == "quotes":
            Top.quotes_frame.grid(row=1, column=1,rowspan=1, sticky="nsew", padx=(10,10), pady=(0,10))
        else:
            Top.quotes_frame.grid_forget()
        if name == "library":
            Top.library_frame.grid(row=1, column=1,rowspan=1, sticky="nsew", padx=(10,10), pady=(0,10))
        else:
            Top.library_frame.grid_forget()
        if name == "stats":
            stats_frame.grid(row=1, column=1,rowspan=1, sticky="nsew", padx=(10,10), pady=(0,10))
        else:
            stats_frame.grid_forget()
        if name == "search":
            Top.search_frame.grid(row=1, column=1,rowspan=1, sticky="nsew", padx=(10,10), pady=(0,10))
        else:
            Top.search_frame.grid_forget()

    """ change the name of the select_frame_by_name function based on which frame is selected. """
    def home_button_event(self):
        self.select_frame_by_name("home")

    def quotes_button_event(self):
        self.select_frame_by_name("quotes")

    def library_button_event(self):
        self.select_frame_by_name("library")

    def stats_button_event(self):
        self.select_frame_by_name("stats") 
   
    def search_button_event(self):
        self.select_frame_by_name("search")     




""" Creates instances of login and frame windows """        
if __name__ == "__main__":
    frames = Frames()
    login_window = LoginWindow(frames)
    login_window.mainloop()
    frames.mainloop()