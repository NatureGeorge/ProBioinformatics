# Perl: Find motif in chr19 with cds data
> ZeFeng Zhu 20190513
## Content
* Get Target Gene & cdsStart Info Using Hash
* Get Promoter Region
* Find Motif & Calculate distance

## Use
```perl
# @Date:   2019-05-07T08:28:32+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_BioPerl
# @Last modified time: 2019-05-13T15:39:32+08:00
use strict;
use POSIX;
```

## Codes *(Perl Language)*
### Get Target Gene & cdsStart Info Using Hash

```perl
my %cdsINFO_hash;
my @arr;
my $name;
my $strand;
my $chrID;
my $cdsStart;
# Read File
my $infile_1 = './coordinate-mm10';
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
```
#### Data Structure
```perl
foreach my $key (keys %cdsINFO_hash) {
  print "$key => $cdsINFO_hash{$key}\n";
}
'''
  NM_029499 => 11414816
  NM_021474 => 5475067
  NM_009045 => 5637834
  NM_024450 => 44203520
  NM_029372 => 58512357
  ...
'''
# Sort By Value
foreach my $key (sort {$cdsINFO_hash{$a} <=> $cdsINFO_hash{$b}} keys %cdsINFO_hash) {
  print "$key => $cdsINFO_hash{$key}\n";
}
'''
  NM_172252 => 3283071
  NR_105950 => 3288983
  NM_013495 => 3349201
  NM_001039658 => 3388949
  NM_001039657 => 3388949
  ...
'''
```
### Get Promoter Region
```perl
# Read File
my $infile_2 = './chr19.fa';
open(IN_2, $infile_2) || die "Can't open infile_2: $infile_2";

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
  ...
}
```
> So far, the whole sequence of Corresponding Promoter Region is stored in $temp_seq.

### Find Motif & Calculate distance
```perl
...
# Make Output File
my $outfile = 'C:/Users/Nature/Desktop/M_BioPerl/data/0507/chr19_+_motif_result.csv';
open(OUT, ">$outfile") || die "Can't make outfile: $outfile";
print OUT "name,cdsStart(+),dis\n";

my $motif = "TTCATTCATTCA";
my $offset;
my $result;
my $dis;
foreach my $key ( sort {$cdsINFO_hash{$a} <=> $cdsINFO_hash{$b}} keys %cdsINFO_hash) {
  ...
  # Use index() to get all the possible locations of motif
  $offset = 0;
  $temp_seq = uc($temp_seq); # Use uc() to get upper letter version of sequence
  $result = index($temp_seq, $motif, $offset);
  # Use array to store the result of dis
  my @disArray;
  while ($result != -1) {
    $dis = $result-10000; # Relative distance of motif
    print "Found $motif at $result, ($dis)\n";
    push(@disArray, $dis);
    $offset = $result + 1;
    $result = index($temp_seq, $motif, $offset);
  }
  print OUT "$key,$cdsINFO_hash{$key},@disArray\n";
}
```
