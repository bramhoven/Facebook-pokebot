import curses
import curses.panel
import getpass
import threading
import time
from pokebot import Pokebot

shutdownStats = False
shutdownRefresh = False

def init():
    global screen
    global window_options
    global window_stats
    global mail
    global pwd
    global interval
    global bot

    mail = raw_input("Email: ")
    pwd = getpass.getpass("Password: ")
    interval = raw_input("Interval: ")
    interval = "0"
    bot = Pokebot(mail, pwd, interval)

    screen = curses.initscr()
    height, width = screen.getmaxyx()
    screen.border(0)
    curses.curs_set(0)

    window_options = curses.newwin(9, width-2, 1, 1)
    window_stats = curses.newwin(height-11, width-2, 10, 1)

    reset_windows()
    reset_windows()
    threading.Thread(target=refresh).start()

def reset_windows():
    screen.border(0)
    screen.refresh()

    window_options.clear()
    window_options.refresh()
    window_options.border(0)
    window_options.addstr(0, 1, "Facebook Pokebot")
    window_options.addstr(2, 2, "[1] Start Bot")
    window_options.addstr(3, 2, "[2] Stop Bot")
    window_options.addstr(4, 2, "[3] Quit")
    window_options.addstr(7, 2, "Select a option: ")
    window_options.refresh()

    window_stats.clear()
    window_stats.refresh()
    window_stats.border(0)
    window_stats.addstr(0, 1, "Statistics")
    window_stats.refresh()

def refresh():
    while not shutdownRefresh:
        get_input()

def refresh_stats():
    while not shutdownStats:
        stats = bot.get_stats()
        index = 0
        for name, amount in stats.iteritems():
            window_stats.addstr(1+index, 1, name + ": " + str(amount) + " pokes")
            index += 1

        window_stats.refresh()
    reset_windows()

def get_input():
    global bot
    global shutdownStats

    curses.echo()
    option = screen.getstr(8, 20, 5)
    curses.noecho()
    if option == "1":
        if not bot.isAlive():
            bot.shutdown = False
            shutdownStats = False
            bot.start()
            threading.Thread(target=refresh_stats).start()
    elif option == "2":
        if bot.isAlive():
            bot.shutdown = True
            shutdownStats = True
            bot = Pokebot(mail, pwd, interval)
    elif option == "3":
        close()
    elif option == "^C":
        close()
    else:
        debug(" Wrong input ")
    reset_windows()

def debug(msg):
    screen.addstr(24, 1, msg)

def close():
    global bot
    global shutdownStats
    
    if bot.isAlive():
        bot.shutdown = True
        shutdownStats = True
        bot = Pokebot(mail, pwd, interval)
    shutdownRefresh = True
    curses.endwin()

if __name__ == "__main__":
    init()
