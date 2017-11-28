import sys, os, sha, glob, pickle
import pydida.vars, pydida.varcmd

datadir = "/home/tsilande/projects/pydida/res"      # should be created
tmpldir = "/home/tsilande/projects/pydida/www/templates" 

site_url = "http://localhost:8040"
css_path = "%s/korita.css" % site_url

# SESSION HANDLING

def create_session():
    while True:
        try:
            id = sha.new(os.urandom(16)).hexdigest()
            dir = sdir(id)
            os.mkdir(dir)
            os.mkdir(wfn(dir,""))
            break
        except:
            pass

    return (id, dir,
            lambda x: sfn(dir,x),
            lambda x: wfn(dir, x),
            cfn(dir),
            get_syntax(dir))

def sdir(id):
    return os.path.join(datadir, "d"+id)

def get_sid(form):
    return form.getfirst('sid')
    
def get_session(form):
    id = get_sid(form)
    dir = sdir(id)
    return (id, dir,
            lambda x: sfn(dir,x),
            lambda x: wfn(dir, x),
            cfn(dir),
            get_syntax(dir))


def delete_session(id, clean=True): # use rmtree instead
    if clean:
        dir = sdir(id)
        for fn in os.listdir(dir):
            os.remove(os.path.join(dir, fn))
        os.rmdir(dir)

    
def sfn(sdir, pat): 
    return os.path.join(sdir, pat)

def wfn(sdir, pat): 
    return os.path.join(sdir, "work", str(pat))

def cfn(sdir):
    return sfn(sdir, "cmd_file")

# TEMPLATE PROCESSING

from htmltmpl import TemplateManager, TemplateProcessor

def tmpl(name, sid=None):
    if not name.endswith(".tmpl"):
        name = name+".tmpl"

    name = os.path.join(tmpldir, name)

    template  = TemplateManager().prepare(name)
    tproc     = TemplateProcessor()

    if sid: tproc.set('sid', sid)
    tproc.set('css_path', css_path)
        
    return template, tproc

# ERROR MESSAGING

def error(msg, sid=None):
    template, tproc = tmpl("error", sid)
    tproc.set("msg", msg)
    print "Content-Type: text/html\n"
    print tproc.process(template)
    sys.exit()

# SOME UTILS

def vars(sdir):
    return pydida.vars.vars(sfn(sdir,"vns"))

def sxfn(sdir):
    return sfn(sdir, "cmd_sx")

# option handling could be in its own package


def optcat(*opts):
    r = lambda x: "'" + x +"'"
    return " ".join([a==True and f or
                     (f.startswith("--") and (f+"="+r(a)) or (f+" "+r(a)))
                     for (f,a) in opts if a])

def sx_options(sx):
    flags = {'sep_mark' : 'sep',    'rng_mark'    : 'range',
             'cmd_sep' : 'cmd-sep', 'var_cmd_sep' : 'var-cmd-sep'}
    
    sx0  = pydida.varcmd.syntax({})
    return [("--%s" % flags[k], v) for k,v in sx.items() if sx0[k] != v]



def dump(obj, sdir, fn):
    pickle.dump(obj, file(sfn(sdir, fn), "w"))

def load(sdir, fn):
    return pickle.load(file(sfn(sdir, fn)))


def set_syntax(sdir, sx):
    dump(sx, sdir, "cmd_sx")

def get_syntax(sdir):
    sxfn = sfn(sdir,"cmd_sx")
    if os.path.exists(sxfn):
        return load(sdir, "cmd_sx")
    else:
        return pydida.varcmd.syntax({})

def save_cmds(fn, s):
    file(fn, "w").write(s.replace("\r\n", "\n"))
