# PAR-Workschedule

Detta program konverterar en av PARPAS genererad PDF till iCalendar-fil (ICS). En ICS-fil kan importeras i de flesta sorters kalenderprogram, exempelvis Google Calendar för att lättare hålla koll på ditt schema då krångel med PARPAS uppstår.

## Setup

#### Clone repo:
```
git clone git@github.com:JonatanLindstroom/PAR-Workschedule.git
cd PAR-Workschedule
```

#### Get pip:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

#### Get packages:
```
pip install chardet
pip install pdfminer.six
pip install icalendar
```

## Disclaimer

Notera att detta inte är något officiellt och iom det finns ingen säkerhet på att programmet fungerar felfritt. Då jag endast haft mitt egna schema att testa programmet med kan oväntade problem uppstå för scheman med andra sorters pass eller från andra parker. Var därför noga med att dubbelkolla att ICS-filen stämmer överens med PDFen. Vid uppdateringar i PARPAS måste din kalender uppdateras manuellt.
