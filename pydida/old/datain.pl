#!/usr/bin/perl -w

$bindir = "$ENV{BAYWAYHOME}/bin";

$formatcheck  = "$bindir/formatcheck.pl";
$missingcount = "$bindir/missingcount.pl";
$analyse      = "$bindir/analyse.pl";
$defcmd       = "$bindir/defcmd.pl";
$dispoint     = "$bindir/dispoint.pl";
$adis2vd      = "$bindir/adis2vd.pl";
$adis2dat     = "$bindir/adis2dat.pl";
#$a2n          = "$bindir/a2n.pl";
$ind_impute   = "$bindir/ind_impute.pl";
$nb_impute    = "$bindir/nb_imputer";

$anafile = "/tmp/ana.$$";
$ahgfile = "/tmp/ahg.$$";
$datfile = "/tmp/dat.$$";
$dspfile = "/tmp/dsp.$$";
$cmdfile = "/tmp/cmd.$$";
$hstfile = "/tmp/hst.$$";

if(4 != @ARGV and 3 != @ARGV ) {
    die "Usage: $0 txtdatafile imp(ign|gi|nb) vdfile idatafile\n".
	"  or   $0 txtdatafile imp(ign|gi|nb) dir\n";
}

my ($txtfile, $imp, $vdfile, $idtfile);

if(4 == @ARGV) {
    ($txtfile, $imp, $vdfile, $idtfile) = @ARGV;
    $anafile = "/tmp/ana.$$";
    $ahgfile = "/tmp/ahg.$$";
    $datfile = "/tmp/dat.$$";
    $dspfile = "/tmp/dsp.$$";
    $cmdfile = "/tmp/cmd.$$";
    $hstfile = "/tmp/hst.$$";
} else {
    ($txtfile, $imp, $dir) = @ARGV;
    $vdfile  = "$dir/data.vd";
    $idtfile = "$dir/data.idt";
    $anafile = "$dir/data.ana";
    $ahgfile = "$dir/data.ahg";
    $datfile = "$dir/data.dat";
    $dspfile = "$dir/data.dsp";
    $cmdfile = "$dir/data.cmd";
    $hstfile = "$dir/data.hst";
    system("mkdir -p $dir");
}


# CHECK FORMAT

my ($ok, $rest) = split(/\t/,`$formatcheck $txtfile`);
if(!$ok) {
    print "ERROR in data format:\n";
    print "$rest";
    exit;
}

chop $rest;
my ($N, $dim) = split(/\s/,$rest);
print "File check OK: N = $N and dim = $dim.\n";

undef $ok;
undef $rest;
undef $dim;

# CHECK MISSING

my ($maxmc,$maxmcdatano);
open(M,"$missingcount $txtfile |");
while (<M>) {
    my ($datano, $mc) = split(/\t/,$_);
    chop $mc;
    if($datano == 1 or $mc > $maxmc) {
	$maxmc = $mc;
	$maxmcdatano = $datano;
    }
}
close(M);

if($maxmc) {
    print "Maximum missings per vector is $maxmc"
	." in data number $maxmcdatano (counting from 1 on).\n";
} else {
    print "No missing data detected.\n";
}

undef $maxmcdatano;


# ANALYSE DATA

system("$analyse $txtfile $anafile $ahgfile");
print "Initial analysis of data done.\n";


# CREATE DEFAULT COMMANDS FOR A2N

system("$defcmd $anafile 6 EQW 3 $cmdfile");
print "Default discretization commands for data created.\n";


# DISCRETIZATION POINTS

system("$dispoint $anafile $ahgfile $cmdfile $dspfile");
print "Discretization points created.\n";


# VALUE DESCRIPION

system("$adis2vd $anafile $dspfile $vdfile");
print "Value descriptions created.\n";


# DATA AND HISTOGRAMS

system("$adis2dat $anafile $dspfile $txtfile $hstfile $datfile");
print "Data and histograms created\n";

# A2N

#system("$a2n $anafile $ARGV[0] $cmdfile $ARGV[2] $hstfile $datfile");
#print "Description file $ARGV[2] created and data discretized.\n";


# IMPUTE

if($imp eq "gi") {
    system("$ind_impute $datfile $hstfile $idtfile");
    print "Missing data imputed with GI method.\n" if ($maxmc);
} elsif($ARGV[1] eq "nb") {
    system("$nb_impute $vdfile $datfile $N $idtfile");
    print "Missing data imputed with NB method.\n" if ($maxmc);
} else {
    system("cp $datfile $idtfile");
}

print "Data file $idtfile created.\n";

#CLEANUP

if(4 == @ARGV) {
    unlink $anafile, $ahgfile, $cmdfile, $dspfile, $datfile, $hstfile;
}
