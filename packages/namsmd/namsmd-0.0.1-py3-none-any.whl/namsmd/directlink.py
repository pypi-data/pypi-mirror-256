from os import system as syst
from urllib.parse import urlparse as urlp
def directdown_linux(link, name, no_check_certificate):
  if name == '':
    path = urlp(link).path.split('/')
    name = path[len(path)-1]
    name = name.replace("%20","_")
    name = name.replace("%28","(")
    name = name.replace("%29",")")
  if no_check_certificate:
    syst(f'wget -O {name} {link} --no-check-certificate')
  else:
    syst(f'wget -O {name} {link}')