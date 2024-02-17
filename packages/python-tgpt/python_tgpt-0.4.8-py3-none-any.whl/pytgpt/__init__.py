from .utils import appdir
import g4f

__version__ = "0.4.8"
__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/python-tgpt"

tgpt_providers = [
    "leo",
    "openai",
    "opengpt",
    "koboldai",
    "bard",
    "phind",
    "llama2",
    "blackboxai",
    "gpt4all",
    "webchatgpt",
    "g4fauto",
]

gpt4free_providers = [
    provider.__name__ for provider in g4f.Provider.__providers__  # if provider.working
]

available_providers = tgpt_providers + gpt4free_providers

__all__ = [
    "appdir",
    "imager",
] + available_providers
