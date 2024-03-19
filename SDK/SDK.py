import customtkinter as ctk
from tkinter import ttk
import socket
import os
from datetime import datetime
import threading
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

    def __init__(self, main_window, decodeur_ip, decodeur_port, liste):
        """"Création de la classe"""
        self.decodeur_ip = decodeur_ip
        self.decodeur_port = decodeur_port
        self.liste = liste
        self.serverAddressPort = (self.decodeur_ip, self.decodeur_port)

        self.main_window = main_window
        self.main_window.title("SDK Décodeur TTS")
        # self.main_window.geometry("1000x600")
        self.main_window.resizable(False, False)
        self.main_window.protocol("WM_DELETE_WINDOW", self._quit)

        self.Frame1 = ctk.CTkFrame(master=self.main_window)
        self.Frame1.grid(row=0, column=0, pady=10, padx=10, columnspan=2, sticky="nsew")

        self.labelURL = ctk.CTkLabel(master=self.Frame1, text="URL :")
        self.labelURL.grid(row=0, column=0, pady=5, padx=5)

        self.entryURL = ctk.CTkEntry(master=self.Frame1,
                                     placeholder_text="ex: rtsp://10.0.0.54   ou   C:\Videos\\top_10_tacos_lyon.mp4   ou   D:\Images\chaton_trop_mimi.jpg",
                                     width=605)
        self.entryURL.grid(row=0, column=1, pady=5, padx=5)

        self.iFrame1 = ctk.CTkFrame(master=self.Frame1)
        self.iFrame1.grid(row=0, column=2, pady=5, padx=5)

        self.labelMon = ctk.CTkLabel(master=self.iFrame1, text="N° Mon :")
        self.labelMon.grid(row=0, column=0, pady=0, padx=5)

        self.monSpinBoxP = ctk.CTkButton(master=self.iFrame1, text="+", width=1, height=1, font=("Arial", 15),
                                         border_spacing=-100, border_width=-1, command=self.mon_spin_box_plus)
        self.monSpinBoxP.grid(row=0, column=1, padx=1, pady=0)

        self.monSpinBoxM = ctk.CTkButton(master=self.iFrame1, text="-", width=11, height=1, font=("Arial", 15),
                                         border_spacing=-100, border_width=-1, command=self.mon_spin_box_minus)
        self.monSpinBoxM.grid(row=0, column=2, padx=1, pady=0)

        self.entryMon = ctk.CTkEntry(master=self.iFrame1, width=35)
        self.entryMon.insert(0, "1")
        self.entryMon.configure(state=ctk.DISABLED)
        self.entryMon.grid(row=0, column=3, padx=5, pady=0)

        self.buttonSend = ctk.CTkButton(master=self.Frame1, text="Envoyer", command=self.send_url_to_decoder, width=15)
        self.buttonSend.grid(row=0, column=3, pady=5, padx=5)

        self.buttonAddToList = ctk.CTkButton(master=self.Frame1, text="Ajouter à la liste",
                                             command=self.add_cam_to_list, width=15)
        self.buttonAddToList.grid(row=0, column=4, pady=5, padx=5)

        self.Frame2 = ctk.CTkFrame(master=self.main_window)
        self.Frame2.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        self.labelCamList = ctk.CTkLabel(master=self.Frame2, text="Liste caméra aquise")
        self.labelCamList.grid(row=0, column=0)

        self.iFrame2 = ctk.CTkFrame(master=self.Frame2)
        self.iFrame2.grid(row=1, column=0, padx=10, pady=10)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="grey65", foreground="black", fieldbackground="grey65")
        self.style.configure("Treeview.Heading", background="grey40", foreground="white")
        self.style.map('Treeview.Heading', background=[('active', 'grey32')])
        self.style.map('Treeview', background=[('selected', 'grey50')])

        self.cameraAddedTreeView = ttk.Treeview(self.iFrame2, height=12)

        self.cameraAddedTreeView["columns"] = "1"
        self.cameraAddedTreeView['show'] = 'headings'
        self.cameraAddedTreeView.column("1", width=336, anchor='w')
        self.cameraAddedTreeView.heading("1", text="URL")

        self.cameraAddedScrollbar = ttk.Scrollbar(self.iFrame2, orient=ctk.VERTICAL,
                                                  command=self.cameraAddedTreeView.yview)
        self.cameraAddedScrollbar.pack(side=ctk.RIGHT, fill=ctk.Y, expand=False)

        self.cameraAddedTreeView.configure(yscrollcommand=self.cameraAddedScrollbar.set)
        self.cameraAddedTreeView.bind("<Double-1>", self.add_cam_to_entry2)
        self.cameraAddedTreeView.pack(side="left", fill="both", expand=True)

        self.iiFrame2 = ctk.CTkFrame(master=self.Frame2)
        self.iiFrame2.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        self.addToEntry = ctk.CTkButton(master=self.iiFrame2, text="Ajouter ↑", width=10,
                                        command=self.add_cam_to_entry1)
        self.addToEntry.pack(padx=5, pady=10)

        self.addToCycleButton = ctk.CTkButton(master=self.iiFrame2, text="Ajouter →", width=10,
                                              command=self.add_cam_to_cyclic)
        self.addToCycleButton.pack(padx=5, pady=10)

        self.delCamListButton = ctk.CTkButton(master=self.iiFrame2, text="Suppr.", width=10,
                                              command=self.remove_cam_list)
        self.delCamListButton.pack(padx=5, pady=10)

        # buttonSaveList = customtkinter.CTkButton(master=iiFrame2, text="Sauver\nliste",width=10, command=saveCamList)
        # buttonSaveList.pack(padx=5, pady=10)
        #
        # buttonLoadList = customtkinter.CTkButton(master=iiFrame2, text="Charger", width=10, command=loadCamList)
        # buttonLoadList.pack(padx=5, pady=10)

        self.Frame3 = ctk.CTkFrame(master=self.main_window)
        self.Frame3.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")

        self.labelCamCyclic = ctk.CTkLabel(master=self.Frame3, text="Liste caméra cyclique")
        self.labelCamCyclic.grid(row=0, column=1)

        self.iiFrame3 = ctk.CTkFrame(master=self.Frame3)
        self.iiFrame3.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        self.delCamCyclicButton = ctk.CTkButton(master=self.iiFrame3, text="Suppr.", width=10,
                                                command=self.remove_cam_cyclic_list)
        self.delCamCyclicButton.pack(padx=5, pady=10)

        self.moveUpButton = ctk.CTkButton(master=self.iiFrame3, text="↑", width=10, command=self.move_cam_up)
        self.moveUpButton.pack(padx=5, pady=10)

        self.moveDownButton = ctk.CTkButton(master=self.iiFrame3, text="↓", width=10, command=self.move_cam_down)
        self.moveDownButton.pack(padx=5, pady=10)

        self.sendCyclicButton = ctk.CTkButton(master=self.iiFrame3, text="Envoyer\ncyclique", width=10,
                                              command=self.send_cyclic_to_decoder)
        self.sendCyclicButton.pack(padx=5, pady=10)

        self.iFrame3 = ctk.CTkFrame(master=self.Frame3)
        self.iFrame3.grid(row=1, column=1, padx=10, pady=10)

        self.cameraCyclicTreeView = ttk.Treeview(self.iFrame3, height=12)

        self.cameraCyclicTreeView["columns"] = ("1", "2")
        self.cameraCyclicTreeView['show'] = 'headings'
        self.cameraCyclicTreeView.column("1", width=300, anchor='w')
        self.cameraCyclicTreeView.column("2", width=50, anchor='c')
        self.cameraCyclicTreeView.heading("1", text="URL")
        self.cameraCyclicTreeView.heading("2", text="DWELL")

        self.cameraAddedScrollbar = ttk.Scrollbar(self.iFrame3, orient=ctk.VERTICAL,
                                                  command=self.cameraCyclicTreeView.yview)
        self.cameraAddedScrollbar.pack(side=ctk.RIGHT, fill=ctk.Y, expand=False)

        self.cameraCyclicTreeView.configure(yscrollcommand=self.cameraAddedScrollbar.set)
        self.cameraCyclicTreeView.pack(side="left", fill="both", expand=True)

        self.Frame4 = ctk.CTkFrame(master=self.main_window)
        self.Frame4.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

        self.labelSdkLog = ctk.CTkLabel(master=self.Frame4, text="Log SDK")
        self.labelSdkLog.grid(row=0, column=0, sticky="w", padx=5)

        self.clearSdkButton = ctk.CTkButton(master=self.Frame4, text="Effacer", width=1, height=1,
                                            command=self.clear_sdk)
        self.clearSdkButton.grid(row=0, column=1, sticky="e", padx=5)

        self.sdkTextBox = ctk.CTkTextbox(master=self.Frame4, height=70, width=475)
        self.sdkTextBox.grid(row=1, column=0, columnspan=2)

        self.Frame5 = ctk.CTkFrame(master=self.main_window)
        self.Frame5.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")

        self.labelSdkLog = ctk.CTkLabel(master=self.Frame5, text="Log Décodeur")
        self.labelSdkLog.grid(row=0, column=0, sticky="w", padx=5)

        self.clearDecoderButton = ctk.CTkButton(master=self.Frame5, text="Effacer", width=1, height=1,
                                                command=self.clear_decoder)
        self.clearDecoderButton.grid(row=0, column=1, sticky="e", padx=5)

        self.decoderTextBox = ctk.CTkTextbox(master=self.Frame5, height=70, width=484, state=ctk.DISABLED)
        self.decoderTextBox.grid(row=1, column=0, columnspan=2)

        self.Frame6 = ctk.CTkFrame(master=self.main_window)
        self.Frame6.grid(row=3, column=0, pady=10, padx=10, columnspan=2, sticky="w")

        self.labelCommand = ctk.CTkLabel(master=self.Frame6, text="Commandes")
        self.labelCommand.grid(row=0, column=0, sticky="w", padx=5)

        self.sendLifeCommandButton = ctk.CTkButton(master=self.Frame6, text="Envoyer signal de vie", width=10,
                                                   command=self.send_life_command)
        self.sendLifeCommandButton.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.sendSetBlackCamButton = ctk.CTkButton(master=self.Frame6, text="Mise au noir", width=10,
                                                   command=self.send_set_black)
        self.sendSetBlackCamButton.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.sendSetSingleButton = ctk.CTkButton(master=self.Frame6, text="1x1", width=10, command=self.send_set_single)
        self.sendSetSingleButton.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.sendSetQuadButton = ctk.CTkButton(master=self.Frame6, text="2x2", width=10, command=self.send_set_quad)
        self.sendSetQuadButton.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.sendSetNanoButton = ctk.CTkButton(master=self.Frame6, text="3x3", width=10, command=self.send_set_nano)
        self.sendSetNanoButton.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        self.sendSet16 = ctk.CTkButton(master=self.Frame6, text="4x4", width=10, command=self.send_set_sixteen)
        self.sendSet16.grid(row=1, column=5, padx=5, pady=5, sticky="w")

        self.iFrame6 = ctk.CTkFrame(master=self.Frame6)
        self.iFrame6.grid(row=1, column=6, padx=5)

        self.labelCustomPrepo = ctk.CTkLabel(master=self.iFrame6, text="Custom\nprépo :", font=("Arial", 11))
        self.labelCustomPrepo.grid(row=0, column=0, sticky="w", padx=5)

        self.customMonSpinBoxP = ctk.CTkButton(master=self.iFrame6, text="+", width=1, height=1, font=("Arial", 15),
                                               border_spacing=-100, border_width=-1,
                                               command=self.custom_mon_spin_box_plus)
        self.customMonSpinBoxP.grid(row=0, column=1, padx=1, pady=0)

        self.customMonSpinBoxM = ctk.CTkButton(master=self.iFrame6, text="-", width=11, height=1, font=("Arial", 15),
                                               border_spacing=-100, border_width=-1,
                                               command=self.custom_mon_spin_box_minus)
        self.customMonSpinBoxM.grid(row=0, column=2, padx=1, pady=0)

        self.entryCustomMon = ctk.CTkEntry(master=self.iFrame6, width=35)
        self.entryCustomMon.insert(0, "1")
        self.entryCustomMon.configure(state=ctk.DISABLED)
        self.entryCustomMon.grid(row=0, column=3, padx=5, pady=0)

        self.sendCustomMonPrepoButton = ctk.CTkButton(master=self.Frame6, text="Envoyer", width=5,
                                                      command=self.send_custom_prepo)
        self.sendCustomMonPrepoButton.grid(row=1, column=7, padx=5)

        self.Frame7 = ctk.CTkFrame(master=self.main_window)
        self.Frame7.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="e")

        self.labelCommand = ctk.CTkLabel(master=self.Frame7, text="Info. du décodeur")
        self.labelCommand.grid(row=0, column=0, columnspan=2, sticky="w", padx=5)

        self.applyDecoderInfoButton = ctk.CTkButton(master=self.Frame7, text="Appliquer", width=1, height=1,
                                                    command=self.apply_new_decoder_info)
        self.applyDecoderInfoButton.grid(row=0, column=2, padx=5, pady=5, columnspan=2, sticky="e")

        self.labelIp = ctk.CTkLabel(master=self.Frame7, text="IP :")
        self.labelIp.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.ipDecoderEntry = ctk.CTkEntry(master=self.Frame7, width=110, height=10)
        self.ipDecoderEntry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.labelPort = ctk.CTkLabel(master=self.Frame7, text="  Port :")
        self.labelPort.grid(row=1, column=2, padx=5, pady=5)

        self.portDecoderEntry = ctk.CTkEntry(master=self.Frame7, width=50, height=10)
        self.portDecoderEntry.grid(row=1, column=3, padx=5, pady=5)

        for i in range(len(sdkSettings[2])):
            self.cameraAddedTreeView.insert("", 'end', values=(liste[i]))

        self.ipDecoderEntry.insert(0, decodeur_ip)
        self.portDecoderEntry.insert(0, decodeur_port)

        self.send_life_command()
        ThUDP = threading.Thread(target=recvd_from_decoder, args=(self,)).start()

        self.main_window.mainloop()

    def print_sdk_log(self, sentence):
        """Affiche les logs dans la partie sdl log"""
        self.sdkTextBox.configure(state=ctk.NORMAL)
        actual_date = datetime.now()
        date_string = actual_date.strftime("%d/%m %H:%M:%S.%f")[:-3]
        self.sdkTextBox.insert('1.0', date_string + "  |  " + sentence + "\n")
        self.sdkTextBox.configure(state=ctk.DISABLED)

    def print_decoder_log(self, sentence):
        """Affiche les logs dans la partie decodeur log"""
        self.decoderTextBox.configure(state=ctk.NORMAL)
        actual_date = datetime.now()
        date_string = actual_date.strftime("%d/%m %H:%M:%S.%f")[:-3]
        self.decoderTextBox.insert('1.0', date_string + "  |  " + sentence + "\n")
        self.decoderTextBox.configure(state=ctk.DISABLED)

    def wype_entry_url(self):
        """vide la barre de saisie de ses élements"""
        self.entryURL.delete(0, ctk.END)

    def is_url_correct(self, url):
        """Vérifie que l'url fournie est correcte (pas de séparateur, d'espace, et de '"' qui peuvent faire dysfonctionner le code"""
        if url.__contains__(SEPARATOR):  # or url.__contains__(" ") == True
            self.print_sdk_log("L'URL contient un caractère incompatible ! Le média n'a pas été envoyé")
            return 1
        elif url != "" and url[0] != '"':
            return 2
        else:
            self.print_sdk_log("URL vide ou incomplète !")
            return 3

    def send_url_to_decoder(self):
        """Prépare la commande et l'envoie à la fonction send_to_decoder"""
        try:
            test_if_int = int(self.entryMon.get())
            if self.is_url_correct(self.entryURL.get()) == 2:
                bytes_to_send = SDK_COMMAND1 + SEPARATOR + self.entryMon.get() + SEPARATOR + self.entryURL.get().format(
                    'user_url')
                send_to_decoder(bytes_to_send, self.serverAddressPort)
                # wypeEntryURL()
                self.print_sdk_log("Média envoyé sur le moniteur " + self.entryMon.get())
        except ValueError:
            self.print_sdk_log("Num. moniteur invalide")

    def add_cam_to_list(self):
        """Récupère l'url dans la barre de saisie et l'ajoute au tableau des caméras ajoutées"""
        if self.is_url_correct(self.entryURL.get()) == 2:
            self.cameraAddedTreeView.insert("", 'end', values=(self.entryURL.get().encode('unicode_escape')))
            # wypeEntryURL()

    def add_cam_to_entry1(self):
        """Ajoute la caméra à la barre de saisie, utilisé par le bouton adéquat"""
        if self.cameraAddedTreeView.focus() != "":
            self.wype_entry_url()
            self.entryURL.insert(0,
                                 (self.cameraAddedTreeView.item(self.cameraAddedTreeView.focus())["values"])[0].replace(
                                     "\\\\", "\\"))

    def add_cam_to_entry2(self, null):
        """Ajoute la caméra à la barre de saisie, utilisé par le double-clic sur un item du tableau des caméras ajoutées"""
        if self.cameraAddedTreeView.focus() != "":
            self.wype_entry_url()
            self.entryURL.insert(0, (self.cameraAddedTreeView.item(self.cameraAddedTreeView.focus())["values"])[0])

    def remove_cam_list(self):
        """Supprime le ou les item(s) sélectionné(s) du tableau des caméras ajoutées"""
        selected_items = self.cameraAddedTreeView.selection()
        for selected_item in selected_items:
            self.cameraAddedTreeView.delete(selected_item)

    def add_cam_to_cyclic(self):
        """Ajoute la caméra sélectionnée du tableau des caméras ajoutées au tableau des caméras cyclique, passant par un pop-up demandant le DWELL"""
        if self.cameraAddedTreeView.focus() != "":
            ask_dwell_pop_up = ctk.CTkInputDialog(text="Renseignez le DWELL pour ce média (en seconde)", title="DWELL")
            dwell_value = ask_dwell_pop_up.get_input()
            try:
                dwell_value = int(dwell_value)
                if dwell_value > 0:
                    self.cameraCyclicTreeView.insert("", 'end', values=(
                    (self.cameraAddedTreeView.item(self.cameraAddedTreeView.focus())["values"])[0].replace("\\\\",
                                                                                                           "\\"),
                    dwell_value))
                else:
                    self.print_sdk_log("Mauvais DWELL renseigné")
            except ValueError:
                self.print_sdk_log("Mauvais DWELL renseigné")

    def remove_cam_cyclic_list(self):
        """Supprime le ou les item(s) sélectionné(s) du tableau des caméras cyclique"""
        selected_items = self.cameraCyclicTreeView.selection()
        for selected_item in selected_items:
            self.cameraCyclicTreeView.delete(selected_item)

    def move_cam_up(self):
        """Monte d'un cran l'item sélectionné dans le tableau des caméras cyclique"""
        selected_items = self.cameraCyclicTreeView.selection()
        if len(selected_items) == 1:
            self.cameraCyclicTreeView.move(selected_items, self.cameraCyclicTreeView.parent(selected_items),
                                           self.cameraCyclicTreeView.index(selected_items) - 1)

    def move_cam_down(self):
        """Descend d'un cran l'item sélectionné dans le tableau des caméras cyclique"""
        selected_items = self.cameraCyclicTreeView.selection()
        if len(selected_items) == 1:
            self.cameraCyclicTreeView.move(selected_items, self.cameraCyclicTreeView.parent(selected_items),
                                           self.cameraCyclicTreeView.index(selected_items) + 1)

    def send_cyclic_to_decoder(self):
        """Prépare la commande et l'envoie à la fonction send_to_decoder"""
        try:
            tesIfInt = int(self.entryMon.get())
            children = self.cameraCyclicTreeView.get_children("")
            cyclic_list = []
            for child in children:
                cyclic_list.append(self.cameraCyclicTreeView.item(child)["values"])
            if len(cyclic_list) == 0:
                self.print_sdk_log("Aucun média pour lancer le cyclique")
            else:
                sentence = ""
                for x in range(len(cyclic_list)):
                    sentence = sentence + (SEPARATOR + cyclic_list[x][0] + SEPARATOR + str(cyclic_list[x][1]))
                bytes_to_send = SDK_COMMAND2 + SEPARATOR + self.entryMon.get() + sentence
                send_to_decoder(bytes_to_send.replace("\\\\", "\\"), self.serverAddressPort)
                self.print_sdk_log("Cyclique envoyé sur le moniteur " + self.entryMon.get())
        except ValueError:
            self.print_sdk_log("Num. moniteur invalide")

    def send_life_command(self):
        """Prépare la commande et l'envoie à la fonction send_to_decoder"""
        bytes_to_send = SDK_COMMAND3
        send_to_decoder(bytes_to_send, self.serverAddressPort)
        self.print_sdk_log("Envoi d'un signal de vie")

    def send_set_black(self):
        """Prépare la commande et l'envoie à la fonction send_to_decoder"""
        bytes_to_send = SDK_COMMAND4 + SEPARATOR + self.entryMon.get()
        send_to_decoder(bytes_to_send, self.serverAddressPort)
        self.print_sdk_log("Envoi de la mise au noir")

    def send_set_single(self):
        """Prépare la commande et l'envoie à la fonction send_to_decoder"""
        bytes_to_send = SDK_COMMAND5 + SEPARATOR + "1"
        send_to_decoder(bytes_to_send, self.serverAddressPort)
        self.print_sdk_log("Envoi du passage en single")

    def send_set_quad(self):
        """Prépare la commande et l'envoie à la fonction send_to_decoder"""
        bytes_to_send = SDK_COMMAND5 + SEPARATOR + "4"
        send_to_decoder(bytes_to_send, self.serverAddressPort)
        self.print_sdk_log("Envoi du passage en quad")

    def send_set_nano(self):
        """Prépare la commande et l'envoie à la fonction send_to_decoder"""
        bytes_to_send = SDK_COMMAND5 + SEPARATOR + "9"
        send_to_decoder(bytes_to_send, self.serverAddressPort)
        self.print_sdk_log("Envoi du passage en nano")

    def send_set_sixteen(self):
        """Prépare la commande et l'envoie à la fonction send_to_decoder"""
        bytes_to_send = SDK_COMMAND5 + SEPARATOR + "16"
        send_to_decoder(bytes_to_send, self.serverAddressPort)
        self.print_sdk_log("Envoi du passage en 4x4")

    def send_custom_prepo(self):
        """Prépare la commande et l'envoie à la fonction send_to_decoder"""
        if int(self.entryCustomMon.get()) == 1:
            self.send_set_single()
        elif int(self.entryCustomMon.get()) == 4:
            self.send_set_quad()
        elif int(self.entryCustomMon.get()) == 9:
            self.send_set_nano()
        elif int(self.entryCustomMon.get()) == 16:
            self.send_set_sixteen()
        else:
            bytes_to_send = SDK_COMMAND5 + SEPARATOR + self.entryCustomMon.get()
            send_to_decoder(bytes_to_send, self.serverAddressPort)
            self.print_sdk_log("Envoi du passage prépo custom")

    def clear_sdk(self):
        """Vide les logs sdk"""
        self.sdkTextBox.configure(state=ctk.NORMAL)
        self.sdkTextBox.delete('1.0', ctk.END)
        self.sdkTextBox.configure(state=ctk.DISABLED)

    def clear_decoder(self):
        """Vide les logs encodeur"""
        self.decoderTextBox.configure(state=ctk.NORMAL)
        self.decoderTextBox.delete('1.0', ctk.END)
        self.decoderTextBox.configure(state=ctk.DISABLED)

    def apply_new_decoder_info(self):
        """Récupère nes nouveaux paramètres et les enregistre dans le fichier sdkConf.ini"""
        try:
            new_ip = self.ipDecoderEntry.get()
            new_port = int(self.portDecoderEntry.get())
            self.serverAddressPort = (new_ip, new_port)
            config_ini = configparser.ConfigParser()
            config_ini.optionxform = str
            config_ini.read("C:\Decodeur\sdkConf.ini")
            config_ini.set("SDK", "IPdecodeur", new_ip)
            config_ini.set("SDK", "PORTdecodeur", str(new_port))
            config_ini.write(open("C:\Decodeur\sdkConf.ini", "w"))
            self.print_sdk_log("IP et port mis à jour")
        except ValueError:
            self.print_sdk_log("L'IP et port n'ont pas pu être mis à jour, vérifier la syntaxe")

    def mon_spin_box_plus(self):
        """+1 au numéro moniteur dans la section du moniteur choisi"""
        string_int = int(self.entryMon.get())
        if string_int != 99:
            self.entryMon.configure(state=ctk.NORMAL)
            self.entryMon.delete(0, ctk.END)
            self.entryMon.insert(0, string_int + 1)
            self.entryMon.configure(state=ctk.DISABLED)

    def mon_spin_box_minus(self):
        """-1 au numéro moniteur dans la section du moniteur choisi"""
        string_int = int(self.entryMon.get())
        if string_int != 1:
            self.entryMon.configure(state=ctk.NORMAL)
            self.entryMon.delete(0, ctk.END)
            self.entryMon.insert(0, string_int - 1)
            self.entryMon.configure(state=ctk.DISABLED)

    def custom_mon_spin_box_plus(self):
        """+1 à la préposition dans la section custom. prépo"""
        string_int = int(self.entryCustomMon.get())
        if string_int != 99:
            self.entryCustomMon.configure(state=ctk.NORMAL)
            self.entryCustomMon.delete(0, ctk.END)
            self.entryCustomMon.insert(0, string_int + 1)
            self.entryCustomMon.configure(state=ctk.DISABLED)

    def custom_mon_spin_box_minus(self):
        """-1 à la préposition dans la section custom. prépo"""
        string_int = int(self.entryCustomMon.get())
        if string_int != 1:
            self.entryCustomMon.configure(state=ctk.NORMAL)
            self.entryCustomMon.delete(0, ctk.END)
            self.entryCustomMon.insert(0, string_int - 1)
            self.entryCustomMon.configure(state=ctk.DISABLED)

    def _quit(self):
        """Appelé lorsqu'on ferme la fenêtre. Récupère les infos et les enregistres dans sdkConf.ini, ferme le socket et l'IHM"""
        try:
            new_ip = self.ipDecoderEntry.get()
            new_port = self.portDecoderEntry.get()
            children = self.cameraAddedTreeView.get_children()
            cam_list = ""
            for child in children:
                temp = str(self.cameraAddedTreeView.item(child)["values"])
                cam_list = cam_list + temp

            config_ini = configparser.ConfigParser()
            config_ini.optionxform = str
            config_ini.read("C:\Decodeur\sdkConf.ini")
            config_ini.set("SDK", "IPdecodeur", new_ip)
            config_ini.set("SDK", "PORTdecodeur", new_port)
            if cam_list != "":
                config_ini.set("CAMERA_LIST", "LISTE", cam_list)
            config_ini.write(open("C:\Decodeur\sdkConf.ini", "w"))
        except:
            pass
        UDPClientSocket.close()
        self.main_window.quit()
        os._exit(1)


