# Otaku-Streamer-Downloader

## steeps:

```$ pip install pipenv```

```[in cloned] $ pipenv install```

```
create .env file
username=<otaku-streamer username>
password=<otaku-streamer password>
```
> example:

  .env
  
  username=user1
  
  password=password1

## run without switching to virtual env
```
[in clone] $ pipenv run python downloader.py
$ <enter url of anime>
example:
$ https://beta.otaku-streamers.com/title/4481/Gate:_Jieitai_Kanochi_nite,_Kaku_Tatakaeri
```

*note: paste the main page link, not the singular episode such as*

*https://beta.otaku-streamers.com/watch/4481/episode1-Gate:_Jieitai_Kanochi_nite,_Kaku_Tatakaeri*

## run with switching to the virutal env
```
[in clone] $ pipenv shell
$ <enter url of anime>
example:
$ https://beta.otaku-streamers.com/title/4481/Gate:_Jieitai_Kanochi_nite,_Kaku_Tatakaeri
```

*note: to get out of virtual env,*

*$ deactivate*
