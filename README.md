# BF Instagram Bot

With this bot you can screpa follower / following user list of a specified target account, and get an excel spdreadsheet including account name, link, number of followers and profile pic.

### Foder structure
This is the basic folder structure
```sh
get_followings.py
generate_excel.py
export/
    requests/
    csvs/
    xlsx/
    images/
```

### Logearte con instaloader
Logearte con una cuenta de IG. No usar una cuenta importante, es probable que acabe bloqueada. Debes instalar librería instaloader, y ejecutar el comando para estar logeado
```sh
instaloader --login
```

### Scrape instagram target account
Correr script para sacar csv con una lista de cuentas followings y followers. Especificar los 3 parámetros: tu cuenta, la cuenta a screapear, y qué lista atacar (followers, following, o ambas)
```sh
get_followings.py  [yourAccount] [targetAccount] [followers|following|both]
```

For example:
```sh
python3 ./get_followings.py anapurna2049 crialme both
```

### Screape pictures and other data
Correr script para scrappear fotos, num de followers y generar excel. Especificar parámetro el nombre del archivo csv obtenido en el paso anterior.
```sh
python3 ./generate_excel.py nameCsvFile
```

For example:
```sh
python3 ./generate_excel.py crialme_26_following_f09ada98-6fe3-11ed-8062-600308a0c376
```