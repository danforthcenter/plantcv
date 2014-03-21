#!/usr/bin/perl
use strict;
use warnings;
use Getopt::Std;
use threads;
use Thread::Queue;
use Cwd;
use DBI;
use FindBin qw($Bin);

my (%opt, $dir, $pipeline, $threads, $num, $roi, @images, $image_dir, $sqldb, $type);
getopts('d:p:t:n:m:i:s:T:rch', \%opt);
arg_check();

## Temporary file names
my $snapshot_tmp = 'snapshots.tab';
my $runinfo_tmp = 'runinfo.tab';
my $vis_shapes = 'vis_shapes.tab';
my $vis_colors = 'vis_colors.tab';
my $nir_shapes = 'nir_shapes.tab';
my $nir_signal = 'nir_signal.tab';
my $flu_shapes = 'flu_shapes.tab';
my $flu_signal = 'flu_signal.tab';

################################################################################
# Begin main
################################################################################

## Database setup
if ($opt{'c'}) {
  if (-e $sqldb) {
    unlink($sqldb);
  }
  # Create new database and initialize with template schema
  `sqlite3 $sqldb '.read $Bin/docs/results.sql'`;
}

# Connect to the SQLite database
my $dbh = DBI->connect("dbi:SQLite:dbname=$sqldb","","");

## Read image file names
opendir (DIR, $dir) or die "Cannot open directory $dir: $!\n\n";
while (my $img = readdir(DIR)) {
  next if (substr($img,0,1) eq '.');
  $img =~ s/ /\\ /g;
  push @images, $img;
}
closedir DIR;

## Create job list
our @jobs;
# Pipeline script prototype, img will be replaced by the actual image file path
my @args = (
  'python',
  $pipeline,
  '-i',
  'img',
  '-m',
  $roi,
  '-o',
  $image_dir
);
if ($opt{'r'}) {
  # For 1 to number of requested images
  for (my $n = 1; $n <= $num; $n++) {
    my $random_image = $images[rand(@images)];
    $args[3] = $dir.'/'.$random_image;
    push @jobs, join(' ', @args);
  }
} else {
  foreach my $img (@images) {
    $args[3] = $dir.'/'.$img;
    push @jobs, join(' ', @args);
  }
}

## Initialize and run threads
my $jobq = Thread::Queue->new();
my $resultq = Thread::Queue->new();
# Enqueue jobs
foreach my $job (@jobs) {
  $jobq->enqueue($job);
}
# Enqueue exits
for (my $t = 1; $t <= $threads; $t++) {
  $jobq->enqueue("EXIT");
}
# Create thread pool
for (my $t = 1; $t <= $threads; $t++) {
  threads->create("process");
}

## Dequeue data from the results queue
open(SNAP, ">$snapshot_tmp") or die "Cannot open file $snapshot_tmp: $!\n\n";
open(RUN, ">$runinfo_tmp") or die "Cannot open file $runinfo_tmp: $!\n\n";

if ($type eq 'vis') {
  open(SHAPE, ">$vis_shapes") or die "Cannot open file $vis_shapes: $!\n\n";
  open(SIG, ">$vis_colors") or die "Cannot open file $vis_colors: $!\n\n";
} elsif ($type eq 'nir') {
  open(SHAPE, ">$nir_shapes") or die "Cannot open file $nir_shapes: $!\n\n";
  open(SIG, ">$nir_signal") or die "Cannot open file $nir_signal: $!\n\n";
} elsif ($type eq 'flu') {
  open(SHAPE, ">$flu_shapes") or die "Cannot open file $flu_shapes: $!\n\n";
  open(SIG, ">$flu_signal") or die "Cannot open file $flu_signal: $!\n\n";
}

while (threads->list(threads::running)) {
  while ($resultq->pending) {
    my $result = $resultq->dequeue();
    my @results = split /\n/, $result;
    my $image = shift(@results);
    
    # Shape results
  }
  sleep 2;
}
while ($resultq->pending) {
  my $result = $resultq->dequeue();
  print $result;
}

## Populated database

close SIG;
close SHAPE;
close RUN;
close SNAP;
exit;
################################################################################
# End main
################################################################################

################################################################################
# Begin functions
################################################################################

########################################
# Function: process
#   Execute image processing jobs
########################################
sub process {
  while (my $job = $jobq->dequeue()) {
    last if ($job eq 'EXIT');
    my $result;
    open JOB, "$job |" or die "Cannot execute job $job: $!\n\n";
    while (my $data = <JOB>) {
      $result .= $data;
    }
    close JOB;
    $resultq->enqueue($result);
  }
  threads->detach();
}

########################################
# Function: arg_check
#   Evaluates input arguments
########################################
sub arg_check {
  if ($opt{'h'}) {
    arg_error();
  }
  if ($opt{'d'}) {
    $dir = $opt{'d'};
  } else {
    arg_error("An input directory is required!");
  }
  if ($opt{'p'}) {
    $pipeline = $opt{'p'};
  } else {
    arg_error("A pipeline script file is required!");
  }
  if ($opt{'s'}) {
    $sqldb = $opt{'s'};
  } else {
    arg_error("A SQLite database filename is required!");
  }
  if ($opt{'t'}) {
    $threads = $opt{'t'};
  } else {
    $threads = 1;
  }
  if ($opt{'n'}) {
    $num = $opt{'n'};
  } else {
    $num = 10;
  }
  if ($opt{'m'}) {
    # For now we will have to include this. Maybe it should be hardcoded in the pipeline?
    $roi = $opt{'m'};
  } else {
    arg_error("A ROI image file is required!");
  }
  if ($opt{'i'}) {
    $image_dir = $opt{'i'};
  } else {
    $image_dir = getcwd();
  }
  if ($opt{'T'}) {
    $type = $opt{'T'};
  } else {
    $type = 'vis';
  }
}

########################################
# Function: arg_error
#   Prints error messages and usage instructions
########################################
sub arg_error {
  my $error = shift;
  if ($error) {
    print STDERR $error."\n";
  }
  my $usage = "
usage: image_analysis.pl -d DIR -p PIPELINE [-r] [-n NUM] [-t THREADS] [-T TYPE] [-h]

Multi-threaded execution of a plantcv image processing pipeline with
specific or randomly selected images.

arguments:
  -d DIR                Input directory containing images.
  -p PIPELINE           Pipeline script file.
  -m ROI                ROI image.
  -s DB                 SQLite database file name.
  -i DIR                Output directory for images. Not required by all pipelines, Default = cwd;
  -t THREADS            Number of threads/CPU to use. Default = 1.
  -T TYPE               Pipeline type (vis, nir, flu), Default = vis.
  -r                    Select a random set of images from the input directory.
  -n NUM                Number of random images to test. Only used with -r. Default = 10.
  -c                    Create output database (SQLite). Default behaviour adds to existing database.
                        Warning: activating this option will delete an existing database!
  -h, --help            show this help message and exit

  ";
  print STDERR $usage;
  exit 1;
}

################################################################################
# End functions
################################################################################