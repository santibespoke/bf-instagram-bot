# bf-instagram-bot

With this bot you can screpe follower / following user list of a specified target account, and get an excel spdreadsheet including account name, link, number of followers and profile pic.

##Foder structure
This is the basic folder structure
```sh
- get_followings.py
- export/
    - generate_excel.py
    - requests/
    - csvs/
    - xlsx/
    - images/
```

##Logearte con instaloader
Logearte con una cuenta de IG
```sh
instaloader --login
```

##Scrape instagram target account
Correr script para sacar csv con una lista de cuentas followings y followers
```sh
get_followings.py  [yourAccount] [targetAccount] [followers|following|both]
python3 ./get_followings.py anapurna2049 crialme both
```

##Screape pictures and other data
Correr script para scrappear fotos, num de followers y generar excel
```shpython3 ./generate_excel.py nameCsvFile
```