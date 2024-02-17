import pygame
import ctypes
import platform
import logging
from . import widgets, colors

def init():
    if colors.scheme == "pitchblack":
        logging.critical("No theme is set, set a theme by using wyper.colors.setScheme* methods")
    if platform.system() == "Windows":
        ctypes.windll.user32.SetProcessDPIAware()
        widgets.BuildContext().scale = ctypes.windll.shcore.GetScaleFactorForDevice(0)/100
    pygame.init()

scale = widgets._scale

__all__ = ["layouthandler", "widgets", "colors"]