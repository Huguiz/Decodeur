import vlc
import customtkinter
from tkinter import *
import os
import time
import threading
import socket
import configparser
import ipaddress

BUFFER_SIZE = 1024

SEPARATOR = ";"

SDK_COMMAND1 = "1"
SDK_COMMAND2 = "2"
SDK_COMMAND3 = "3"
SDK_COMMAND4 = "4"
SDK_COMMAND5 = "5"

"""
Séparateur utilisé : ¥

Liste commandes :

1 = Envoi d'un média
Ex: 1¥1¥rtsp://10.0.0.1
    NumCommande ¥ NumMon ¥ CheminMédia

2 = Envoi d'un cyclique
Ex: 2¥1¥rtsp://10.0.0.1¥5¥rtsp://10.0.0.2¥10¥rtsp://10.0.0.3¥7
    NumCommande ¥ NumMon ¥ CheminMédia1 ¥ DwellMedia1 ¥ CheminMédia2 ¥ DwellMedia2 ¥ CheminMédia3 ¥ DwellMedia3

3 = Envoi signal de vie
Ex: 3
    NumCommande

4 = Envoi de la mise au noir
Ex: 4¥1
    NumCommande ¥ NumMon

5 = Envoi du changement de pré-position des moniteurs
Ex: 5¥4
    NumCommande ¥ Prépo à afficher (ici quad)
"""


