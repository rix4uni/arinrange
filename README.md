## arinrange

Net Range scraping on whois.arin.net.

## Installation
```
git clone https://github.com/rix4uni/arinrange.git
cd arinrange
python3 setup.py install
```

## pipx
Quick setup in isolated python environment using [pipx](https://pypa.github.io/pipx/)
```
pipx install --force git+https://github.com/rix4uni/arinrange.git
```

## Usage
```
python3 arinrange -h
usage: arinrange [-h] [--timeout TIMEOUT] [--silent] [--version]

Net Range scraping on whois.arin.net

options:
  -h, --help         show this help message and exit
  --timeout TIMEOUT  Timeout (in seconds) for http client (default 15)
  --silent           Run without printing the banner
  --version          Show current version of arinrange
```

## Example usages

Single ORGs:
```
echo "Twitch Interactive" | arinrange
```

Multiple ORGs:
```
cat orgs.txt
Twitch Interactive
Tesla Motors, Inc.
```

```
cat orgs.txt | arinrange
```

Output of Single ORGs:
```
echo "Twitch Interactive" | arinrange --silent
65.116.147.160-65.116.147.167
2001:428:2001:310::-2001:428:2001:310:FFFF:FFFF:FFFF:FFFF
2001:428:6002:600::-2001:428:6002:6FF:FFFF:FFFF:FFFF:FFFF
```

Intigrate with mapcidr:
```
echo "Twitch Interactive" | arinrange --silent | mapcidr -silent -aggregate
65.116.147.160/29
2001:428:2001:310::/64
2001:428:6002:600::/56
```