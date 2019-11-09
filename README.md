# scraping

## Setup

```
python -m pip install pytube BeautifulSoup4 pprint requests

# on Debian
sudo apt-get install ffmpeg
# or on Mac OS
brew install ffmpeg
```

## Examples

### Simple
```sh
python get_urls.py -p "Leffen"
python download.py -p "Leffen"

python get_urls.py -c "Falco"
python download.py -c "Falco"

python get_urls.py -t "GENESIS 5"
python download.py -t "GENESIS 5"
```

### Complex
```sh
python get_urls.py -p "Armada" -c "Fox"
python download.py -p "Armada" -c "Fox"

python get_urls.py -p "Mango" -t "WTFox"
python download.py -p "Mango" -t "WTFox"
```

### Limiting Number of Downloads
```sh
python get_vods.py -p "Armada" -l 25
python get_vods.py -p "Armada" -l 25
```
