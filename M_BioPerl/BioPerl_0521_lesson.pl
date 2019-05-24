# @Date:   2019-05-21T08:43:39+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioPerl_0521_lesson.pl
# @Last modified time: 2019-05-24T22:34:43+08:00
use strict;
use POSIX;
use List::Util qw/sum/;

my $infile_1 = 'C:/Users/Nature/Desktop/M_BioPerl/data/0521/0input-100.fastq';
open(IN_1, $infile_1) || die "Can't open infile_1: $infile_1";

my @matrix;
my @qValue_Mean_matrix;
my @qValue_Quartile_matrix;

sub temp{
  return($_ - 33);
}

# Collcet data and transfrom it into a multidimensional matrix
while(<IN_1>){
  if($. % 4 == 0){
    $_ =~ s/[\r\n\s+]//g;
    my @new = map(temp, map(ord, split(//, $_)));
    push @matrix,[@new];
  }
}

sub getQuartile_exc{
  # Def a subFunction that get the median index of a particular range
  sub getMidIndex_exc{
     my ($beg, $end) = @_;
     my $midIndex = $end - $beg + 1;
     $midIndex = floor(($midIndex + 1) / 2) - 1;
     return ($midIndex + $beg);
  }
  my @temp_array = @_;
  my $length = @temp_array;
	my $q2 = getMidIndex_exc(0, $length); # Index of median of entire data
	my $q1 = getMidIndex_exc(0, $q2); # Median of first half
	my $q3 = getMidIndex_exc($q2 + 1, $length); # Median of second half
	return ($temp_array[$q1], $temp_array[$q2], $temp_array[$q3]);
}

for (@matrix) {
    my @temp_array = sort{$a <=> $b} @{$_};
    my @quartile_array = getQuartile_exc(@temp_array);
    push @qValue_Quartile_matrix, [@quartile_array];
    push @qValue_Mean_matrix, [sum(@{$_}) / @{$_}];
}

sub print_array{
    for (@_) {
        print "[ @{$_} ]\n";
    }
    print "----------END----------\n\n";
}

print "qValue_Quartile_matrix:\n";
print_array(@qValue_Quartile_matrix);
print "qValue_Mean_matrix:\n";
print_array(@qValue_Mean_matrix);

close IN_1;
