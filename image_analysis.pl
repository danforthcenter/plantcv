#!/usr/bin/perl
use strict;
use warnings;
use Getopt::Std;
use threads;
use Thread::Queue;
use Cwd;
use DBI;
use FindBin qw($Bin);
use Config::Tiny;
use Time::Local;
use POSIX qw(strftime);

my (%opt, $dir, $pipeline, $threads, $num,  @images, $image_dir, $sqldb, $type, %snapshots, %ids, $zoom_setting, $roi);
my %is_valid = (
  'vis_sv' => 1,
  'vis_tv' => 1,
  'nir_tv' => 1,
  'nir_sv' => 1,
  'flu_tv' => 1
);
getopts('d:p:t:n:i:s:T:z:m:rch', \%opt);
arg_check();

## Job start time
my $start_time = strftime("%Y-%m-%d_%H:%M:%S", localtime());

## Temporary file names
my $snapshot_tmp = $type.'_z'.$zoom_setting.'_snapshots.tab';
my $runinfo_tmp = $type.'_z'.$zoom_setting.'_runinfo.tab';
my $vis_shapes = $type.'_z'.$zoom_setting.'_vis_shapes.tab';
my $vis_colors = $type.'_z'.$zoom_setting.'_vis_colors.tab';
my $nir_shapes = $type.'_z'.$zoom_setting.'_nir_shapes.tab';
my $nir_signal = $type.'_z'.$zoom_setting.'_nir_signal.tab';
my $flu_shapes = $type.'_z'.$zoom_setting.'_flu_shapes.tab';
my $flu_signal = $type.'_z'.$zoom_setting.'_flu_signal.tab';
my $analysis_images = $type.'_z'.$zoom_setting.'_analysis_images.tab';
my $boundary_data = $type.'_z'.$zoom_setting.'_boundary_data.tab';

# Later connect to Bioinfo site to get version
our $outlier_vs = 0;

# Log files
my $skipped_log = 'plantcv_skipped_images_'.$type.'_z'.$zoom_setting.'_'.$start_time.'.log';
my $fail_log = 'plantcv_failed_images_'.$type.'_z'.$zoom_setting.'_'.$start_time.'.log';
open(SKIP, ">$skipped_log") or die "Cannot open file $skipped_log: $!\n\n";
open(FAIL, ">$fail_log") or die "Cannot open file $fail_log: $!\n\n";

# Open temporary database files
open(SNAP, ">$snapshot_tmp") or die "Cannot open file $snapshot_tmp: $!\n\n";
open(RUN, ">$runinfo_tmp") or die "Cannot open file $runinfo_tmp: $!\n\n";
open(IMG, ">$analysis_images") or die "Cannot open file $analysis_images: $!\n\n";
open(BOUND, ">$boundary_data") or die "Cannot open file $boundary_data: $!\n\n";

if ($type =~ /vis/) {
  open(SHAPE, ">$vis_shapes") or die "Cannot open file $vis_shapes: $!\n\n";
  open(SIG, ">$vis_colors") or die "Cannot open file $vis_colors: $!\n\n";
} elsif ($type =~ /nir/) {
  open(SHAPE, ">$nir_shapes") or die "Cannot open file $nir_shapes: $!\n\n";
  open(SIG, ">$nir_signal") or die "Cannot open file $nir_signal: $!\n\n";
} elsif ($type =~ /flu/) {
  open(SHAPE, ">$flu_shapes") or die "Cannot open file $flu_shapes: $!\n\n";
  open(SIG, ">$flu_signal") or die "Cannot open file $flu_signal: $!\n\n";
}

################################################################################
# Begin main
################################################################################

# Database setup
###########################################
if ($opt{'c'}) {
  if (-e $sqldb) {
    print STDERR "WARNING: SQLite database file $sqldb already exists are you sure you want to delete it? (y/n) ";
    my $response = <STDIN>;
    chomp $response;
    if ($response =~ /^y/i) {
      unlink($sqldb);
    } else {
      print STDERR "Okay, stopping\n\n";
      exit;
    }
  }
  my $schema = "$Bin/docs/results.sql";
  unless (-e $schema) {
    print STDERR "Schema file not found: $schema does not exists!\n\n";
    exit 1;
  }
  # Create new database and initialize with template schema
  `sqlite3 $sqldb '.read $Bin/docs/results.sql'`;
}

# Connect to the SQLite database
my $dbh = DBI->connect("dbi:SQLite:dbname=$sqldb","","");
###########################################

# Get last image, snapshot, and run entries
###########################################
foreach my $field ('image_id', 'snapshot_id') {
  my $sth = $dbh->prepare("SELECT MAX(`$field`) as max FROM `snapshots`");
  $sth->execute();
  while (my $result = $sth->fetchrow_hashref) {
    $ids{$field} = $result->{'max'};
  }
  if (!exists($ids{$field})) {
    $ids{$field} = 0;
  }
}

