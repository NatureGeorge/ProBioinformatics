# @Date:   2019-04-09T08:55:04+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_BioPerl
# @Last modified time: 2019-04-15T16:03:01+08:00
use strict;
# Declare Variable
my $id;
my $GC;
my $AT;
my $seq;
my $GC_freq;
my $length;

# Prepare for the Input and Output Files
unless (@ARGV==2) {die"Usage: perl $0 <input.fa> <out.len>\n";}
my ($infile,$outfile) = @ARGV;
open(IN,$infile) || die "error: can't open infile: $infile";
open(OUT,">$outfile") || die "error: can't make outfile: $outfile";

# Define a function that calculate the frequence of GC bases
sub cal{
  $_ = $seq;
  $GC = (tr/GC/GC/);
  $AT = (tr/AT/AT/);
  $length = $GC + $AT;
  $GC_freq = $GC / $length;
  print OUT ">$id\tlength:$length\tGC_freq:$GC_freq\n$seq\n";
  $seq = "";
}
# Use circle to get info
foreach(<IN>){
  if($_ =~ /^>(.*)\n/){
    cal() if($id);
    $id = $1;
  }elsif($_ !~ /^>/){
    $_ =~ s/[\r\n\s+]//g;
    $seq = $seq.$_;
  }
}
# Get the info of the final sequence
cal();
# Close files
close(IN);
close(OUT);
