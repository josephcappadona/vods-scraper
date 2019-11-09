# scraping

## Setup

```
sudo pip install pytube BeautifulSoup4 pprint
sudo apt-get install ffmpeg
```

## Examples

### Simple
```sh
python get_vods.py -p "Leffen"
python download.py -p "Leffen"

python get_vods.py -c "Falco"
python download.py -c "Falco"

python get_vods.py -t "GENESIS 5"
python download.py -t "GENESIS 5"
```

### Complex
```sh
python get_vods.py -p "Armada" -c "Fox"
python download.py -p "Armada" -c "Fox"

python get_vods.py -p "Mango" -t "WTFox"
python download.py -p "Mango" -t "WTFox"
```

### Limiting Number of Downloads
```sh
python get_vods.py -p "Armada" -l 25
python get_vods.py -p "Armada" -l 25
```