my $sth = $dbh->prepare("SELECT MAX(`run_id`) as max FROM `runinfo`");
$sth->execute();
while (my $result = $sth->fetchrow_hashref) {
  $ids{'run_id'} = $result->{'max'};
}
if (!exists($ids{'run_id'})) {
  $ids{'run_id'} = 0;
}
###########################################

# Run info
###########################################
# Next run ID
$ids{'run_id'}++;
my $analysis_time = time;
my @run = ($ids{'run_id'}, $analysis_time, $pipeline, $outlier_vs);
print RUN join("\t", @run)."\n";
###########################################

# Read image file names
###########################################
opendir (DIR, $dir) or die "Cannot open directory $dir: $!\n\n";
while (my $img = readdir(DIR)) {
  next if (substr($img,0,1) eq '.');
  
  # The directory might contain many types of images
  # Does this image match the input settings?
  if ($img =~ /$type.+z$zoom_setting/i) {
    push @images, $img;  
  } else {
    print SKIP $img."\n";
  }
}
closedir DIR;
###########################################

# Create job list
###########################################
our @jobs;
# Pipeline script prototype
# img will be replaced by the actual image file path
my @args = ('python', $pipeline, '-i', 'img', '-o', $image_dir);
if ($roi) {
	push @args, ('-m', $roi);
}


if ($opt{'r'}) {
  # For 1 to number of requested images
  for (my $n = 1; $n <= $num; $n++) {
    my $random_image = $images[rand(@images)];
    $args[3] = "'".$dir.'/'.$random_image."'";
    push @jobs, join(' ', @args);
  }
} else {
  foreach my $img (@images) {
    $args[3] = "'".$dir.'/'.$img."'";
    push @jobs, join(' ', @args);
  }
}
###########################################

# Initialize and run threads
###########################################
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
###########################################

# Dequeue data from the results queue
###########################################
while (threads->list(threads::running)) {
  while ($resultq->pending) {
    my $result = $resultq->dequeue();
    my @results = split /\n/, $result;
    process_results(@results);
  }
  sleep 2;
}
while ($resultq->pending) {
  my $result = $resultq->dequeue();
  my @results = split /\n/, $result;
  process_results(@results);
}

# Cleanup
###########################################
close SIG;
close SHAPE;
close RUN;
close SNAP;
close SKIP;
close FAIL;
close IMG;
close BOUND;
###########################################

# Populated database
###########################################
# Run info
`sqlite3 -separator \$'\t' $sqldb '.import $runinfo_tmp runinfo'`;
# Snapshots
`sqlite3 -separator \$'\t' $sqldb '.import $snapshot_tmp snapshots'`;
# Analysis images
`sqlite3 -separator \$'\t' $sqldb '.import $analysis_images analysis_images'`;
# Boundary data
`sqlite3 -separator \$'\t' $sqldb '.import $boundary_data boundary_data'`;
if ($type =~ /vis/) {
  `sqlite3 -separator \$'\t' $sqldb '.import $vis_shapes vis_shapes'`;  
  `sqlite3 -separator \$'\t' $sqldb '.import $vis_colors vis_colors'`;  
} elsif ($type =~ /nir/) {
  `sqlite3 -separator \$'\t' $sqldb '.import $nir_shapes nir_shapes'`;  
  `sqlite3 -separator \$'\t' $sqldb '.import $nir_signal nir_signal'`;  
} elsif ($type =~ /flu/) {
  `sqlite3 -separator \$'\t' $sqldb '.import $flu_shapes flu_shapes'`;  
  `sqlite3 -separator \$'\t' $sqldb '.import $flu_signal flu_signal'`;  
}
###########################################

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
    my $result = $job."\n";
    open JOB, "$job 2> /dev/null |" or die "Cannot execute job $job: $!\n\n";
    while (my $data = <JOB>) {
      $result .= $data;
    }
    close JOB;
    $resultq->enqueue($result);
  }
  threads->detach();
}