def send_to_decoder(request, decodeur_info):
    """Envoie la commande reçu à l'IP & port fourni"""
    UDPClientSocket.sendto(str.encode(request), decodeur_info)


def recvd_from_decoder(ctk_window):
    """Ecoute les retours du décodeur et les affiches avec la fonciton print_decoder_log. Lancé par un thread"""
    while True:
        try:
            received_frame = UDPClientSocket.recvfrom(BUFFER_SIZE)
            message = received_frame[0]
            sentence = message.decode("utf-8")
            SetMonitorArrangement.print_decoder_log(ctk_window, sentence)
        except ConnectionResetError:
            SetMonitorArrangement.print_sdk_log(ctk_window, "Erreur durant l'envoi de la commande")


def is_conf_file_exist():
    """Vérifie si le dossier Décodeur existe et/ou le créer, vérifie si le sdkConf.ini existe et/ou le créer"""
    if not os.path.isdir("C:/Decodeur"):
        os.mkdir("C:/Decodeur")
    if not os.path.isfile("C:/Decodeur/sdkConf.ini"):
        config_ini = configparser.ConfigParser()
        config_ini.optionxform = str
        config_ini["SDK"] = {"IPdecodeur": "192.168.1.100", "PORTdecodeur": "50050"}
        config_ini["CAMERA_LIST"] = {
            "LISTE": "['C:\\\\Decodeur\\\\Media\\\\default.png']['C:\\\\Decodeur\\\\Media\\\\test.png']['C:\\\\Decodeur\\\\Media\\\\video1.mp4']['C:\\\\Decodeur\\\\Media\\\\video2.mp4']['C:\\\\Decodeur\\\\Media\\\\video3.mp4']['C:\\\\Decodeur\\\\Media\\\\video4.mp4']['C:\\\\Decodeur\\\\Media\\\\video5.mp4']['C:\\\\Decodeur\\\\Media\\\\video6.mp4']['C:\\\\Decodeur\\\\Media\\\\video7.mp4']"}
        config_ini.write(open("C:\Decodeur\sdkConf.ini", "w"))


