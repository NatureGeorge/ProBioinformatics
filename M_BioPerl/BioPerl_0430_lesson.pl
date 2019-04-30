# @Date:   2019-04-30T08:17:31+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_BioPerl
# @Last modified time: 2019-04-30T08:57:55+08:00
use strict;
unless(@ARGV==3){die "Usage Perl: $0 <infile_1.txt> <infile_2.txt> <outfile.txt>";}
my ($infile_1,$infile_2,$outfile) = @ARGV;
open(IN_1, $infile_1) || die "Can't open infile_1: $infile_1";
open(IN_2, $infile_2) || die "Can't open infile_2: $infile_2";
open(OUT, ">$outfile") || die "Can't make outfile: $outfile";

my %hash_1;
my %hash_2;
my $temp;

while(<IN_1>){
  @info = split /\t/, $_;
  $hash_1{$info[0]} = $info[1];
}

while(<IN_2>){
  @info = split /\t/, $_;
  $hash_2{$info[0]} = $info[1];
}

foreach my $key (sort keys %hash_1){
  $temp = $hash_1{$key} * $hash_2{$key};
  print OUT "$key\t$temp\n";
}

close IN_1;
close IN_2;
close OUT;
