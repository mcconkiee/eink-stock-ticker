import pandas as pd


class Tickers:
    def __init__(self) -> None:
        pass
    def get_tickers(self):
        # url = "https://drive.google.com/uc?export=download&id=1-D8LmKFINHOKzYxr9JgANm2Ffpw72S_L"
        url='https://drive.google.com/file/d/1LRdeRaR2hsgjKE7z1bc7FgXeN-Z_ZT9l/view?usp=share_link'
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]
        data = pd.read_csv(url)
        return data