########################################
# Function: process_results
########################################
sub process_results {
  my @results = @_;
  
  # Job info
  ###########################################
  # Job
  my $job = shift @results;
  my @job = split /'/, $job;
  my @image = split /\//, $job[1];
  my $image = pop(@image);
  my $path = join('/', @image);
  ###########################################
  
  # Parse filename
  ###########################################
  my ($id, $year, $month, $day_time, $label, $camera_label) = split /-/, $image;
  $camera_label =~ s/FLUO/FLU/i;
  $camera_label =~ s/\.png//;
  my @camera_parts = split /_/, $camera_label;
  my $camera = lc($camera_parts[0].'_'.$camera_parts[1]);
  my ($frame, $zoom);
  if ($type eq 'vis_tv') {
    $frame = 0;
    if ($zoom_setting) {
      $zoom = $camera_parts[2];
    } else {
      $zoom = 0;
    }
  } elsif ($type eq 'flu_tv') {
    $frame = $camera_parts[3];
    $zoom = 0;
  } else {
    $frame = $camera_parts[2];
    if ($zoom_setting) {
      $zoom = $camera_parts[3];
    } else {
      $zoom = 0;
    }
  }
  $zoom =~ s/z//i;

  my ($day, $time) = split /\s/, $day_time;
  my ($hour, $min, $sec) = split /_/, $time;
  # Time since Unix Epoch
	# For timelocal months are coded 0-11, so reduce month by 1
	$month--;
	my $epoch_time = timelocal($sec,$min,$hour,$day,$month,$year);
  ###########################################
  
  # DB IDs
  ###########################################
  # New image ID
  $ids{'image_id'}++;
  my $image_id = $ids{'image_id'};
  # Snapshot ID
  my $snapshot_id;
  if (exists($snapshots{$id}->{$epoch_time})) {
    $snapshot_id = $snapshots{$id}->{$epoch_time};
  } else {
    # New snapshot ID
    $ids{'snapshot_id'}++;
    $snapshot_id = $ids{'snapshot_id'};
    $snapshots{$id}->{$epoch_time} = $snapshot_id;
  }
  my @snap = ($image_id, $ids{'run_id'}, $snapshot_id, $id, $epoch_time, $camera, $frame, $zoom, "$path/$image");
  ###########################################

	my $success = 0;
	while (@results) {
		my $line = shift @results;
		my @fields = split /\t/, $line;
		if ($fields[0] eq 'IMAGE') {
			# Analysis image
			###########################################
			my @img = ($image_id, $fields[1], $fields[2]);
			print IMG join("\t", @img)."\n";
			$success = 1;
		} elsif ($fields[0] eq 'HEADER_SHAPES') {
			# Shape results
      ###########################################
			my $data = shift @results;
			my @shape = shape_results($line, $data, $zoom);
			unshift(@shape, $image_id);
			print SHAPE join("\t", @shape)."\n";
			$success = 1;
		} elsif ($fields[0] eq 'HEADER_HISTOGRAM') {
			# Signal results
			###########################################
			my $data = shift @results;
			my @signal;
			if ($type =~ /vis/) {
				@signal = color_results($line, $data);
			} else {
				@signal = signal_results($line, $data);
			}
			
			unshift(@signal, $image_id);
			print SIG join("\t", @signal)."\n";
		} elsif ($fields[0] =~ /HEADER_BOUNDARY(\d+)/) {
			# Boundary results
			###########################################
			my $x = $1;
			my $data = shift @results;
			my @bound = boundary_results($line, $data);
			unshift(@bound, $x);
			unshift(@bound, $image_id);
			print BOUND join("\t", @bound)."\n";
			$success = 1;
		} else {
			print STDERR "ERROR: unrecognized output line\n  $line\n";
		}
	}
	
	# Did the job succeed?
  ###########################################
  if ($success == 0) {
    print FAIL "$image: FAILED\n";
    return;
  }
  print SNAP join("\t", @snap)."\n";
}

########################################
# Function: shape_results
#   Process shape results
########################################
sub shape_results {
  my $header = shift;
  my $data = shift;
  my $zoom = shift;
  
  my @data = split /\t/, $data;
  my $ci = column_index($header);
  
  my $area_raw = $data[$ci->{'area'}];
  my $area_corrected = 0;
  my $hull_area = $data[$ci->{'hull-area'}];
  my $solidity = $data[$ci->{'solidity'}];
  my $perimeter = $data[$ci->{'perimeter'}];
  my $extent_x = $data[$ci->{'width'}];
  my $extent_y = $data[$ci->{'height'}];
  my $centroid_x = $data[$ci->{'center-of-mass-x'}];
  my $centroid_y = $data[$ci->{'center-of-mass-y'}];
  my $longest_axis = $data[$ci->{'longest_axis'}];
  my $in_bounds = $data[$ci->{'in_bounds'}];
  
  # Zoom calibration: Note that TV correction has to be done during analysis
  if ($zoom > 0) {
    $area_corrected = $area_raw / zoom_calibration($zoom);
  }
  
  my @shape = ($area_raw, $area_corrected, $hull_area, $solidity, $perimeter,
               $extent_x, $extent_y, $centroid_x, $centroid_y, $longest_axis, $in_bounds
              );
  return @shape;
}

