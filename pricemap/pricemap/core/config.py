""" This is the config for the app """

from pydantic import BaseSettings


class Settings(BaseSettings):
    """_summary_ : This is the settings class for the application.
    Args:
        BaseSettings (_type_): _description_ - The base settings class.
    """

    DISTRICT_GEOMS = {
        "75101": 32682,
        "75102": 32683,
        "75103": 32684,
        "75104": 32685,
        "75105": 32686,
        "75106": 32687,
        "75107": 32688,
        "75108": 32689,
        "75109": 32690,
        "75110": 32691,
        "75111": 32692,
        "75112": 32693,
        "75113": 32694,
        "75114": 32695,
        "75115": 32696,
        "75116": 32697,
        "75117": 32698,
        "75118": 32699,
        "75119": 32700,
        "75120": 32701,
    }


settings = Settings()
