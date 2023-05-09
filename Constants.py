IMAGES = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO = ('AVI', 'MP4', 'MOV', 'MKV')
DOCS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
MUSIC = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVES = ('ZIP', 'GZ', 'TAR')
OTHER = ''' !@#$%&?()*+'''
CIRILIC_SYMV = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєії"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji"
               )
TRANS = {}


for k, l in zip(CIRILIC_SYMV, TRANSLATION):
    TRANS[ord(k)] = l
    TRANS[ord(k.upper())] = l.upper()