class SetMonitorArrangement:

    def __init__(self, parent, number_of_mon, background_color):
        """"Création de la classe"""
        self.BorderSize = None

        self.parent = parent

        self.backgroundColor = background_color

        self.numberOfMon = number_of_mon

        self.frameWidth = self.parent.winfo_screenwidth()
        self.frameHeight = self.parent.winfo_screenheight()

        self.mon1CyclicStatus = False
        self.mon2CyclicStatus = False
        self.mon3CyclicStatus = False
        self.mon4CyclicStatus = False
        self.mon5CyclicStatus = False
        self.mon6CyclicStatus = False
        self.mon7CyclicStatus = False
        self.mon8CyclicStatus = False
        self.mon9CyclicStatus = False
        self.mon10CyclicStatus = False
        self.mon11CyclicStatus = False
        self.mon12CyclicStatus = False
        self.mon13CyclicStatus = False
        self.mon14CyclicStatus = False
        self.mon15CyclicStatus = False
        self.mon16CyclicStatus = False

        self.closeMon1Cyclic = False
        self.closeMon2Cyclic = False
        self.closeMon3Cyclic = False
        self.closeMon4Cyclic = False
        self.closeMon5Cyclic = False
        self.closeMon6Cyclic = False
        self.closeMon7Cyclic = False
        self.closeMon8Cyclic = False
        self.closeMon9Cyclic = False
        self.closeMon10Cyclic = False
        self.closeMon11Cyclic = False
        self.closeMon12Cyclic = False
        self.closeMon13Cyclic = False
        self.closeMon14Cyclic = False
        self.closeMon15Cyclic = False
        self.closeMon16Cyclic = False

        self.videoPanel1 = None
        self.videoPanel2 = None
        self.videoPanel3 = None
        self.videoPanel4 = None
        self.videoPanel5 = None
        self.videoPanel6 = None
        self.videoPanel7 = None
        self.videoPanel8 = None
        self.videoPanel9 = None
        self.videoPanel10 = None
        self.videoPanel11 = None
        self.videoPanel12 = None
        self.videoPanel13 = None
        self.videoPanel14 = None
        self.videoPanel15 = None
        self.videoPanel16 = None

        self.vlcPlayer1 = None
        self.vlcPlayer2 = None
        self.vlcPlayer3 = None
        self.vlcPlayer4 = None
        self.vlcPlayer5 = None
        self.vlcPlayer6 = None
        self.vlcPlayer7 = None
        self.vlcPlayer8 = None
        self.vlcPlayer9 = None
        self.vlcPlayer10 = None
        self.vlcPlayer11 = None
        self.vlcPlayer12 = None
        self.vlcPlayer13 = None
        self.vlcPlayer14 = None
        self.vlcPlayer15 = None
        self.vlcPlayer16 = None

        self.vlcInstance1 = None
        self.vlcInstance2 = None
        self.vlcInstance3 = None
        self.vlcInstance4 = None
        self.vlcInstance5 = None
        self.vlcInstance6 = None
        self.vlcInstance7 = None
        self.vlcInstance8 = None
        self.vlcInstance9 = None
        self.vlcInstance10 = None
        self.vlcInstance11 = None
        self.vlcInstance12 = None
        self.vlcInstance13 = None
        self.vlcInstance14 = None
        self.vlcInstance15 = None
        self.vlcInstance16 = None

        self.threadMonCyclic1 = None
        self.threadMonCyclic2 = None
        self.threadMonCyclic3 = None
        self.threadMonCyclic4 = None
        self.threadMonCyclic5 = None
        self.threadMonCyclic6 = None
        self.threadMonCyclic7 = None
        self.threadMonCyclic8 = None
        self.threadMonCyclic9 = None
        self.threadMonCyclic10 = None
        self.threadMonCyclic11 = None
        self.threadMonCyclic12 = None
        self.threadMonCyclic13 = None
        self.threadMonCyclic14 = None
        self.threadMonCyclic15 = None
        self.threadMonCyclic16 = None

        if self.numberOfMon == 1:
            self.single()
        elif self.numberOfMon == 4:
            self.quad()
        elif self.numberOfMon == 9:
            self.nano()
        elif self.numberOfMon == 16:
            self.sixteen()
        elif self.numberOfMon == 8:
            self.eight()
        elif self.numberOfMon == 13:
            self.thirteen()
        elif self.numberOfMon == 6:
            self.six()

    def single(self):
        """
        ┌─────────────┐
        │             │
        │     MON1    │
        │             │
        └─────────────┘
        """

        self.numberOfMon = 1

        mon_width = self.frameWidth
        mon_height = self.frameHeight

        self.videoPanel1 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel1.place(x=0, y=0)
        self.vlcInstance1 = vlc.Instance()
        self.vlcPlayer1 = self.vlcInstance1.media_player_new()
        self.vlcPlayer1.set_hwnd(self.videoPanel1.winfo_id())
        self.vlcPlayer1.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.parent.update()
        # self.set_default_to_all_mon()

    def quad(self):
        """
        ┌──────┬──────┐
        │ MON1 │ MON2 │
        ├──────┼──────┤
        │ MON3 │ MON4 │
        └──────┴──────┘
        """

        self.numberOfMon = 4

        self.BorderSize = 4

        mon_width = (self.frameWidth - self.BorderSize) / 2
        mon_height = (self.frameHeight - self.BorderSize) / 2

        self.videoPanel1 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel1.place(x=0, y=0)
        self.vlcInstance1 = vlc.Instance()
        self.vlcPlayer1 = self.vlcInstance1.media_player_new()
        self.vlcPlayer1.set_hwnd(self.videoPanel1.winfo_id())
        self.vlcPlayer1.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel2 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel2.place(x=mon_width + self.BorderSize, y=0)
        self.vlcInstance2 = vlc.Instance()
        self.vlcPlayer2 = self.vlcInstance2.media_player_new()
        self.vlcPlayer2.set_hwnd(self.videoPanel2.winfo_id())
        self.vlcPlayer2.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel3 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel3.place(x=0, y=mon_height + self.BorderSize)
        self.vlcInstance3 = vlc.Instance()
        self.vlcPlayer3 = self.vlcInstance3.media_player_new()
        self.vlcPlayer3.set_hwnd(self.videoPanel3.winfo_id())
        self.vlcPlayer3.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel4 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel4.place(x=mon_width + self.BorderSize, y=mon_height + self.BorderSize)
        self.vlcInstance4 = vlc.Instance()
        self.vlcPlayer4 = self.vlcInstance4.media_player_new()
        self.vlcPlayer4.set_hwnd(self.videoPanel4.winfo_id())
        self.vlcPlayer4.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.parent.update()
        # self.set_default_to_all_mon()

    def nano(self):
        """
        ┌──────┬──────┬──────┐
        │ MON1 │ MON2 │ MON3 │
        ├──────┼──────┼──────┤
        │ MON4 │ MON5 │ MON6 │
        ├──────┼──────┼──────┤
        │ MON7 │ MON8 │ MON9 │
        └──────┴──────┴──────┘
        """

        self.numberOfMon = 9

        self.BorderSize = 3

        mon_width = (self.frameWidth - (self.BorderSize * 2)) / 3
        mon_height = (self.frameHeight - (self.BorderSize * 2)) / 3

        self.videoPanel1 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel1.place(x=0, y=0)
        self.vlcInstance1 = vlc.Instance()
        self.vlcPlayer1 = self.vlcInstance1.media_player_new()
        self.vlcPlayer1.set_hwnd(self.videoPanel1.winfo_id())
        self.vlcPlayer1.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel2 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel2.place(x=(1 * mon_width) + (1 * self.BorderSize), y=0)
        self.vlcInstance2 = vlc.Instance()
        self.vlcPlayer2 = self.vlcInstance2.media_player_new()
        self.vlcPlayer2.set_hwnd(self.videoPanel2.winfo_id())
        self.vlcPlayer2.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel3 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel3.place(x=(2 * mon_width) + (2 * self.BorderSize), y=0)
        self.vlcInstance3 = vlc.Instance()
        self.vlcPlayer3 = self.vlcInstance3.media_player_new()
        self.vlcPlayer3.set_hwnd(self.videoPanel3.winfo_id())
        self.vlcPlayer3.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel4 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel4.place(x=0, y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance4 = vlc.Instance()
        self.vlcPlayer4 = self.vlcInstance4.media_player_new()
        self.vlcPlayer4.set_hwnd(self.videoPanel4.winfo_id())
        self.vlcPlayer4.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel5 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel5.place(x=(1 * mon_width) + (1 * self.BorderSize), y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance5 = vlc.Instance()
        self.vlcPlayer5 = self.vlcInstance5.media_player_new()
        self.vlcPlayer5.set_hwnd(self.videoPanel5.winfo_id())
        self.vlcPlayer5.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel6 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel6.place(x=(2 * mon_width) + (2 * self.BorderSize), y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance6 = vlc.Instance()
        self.vlcPlayer6 = self.vlcInstance6.media_player_new()
        self.vlcPlayer6.set_hwnd(self.videoPanel6.winfo_id())
        self.vlcPlayer6.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel7 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel7.place(x=0, y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance7 = vlc.Instance()
        self.vlcPlayer7 = self.vlcInstance7.media_player_new()
        self.vlcPlayer7.set_hwnd(self.videoPanel7.winfo_id())
        self.vlcPlayer7.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel8 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel8.place(x=(1 * mon_width) + (1 * self.BorderSize), y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance8 = vlc.Instance()
        self.vlcPlayer8 = self.vlcInstance8.media_player_new()
        self.vlcPlayer8.set_hwnd(self.videoPanel8.winfo_id())
        self.vlcPlayer8.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel9 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel9.place(x=(2 * mon_width) + (2 * self.BorderSize), y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance9 = vlc.Instance()
        self.vlcPlayer9 = self.vlcInstance9.media_player_new()
        self.vlcPlayer9.set_hwnd(self.videoPanel9.winfo_id())
        self.vlcPlayer9.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.parent.update()
        # self.set_default_to_all_mon()

    def sixteen(self):
        """
        ┌───────┬───────┬───────┬───────┐
        │ MON1  │ MON2  │ MON3  │ MON4  │
        ├───────┼───────┼───────┼───────┤
        │ MON5  │ MON6  │ MON7  │ MON8  │
        ├───────┼───────┼───────┼───────┤
        │ MON9  │ MON10 │ MON11 │ MON12 │
        ├───────┼───────┼───────┼───────┤
        │ MON13 │ MON14 │ MON15 │ MON16 │
        └───────┴───────┴───────┴───────┘
        """

        self.numberOfMon = 16

        self.BorderSize = 4

        mon_width = (self.frameWidth - (self.BorderSize * 3)) / 4
        mon_height = (self.frameHeight - (self.BorderSize * 3)) / 4

        self.videoPanel1 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel1.place(x=0, y=0)
        self.vlcInstance1 = vlc.Instance()
        self.vlcPlayer1 = self.vlcInstance1.media_player_new()
        self.vlcPlayer1.set_hwnd(self.videoPanel1.winfo_id())
        self.vlcPlayer1.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel2 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel2.place(x=(1 * mon_width) + (1 * self.BorderSize), y=0)
        self.vlcInstance2 = vlc.Instance()
        self.vlcPlayer2 = self.vlcInstance2.media_player_new()
        self.vlcPlayer2.set_hwnd(self.videoPanel2.winfo_id())
        self.vlcPlayer2.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel3 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel3.place(x=(2 * mon_width) + (2 * self.BorderSize), y=0)
        self.vlcInstance3 = vlc.Instance()
        self.vlcPlayer3 = self.vlcInstance3.media_player_new()
        self.vlcPlayer3.set_hwnd(self.videoPanel3.winfo_id())
        self.vlcPlayer3.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel4 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel4.place(x=(3 * mon_width) + (3 * self.BorderSize), y=0)
        self.vlcInstance4 = vlc.Instance()
        self.vlcPlayer4 = self.vlcInstance4.media_player_new()
        self.vlcPlayer4.set_hwnd(self.videoPanel4.winfo_id())
        self.vlcPlayer4.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel5 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel5.place(x=0, y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance5 = vlc.Instance()
        self.vlcPlayer5 = self.vlcInstance5.media_player_new()
        self.vlcPlayer5.set_hwnd(self.videoPanel5.winfo_id())
        self.vlcPlayer5.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel6 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel6.place(x=(1 * mon_width) + (1 * self.BorderSize), y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance6 = vlc.Instance()
        self.vlcPlayer6 = self.vlcInstance6.media_player_new()
        self.vlcPlayer6.set_hwnd(self.videoPanel6.winfo_id())
        self.vlcPlayer6.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel7 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel7.place(x=(2 * mon_width) + (2 * self.BorderSize), y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance7 = vlc.Instance()
        self.vlcPlayer7 = self.vlcInstance7.media_player_new()
        self.vlcPlayer7.set_hwnd(self.videoPanel7.winfo_id())
        self.vlcPlayer7.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel8 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel8.place(x=(3 * mon_width) + (3 * self.BorderSize), y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance8 = vlc.Instance()
        self.vlcPlayer8 = self.vlcInstance8.media_player_new()
        self.vlcPlayer8.set_hwnd(self.videoPanel8.winfo_id())
        self.vlcPlayer8.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel9 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel9.place(x=0, y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance9 = vlc.Instance()
        self.vlcPlayer9 = self.vlcInstance9.media_player_new()
        self.vlcPlayer9.set_hwnd(self.videoPanel9.winfo_id())
        self.vlcPlayer9.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel10 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel10.place(x=(1 * mon_width) + (1 * self.BorderSize), y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance10 = vlc.Instance()
        self.vlcPlayer10 = self.vlcInstance10.media_player_new()
        self.vlcPlayer10.set_hwnd(self.videoPanel10.winfo_id())
        self.vlcPlayer10.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel11 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel11.place(x=(2 * mon_width) + (2 * self.BorderSize), y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance11 = vlc.Instance()
        self.vlcPlayer11 = self.vlcInstance11.media_player_new()
        self.vlcPlayer11.set_hwnd(self.videoPanel11.winfo_id())
        self.vlcPlayer11.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel12 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel12.place(x=(3 * mon_width) + (3 * self.BorderSize), y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance12 = vlc.Instance()
        self.vlcPlayer12 = self.vlcInstance12.media_player_new()
        self.vlcPlayer12.set_hwnd(self.videoPanel12.winfo_id())
        self.vlcPlayer12.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel13 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel13.place(x=0, y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance13 = vlc.Instance()
        self.vlcPlayer13 = self.vlcInstance13.media_player_new()
        self.vlcPlayer13.set_hwnd(self.videoPanel13.winfo_id())
        self.vlcPlayer13.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel14 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel14.place(x=(1 * mon_width) + (1 * self.BorderSize), y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance14 = vlc.Instance()
        self.vlcPlayer14 = self.vlcInstance14.media_player_new()
        self.vlcPlayer14.set_hwnd(self.videoPanel14.winfo_id())
        self.vlcPlayer14.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel15 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel15.place(x=(2 * mon_width) + (2 * self.BorderSize), y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance15 = vlc.Instance()
        self.vlcPlayer15 = self.vlcInstance15.media_player_new()
        self.vlcPlayer15.set_hwnd(self.videoPanel15.winfo_id())
        self.vlcPlayer15.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel16 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel16.place(x=(3 * mon_width) + (3 * self.BorderSize), y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance16 = vlc.Instance()
        self.vlcPlayer16 = self.vlcInstance16.media_player_new()
        self.vlcPlayer16.set_hwnd(self.videoPanel16.winfo_id())
        self.vlcPlayer16.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.parent.update()
        # self.set_default_to_all_mon()

    def eight(self):
        """
        ┌───────┬───────────────────────┐
        │ MON1  │                       │
        ├───────┼                       │
        │ MON2  │         MON8          │
        ├───────┼                       │
        │ MON3  │                       │
        ├───────┼───────┬───────┬───────┤
        │ MON4  │ MON5  │ MON6  │ MON7  │
        └───────┴───────┴───────┴───────┘
        """

        self.numberOfMon = 8

        self.BorderSize = 4

        mon_width = (self.frameWidth - (self.BorderSize * 3)) / 4
        mon_height = (self.frameHeight - (self.BorderSize * 3)) / 4

        self.videoPanel1 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel1.place(x=0, y=0)
        self.vlcInstance1 = vlc.Instance()
        self.vlcPlayer1 = self.vlcInstance1.media_player_new()
        self.vlcPlayer1.set_hwnd(self.videoPanel1.winfo_id())
        self.vlcPlayer1.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel2 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel2.place(x=0, y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance2 = vlc.Instance()
        self.vlcPlayer2 = self.vlcInstance2.media_player_new()
        self.vlcPlayer2.set_hwnd(self.videoPanel2.winfo_id())
        self.vlcPlayer2.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel3 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel3.place(x=0, y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance3 = vlc.Instance()
        self.vlcPlayer3 = self.vlcInstance3.media_player_new()
        self.vlcPlayer3.set_hwnd(self.videoPanel3.winfo_id())
        self.vlcPlayer3.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel4 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel4.place(x=0, y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance4 = vlc.Instance()
        self.vlcPlayer4 = self.vlcInstance4.media_player_new()
        self.vlcPlayer4.set_hwnd(self.videoPanel4.winfo_id())
        self.vlcPlayer4.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel5 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel5.place(x=(1 * mon_width) + (1 * self.BorderSize), y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance5 = vlc.Instance()
        self.vlcPlayer5 = self.vlcInstance5.media_player_new()
        self.vlcPlayer5.set_hwnd(self.videoPanel5.winfo_id())
        self.vlcPlayer5.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel6 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel6.place(x=(2 * mon_width) + (2 * self.BorderSize), y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance6 = vlc.Instance()
        self.vlcPlayer6 = self.vlcInstance6.media_player_new()
        self.vlcPlayer6.set_hwnd(self.videoPanel6.winfo_id())
        self.vlcPlayer6.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel7 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel7.place(x=(3 * mon_width) + (3 * self.BorderSize), y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance7 = vlc.Instance()
        self.vlcPlayer7 = self.vlcInstance7.media_player_new()
        self.vlcPlayer7.set_hwnd(self.videoPanel7.winfo_id())
        self.vlcPlayer7.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel8 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=(mon_width * 3) + (self.BorderSize * 2), height=(mon_height * 3) + (self.BorderSize * 2))
        self.videoPanel8.place(x=(1 * mon_width) + (1 * self.BorderSize), y=0)
        self.vlcInstance8 = vlc.Instance()
        self.vlcPlayer8 = self.vlcInstance8.media_player_new()
        self.vlcPlayer8.set_hwnd(self.videoPanel8.winfo_id())
        self.vlcPlayer8.video_set_aspect_ratio(
            str((int(mon_width) * 3) + self.BorderSize * 2) + ":" + str((int(mon_height) * 3) + self.BorderSize * 2))

        self.parent.update()
        # self.set_default_to_all_mon()

    def thirteen(self):
        """
        ┌───────┬───────┬───────┬───────┐
        │ MON1  │ MON2  │ MON3  │ MON4  │
        ├───────┼───────┴───────┼───────┤
        │ MON5  │               │ MON6  │
        ├───────┤     MON13     ├───────┤
        │ MON7  │               │ MON8  │
        ├───────┼───────┬───────┼───────┤
        │ MON9  │ MON10 │ MON11 │ MON12 │
        └───────┴───────┴───────┴───────┘
        """

        self.numberOfMon = 13

        self.BorderSize = 4

        mon_width = (self.frameWidth - (self.BorderSize * 3)) / 4
        mon_height = (self.frameHeight - (self.BorderSize * 3)) / 4

        self.videoPanel1 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel1.place(x=0, y=0)
        self.vlcInstance1 = vlc.Instance()
        self.vlcPlayer1 = self.vlcInstance1.media_player_new()
        self.vlcPlayer1.set_hwnd(self.videoPanel1.winfo_id())
        self.vlcPlayer1.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel2 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel2.place(x=(1 * mon_width) + (1 * self.BorderSize), y=0)
        self.vlcInstance2 = vlc.Instance()
        self.vlcPlayer2 = self.vlcInstance2.media_player_new()
        self.vlcPlayer2.set_hwnd(self.videoPanel2.winfo_id())
        self.vlcPlayer2.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel3 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel3.place(x=(2 * mon_width) + (2 * self.BorderSize), y=0)
        self.vlcInstance3 = vlc.Instance()
        self.vlcPlayer3 = self.vlcInstance3.media_player_new()
        self.vlcPlayer3.set_hwnd(self.videoPanel3.winfo_id())
        self.vlcPlayer3.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel4 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel4.place(x=(3 * mon_width) + (3 * self.BorderSize), y=0)
        self.vlcInstance4 = vlc.Instance()
        self.vlcPlayer4 = self.vlcInstance4.media_player_new()
        self.vlcPlayer4.set_hwnd(self.videoPanel4.winfo_id())
        self.vlcPlayer4.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel5 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel5.place(x=0, y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance5 = vlc.Instance()
        self.vlcPlayer5 = self.vlcInstance5.media_player_new()
        self.vlcPlayer5.set_hwnd(self.videoPanel5.winfo_id())
        self.vlcPlayer5.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel6 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel6.place(x=(3 * mon_width) + (3 * self.BorderSize), y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance6 = vlc.Instance()
        self.vlcPlayer6 = self.vlcInstance6.media_player_new()
        self.vlcPlayer6.set_hwnd(self.videoPanel6.winfo_id())
        self.vlcPlayer6.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel7 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel7.place(x=0, y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance7 = vlc.Instance()
        self.vlcPlayer7 = self.vlcInstance7.media_player_new()
        self.vlcPlayer7.set_hwnd(self.videoPanel7.winfo_id())
        self.vlcPlayer7.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel8 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel8.place(x=(3 * mon_width) + (3 * self.BorderSize), y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance8 = vlc.Instance()
        self.vlcPlayer8 = self.vlcInstance8.media_player_new()
        self.vlcPlayer8.set_hwnd(self.videoPanel8.winfo_id())
        self.vlcPlayer8.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel9 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel9.place(x=0, y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance9 = vlc.Instance()
        self.vlcPlayer9 = self.vlcInstance9.media_player_new()
        self.vlcPlayer9.set_hwnd(self.videoPanel9.winfo_id())
        self.vlcPlayer9.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel10 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel10.place(x=(1 * mon_width) + (1 * self.BorderSize), y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance10 = vlc.Instance()
        self.vlcPlayer10 = self.vlcInstance10.media_player_new()
        self.vlcPlayer10.set_hwnd(self.videoPanel10.winfo_id())
        self.vlcPlayer10.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel11 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel11.place(x=(2 * mon_width) + (2 * self.BorderSize), y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance11 = vlc.Instance()
        self.vlcPlayer11 = self.vlcInstance11.media_player_new()
        self.vlcPlayer11.set_hwnd(self.videoPanel11.winfo_id())
        self.vlcPlayer11.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel12 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel12.place(x=(3 * mon_width) + (3 * self.BorderSize), y=(3 * mon_height) + (3 * self.BorderSize))
        self.vlcInstance12 = vlc.Instance()
        self.vlcPlayer12 = self.vlcInstance12.media_player_new()
        self.vlcPlayer12.set_hwnd(self.videoPanel12.winfo_id())
        self.vlcPlayer12.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel13 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=(2 * mon_width) + self.BorderSize, height=(2 * mon_height) + self.BorderSize)
        self.videoPanel13.place(x=(1 * mon_width) + (1 * self.BorderSize), y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance13 = vlc.Instance()
        self.vlcPlayer13 = self.vlcInstance13.media_player_new()
        self.vlcPlayer13.set_hwnd(self.videoPanel13.winfo_id())
        self.vlcPlayer13.video_set_aspect_ratio(str((int(mon_width) * 2) + self.BorderSize) + ":" + str((int(mon_height) * 2) + self.BorderSize))

        self.parent.update()
        # self.set_default_to_all_mon()

    def six(self):
        """
        ┌──────┬─────────────┐
        │ MON1 │             │
        ├──────┤    MON6     │
        │ MON2 │             │
        ├──────┼──────┬──────┤
        │ MON3 │ MON4 │ MON5 │
        └──────┴──────┴──────┘
        """

        self.numberOfMon = 6

        self.BorderSize = 3

        mon_width = (self.frameWidth - (self.BorderSize * 2)) / 3
        mon_height = (self.frameHeight - (self.BorderSize * 2)) / 3

        self.videoPanel1 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel1.place(x=0, y=0)
        self.vlcInstance1 = vlc.Instance()
        self.vlcPlayer1 = self.vlcInstance1.media_player_new()
        self.vlcPlayer1.set_hwnd(self.videoPanel1.winfo_id())
        self.vlcPlayer1.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel2 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel2.place(x=0, y=(1 * mon_height) + (1 * self.BorderSize))
        self.vlcInstance2 = vlc.Instance()
        self.vlcPlayer2 = self.vlcInstance2.media_player_new()
        self.vlcPlayer2.set_hwnd(self.videoPanel2.winfo_id())
        self.vlcPlayer2.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel3 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel3.place(x=0, y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance3 = vlc.Instance()
        self.vlcPlayer3 = self.vlcInstance3.media_player_new()
        self.vlcPlayer3.set_hwnd(self.videoPanel3.winfo_id())
        self.vlcPlayer3.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel4 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel4.place(x=(1 * mon_width) + (1 * self.BorderSize), y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance4 = vlc.Instance()
        self.vlcPlayer4 = self.vlcInstance4.media_player_new()
        self.vlcPlayer4.set_hwnd(self.videoPanel4.winfo_id())
        self.vlcPlayer4.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel5 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=mon_width, height=mon_height)
        self.videoPanel5.place(x=(2 * mon_width) + (2 * self.BorderSize), y=(2 * mon_height) + (2 * self.BorderSize))
        self.vlcInstance5 = vlc.Instance()
        self.vlcPlayer5 = self.vlcInstance5.media_player_new()
        self.vlcPlayer5.set_hwnd(self.videoPanel5.winfo_id())
        self.vlcPlayer5.video_set_aspect_ratio(str(int(mon_width)) + ":" + str(int(mon_height)))

        self.videoPanel6 = Frame(self.parent, bg=self.backgroundColor, highlightthickness=0, width=(2 * mon_width) + self.BorderSize, height=(2 * mon_height) + self.BorderSize)
        self.videoPanel6.place(x=(1 * mon_width) + (1 * self.BorderSize), y=0)
        self.vlcInstance6 = vlc.Instance()
        self.vlcPlayer6 = self.vlcInstance6.media_player_new()
        self.vlcPlayer6.set_hwnd(self.videoPanel6.winfo_id())
        self.vlcPlayer6.video_set_aspect_ratio(str((int(mon_width) * 2) + self.BorderSize) + ":" + str((int(mon_height) * 2) + self.BorderSize))

        self.parent.update()
        # self.set_default_to_all_mon()

    def kill_all_mon(self):
        """Tue tout les moniteurs existant. Appelé avant de changer de prépo."""
        self.videoPanel1.destroy()
        if self.numberOfMon >= 4:
            self.videoPanel2.destroy()
            self.videoPanel3.destroy()
            self.videoPanel4.destroy()
            if self.numberOfMon >= 6:
                self.videoPanel5.destroy()
                self.videoPanel6.destroy()
                if self.numberOfMon >= 8:
                    self.videoPanel7.destroy()
                    self.videoPanel8.destroy()
                    if self.numberOfMon >= 9:
                        self.videoPanel9.destroy()
                        if self.numberOfMon >= 13:
                            self.videoPanel10.destroy()
                            self.videoPanel11.destroy()
                            self.videoPanel12.destroy()
                            self.videoPanel13.destroy()
                            if self.numberOfMon >= 16:
                                self.videoPanel14.destroy()
                                self.videoPanel15.destroy()
                                self.videoPanel16.destroy()

    def set_media_to_mon(self, mon_number, url):
        """Lance le média sur le moniteur choisi"""
        if mon_number == 1:
            self.vlcPlayer1.stop()
            media_temp = self.vlcInstance1.media_new(url)
            self.vlcPlayer1.set_media(media_temp)
            self.vlcPlayer1.play()
        elif mon_number == 2:
            self.vlcPlayer2.stop()
            media_temp = self.vlcInstance2.media_new(url)
            self.vlcPlayer2.set_media(media_temp)
            self.vlcPlayer2.play()
        elif mon_number == 3:
            self.vlcPlayer3.stop()
            media_temp = self.vlcInstance3.media_new(url)
            self.vlcPlayer3.set_media(media_temp)
            self.vlcPlayer3.play()
        elif mon_number == 4:
            self.vlcPlayer4.stop()
            media_temp = self.vlcInstance4.media_new(url)
            self.vlcPlayer4.set_media(media_temp)
            self.vlcPlayer4.play()
        elif mon_number == 5:
            self.vlcPlayer5.stop()
            media_temp = self.vlcInstance5.media_new(url)
            self.vlcPlayer5.set_media(media_temp)
            self.vlcPlayer5.play()
        elif mon_number == 6:
            self.vlcPlayer6.stop()
            media_temp = self.vlcInstance6.media_new(url)
            self.vlcPlayer6.set_media(media_temp)
            self.vlcPlayer6.play()
        elif mon_number == 7:
            self.vlcPlayer7.stop()
            media_temp = self.vlcInstance7.media_new(url)
            self.vlcPlayer7.set_media(media_temp)
            self.vlcPlayer7.play()
        elif mon_number == 8:
            self.vlcPlayer8.stop()
            media_temp = self.vlcInstance8.media_new(url)
            self.vlcPlayer8.set_media(media_temp)
            self.vlcPlayer8.play()
        elif mon_number == 9:
            self.vlcPlayer9.stop()
            media_temp = self.vlcInstance9.media_new(url)
            self.vlcPlayer9.set_media(media_temp)
            self.vlcPlayer9.play()
        elif mon_number == 10:
            self.vlcPlayer10.stop()
            media_temp = self.vlcInstance10.media_new(url)
            self.vlcPlayer10.set_media(media_temp)
            self.vlcPlayer10.play()
        elif mon_number == 11:
            self.vlcPlayer11.stop()
            media_temp = self.vlcInstance11.media_new(url)
            self.vlcPlayer11.set_media(media_temp)
            self.vlcPlayer11.play()
        elif mon_number == 12:
            self.vlcPlayer12.stop()
            media_temp = self.vlcInstance12.media_new(url)
            self.vlcPlayer12.set_media(media_temp)
            self.vlcPlayer12.play()
        elif mon_number == 13:
            self.vlcPlayer13.stop()
            media_temp = self.vlcInstance13.media_new(url)
            self.vlcPlayer13.set_media(media_temp)
            self.vlcPlayer13.play()
        elif mon_number == 14:
            self.vlcPlayer14.stop()
            media_temp = self.vlcInstance14.media_new(url)
            self.vlcPlayer14.set_media(media_temp)
            self.vlcPlayer14.play()
        elif mon_number == 15:
            self.vlcPlayer15.stop()
            media_temp = self.vlcInstance15.media_new(url)
            self.vlcPlayer15.set_media(media_temp)
            self.vlcPlayer15.play()
        elif mon_number == 16:
            self.vlcPlayer16.stop()
            media_temp = self.vlcInstance16.media_new(url)
            self.vlcPlayer16.set_media(media_temp)
            self.vlcPlayer16.play()

        self.parent.update()

    def cyclic_mon1(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon1CyclicStatus = True
        while not self.closeMon1Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(1, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon1Cyclic:
                        break
                if self.closeMon1Cyclic:
                    break
        self.mon1CyclicStatus = False

    def close_cyclic_mon1(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon1Cyclic = True
        while self.mon1CyclicStatus:
            time.sleep(0.1)
        self.closeMon1Cyclic = False

    def cyclic_mon1_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon1()
        self.threadMonCyclic1 = threading.Thread(target=self.cyclic_mon1, args=(sentence,)).start()

    def cyclic_mon2(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon2CyclicStatus = True
        while not self.closeMon2Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(2, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon2Cyclic:
                        break
                if self.closeMon2Cyclic:
                    break
        self.mon2CyclicStatus = False

    def close_cyclic_mon2(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon2Cyclic = True
        while self.mon2CyclicStatus:
            time.sleep(0.1)
        self.closeMon2Cyclic = False

    def cyclic_mon2_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon2()
        self.threadMonCyclic2 = threading.Thread(target=self.cyclic_mon2, args=(sentence,)).start()

    def cyclic_mon3(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon3CyclicStatus = True
        while not self.closeMon3Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(3, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon3Cyclic:
                        break
                if self.closeMon3Cyclic:
                    break
        self.mon3CyclicStatus = False

    def close_cyclic_mon3(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon3Cyclic = True
        while self.mon3CyclicStatus:
            time.sleep(0.1)
        self.closeMon3Cyclic = False

    def cyclic_mon3_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon3()
        self.threadMonCyclic3 = threading.Thread(target=self.cyclic_mon3, args=(sentence,)).start()

    def cyclic_mon4(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon4CyclicStatus = True
        while not self.closeMon4Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(4, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon4Cyclic:
                        break
                if self.closeMon4Cyclic:
                    break
        self.mon4CyclicStatus = False

    def close_cyclic_mon4(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon4Cyclic = True
        while self.mon4CyclicStatus:
            time.sleep(0.1)
        self.closeMon4Cyclic = False

    def cyclic_mon4_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon4()
        self.threadMonCyclic4 = threading.Thread(target=self.cyclic_mon4, args=(sentence,)).start()

    def cyclic_mon5(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon5CyclicStatus = True
        while not self.closeMon5Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(5, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon5Cyclic:
                        break
                if self.closeMon5Cyclic:
                    break
        self.mon5CyclicStatus = False

    def close_cyclic_mon5(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon5Cyclic = True
        while self.mon5CyclicStatus:
            time.sleep(0.1)
        self.closeMon5Cyclic = False

    def cyclic_mon5_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon5()
        self.threadMonCyclic5 = threading.Thread(target=self.cyclic_mon5, args=(sentence,)).start()

    def cyclic_mon6(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon6CyclicStatus = True
        while not self.closeMon6Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(6, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon6Cyclic:
                        break
                if self.closeMon6Cyclic:
                    break
        self.mon6CyclicStatus = False

    def close_cyclic_mon6(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon6Cyclic = True
        while self.mon6CyclicStatus:
            time.sleep(0.1)
        self.closeMon6Cyclic = False

    def cyclic_mon6_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon6()
        self.threadMonCyclic6 = threading.Thread(target=self.cyclic_mon6, args=(sentence,)).start()

    def cyclic_mon7(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon7CyclicStatus = True
        while not self.closeMon7Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(7, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon7Cyclic:
                        break
                if self.closeMon7Cyclic:
                    break
        self.mon7CyclicStatus = False

    def close_cyclic_mon7(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon7Cyclic = True
        while self.mon7CyclicStatus:
            time.sleep(0.1)
        self.closeMon7Cyclic = False

    def cyclic_mon7_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon7()
        self.threadMonCyclic7 = threading.Thread(target=self.cyclic_mon7, args=(sentence,)).start()

    def cyclic_mon8(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon8CyclicStatus = True
        while not self.closeMon8Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(8, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon8Cyclic:
                        break
                if self.closeMon8Cyclic:
                    break
        self.mon8CyclicStatus = False

    def close_cyclic_mon8(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon8Cyclic = True
        while self.mon8CyclicStatus:
            time.sleep(0.1)
        self.closeMon8Cyclic = False

    def cyclic_mon8_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon8()
        self.threadMonCyclic8 = threading.Thread(target=self.cyclic_mon8, args=(sentence,)).start()

    def cyclic_mon9(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon9CyclicStatus = True
        while not self.closeMon9Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(9, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon9Cyclic:
                        break
                if self.closeMon9Cyclic:
                    break
        self.mon9CyclicStatus = False

    def close_cyclic_mon9(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon9Cyclic = True
        while self.mon9CyclicStatus:
            time.sleep(0.1)
        self.closeMon9Cyclic = False

    def cyclic_mon9_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon9()
        self.threadMonCyclic9 = threading.Thread(target=self.cyclic_mon9, args=(sentence,)).start()

    def cyclic_mon10(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon10CyclicStatus = True
        while not self.closeMon10Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(10, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon10Cyclic:
                        break
                if self.closeMon10Cyclic:
                    break
        self.mon10CyclicStatus = False

    def close_cyclic_mon10(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon10Cyclic = True
        while self.mon10CyclicStatus:
            time.sleep(0.1)
        self.closeMon10Cyclic = False

    def cyclic_mon10_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon10()
        self.threadMonCyclic10 = threading.Thread(target=self.cyclic_mon10, args=(sentence,)).start()

    def cyclic_mon11(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon11CyclicStatus = True
        while not self.closeMon11Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(11, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon11Cyclic:
                        break
                if self.closeMon11Cyclic:
                    break
        self.mon11CyclicStatus = False

    def close_cyclic_mon11(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon11Cyclic = True
        while self.mon11CyclicStatus:
            time.sleep(0.1)
        self.closeMon11Cyclic = False

    def cyclic_mon11_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon11()
        self.threadMonCyclic11 = threading.Thread(target=self.cyclic_mon11, args=(sentence,)).start()

    def cyclic_mon12(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon12CyclicStatus = True
        while not self.closeMon12Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(12, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon12Cyclic:
                        break
                if self.closeMon12Cyclic:
                    break
        self.mon12CyclicStatus = False

    def close_cyclic_mon12(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon12Cyclic = True
        while self.mon12CyclicStatus:
            time.sleep(0.1)
        self.closeMon12Cyclic = False

    def cyclic_mon12_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon12()
        self.threadMonCyclic12 = threading.Thread(target=self.cyclic_mon12, args=(sentence,)).start()

    def cyclic_mon13(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon13CyclicStatus = True
        while not self.closeMon13Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(13, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon13Cyclic:
                        break
                if self.closeMon13Cyclic:
                    break
        self.mon13CyclicStatus = False

    def close_cyclic_mon13(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon13Cyclic = True
        while self.mon13CyclicStatus:
            time.sleep(0.1)
        self.closeMon13Cyclic = False

    def cyclic_mon13_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon13()
        self.threadMonCyclic13 = threading.Thread(target=self.cyclic_mon13, args=(sentence,)).start()

    def cyclic_mon14(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon14CyclicStatus = True
        while not self.closeMon14Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(14, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon14Cyclic:
                        break
                if self.closeMon14Cyclic:
                    break
        self.mon14CyclicStatus = False

    def close_cyclic_mon14(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon14Cyclic = True
        while self.mon14CyclicStatus:
            time.sleep(0.1)
        self.closeMon14Cyclic = False

    def cyclic_mon14_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon14()
        self.threadMonCyclic14 = threading.Thread(target=self.cyclic_mon14, args=(sentence,)).start()

    def cyclic_mon15(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon15CyclicStatus = True
        while not self.closeMon15Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(15, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon15Cyclic:
                        break
                if self.closeMon15Cyclic:
                    break
        self.mon15CyclicStatus = False

    def close_cyclic_mon15(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon15Cyclic = True
        while self.mon15CyclicStatus:
            time.sleep(0.1)
        self.closeMon15Cyclic = False

    def cyclic_mon15_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon15()
        self.threadMonCyclic15 = threading.Thread(target=self.cyclic_mon15, args=(sentence,)).start()

    def cyclic_mon16(self, sentence):
        """Lance le cyclique sur ce moniteur"""
        self.mon16CyclicStatus = True
        while not self.closeMon16Cyclic:
            for i in range(2, len(sentence), 2):
                self.set_media_to_mon(16, sentence[i])
                for y in range(int(sentence[i + 1])):
                    time.sleep(1)
                    if self.closeMon16Cyclic:
                        break
                if self.closeMon16Cyclic:
                    break
        self.mon16CyclicStatus = False

    def close_cyclic_mon16(self):
        """Ferme le cyclique (si présent) sur ce moniteur"""
        self.closeMon16Cyclic = True
        while self.mon16CyclicStatus:
            time.sleep(0.1)
        self.closeMon16Cyclic = False

    def cyclic_mon16_lookup(self, sentence):
        """S'assure de fermer le cyclique s'il y en a un sur ce moniteur, et lance un nouveau en appelant la fonction threadMonCyclicXX"""
        self.close_cyclic_mon16()
        self.threadMonCyclic16 = threading.Thread(target=self.cyclic_mon16, args=(sentence,)).start()

    def kill_all_cyclic(self):
        """Arrete tout les cycliques présents"""
        temp_thread1 = threading.Thread(target=self.close_cyclic_mon1)
        temp_thread2 = threading.Thread(target=self.close_cyclic_mon2)
        temp_thread3 = threading.Thread(target=self.close_cyclic_mon3)
        temp_thread4 = threading.Thread(target=self.close_cyclic_mon4)
        temp_thread5 = threading.Thread(target=self.close_cyclic_mon5)
        temp_thread6 = threading.Thread(target=self.close_cyclic_mon6)
        temp_thread7 = threading.Thread(target=self.close_cyclic_mon7)
        temp_thread8 = threading.Thread(target=self.close_cyclic_mon8)
        temp_thread9 = threading.Thread(target=self.close_cyclic_mon9)
        temp_thread10 = threading.Thread(target=self.close_cyclic_mon10)
        temp_thread11 = threading.Thread(target=self.close_cyclic_mon11)
        temp_thread12 = threading.Thread(target=self.close_cyclic_mon12)
        temp_thread13 = threading.Thread(target=self.close_cyclic_mon13)
        temp_thread14 = threading.Thread(target=self.close_cyclic_mon14)
        temp_thread15 = threading.Thread(target=self.close_cyclic_mon15)
        temp_thread16 = threading.Thread(target=self.close_cyclic_mon16)

        temp_thread1.start()
        temp_thread2.start()
        temp_thread3.start()
        temp_thread4.start()
        temp_thread5.start()
        temp_thread6.start()
        temp_thread7.start()
        temp_thread8.start()
        temp_thread9.start()
        temp_thread10.start()
        temp_thread11.start()
        temp_thread12.start()
        temp_thread13.start()
        temp_thread14.start()
        temp_thread15.start()
        temp_thread16.start()

        temp_thread1.join()
        temp_thread2.join()
        temp_thread3.join()
        temp_thread4.join()
        temp_thread5.join()
        temp_thread6.join()
        temp_thread7.join()
        temp_thread8.join()
        temp_thread9.join()
        temp_thread10.join()
        temp_thread11.join()
        temp_thread12.join()
        temp_thread13.join()
        temp_thread14.join()
        temp_thread15.join()
        temp_thread16.join()

    def set_default_to_all_mon(self):
        """Met le logo tts sur tout les moniteurs présents"""
        self.set_media_to_mon(1, "C:\\Decodeur\\Media\\default.png")
        if self.numberOfMon >= 4:
            self.set_media_to_mon(2, "C:\\Decodeur\\Media\\default.png")
            self.set_media_to_mon(3, "C:\\Decodeur\\Media\\default.png")
            self.set_media_to_mon(4, "C:\\Decodeur\\Media\\default.png")
            if self.numberOfMon >= 6:
                self.set_media_to_mon(5, "C:\\Decodeur\\Media\\default.png")
                self.set_media_to_mon(6, "C:\\Decodeur\\Media\\default.png")
                if self.numberOfMon >= 8:
                    self.set_media_to_mon(7, "C:\\Decodeur\\Media\\default.png")
                    self.set_media_to_mon(8, "C:\\Decodeur\\Media\\default.png")
                    if self.numberOfMon >= 9:
                        self.set_media_to_mon(9, "C:\\Decodeur\\Media\\default.png")
                        if self.numberOfMon >= 13:
                            self.set_media_to_mon(10, "C:\\Decodeur\\Media\\default.png")
                            self.set_media_to_mon(11, "C:\\Decodeur\\Media\\default.png")
                            self.set_media_to_mon(12, "C:\\Decodeur\\Media\\default.png")
                            self.set_media_to_mon(13, "C:\\Decodeur\\Media\\default.png")
                            if self.numberOfMon >= 16:
                                self.set_media_to_mon(14, "C:\\Decodeur\\Media\\default.png")
                                self.set_media_to_mon(15, "C:\\Decodeur\\Media\\default.png")
                                self.set_media_to_mon(16, "C:\\Decodeur\\Media\\default.png")


def is_conf_file_exist():
    """Vérifie si le dossier Décodeur existe et/ou le créer, vérifie si le decodeurConf.ini existe et/ou le créer"""
    if not os.path.isdir("C:/Decodeur"):
        os.mkdir("C:/Decodeur")
    if not os.path.isfile("C:/Decodeur/decodeurConf.ini"):
        config_ini = configparser.ConfigParser()
        config_ini.optionxform = str
        config_ini["DECODEUR"] = {"IPdecodeur": "192.168.1.1", "PORTdecodeur": "50050", "PrepoType": "4", "BorderColor": "black", "BackgroundrColor": "grey30"}
        config_ini.write(open("C:\Decodeur\decodeurConf.ini", "w"))


def read_conf_file():
    """Lit decodeurConf.ini et retourne les informations"""
    config_ini = configparser.ConfigParser()
    config_ini.optionxform = str
    config_ini.read("C:\Decodeur\decodeurConf.ini")
    return config_ini["DECODEUR"]["IPdecodeur"], config_ini["DECODEUR"]["PORTdecodeur"], config_ini["DECODEUR"]["PrepoType"], config_ini["DECODEUR"]["BorderColor"], config_ini["DECODEUR"]["BackgroundrColor"]


def _quit(null):
    """Appelé lorsqu'on ferme la fenêtre. Récupère les infos et les enregistres dans decodeurConf.ini, ferme le socket et l'IHM"""
    config_ini = configparser.ConfigParser()
    config_ini.optionxform = str
    config_ini.read("C:\Decodeur\decodeurConf.ini")
    config_ini.set("DECODEUR", "PrepoType", str(monitorDisplay.numberOfMon))
    config_ini.write(open("C:\Decodeur\decodeurConf.ini", "w"))
    UDPServerSocket.close()
    root.quit()  # stops mainloop
    # root.destroy()  # this is necessary on Windows to prevent Fatal Python Error: PyEval_RestoreThread: NULL state
    os._exit(1)


def toggle_cursor(null):
    """Change l'état du curseur en appuyant sur <c>. N'est finalement pas très utile et va surement dégager"""
    global cursorState
    if cursorState:
        root.config(cursor="none")
        cursorState = False
    else:
        root.config(cursor="")
        cursorState = True


def server_udp():
    """Serveur gérant l'écoute et le renvoit de commandes, lancé par un thread"""
    global cursorState
    while True:
        received_frame = UDPServerSocket.recvfrom(BUFFER_SIZE)
        message = received_frame[0]

        sentence = (message.decode("utf-8").split(SEPARATOR))

        if sentence[0] == SDK_COMMAND1:  # Commutation
            if int(sentence[1]) > monitorDisplay.numberOfMon:
                UDPServerSocket.sendto(str.encode("Moniteur innexistant"), received_frame[1])
            else:
                root.config(cursor="none")
                cursorState = False
                if int(sentence[1]) == 1:  # Moniteur 1
                    temp_thread1 = threading.Thread(target=monitorDisplay.close_cyclic_mon1)
                    temp_thread1.start()
                    temp_thread1.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 2:  # Moniteur 2
                    temp_thread2 = threading.Thread(target=monitorDisplay.close_cyclic_mon2)
                    temp_thread2.start()
                    temp_thread2.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 3:  # Moniteur 3
                    temp_thread3 = threading.Thread(target=monitorDisplay.close_cyclic_mon3)
                    temp_thread3.start()
                    temp_thread3.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 4:  # Moniteur 4
                    temp_thread4 = threading.Thread(target=monitorDisplay.close_cyclic_mon4)
                    temp_thread4.start()
                    temp_thread4.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 5:  # Moniteur 5
                    temp_thread5 = threading.Thread(target=monitorDisplay.close_cyclic_mon5)
                    temp_thread5.start()
                    temp_thread5.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 6:  # Moniteur 6
                    temp_thread6 = threading.Thread(target=monitorDisplay.close_cyclic_mon6)
                    temp_thread6.start()
                    temp_thread6.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 7:  # Moniteur 7
                    temp_thread7 = threading.Thread(target=monitorDisplay.close_cyclic_mon7)
                    temp_thread7.start()
                    temp_thread7.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 8:  # Moniteur 8
                    temp_thread8 = threading.Thread(target=monitorDisplay.close_cyclic_mon8)
                    temp_thread8.start()
                    temp_thread8.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 9:  # Moniteur 9
                    temp_thread9 = threading.Thread(target=monitorDisplay.close_cyclic_mon9)
                    temp_thread9.start()
                    temp_thread9.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 10:  # Moniteur 10
                    temp_thread10 = threading.Thread(target=monitorDisplay.close_cyclic_mon10)
                    temp_thread10.start()
                    temp_thread10.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 11:  # Moniteur 11
                    temp_thread11 = threading.Thread(target=monitorDisplay.close_cyclic_mon11)
                    temp_thread11.start()
                    temp_thread11.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 12:  # Moniteur 12
                    temp_thread12 = threading.Thread(target=monitorDisplay.close_cyclic_mon12)
                    temp_thread12.start()
                    temp_thread12.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 13:  # Moniteur 13
                    temp_thread13 = threading.Thread(target=monitorDisplay.close_cyclic_mon13)
                    temp_thread13.start()
                    temp_thread13.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 14:  # Moniteur 14
                    temp_thread14 = threading.Thread(target=monitorDisplay.close_cyclic_mon14)
                    temp_thread14.start()
                    temp_thread14.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 15:  # Moniteur 15
                    temp_thread15 = threading.Thread(target=monitorDisplay.close_cyclic_mon15)
                    temp_thread15.start()
                    temp_thread15.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])
                elif int(sentence[1]) == 16:  # Moniteur 16
                    temp_thread16 = threading.Thread(target=monitorDisplay.close_cyclic_mon16)
                    temp_thread16.start()
                    temp_thread16.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), sentence[2])



        elif sentence[0] == SDK_COMMAND2:  # Cyclique
            if int(sentence[1]) > monitorDisplay.numberOfMon:
                UDPServerSocket.sendto(str.encode("Moniteur innexistant"), received_frame[1])
            else:
                root.config(cursor="none")
                cursorState = False
                if sentence[1] == "1":  # Moniteur 1
                    monitorDisplay.cyclic_mon1_lookup(sentence)
                elif sentence[1] == "2":  # Moniteur 2
                    monitorDisplay.cyclic_mon2_lookup(sentence)
                elif sentence[1] == "3":  # Moniteur 3
                    monitorDisplay.cyclic_mon3_lookup(sentence)
                elif sentence[1] == "4":  # Moniteur 4
                    monitorDisplay.cyclic_mon4_lookup(sentence)
                elif sentence[1] == "5":  # Moniteur 5
                    monitorDisplay.cyclic_mon5_lookup(sentence)
                elif sentence[1] == "6":  # Moniteur 6
                    monitorDisplay.cyclic_mon6_lookup(sentence)
                elif sentence[1] == "7":  # Moniteur 7
                    monitorDisplay.cyclic_mon7_lookup(sentence)
                elif sentence[1] == "8":  # Moniteur 8
                    monitorDisplay.cyclic_mon8_lookup(sentence)
                elif sentence[1] == "9":  # Moniteur 9
                    monitorDisplay.cyclic_mon9_lookup(sentence)
                elif sentence[1] == "10":  # Moniteur 10
                    monitorDisplay.cyclic_mon10_lookup(sentence)
                elif sentence[1] == "11":  # Moniteur 11
                    monitorDisplay.cyclic_mon11_lookup(sentence)
                elif sentence[1] == "12":  # Moniteur 12
                    monitorDisplay.cyclic_mon12_lookup(sentence)
                elif sentence[1] == "13":  # Moniteur 13
                    monitorDisplay.cyclic_mon13_lookup(sentence)
                elif sentence[1] == "14":  # Moniteur 14
                    monitorDisplay.cyclic_mon14_lookup(sentence)
                elif sentence[1] == "15":  # Moniteur 15
                    monitorDisplay.cyclic_mon15_lookup(sentence)
                elif sentence[1] == "16":  # Moniteur 16
                    monitorDisplay.cyclic_mon16_lookup(sentence)



        elif sentence[0] == SDK_COMMAND3:  # Signal de vie
            UDPServerSocket.sendto(str.encode("Réponse signal de vie"), received_frame[1])



        elif sentence[0] == SDK_COMMAND4:  # Mise au noir
            if int(sentence[1]) > monitorDisplay.numberOfMon:
                UDPServerSocket.sendto(str.encode("Moniteur innexistant"), received_frame[1])
            else:
                if int(sentence[1]) == 1:  # Moniteur 1
                    temp_thread1 = threading.Thread(target=monitorDisplay.close_cyclic_mon1)
                    temp_thread1.start()
                    temp_thread1.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 2:  # Moniteur 2
                    temp_thread2 = threading.Thread(target=monitorDisplay.close_cyclic_mon2)
                    temp_thread2.start()
                    temp_thread2.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 3:  # Moniteur 3
                    temp_thread3 = threading.Thread(target=monitorDisplay.close_cyclic_mon3)
                    temp_thread3.start()
                    temp_thread3.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 4:  # Moniteur 4
                    temp_thread4 = threading.Thread(target=monitorDisplay.close_cyclic_mon4)
                    temp_thread4.start()
                    temp_thread4.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 5:  # Moniteur 5
                    temp_thread5 = threading.Thread(target=monitorDisplay.close_cyclic_mon5)
                    temp_thread5.start()
                    temp_thread5.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 6:  # Moniteur 6
                    temp_thread6 = threading.Thread(target=monitorDisplay.close_cyclic_mon6)
                    temp_thread6.start()
                    temp_thread6.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 7:  # Moniteur 7
                    temp_thread7 = threading.Thread(target=monitorDisplay.close_cyclic_mon7)
                    temp_thread7.start()
                    temp_thread7.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 8:  # Moniteur 8
                    temp_thread8 = threading.Thread(target=monitorDisplay.close_cyclic_mon8)
                    temp_thread8.start()
                    temp_thread8.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 9:  # Moniteur 9
                    temp_thread9 = threading.Thread(target=monitorDisplay.close_cyclic_mon9)
                    temp_thread9.start()
                    temp_thread9.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 10:  # Moniteur 10
                    temp_thread10 = threading.Thread(target=monitorDisplay.close_cyclic_mon10)
                    temp_thread10.start()
                    temp_thread10.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 11:  # Moniteur 11
                    temp_thread11 = threading.Thread(target=monitorDisplay.close_cyclic_mon11)
                    temp_thread11.start()
                    temp_thread11.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 12:  # Moniteur 12
                    temp_thread12 = threading.Thread(target=monitorDisplay.close_cyclic_mon12)
                    temp_thread12.start()
                    temp_thread12.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 13:  # Moniteur 13
                    temp_thread13 = threading.Thread(target=monitorDisplay.close_cyclic_mon13)
                    temp_thread13.start()
                    temp_thread13.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 14:  # Moniteur 14
                    temp_thread14 = threading.Thread(target=monitorDisplay.close_cyclic_mon14)
                    temp_thread14.start()
                    temp_thread14.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 15:  # Moniteur 15
                    temp_thread15 = threading.Thread(target=monitorDisplay.close_cyclic_mon15)
                    temp_thread15.start()
                    temp_thread15.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")
                elif int(sentence[1]) == 16:  # Moniteur 16
                    temp_thread16 = threading.Thread(target=monitorDisplay.close_cyclic_mon16)
                    temp_thread16.start()
                    temp_thread16.join()
                    monitorDisplay.set_media_to_mon(int(sentence[1]), "C:\Decodeur\Media\default.png")



        elif sentence[0] == SDK_COMMAND5:  # Changer de prépo
            root.config(cursor="none")
            cursorState = False
            if sentence[1] == "1":
                monitorDisplay.kill_all_cyclic()
                monitorDisplay.kill_all_mon()
                monitorDisplay.single()
            elif sentence[1] == "4":
                monitorDisplay.kill_all_cyclic()
                monitorDisplay.kill_all_mon()
                monitorDisplay.quad()
            elif sentence[1] == "6":
                monitorDisplay.kill_all_cyclic()
                monitorDisplay.kill_all_mon()
                monitorDisplay.six()
            elif sentence[1] == "8":
                monitorDisplay.kill_all_cyclic()
                monitorDisplay.kill_all_mon()
                monitorDisplay.eight()
            elif sentence[1] == "9":
                monitorDisplay.kill_all_cyclic()
                monitorDisplay.kill_all_mon()
                monitorDisplay.nano()
            elif sentence[1] == "13":
                monitorDisplay.kill_all_cyclic()
                monitorDisplay.kill_all_mon()
                monitorDisplay.thirteen()
            elif sentence[1] == "16":
                monitorDisplay.kill_all_cyclic()
                monitorDisplay.kill_all_mon()
                monitorDisplay.sixteen()
            else:
                UDPServerSocket.sendto(str.encode("Prépo. inconnue"), received_frame[1])



        else:
            UDPServerSocket.sendto(str.encode("Commande inconnue/incomprise"), received_frame[1])


if __name__ == "__main__":
    """Lancement du programme"""
    is_conf_is_readable = True
    error = ""

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    info_window = customtkinter.CTk()

    is_conf_file_exist()  # Vérification de l'existance du .ini
    decoderSettings = read_conf_file()  # Lecture du .ini

    ip_address = decoderSettings[0]

    if is_conf_is_readable:  # Vérif si IP correcte
        try:
            test_ip_address = ipaddress.ip_address(ip_address)
        except ValueError:
            is_conf_is_readable = False
            error = "L'adresse IP est invalide\nVérifier dans C:\Decodeur\decodeurConf.ini"

    if is_conf_is_readable:  # Vérif si port correcte
        try:
            port = int(decoderSettings[1])
            if port < 1 or port > 65535:
                is_conf_is_readable = False
                error = "Le port est invalide\nVérifier dans C:\Decodeur\decodeurConf.ini"
        except ValueError:
            is_conf_is_readable = False
            error = "Le port est invalide\nVérifier dans C:\Decodeur\decodeurConf.ini"

    if is_conf_is_readable:  # Vérif si prépo correcte
        try:
            prepo_type = int(decoderSettings[2])
            if prepo_type not in [1, 4, 6, 8, 9, 13, 16]:
                is_conf_is_readable = False
                error = "La préposition est invalide\nVérifier dans C:\Decodeur\decodeurConf.ini\n(Doit être comprise entre 1, 4, 6, 8, 9, 13, 16)"
        except ValueError:
            is_conf_is_readable = False
            error = "La préposition est invalide\nVérifier dans C:\Decodeur\decodeurConf.ini\n(Doit être comprise entre 1, 4, 6, 8, 9, 13, 16)"

    if is_conf_is_readable:  # Vérif il arrive a ouvrir un socket sur l'IP fournie
        while True:
            try:
                if not is_conf_is_readable:
                    break
                else:
                    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
                    UDPServerSocket.bind((ip_address, port))
                    ThUDP = threading.Thread(target=server_udp).start()
                    is_conf_is_readable = True
                break
            except OSError:  # Si IP non trouvée, demande à l'utilisateur d'en renseigner une a nouveau
                while True:
                    try:
                        ask_ip_address = customtkinter.CTkInputDialog(text="Entrez l'IP sur laquelle le décodeur va dialoguer\n\nCette IP doit faire référence à une de vos cartes réseau", title="DWELL")
                        ip_address = ask_ip_address.get_input()
                        if ip_address is None or ip_address == "":  # → Appuyez sur x ou quitter, quitte sans faire de message d'erreur
                            is_conf_is_readable = False
                            break
                        else:
                            test_ip_address = ipaddress.ip_address(ip_address)
                            # info_window.quit()
                            config_ini = configparser.ConfigParser()
                            config_ini.optionxform = str
                            config_ini.read("C:\Decodeur\decodeurConf.ini")
                            config_ini.set("DECODEUR", "IPdecodeur", ip_address)
                            config_ini.write(open("C:\Decodeur\decodeurConf.ini", "w"))
                            break
                    except ValueError:
                        pass

    if is_conf_is_readable:  # Si le .ini est OK, lance l'appli
        root = Tk()
        root.title("Décodeur TTS")
        root.attributes('-fullscreen', True)
        root.protocol("WM_DELETE_WINDOW", _quit)
        root['background'] = decoderSettings[3]

        root.bind('<Escape>', _quit)
        root.bind('<c>', toggle_cursor)
        cursorState = False
        root.config(cursor="none")

        monitorDisplay = SetMonitorArrangement(root, prepo_type, decoderSettings[4])

        root.mainloop()

    elif error != "":  # Si erreur présente, l'affiche sous forme de message box
        info_window.title("Erreur")
        info_window.resizable(False, False)
        frame1 = customtkinter.CTkFrame(info_window)
        frame1.pack(expand=True, fill=BOTH)
        label1 = customtkinter.CTkLabel(frame1, text="Erreur durant l'ouverture du décodeur :", font=("Arial", 20), text_color="orange red").pack(padx=20, pady=00)
        label2 = customtkinter.CTkLabel(frame1, text=error, font=("Arial", 15)).pack(padx=20, pady=25)
        button1 = customtkinter.CTkButton(frame1, text="OK", command=info_window.destroy).pack(padx=20, pady=20)
        info_window.mainloop()
