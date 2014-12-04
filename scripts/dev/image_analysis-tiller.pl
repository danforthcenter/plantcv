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
use Data::Dumper;
use Capture::Tiny ':all';

my (%opt, $dir, $pipeline, $threads, $num, $image_dir, $sqldb, $type, %ids, $zoom_setting, $roi, $start_date, $end_date);
our ($meta);
my %is_valid = (
  'vis_sv' => 1,
  'vis_tv' => 1,
  'nir_tv' => 1,
  'nir_sv' => 1,
  'flu_tv' => 1
);
my $command = $0.' '.join(' ', @ARGV);
getopts('d:p:t:n:i:s:T:z:m:D:rcfh', \%opt);
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
my $tillering_data= $type.'_z'.$zoom_setting.'_tillering_data.tab';

# Later connect to Bioinfo site to get version
our $outlier_vs = 0;

# Log files
my $skipped_log = 'plantcv_skipped_images_'.$type.'_z'.$zoom_setting.'_'.$start_time.'.log';
my $fail_log = 'plantcv_failed_images_'.$type.'_z'.$zoom_setting.'_'.$start_time.'.log';
my $error_log = 'plantcv_errors_'.$type.'_z'.$zoom_setting.'_'.$start_time.'.log';
open(SKIP, ">$skipped_log") or die "Cannot open file $skipped_log: $!\n\n";
open(FAIL, ">$fail_log") or die "Cannot open file $fail_log: $!\n\n";
open(ERROR, ">$error_log") or die "Cannot open file $error_log: $!\n\n";

# Open temporary database files
open(SNAP, ">$snapshot_tmp") or die "Cannot open file $snapshot_tmp: $!\n\n";
open(RUN, ">$runinfo_tmp") or die "Cannot open file $runinfo_tmp: $!\n\n";
open(IMG, ">$analysis_images") or die "Cannot open file $analysis_images: $!\n\n";
open(BOUND, ">$boundary_data") or die "Cannot open file $boundary_data: $!\n\n";
open(TILLER, ">$tillering_data") or die "Cannot open file $tillering_data: $!\n\n";

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
} else {
	unless (-e $sqldb) {
		arg_error("The database $sqldb does not exist and you did not ask to create it [-c].");
		exit 1;
	}
}

# Connect to the SQLite database
my $dbh = DBI->connect("dbi:SQLite:dbname=$sqldb","","");
###########################################

# Get last image and run entries
###########################################
my $sth = $dbh->prepare("SELECT MAX(`image_id`) as max FROM `snapshots`");
$sth->execute();
while (my $result = $sth->fetchrow_hashref) {
  $ids{'image_id'} = $result->{'max'};
}
if (!exists($ids{'image_id'})) {
  $ids{'image_id'} = 0;
}

$sth = $dbh->prepare("SELECT MAX(`run_id`) as max FROM `runinfo`");
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
my @run = ($ids{'run_id'}, $analysis_time, $command, $outlier_vs);
print RUN join("\t", @run)."\n";
###########################################

# Read image file names
###########################################
if ($opt{'f'}) {
	# Input directory is in flat format (single directory with images in it)
	$meta = read_flat_image_dir($dir, $type, $zoom_setting);
} else {
	# Input directory is in snapshot format with subdirectories for each snapshot
	$meta = read_snapshot_dir($dir, $type, $zoom_setting, $start_date, $end_date);
}
###########################################

# Create job list
###########################################
our @jobs;

