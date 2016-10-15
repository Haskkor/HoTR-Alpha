import os
import pickle

__author__ = "Jérémy Farnault"


class Save:
    """
    CLASSE POUR LA SAUVEGARDE
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

    def save_all(self, dict_to_save):
        """
        Sauvegarde un dictionnaire entier dans un fichier
        """
        with open(self.file_name, 'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(dict_to_save)
            file.close()

    def save_new_object(self, object_name, object_to_save):
        """
        Sauvegarde un nouvel élément dans un fichier
        """
        saves = {}
        if os.path.isfile(self.file_name):
            with open(self.file_name, 'rb') as file:
                depickler = pickle.Unpickler(file)
                saves = depickler.load()
                file.close()
        saves[object_name] = object_to_save
        with open(self.file_name, 'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(saves)
            file.close()

    def delete_elem(self, object_name):
        """
        Supprime un élément sauvegardé dans un fichier
        """
        with open(self.file_name, 'rb') as file:
            depickler = pickle.Unpickler(file)
            saves = depickler.load()
            file.close()
        del saves[object_name]
        with open(self.file_name, 'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(saves)
            file.close()
