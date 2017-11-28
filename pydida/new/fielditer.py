class LineIter :
    def __init__(self, filename):
        self.f = file(filename)

    def close(self):
        self.f.close()

    def next(self):
        return FieldIter(self.f)

class FieldIter:
    buflen = 1024

    def __init__(self, f):
        self.f = f
        self.i = -1
        self.table_len = -1

    def __iter__(self):
        return self;

    def get_new_table(self):
        buffer = f.readline(buflen)
        if buffer[-1] != "\n":
            c=""
            cs=[]
            while c != sep and c!="\n":
                cs.append(c)
            cs.append(c)
            buffer = buffer + "".join(cs)
            
        self.is_last_table = buffer[-1] == "\n"
        self.table         = sep.split(buffer[:-1])
        self.table_len     = len(self.table)
        self.i             = 0


    def next():
        if(self.i == self.table_len):
            if self.is_last_table:
                raise StopIteration
            else:
                self.get_new_table()

        self.i += 1
        return self.table[self.i - 1]

                
