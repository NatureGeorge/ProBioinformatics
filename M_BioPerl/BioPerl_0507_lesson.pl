# @Date:   2019-05-07T08:28:32+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_BioPerl
# @Last modified time: 2019-05-13T16:25:18+08:00
use strict;
use POSIX;
# unless(@ARGV==3){die "Usage Perl: $0 <CDS_Start_file.txt> <CHR_file.fa> <outfile.txt>";}
# my ($infile_1,$infile_2,$outfile) = @ARGV;
my $infile_1 = 'C:/Users/Nature/Desktop/M_BioPerl/data/0507/coordinate-mm10';
my $infile_2 = 'C:/Users/Nature/Desktop/M_BioPerl/data/0507/chr19.fa';
my $outfile = 'C:/Users/Nature/Desktop/M_BioPerl/data/0507/chr19_+_motif_result.csv';
open(IN_1, $infile_1) || die "Can't open infile_1: $infile_1";
open(IN_2, $infile_2) || die "Can't open infile_2: $infile_2";
# open(OUT, ">$outfile") || die "Can't make outfile: $outfile";
# print OUT "name,cdsStart(+),dis\n";

my %cdsINFO_hash;
my @arr;
my $name;
my $strand;
my $chrID;
my $cdsStart;

readline IN_1;
while(<IN_1>){
  @arr = split /\s+/, $_;
  $name = $arr[1];
  $chrID = $arr[2];
  $strand = $arr[3];
  $cdsStart = $arr[6];
  if ($chrID eq 'chr19' and $strand eq '+'){
    $cdsINFO_hash{$name} = $cdsStart;
  }
}

my $motif = "TTCATTCATTCA";
my $count;
my $temp_seq;
my $locate;
my $line_a;
my $line_b;
my $head;
my $tail;
my $offset;
my $result;
my $dis;
foreach my $key ( sort {$cdsINFO_hash{$a} <=> $cdsINFO_hash{$b}} keys %cdsINFO_hash) {
  $locate = $cdsINFO_hash{$key};
  $line_a = floor(($locate-10000) / 50);
  $line_b = $line_a + 400;

  print "$key => $cdsINFO_hash{$key} => $line_a,$line_b\n";

  seek(IN_2,7+51*$line_a,0);
  $head = <IN_2>;
  $count = 1;
  $temp_seq = substr $head,($locate-10000-$line_a*50-1);
  $temp_seq =~ s/[\r\n\s+]//g;

  while (<IN_2>){
    $_ =~ s/[\r\n\s+]//g;
    $temp_seq .= $_;
    $count += 1;
    if (tell IN_2 == 7+51*$line_b){
      $tail = <IN_2>;
      $count += 1;
      $temp_seq .= substr $tail,0,($locate+10000-$line_b*50);
      last;
    }
  }

  my $seqLen = length($temp_seq);
  print "Length: $seqLen\n";
  my @words = ($temp_seq =~ /(TTCATTCATTCA)/ig);
  if (@words){
    print "RE: @words \n";
  }
  #  $end = pos($seq);
	#	$start = $end - $len + 1;

  $offset = 0;
  $result = index(uc($temp_seq), $motif, $offset);
  my @disArray;
  while ($result != -1) {
    $dis = $result-10000;
    print "Found $motif at $result, ($dis)\n";
    push(@disArray, $dis);
    $offset = $result + 1;
    $result = index(uc($temp_seq), $motif, $offset);
  }
  print "#--------------------------------------------------count: $count--#\n";
  print OUT "$key,$cdsINFO_hash{$key},@disArray\n";
}

close IN_1;
close IN_2;
# close OUT
