# scraping

## Setup

```
sudo pip install pytube BeautifulSoup4 pprint requests
sudo apt-get install ffmpeg
```

## Examples

### Simple
```
python get_urls.py -p "Leffen"
python download.py -p "Leffen"

python get_urls.py -c "Falco"
python download.py -c "Falco"

python get_urls.py -t "GENESIS 5"
python download.py -t "GENESIS 5"
```

### Complex
```
python get_urls.py -p "Armada" -c "Fox"
python download.py -p "Armada" -c "Fox"

python get_urls.py -p "Mango" -t "WTFox"
python download.py -p "Mango" -t "WTFox"
```