if ($opt{'r'}) {
  # For 1 to number of requested images
	my @images = keys(%{$meta});
  for (my $n = 1; $n <= $num; $n++) {
		# Random image
		my $random_image = $images[rand(@images)];
		my $mdata = $meta->{$random_image};
		if ($opt{'f'}) {
			# Images are in one directory
			my $job = job_builder($type, $pipeline, $image_dir, "'$dir/$random_image'", $roi);
			push @jobs, $job;
		} else {
			if ($type eq 'flu_tv') {
				# For FLU images the pipeline needs three frames
				my ($fdark, $fmin, $fmax) = split /,/, $mdata->{'multi'};
				my $job = flu_job_builder($type, $pipeline, $image_dir, "'$dir/snapshot$mdata->{'snapshot'}/$fdark.png'", "'$dir/snapshot$mdata->{'snapshot'}/$fmin.png'", "'$dir/snapshot$mdata->{'snapshot'}/$fmax.png'", $roi);
				push @jobs, $job;
			} else {
				my $job = job_builder($type, $pipeline, $image_dir, "'$dir/snapshot$mdata->{'snapshot'}/$random_image.png'", $roi);
				push @jobs, $job;
			}
		}
  }
} else {
	# For each snapshot
	while (my ($img, $mdata) = each(%{$meta})) {
		if ($opt{'f'}) {
			# Images are in one directory
			my $job = job_builder($type, $pipeline, $image_dir, "'$dir/$img'", $roi);
			push @jobs, $job;
		} else {
			if ($type eq 'flu_tv') {
				# For FLU images the pipeline needs three frames
				my ($fdark, $fmin, $fmax) = split /,/, $mdata->{'multi'};
				my $job = flu_job_builder($type, $pipeline, $image_dir, "'$dir/snapshot$mdata->{'snapshot'}/$fdark.png'", "'$dir/snapshot$mdata->{'snapshot'}/$fmin.png'", "'$dir/snapshot$mdata->{'snapshot'}/$fmax.png'", $roi);
				push @jobs, $job;
			} else {
				my $job = job_builder($type, $pipeline, $image_dir, "'$dir/snapshot$mdata->{'snapshot'}/$img.png'", $roi);
				push @jobs, $job;
			}
		}
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
    process_results($type, $zoom_setting, @results);
  }
  sleep 2;
}
while ($resultq->pending) {
  my $result = $resultq->dequeue();
  my @results = split /\n/, $result;
  process_results($type, $zoom_setting, @results);
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
close TILLER;
close ERROR;
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
# Tiller data
`sqlite3 -separator \$'\t' $sqldb '.import $tillering_data tillering_data'`;

if ($type =~ /vis/) {
  `sqlite3 -separator \$'\t' $sqldb '.import $vis_shapes vis_shapes'`;  
  `sqlite3 -separator \$'\t' $sqldb '.import $vis_colors vis_colors'`;  
} elsif ($type =~ /nir/) {
  `sqlite3 -separator \$'\t' $sqldb '.import $nir_shapes nir_shapes'`;  
  `sqlite3 -separator \$'\t' $sqldb '.import $nir_signal nir_signal'`;  
} elsif ($type =~ /flu/) {
  `sqlite3 -separator \$'\t' $sqldb '.import $flu_shapes flu_shapes'`;  
  `sqlite3 -separator \$'\t' $sqldb '.import $flu_signal flu_fvfm'`;  
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
# Function: job_builder
#   Builds a command string
########################################
sub job_builder {
	my $type = shift;
	my $pipeline = shift;
	my $image_dir = shift;
	my $img = shift;
	my $roi = shift;
	
	# Pipeline script prototype
	# img will be replaced by the actual image file path
	my @args = ('python', $pipeline, '-i', 'img', '-o', $image_dir);
	if ($roi) {
		push @args, ('-m', $roi);
	}
	
	$args[3] = $img;
	
	return join(' ', @args);
}

########################################
# Function: flu_job_builder
#   Builds a command string for FLU pipelines
########################################
sub flu_job_builder {
	my $type = shift;
	my $pipeline = shift;
	my $image_dir = shift;
	my $fdark = shift;
	my $fmin = shift;
	my $fmax = shift;
	my $roi = shift;
	
	# Pipeline script prototype
	# img will be replaced by the actual image file path
	my @args = ('python', $pipeline, '-i1', 'img', '-i2', 'img', '-i3', 'img', '-o', $image_dir);
	if ($roi) {
		push @args, ('-m', $roi);
	}
	
	$args[3] = $fdark;
	$args[5] = $fmin;
	$args[7] = $fmax;
	
	return join(' ', @args);
}

########################################
# Function: read_flat_image_dir
#   Reads images from a single directory
########################################
sub read_flat_image_dir {
	my $dir = shift;
	my $type = shift;
	my $zoom_setting = shift;
	
	my %meta;
	opendir (DIR, $dir) or die "Cannot open directory $dir: $!\n\n";
	while (my $img = readdir(DIR)) {
		next if (substr($img,0,1) eq '.');
		
		# The directory might contain many types of images
		# Does this image match the input settings?
		if ($img =~ /$type.+z$zoom_setting/i) {
			my ($plant_id, $datetime, $frame, $zoom, $lifter) = parse_filename($img, $type, $zoom_setting);
			$meta{$img}->{'plant_id'} = $plant_id;
			$meta{$img}->{'datetime'} = $datetime;
			$meta{$img}->{'frame'} = $frame;
			$meta{$img}->{'lifter'} = $lifter;
		} else {
			print SKIP $img."\n";
		}
	}
	closedir DIR;
	return \%meta;
}

########################################
# Function: read_flat_image_dir
#   Reads images from a single directory
########################################
sub read_snapshot_dir {
	my $dir = shift;
	my $type = shift;
	my $zoom_setting = shift;
	my $start_date = shift;
	my $end_date = shift;
	
	# For image name compatibility
	$type =~ s/flu/fluo/;
	
	my %meta;
	# Open snapshot metadata file
	open(CSV, "$dir/SnapshotInfo.csv") or die "Cannot open $dir/SnapshotInfo.csv: #!\n\n";
	# Shift off header
	my $header = <CSV>;
	chomp $header;
	my @header = split /,/, $header;
	my %index;
	for (my $i = 0; $i < scalar(@header); $i++) {
		$index{$header[$i]} = $i;
	}
	
	while (my $line = <CSV>) {
		chomp $line;
		#my ($snapshot_id, $plant_id, $car_id, $datetime, $weight_before, $weight_after, $water_vol, $completed, $measure_label, $tiles) = split /,/, $line;
		my @fields = split /,/, $line;
		next if (!$fields[$index{'tiles'}]);
		my $snapshot_id = $fields[$index{'id'}];
		my $plant_id = $fields[$index{'plant barcode'}];
		my $datetime = $fields[$index{'timestamp'}];
		my $tiles = $fields[$index{'tiles'}];
		my ($date, $time) = split /\s/, $datetime;
		my ($year, $month, $day) = split /-/, $date;
		my ($hour, $min, $sec) = split /:/, $time;
	
		# Time since Unix Epoch
		# For timelocal months are coded 0-11, so reduce month by 1
		$month--;
		my $epoch_time = timelocal($sec,$min,$hour,$day,$month,$year);
		
		# Is this snapshot within the defined date range?
		next if ($epoch_time < $start_date || $epoch_time > $end_date);
		
		my @tiles = split /;/, $tiles;
		
		# Check for the requested image files
		my @matches;
		if ($opt{'D'}) {
			@matches = grep(/^$type/i, @tiles);
		} else {
			@matches = grep(/^$type.+[hz]$zoom_setting\_/i, @tiles);
		}
		
		@matches = sort @matches;
		# Build image meta object
		if (@matches && $type eq 'fluo_tv') {
			$meta{$matches[0]}->{'frame'} = 0;
			$meta{$matches[0]}->{'plant_id'} = $plant_id;
			$meta{$matches[0]}->{'datetime'} = $datetime;
			$meta{$matches[0]}->{'snapshot'} = $snapshot_id;
			$meta{$matches[0]}->{'multi'} = join(',', @matches);
			$meta{$matches[0]}->{'lifter'} = $zoom_setting;
		} elsif (@matches) {
			foreach my $tile (@matches) {
				my @parts = split /_/, $tile;
				my $frame = 0;
				if ($parts[1] eq 'SV') {
					$meta{$tile}->{'frame'} = $parts[2];
					if (exists($parts[4]) && substr($parts[4],0,1) eq 'h') {
						$parts[4] =~ s/h//;
						$meta{$tile}->{'lifter'} = $parts[4];
					} else {
						$meta{$tile}->{'lifter'} = 0;
					}
				} else {
					$meta{$tile}->{'frame'} = 0;
					if (exists($parts[3]) && substr($parts[3],0,1) eq 'h') {
						$parts[3] =~ s/h//;
						$meta{$tile}->{'lifter'} = $parts[3];
					}
				}
				$meta{$tile}->{'plant_id'} = $plant_id;
				$meta{$tile}->{'datetime'} = $datetime;
				$meta{$tile}->{'snapshot'} = $snapshot_id;
			}
		}
	}
	
	close CSV;
	return \%meta;
}

########################################
# Function: parse_filename
#   Parses filenames from dbImportExport
########################################
sub parse_filename {
	my $image = shift;
	my $type = shift;
	my $zoom_setting = shift;

	# Parse filename
  ###########################################
  my ($id, $year, $month, $day_time, $label, $camera_label) = split /-/, $image;
	# Temporarily fix lifter at 0
	my $lifter = 0;
	$day_time =~ s/_/:/g;
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
	
	return ($id, $year.'-'.$month.'-'.$day_time, $frame, $zoom, $lifter);
}

########################################
# Function: process
#   Execute image processing jobs
########################################
sub process {
  while (my $job = $jobq->dequeue()) {
    last if ($job eq 'EXIT');
    my $result = $job."\n";
		my ($stdout, $stderr, $exit) = capture {
			system($job);
		};
    #open JOB, "$job 2>> $error_log |" or die "Cannot execute job $job: $!\n\n";
    #while (my $data = <JOB>) {
    #  $result .= $data;
    #}
    #close JOB;
		
		# Append results
		$result .= $stdout;
		
		# Print error messages
		print ERROR $job."\n";
		print ERROR $stderr."\n\n";
		
    $resultq->enqueue($result);
  }
  threads->detach();
}

########################################
# Function: process_results
########################################
sub process_results {
	my $camera = shift;
	my $zoom = shift;
  my @results = @_;
  
  # Job info
  ###########################################
  # Job
  my $job = shift @results;
  my @job = split /'/, $job;
  my @image = split /\//, $job[1];
  my $image = pop(@image);
	if (!$opt{'f'}) {
		$image =~ s/\.png//;	
	}
  my $path = join('/', @image);
  ###########################################
  
  # Process attributes
  ###########################################
	my $plant_id = $meta->{$image}->{'plant_id'};
	my $datetime = $meta->{$image}->{'datetime'};
	my $frame = $meta->{$image}->{'frame'};
	my $lifter = $meta->{$image}->{'lifter'};
	my @multi;
	if ($camera eq 'flu_tv') {
		@multi = split /,/, $meta->{$image}->{'multi'};
		for (my $i = 0; $i < scalar(@multi); $i++) {
			$multi[$i] = $path.'/'.$multi[$i].'.png';
		}
	}
	my ($date, $time) = split /\s/, $datetime;
	my ($year, $month, $day) = split /-/, $date;
	my ($hour, $min, $sec) = split /:/, $time;

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
	my @snap;
	if ($camera eq 'flu_tv') {
		@snap = ($image_id, $ids{'run_id'}, $plant_id, $epoch_time, $camera, $frame, $zoom, $lifter, join(',', @multi));
	} else {
		@snap = ($image_id, $ids{'run_id'}, $plant_id, $epoch_time, $camera, $frame, $zoom, $lifter, "$path/$image.png");
	}
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
			} elsif ($type =~ /nir/) {
				@signal = nir_results($line, $data);
			} elsif ($type =~ /flu/) {
				@signal = flu_results($line, $data);
			}
			
			unshift(@signal, $image_id);
			print SIG join("\t", @signal)."\n";
			$success = 1;
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
		} elsif ($fields[0] =~ /HEADER_TILLERING(\d+)/) {
			# Tiller results
			###########################################
			my $x = $1;
			my $data = shift @results;
			my @tiller = tillering_results($line, $data);
			unshift(@tiller, $x);
			unshift(@tiller, $image_id);
			print TILLER join("\t", @tiller)."\n";
			$success = 1;
		}else {
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
  
  my $area = $data[$ci->{'area'}];
  #my $area_corrected = 0;
  my $hull_area = $data[$ci->{'hull-area'}];
  my $solidity = $data[$ci->{'solidity'}];
  my $perimeter = $data[$ci->{'perimeter'}];
  my $extent_x = $data[$ci->{'width'}];
  my $extent_y = $data[$ci->{'height'}];
  my $centroid_x = $data[$ci->{'center-of-mass-x'}];
  my $centroid_y = $data[$ci->{'center-of-mass-y'}];
  my $longest_axis = $data[$ci->{'longest_axis'}];
	my $vertices = $data[$ci->{'hull_vertices'}];
  my $in_bounds = $data[$ci->{'in_bounds'}];
  
  # Zoom calibration: Note that TV correction has to be done during analysis
  #if ($zoom > 0) {
  #  $area_corrected = $area_raw / zoom_calibration($zoom);
  #}
  
  my @shape = ($area, $hull_area, $solidity, $perimeter,
               $extent_x, $extent_y, $centroid_x, $centroid_y, $longest_axis, $vertices, $in_bounds
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
  
  my @bound = ($height_above_bound, $height_below_bound, $above_bound_area,$percent_above_bound_area, $below_bound_area, $percent_below_bound_area
              );
  return @bound;
}

########################################
# Function: tillering_results
#   Process tillering results
########################################
sub tillering_results {
    my $header = shift;
    my $data = shift;
    
    my @data = split /\t/, $data;
    my $ci = column_index($header);
    
    my $raw_tillering_count = $data[$ci->{'raw_tillering_count'}];
    my $raw_tillering_width = $data[$ci->{'raw_tillering_widths'}];
    my $average_tillering_width = $data[$ci->{'average_tillering_width'}];
    my $median_tillering_width = $data[$ci->{'median_tillering_width'}];
    my $std_tillering_width = $data[$ci->{'std_tillering_width'}];
    
    my @tiller = ($raw_tillering_count, $raw_tillering_width, $average_tillering_width,$median_tillering_width, $std_tillering_width
    );
    return @tiller;
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
# Function: nir_results
#   Process NIR reflectance results
########################################
sub nir_results {
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
# Function: flu_results
#   Process NIR reflectance results
########################################
sub flu_results {
  my $header = shift;
  my $data = shift;
  
  $data =~ s/[\[\]]//g;
  $data =~ s/, /,/g;
  my @data = split /\t/, $data;
  my $ci = column_index($header);
  
  my $bins = $data[$ci->{'bin-number'}];
	my $fvfm_bins = $data[$ci->{'fvfm_bins'}];
  my $fvfm = $data[$ci->{'fvfm_hist'}];
	my $peak = $data[$ci->{'fvfm_hist_peak'}];
	my $median = $data[$ci->{'fvfm_median'}];
	my $qc = $data[$ci->{'fdark_passed_qc'}];
  
  my @signal = ($bins, $fvfm_bins, $fvfm, $peak, $median, $qc);
  
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
    arg_error("A camera zoom setting is required!");
  }
	if ($opt{'m'}) {
		$roi = $opt{'m'};
	} elsif ($type eq 'vis_tv' || $type eq 'flu_tv') {
		arg_error("$type pipelines require an ROI image!");
	}
	if (!$opt{'f'}) {
		# Does the snapshot metadata file exist?
		unless (-e "$dir/SnapshotInfo.csv") {
			arg_error("The snapshot metadata file SnapshotInfo.csv does not exist in $dir. Perhaps you did not mean to use the -f option?");
		}
	}
	if ($opt{'D'}) {
		my ($start, $end) = split /_/, $opt{'D'};
		if (!$end) {
			$end = strftime("%Y-%m-%d-%H-%M-%S", localtime());
		}
		my @start = split /-/, $start;
		my @end = split /-/, $end;
		
		# Time since Unix Epoch
		# For timelocal months are coded 0-11, so reduce month by 1
		$start[1]--;
		$end[1]--;
		$start_date = timelocal(reverse(@start));
		$end_date = timelocal(reverse(@end));
	} else {
		$start_date = 1;
		my $current = strftime("%Y-%m-%d-%H-%M-%S", localtime());
		my @current = split /-/, $current;
		$current[1]--;
		$end_date = timelocal(reverse(@current));
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
usage: image_analysis.pl -d DIR [-f] -p PIPELINE -t TYPE -s DB -z ZOOM [-i DIR] [-T THREADS] [-r] [-n NUM] [-c] [-m ROI] [-h]

Multi-threaded execution of a plantcv image processing pipeline with
specific or randomly selected images.

arguments:
  -d DIR                Input directory containing images or snapshots.
  -f                    Input directory format is flat (directory of images). Default behavior expects a directory of snapshot folders and CSV metafile.
  -p PIPELINE           Pipeline script file.
  -t TYPE               Pipeline type (vis_sv, vis_tv, nir_sv, nir_tv, flu_tv).
  -z ZOOM               Camera zoom setting (INTEGER).
  -s DB                 SQLite database file name.
  -i DIR                Output directory for images. Not required by all pipelines, Default = cwd;
  -T THREADS            Number of threads/CPU to use. Default = 1.
  -r                    Select a random set of images from the input directory.
  -n NUM                Number of random images to test. Only used with -r. Default = 10.
  -c                    Create output database (SQLite). Default behaviour adds to existing database.
                        Warning: activating this option will delete an existing database!
  -m ROI                ROI/mask image. Required by some pipelines (vis_tv, flu_tv).
  -D DATES              Date range. Format: YYYY-MM-DD-hh-mm-ss_YYYY-MM-DD-hh-mm-ss. If the second date is excluded then the current date is assumed.
  -h                    Show this help message and exit

  ";
  print STDERR $usage;
  exit 1;
}

################################################################################
# End functions
################################################################################