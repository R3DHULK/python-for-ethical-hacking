import pikepdf
import datetime
import re
from dateutil.tz import tzutc, tzoffset
import sys
import os


pdf_date_pattern = re.compile(''.join([
    r"(D:)?",
    r"(?P<year>\d\d\d\d)",
    r"(?P<month>\d\d)",
    r"(?P<day>\d\d)",
    r"(?P<hour>\d\d)",
    r"(?P<minute>\d\d)",
    r"(?P<second>\d\d)",
    r"(?P<tz_offset>[+-zZ])?",
    r"(?P<tz_hour>\d\d)?",
    r"'?(?P<tz_minute>\d\d)?'?"]))


def transform_date(date_str):
    """
    Convert a pdf date such as "D:20120321183444+07'00'" into a usable datetime
    http://www.verypdf.com/pdfinfoeditor/pdf-date-format.htm
    (D:YYYYMMDDHHmmSSOHH'mm')
    :param date_str: pdf date string
    :return: datetime object
    """
    global pdf_date_pattern
    match = re.match(pdf_date_pattern, date_str)
    if match:
        date_info = match.groupdict()

        for k, v in date_info.items():  # transform values
            if v is None:
                pass
            elif k == 'tz_offset':
                date_info[k] = v.lower()  # so we can treat Z as z
            else:
                date_info[k] = int(v)

        if date_info['tz_offset'] in ('z', None):  # UTC
            date_info['tzinfo'] = tzutc()
        else:
            multiplier = 1 if date_info['tz_offset'] == '+' else -1
            date_info['tzinfo'] = tzoffset(None, multiplier*(3600 * date_info['tz_hour'] + 60 * date_info['tz_minute']))

        for k in ('tz_offset', 'tz_hour', 'tz_minute'):  # no longer needed
            del date_info[k]

        return datetime.datetime(**date_info)



# get the target pdf file from the command-line arguments
# read the pdf file
os.system("clear")
print(''' 
  ___ ___  ___   _____  _____ ___   _____ ___   ___  _    
 | _ \   \| __| | __\ \/ /_ _| __| |_   _/ _ \ / _ \| |  v. 2. O 
 |  _/ |) | _|  | _| >  < | || _|    | || (_) | (_) | |__ 
 |_| |___/|_|   |___/_/\_\___|_|     |_| \___/ \___/|____|
          c 0 d e   f       0         
                        r        m    R3DHULK  
                           
          https://github.com/R3DHULK                 
''') 
                        
print("")
try:
	pdf = pikepdf.Pdf.open(input(" [*] Enter PDF Name : "))
	print("")
	docinfo = pdf.docinfo
	for key, value in docinfo.items():
		if str(value).startswith("D:"):
			# pdf datetime format, convert to python datetime
			value = transform_date(str(pdf.docinfo["/CreationDate"]))
		print( key, ":", value)
except KeyboardInterrupt:
	print("\n [-] Ctrl+C Detected......Exiting\n")
print("")
input("Enter To Close Window")
