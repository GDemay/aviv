from pydantic import BaseSettings


class Settings(BaseSettings):
    """_summary_ : This is the settings class for the application.
    Args:
        BaseSettings (_type_): _description_ - The base settings class.
    """

    # Create a data structure of GEOMS_ID and Paris Suburbs
    GEOMS_ID_PLUS_TARD = {
        "Paris 1": 32682,
        "Paris 2": 32683,
        "Paris 3": 32684,
        "Paris 4": 32685,
        "Paris 5": 32686,
        "Paris 6": 32687,
        "Paris 7": 32688,
        "Paris 8": 32689,
        "Paris 9": 32690,
        "Paris 10": 32691,
        "Paris 11": 32692,
        "Paris 12": 32693,
        "Paris 13": 32694,
        "Paris 14": 32695,
        "Paris 15": 32696,
        "Paris 16": 32697,
        "Paris 17": 32698,
        "Paris 18": 32699,
        "Paris 19": 32700,
        "Paris 20": 32701,
    }

    GEOMS_IDS = [
        32684,
        32683,
        32682,
        32685,
        32686,
        32687,
        32688,
        32689,
        32690,
        32691,
        32692,
        32693,
        32699,
        32694,
        32695,
        32696,
        32697,
        32698,
        32700,
        32701,
    ]


# Load the environment variables from the .env file

settings = Settings()
