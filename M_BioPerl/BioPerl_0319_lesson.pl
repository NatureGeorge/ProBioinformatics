# @Date:   2019-03-19T08:05:22+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_BioPerl
# @Last modified time: 2019-03-19T09:44:38+08:00
#! /user/bin/perl
use strict;

my %freq;
my $count_sum = 0;
my $cal;
open(input, '<BioPerl_0319_sequence.txt') or die "can not open the file:, $!";
open(output, '>BioPerl_0319_sequence_count.txt');
print output "The frequency of base in NM_000546.5_cds_NP_000537.3_1 [gene=TP53]\n";
foreach(<input>)
{
  if (substr($_,0,1) ne ">" and substr($_,0,1) ne "\n")
  {
    chomp($_);
    for(my $j=0;$j<length($_);$j++)
    {
      $freq{substr($_,$j,1)} += 1;
      $count_sum += 1;
    }
  }
}
while(my($key, $value) = each %freq)
{
  $cal =  sprintf "%.2f",$value / $count_sum;
  print "base:$key, count: $value, frequency: $cal\n";
  print output "base:$key, count: $value, frequency: $cal\n";
}
close(input);
close(output);
