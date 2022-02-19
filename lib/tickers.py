import pandas as pd
import requests

class Tickers:
    def __init__(self) -> None:
        pass
    def get_tickers(self):
        url = "https://drive.google.com/uc?export=download&id=1-D8LmKFINHOKzYxr9JgANm2Ffpw72S_L"        
        data = pd.read_csv(url)
        return data