########################################
# Function: boundary_results
#   Process boundary results
########################################
sub boundary_results {
  my $header = shift;
  my $data = shift;
  
  my @data = split /\t/, $data;
  my $ci = column_index($header);
  
  my $height_above_bound = $data[$ci->{'height_above_bound'}];
  my $height_below_bound = $data[$ci->{'height_below_bound'}];
  my $above_bound_area = $data[$ci->{'above_bound_area'}];
  my $percent_above_bound_area = $data[$ci->{'percent_above_bound_area'}];
  my $below_bound_area = $data[$ci->{'below_bound_area'}];
  my $percent_below_bound_area = $data[$ci->{'percent_below_bound_area'}];
  
  my @bound = ($height_above_bound, $height_below_bound, $above_bound_area,
							 $percent_above_bound_area, $below_bound_area, $percent_below_bound_area
              );
  return @bound;
}

########################################
# Function: color_results
#   Process color results
########################################
sub color_results {
  my $header = shift;
  my $data = shift;
  
  $data =~ s/[\[\]]//g;
  $data =~ s/, /,/g;
  my @data = split /\t/, $data;
  my $ci = column_index($header);
  
  my $bins = $data[$ci->{'bin-number'}];
  my $blue = $data[$ci->{'blue'}];
  my $green = $data[$ci->{'green'}];
  my $red = $data[$ci->{'red'}];
  my $l = $data[$ci->{'lightness'}];
  my $a = $data[$ci->{'green-magenta'}];
  my $b = $data[$ci->{'blue-yellow'}];
  my $hue = $data[$ci->{'hue'}];
  my $saturation = $data[$ci->{'saturation'}];
  my $value = $data[$ci->{'value'}];

  my @signal = ($bins, $blue, $green, $red,
                $l, $a, $b,
                $hue, $saturation, $value);
  
  return @signal;
}

########################################
# Function: signal_results
#   Process signal results
########################################
sub signal_results {
  my $header = shift;
  my $data = shift;
  
  $data =~ s/[\[\]]//g;
  $data =~ s/, /,/g;
  my @data = split /\t/, $data;
  my $ci = column_index($header);
  
  my $bins = $data[$ci->{'bin-number'}];
  my $signal = $data[$ci->{'signal'}];
  
  my @signal = ($bins, $signal);
  
  return @signal;
}

########################################
# Function: column_index
#   Indexes column names from header
########################################
sub column_index {
  my $header = shift;
  my %index;
  
  my @header = split /\t/, $header;
  my $fields = scalar(@header);
  for (my $i = 0; $i < $fields; $i++) {
    $index{$header[$i]} = $i;
  }
  return \%index;
}


########################################
# Calculate zoom calibration factors
#    We need to scale pixel area per
#    camera zoom setting
########################################
sub zoom_calibration {
  my $zoom = shift;
  my $correction_factor = 0.9015 * exp(0.0007 * $zoom);
	return $correction_factor;
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
  if ($opt{'T'}) {
    $threads = $opt{'T'};
  } else {
    $threads = 1;
  }
  if ($opt{'n'}) {
    $num = $opt{'n'};
  } else {
    $num = 10;
  }
  if ($opt{'i'}) {
    $image_dir = $opt{'i'};
  } else {
    $image_dir = getcwd();
  }
  if ($opt{'t'}) {
    $type = $opt{'t'};
    if (!exists($is_valid{$type})) {
      arg_error("Camera type $type is not valid!");
    }
  } else {
    arg_error("A pipeline type is required!");
  }
  if ($opt{'z'}) {
    $zoom_setting = $opt{'z'};
  } else {
    $zoom_setting = 0;
  }
	if ($opt{'m'}) {
		$roi = $opt{'m'};
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
usage: image_analysis.pl -d DIR -p PIPELINE -t TYPE -s DB [-z ZOOM] [-i DIR] [-T THREADS] [-r] [-n NUM] [-c] [-h]

Multi-threaded execution of a plantcv image processing pipeline with
specific or randomly selected images.

arguments:
  -d DIR                Input directory containing images.
  -p PIPELINE           Pipeline script file.
  -t TYPE               Pipeline type (vis_sv, vis_tv, nir_sv, nir_tv, flu_tv).
  -z ZOOM               Optional camera zoom setting (INTEGER).
  -s DB                 SQLite database file name.
  -i DIR                Output directory for images. Not required by all pipelines, Default = cwd;
  -T THREADS            Number of threads/CPU to use. Default = 1.
  -r                    Select a random set of images from the input directory.
  -n NUM                Number of random images to test. Only used with -r. Default = 10.
  -c                    Create output database (SQLite). Default behaviour adds to existing database.
                        Warning: activating this option will delete an existing database!
  -m ROI                ROI/mask image. Required by some pipelines.
  -h, --help            show this help message and exit

  ";
  print STDERR $usage;
  exit 1;
}

################################################################################
# End functions
################################################################################