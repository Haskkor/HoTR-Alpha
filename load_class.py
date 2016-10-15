import os
import pickle

__author__ = "Jérémy Farnault"


class Load:
    """
    CLASSE POUR LE CHARGEMENT DE DONNEES
    """

    def __init__(self, file_name, **kwargs):
        self.file_name = file_name
        self.process_kwargs(kwargs)

    def process_kwargs(self, kwargs):
        defaults = {}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
        self.__dict__.update(defaults)

    @property
    def load(self):
        """
        Charge un ficher demandé et renvoie le dictionnaire qu'il contenait
        """
        loads = {}
        if os.path.isfile(self.file_name):
            with open(self.file_name, 'rb') as file:
                depickler = pickle.Unpickler(file)
                loads = depickler.load()
                file.close()
        return loads