def read_conf_file():
    """Lit sdkConf.ini et retourne les informations"""
    config_ini = configparser.ConfigParser()
    config_ini.optionxform = str
    config_ini.read("C:\Decodeur\sdkConf.ini")
    if config_ini['CAMERA_LIST']['LISTE'] != "":
        bad_sentence1 = config_ini['CAMERA_LIST']['LISTE'].replace("'", "")
        bad_sentence2 = bad_sentence1.replace("[", "")
        bad_sentence3 = bad_sentence2.replace("]", ";")
        if bad_sentence3[-1] == ";":
            bad_sentence3 = bad_sentence3[:-1]
        liste = bad_sentence3.split(";")
    return config_ini["SDK"]["IPdecodeur"], config_ini["SDK"]["PORTdecodeur"], liste


if __name__ == "__main__":
    """Lancement du programme"""
    is_conf_is_readable = True
    error = ""

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    main_window = ctk.CTk()

    is_conf_file_exist()
    sdkSettings = read_conf_file()

    ip_address = sdkSettings[0]

    if is_conf_is_readable:  # Vérif si IP correcte
        try:
            test_ip_address = ipaddress.ip_address(ip_address)
        except ValueError:
            is_conf_is_readable = False
            error = "L'adresse IP du décodeur est invalide\nVérifier dans C:\Decodeur\sdkConf.ini"

    if is_conf_is_readable:  # Vérif si port correcte
        try:
            port = int(sdkSettings[1])
            if port < 1 or port > 65535:
                is_conf_is_readable = False
                error = "Le port est invalide\nVérifier dans C:\Decodeur\sdkConf.ini"
        except ValueError:
            is_conf_is_readable = False
            error = "Le port est invalide\nVérifier dans C:\Decodeur\sdkConf.ini"

    if is_conf_is_readable:  # Si le .ini est OK, lance l'appli
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        decodeur_ip = sdkSettings[0]
        decodeur_port = int(sdkSettings[1])
        media_liste = sdkSettings[2]

        CtkWindow = SetMonitorArrangement(main_window, decodeur_ip, decodeur_port, media_liste)

    elif error != "":  # Si erreur présente, l'affiche sous forme de message box
        main_window.title("Erreur")
        main_window.resizable(False, False)
        frame1 = ctk.CTkFrame(main_window)
        frame1.pack(expand=True, fill=ctk.BOTH)
        label1 = ctk.CTkLabel(frame1, text="Erreur durant l'ouverture du décodeur :", font=("Arial", 20),
                              text_color="orange red").pack(padx=20, pady=00)
        label2 = ctk.CTkLabel(frame1, text=error, font=("Arial", 15)).pack(padx=20, pady=25)
        button1 = ctk.CTkButton(frame1, text="OK", command=main_window.destroy).pack(padx=20, pady=20)
        main_window.mainloop()
