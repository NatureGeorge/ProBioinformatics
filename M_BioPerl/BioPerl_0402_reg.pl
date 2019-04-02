# @Date:   2019-04-02T08:53:32+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_BioPerl
# @Last modified time: 2019-04-02T09:26:14+08:00
# usr/bin/perl -w
use strict;

unless (@ARGV==2) {die"Usage: perl $0 <input.fa> <out.len>\n";}
my ($infile,$outfile) = @ARGV;
open(IN,$infile) || die "error: can't open infile: $infile";
open(OUT,">$outfile") || die "error: can't make outfile: $outfile";

my $seq;
my $len;
my $first = 1;
while(<IN>)
{
  if($_ =~ />(\S+)/)
  {
    $len = length($seq);
    if ($first) {$first = 0;}
    else {print OUT "$len\n";}
    $seq = "";
    print OUT ">$1\t";
  }
  elsif($_ !~ /^>/)
  {
    $_ =~ s/[\r\n\s+]//g;
    $seq .= $_;
  }
}
print OUT length($seq);

close IN;
close OUT;
