""" Very basic GUI for auto_refresher"""
import PySimpleGUI as sg
from auto_refresher import AutoRefresher
from time import sleep
import time as tm


def main_menu():
    """ Basic Menu for input and use of auto refresher bot."""
    layout = [
        [sg.Text("Username: "), sg.InputText(key="usr")],
        [sg.Text("Password: "), sg.InputText(key="pass")],
        [sg.Text("Refresh Frequency (in hours):"), sg.InputText(key="freq")],
        [sg.Button("Start Bot")],
        [sg.Text("Use: Have a good internet connection, enter info correctly, and the bot will refresh all listings"
                 " every hour in the frequency parameter.")],
        [sg.Text("To End Program: Simply close the chrome tab and wait a few seconds. Force Quiting also works.")]
    ]
    main_window = sg.Window("Depop Auto Refresher", layout)

    while True:
        event, values = main_window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == "Start Bot":
            bot = AutoRefresher(indefinite=True, frequency=(int((int(1) * 3599))))
            x = "freshlylaunderedlinens"
            y = "Soliwan159753"
            bot.login(x, y)
            bot.move_sold_items_down()
            bot.load_all_items()
            links = bot.get_item_links()
            bot.refresh_items(links)
            bot.close_driver()


if __name__ == "__main__":
    main_menu()
