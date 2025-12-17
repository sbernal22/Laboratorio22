import requests
url=("https://pokeapi.co/api/v2/pokemon")
params={
    "limit": 10,
}
r=requests.get(url,params=params)
data=r.json()
for pokemon in data["results"]:
    print(pokemon["name"])
