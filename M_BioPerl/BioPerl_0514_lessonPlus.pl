# @Date:   2019-05-14T08:15:59+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioPerl_0514_lessonPlus.pl
# @Last modified time: 2019-05-24T20:25:50+08:00
use strict;
use POSIX;

my %cdsINFO_hash;
my @arr;
my $name;
my $strand;
my $chrID;
my $cdsStart;
# Read File
my $infile_1 = 'C:/Users/Nature/Desktop/M_BioPerl/data/0507/coordinate-mm10';
open(IN_1, $infile_1) || die "Can't open infile_1: $infile_1";
# Skip the row of column names
readline IN_1;
while(<IN_1>){
  # Transform the line into a list
  @arr = split /\s+/, $_;
  $name = $arr[1]; # Gene(Accession Number)
  $chrID = $arr[2];
  $strand = $arr[3];
  $cdsStart = $arr[6];
  # Filter Data
  if ($chrID eq 'chr19' and $strand eq '+'){
    # Collect data using hash
    $cdsINFO_hash{$name} = $cdsStart;
  }
}

# Read File
my $infile_2 = 'C:/Users/Nature/Desktop/M_BioPerl/data/0507/chr19.fa';
open(IN_2, $infile_2) || die "Can't open infile_2: $infile_2";
# Make Output File
my $outfile = 'C:/Users/Nature/Desktop/M_BioPerl/data/0507/chr19_+_motif_result_0514.csv';
open(OUT, ">$outfile") || die "Can't make outfile: $outfile";
print OUT "name,cdsStart(+),dis\n";

my $temp_seq;
my $head;
my $tail;
my $locate;
my $line_a;
my $line_b;
foreach my $key ( sort {$cdsINFO_hash{$a} <=> $cdsINFO_hash{$b}} keys %cdsINFO_hash) {
  $locate = $cdsINFO_hash{$key}; # cdsStart
  # Get the line index of Promoter Region [line_a, line_b]
  $line_a = floor(($locate-10000) / 50);
  $line_b = $line_a + 400;
  # Use seek() to jump to Corresponding Promoter Region
  seek(IN_2,7+51*$line_a,0);
  # First Line of Corresponding Promoter Region
  $head = <IN_2>;
  # Use substr() to get the head sequence of Promoter in the first line
  $temp_seq = substr $head,($locate-10000-$line_a*50-1);
  $temp_seq =~ s/[\r\n\s+]//g; # delete '\n'
  # Get the remaining sequence
  while (<IN_2>){
    $_ =~ s/[\r\n\s+]//g; # delete '\n'
    $temp_seq .= $_;
    # Use tell() to determine whether the loop has reached the tail of Promoter
    if (tell IN_2 == 7+51*$line_b){
      $tail = <IN_2>;
      # Use substr() to get the tail sequence of Promoter in the last line
      $temp_seq .= substr $tail,0,($locate+10000-$line_b*50);
      # End the loop
      last;
    }
  }
  my @disArray = findMotif("TTCATTCATTCA", $temp_seq, $key);
  print OUT "$key,$cdsINFO_hash{$key},@disArray\n";
}


sub findMotif{
  my $motif = $_[0];
  my $temp_seq = $_[1];
  my $id = $_[2];
  # Use index() to get all the possible locations of motif
  my $offset = 0;
  $temp_seq = uc($temp_seq); # Use uc() to get upper letter version of sequence
  my $result = index($temp_seq, $motif, $offset);
  # Use array to store the result of dis
  my @disArray;
  while ($result != -1) {
    my $dis = $result-10000; # Relative distance of motif
    print substr($temp_seq,$result-10,10);
    print " {TTCATTCATTCA} ";
    print substr($temp_seq,$result+12,10);
    # print "\nTEST\n";
    # print substr($temp_seq,$result-10,50);

    print "\n$id Found $motif at $result, ($dis)\n";
    push(@disArray, $dis);
    $offset = $result + 1;
    $result = index($temp_seq, $motif, $offset);
  }
  return @disArray;
}

close IN_1;
close IN_2;
close OUT;

my $end_time = time();
my $elapsed_time = $end_time - $^T;
print "RUN TIME: $elapsed_time";
