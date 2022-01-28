import requests

def get_chart(symbol:str):
    url = "https://yh-finance.p.rapidapi.com/stock/v3/get-chart"

    querystring = {"interval":"15m","symbol":"vix","range":"1d","region":"US","includePrePost":"false","useYfid":"true","includeAdjustedClose":"true","events":"capitalGain,div,split"}

    headers = {
        'x-rapidapi-host': "yh-finance.p.rapidapi.com",
        'x-rapidapi-key': "6a9151b6f2msh5a6da61bb5ea0ddp1ffbe5jsn120757001ee9"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text