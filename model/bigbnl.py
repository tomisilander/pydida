#!/usr/bin/python

import sys, random, os
from operator import __add__

bd = "%s/bin" % os.environ['BAYWAYHOME']
search_pgm = "%s/bn_contd_learner" % bd
tree_pgm   = "%s/bflearner" % bd
eval_pgm   = "%s/modeleval" % bd
orient_pgm = "%s/bf_re-orient.py" % bd

if len(sys.argv) != 6:
    print >>sys.stderr,\
          "Usage: %s vdfile idtfile ess plan_fn res_fn" % sys.argv[0]
    sys.exit(1)

vdfn, idtfn, esss, plan_fn, res_fn = sys.argv[1:]
ess = float(esss)

# READ DATACOUNT WITHOUT LOADING WHOLE DATA
idtf=open(idtfn, "r")
dc = 0
for l in idtf.xreadlines() : dc += 1
idtf.close()


def create_sample(sample_fn, sample_frac):
    sample_size = 0
    idtf=open(idtfn, "r")
    sample_f = open(sample_fn, "w")
    for line in idtf.xreadlines():
        if random.random() < sample_frac:
            sample_f.write(line)
            sample_size += 1
    sample_f.close()
    idtf.close()
    return sample_size


pid = os.getpid()
currdir       = "/tmp/bigbnldir_curr_%d" % pid
prevdir       = "/tmp/bigbnldir_prev_%d" % pid
rprt_fn       = "%s/report" % currdir
search_pid_fn = "%s/pid"    % currdir
sample_fn     = "/tmp/bigbnlsample.%d" % pid

def wheel_get_no(ranked_nets):
    if random.choice((0,1)):
        return ranked_nets[-1][1]
    
    wheel = random.uniform(0, reduce(__add__, [rn[0] for rn in ranked_nets]))
    sel = 0
    sum = ranked_nets[sel][0]
    while sum < wheel:
        sel += 1
        sum += ranked_nets[sel][0]
    return ranked_nets[sel][1]


def run_and_score(sample_size, result_fn, rt, mxts):

    # run search
    
    search_cmd = "%s %s %s %d %f %s %s %d %d %s" \
                 % (search_pgm, vdfn, sample_fn, sample_size, ess, \
                    rprt_fn, result_fn, rt, mxts, search_pid_fn)
    os.system(search_cmd)
    
    # get score for net
    
    eval_cmd = "%s %s %s %d %s %f" \
               % (eval_pgm, vdfn, idtfn, dc, result_fn, ess)
    scorepipe = os.popen(eval_cmd) 
    score = float(scorepipe.readline())
    scorepipe.close()

    return score


# READ THE PLAN

plnf = open(plan_fn)
treecount = int(plnf.readline())
plan = [(float(f), int(c), int(t)) for f, c, t in
        [l.split() for l in plnf.readlines()]]
plnf.close()

def s2hms(tot_s):
    h = tot_s / 3600
    m = (tot_s - h*3600) / 60
    s =  tot_s - h*3600 - m*60
    return (h,m,s)

# REPORT TIME CONSUMPTION OF THE PLAN

sum=0
for sample_frac, sample_count, rt in plan :
    h,m,s = s2hms(sample_count* rt)
    print "Phase %.2f will take %d*%d s = %dh %dm %ds" \
          % (sample_frac, sample_count, rt, h, m , s)
    sum += sample_count * rt
print "Total run time about %dh %dm %ds " % s2hms(sum)


# GET INITIAL TREE

os.mkdir(prevdir)
result_fn = "%s/%d" % (prevdir, 0)
init_cmd = "%s %s %s %d %f %s" % (tree_pgm, vdfn, idtfn, dc, ess, result_fn)
#print init_cmd
scorepipe = os.popen(init_cmd)
tree_score = float(scorepipe.readline())
scorepipe.close()

scores_n_nets = [(tree_score,0)];

# FILL scores_n_nets WITH RE-ORIENTATIONS

for x in range(1,treecount): # should be plan based
    orient_cmd = "%s %s %s/%d" % (orient_pgm, result_fn, prevdir, x)
    os.system(orient_cmd)
    scores_n_nets.append((tree_score,x))
    
best_score, best_net_no = max(scores_n_nets)
os.system("cp %s/%d %s" % (prevdir, best_net_no, res_fn))
print "Best score:", best_score


# THEN EXECITE THE PLAN 

def handle_run(init_fn, sample_frac, sample_no, rt):
    global best_score
    
    print "Handling", sample_frac, sample_no,
    sys.stdout.flush()

    sample_size = create_sample(sample_fn, sample_frac)

    result_fn = "%s/%d" % (currdir, sample_no)
    os.system("cp %s %s" % (init_fn, result_fn))

    # mxts = int(sample_frac*sample_frac*100000000)
    mxts = 1000000
    curr_score = run_and_score(sample_size, result_fn, rt, mxts)
    scores_n_nets.append((curr_score, sample_no))
        
    print curr_score, best_score

    if curr_score > best_score :
        best_score = curr_score
        os.system("cp %s/%d %s" % (currdir, sample_no, res_fn))
        print "Best score:", best_score


def rank_nets(scores_n_nets): # BEST LAST
    scores_n_nets.sort()
    r = 1
    ranked_nets = [(r, scores_n_nets[0][1])]
    for i in range(1,len(scores_n_nets)):
        prev_s, prev_n = scores_n_nets[i-1]
        curr_s, curr_n = scores_n_nets[i]
        if prev_s != curr_s: r = i + 1
        ranked_nets.append((r,curr_n))

    return ranked_nets


# LOOP AS PLANNED

for sample_frac, sample_count, rt in plan :

    ranked_nets = rank_nets(scores_n_nets)
    scores_n_nets[:] = []

    os.mkdir(currdir)

    # run always once with best net
    
    handle_run(res_fn, sample_frac, 0, rt)

    # Then rest of the time with rank selected nets
    
    for sample_no in range(1,sample_count) :

        # find the init_net for the sample

        init_no = wheel_get_no(ranked_nets)
        init_fn = "%s/%d" % (prevdir, init_no)

        handle_run(init_fn, sample_frac, sample_no, rt)
        
    if os.path.exists(prevdir): os.system("rm -fr %s" % prevdir)
    os.rename(currdir, prevdir)

print "Best score:", best_score
os.system("rm -fr %s %s" % (currdir, prevdir))
os.unlink(sample_fn)
