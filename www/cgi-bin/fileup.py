import cgi
cgi.maxlen = 5*10**6

def save(form, field, fname):
    if not form.has_key(field): return False
    fileitem = form[field]
    if not fileitem.file: return False
    if not fileitem.filename: return False

    fout = file(fname, 'wb')
    while 1:
        chunk = fileitem.file.read(100000)
        if not chunk: break
        fout.write (chunk)
    fout.close()

    return True
