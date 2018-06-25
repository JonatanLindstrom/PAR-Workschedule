import os
import PDFminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, resolve1
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
# Import iCalendar modules
from icalendar import Calendar, Event
from datetime import datetime

class Workshift:
    def __init__(self, date, starttime, endtime, info):
        self.date = date
        self.starttime = starttime
        self.endtime = endtime
        self.info = info

    def __str__(self):
        return (self.date + ' ' + self.info + ' ' + self.starttime + ' - ' + self.endtime)

    def __lt__(self, other):
        if self.date < other.date:
            return True
        elif self.date == other.date and self.starttime < other.starttime:
            return True
        return False


def readSchedule(path):
    pdfFile = open(path, mode='rb')
    parser = PDFParser(pdfFile)

    password = ''
    extracted_text = ''

    # Store the parsed content in PDFDocument object
    document = PDFDocument(parser, password)
    pages = (resolve1(document.catalog['Pages'])['Count'])

    # Check if document is extractable, if not abort
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create PDFResourceManager object that stores shared resources such as fonts or images
    rsrcmgr = PDFResourceManager()

    # set parameters for analysis
    laparams = LAParams()

    # Create a PDFDevice object which translates interpreted information into desired format
    # Device needs to be connected to resource manager to store shared resources
    # device = PDFDevice(rsrcmgr)
    # Extract the decive to page aggregator to get LT object elements
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create interpreter object to process page content from PDFDocument
    # Interpreter needs to be connected to resource manager for shared resources and device 
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Ok now that we have everything to process a pdf document, lets process it page by page
    for page in PDFPage.create_pages(document):
        # As the interpreter processes the page stored in PDFDocument object
        interpreter.process_page(page)
        # The device renders the layout from interpreter
        layout = device.get_result()
        # Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()
                
    #close the pdf file
    pdfFile.close()

    #remove unneccessary text
    text = extracted_text.replace('\n', '')
    for i in range(pages + 1):
        text = text.replace(str(i) + '/' + str(pages), '')
    text = text.replace('dag', 'dag\n')
    text = text.replace('Arbetspass', 'Arbetspass\n')
    text = text.replace('Utbildning', 'Utbildning\n')
    text = text.replace('StartSlutStation och position', '\n')
    text = text.split('\n')

    workschedule = []
    workset = set([])

    previous_row = ''
    for row in text:
        if row == '' or row[0].isalpha() or row[0] == ' ' or row[0] == '&':
            continue
        elif 17 < len(row) and row.endswith('dag'):
            row = row[2:len(row)]

        if row.endswith('Arbetspass') or row.endswith('Utbildning'):
            date = previous_row[0:10]
            start = row[0:5]
            end = row[5:10]
            info = row[10:len(row)]
            if (date + start + end + info) not in workset:
                workset.add(date + start + end + info)
                workschedule.append(Workshift(date, start, end, info))

        previous_row = row
    
    workschedule.sort()
    return workschedule


def readCal(path):
    cal = open(path, 'r')
    stringCal = cal.read()
    stringCal = stringCal.strip('\n')
    stringCal = stringCal.replace('\nEND:VCALENDAR', 'END:VCALENDAR')
    stringCal = stringCal.replace('BEGIN:VCALENDAR', '')
    stringCal = stringCal.replace('\nBEGIN:VEVENT', 'BEGIN:VEVENT')
    stringCal = stringCal.split('END:VEVENT')

    for event in stringCal:
        event.split('SUMMARY:')
        print(event)
        #for row in event:
        #    print(row)
            #if event[0] != 'END:VCALENDAR':
            #    print(row)
            #    print('\n')
            # print(event[1].replace('SUMMARY:', ''))
            # print('År: ' + event[2][24:28])
            # print('Månad: ' + event[2][29:30])
            # print('Dag: ' + event[2][31:32])
            # print('Start: ' + event[2][34:35] + ":" event[2][36:37])
            # print('Slut: ' + event[3][32:33] + ":" event[3][34:35])

    return


def createCal():
    path = input('Skriv filvägen för ditt schema (ex. C:\\\\User\\\\Downloads\\\\Schema.pdf): \n')

    print('Läser in schema...')
    schema = readSchedule(path)
    print('Inläsning lyckad!\n')

    print('Skapar iCalendar-fil...')
    writeCal(schema)
    print('Fil skapad!')

    return


def writeCal(workschedule, path=None):
    cal = Calendar()

    for workshift in workschedule:
        event = Event()

        date = workshift.date.split('-')
        stime = workshift.starttime.split(':')
        etime = workshift.endtime.split(':')

        dtstart = datetime(int(date[0]), int(date[1]), int(date[2]), int(stime[0]), int(stime[1], 0))
        dtend = datetime(int(date[0]), int(date[1]), int(date[2]), int(etime[0]), int(etime[1], 0))

        event.add('summary', workshift.info)
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)
        cal.add_component(event)

    f = open('arbetsschema.isc', 'wb')
    f.write(cal.to_ical())
    f.close()

    return cal


def compareCal():
    pathSchedule = 'D:\\Jonatan\\Downloads\\Arbetsschema - Jonatan Lindstrom.pdf'
    #input('Skriv filvägen för ditt schema (ex. C:\\\\User\\\\Downloads\\\\Schema.pdf): \n')
    pathCal = 'D:\\Jonatan\\Documents\\Programmering\\arbetsschema.isc'
    #input('Skriv filvägen för kalendern (ex. C:\\\\User\\\\Downloads\\\\Kalender.isc): \n')

    print('Läser in schema...')
    schema = readSchedule(pathSchedule)
    print('Inläsning lyckad!\n')

    print('Läser in kalender...')
    readCal(pathCal)


def main():
    while True:
        print('Vad vill du göra?\n1. Skapa kalender\n2. Kolla uppdatering\n3. Avsluta\n')
        ans = input('')
        if ans == '1':
            createCal()
        elif ans == '2':
            compareCal()
        elif ans == '3':
            exit()
        else:
            print('Invalid input\n')


path = 'D:\\Jonatan\\Downloads\\Arbetsschema - Jonatan Lindstrom.pdf'
path = 'D:\Jonatan\Downloads\Programmering\arbetsschema.isc'

intro = '''OBS: Detta program är skrivet privat och används på eget bevåg!\n
Jag som skapare garanterar inte att det fungerar felfritt, utan dubbelkolla alltid resultatet.
Utöver Detta bör du komma ihåg att schemat ej uppdateras automatiskt, utan programmet måste köras för varje ny schemaändring.\n''' 

if __name__ == '__main__':
    main()