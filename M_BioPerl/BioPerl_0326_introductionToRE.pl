# usr/bin/perl -w
use strict;

unless (@ARGV==2) {                                              
    die"Usage: perl $0 <input.fa> <out.len\n";  

my ($infile,$outfile) = @ARGV;
open(IN,$infile) || die "error: can't open infile: $infile";      
open(OUT,">$outfile") || die "error: can't make outfile: $outfile";
my $line=<IN>;
if($line=~m/^>(\S+)/)
{
	print OUT ">$1\t";
}

my $seq;

while($line=<IN>)
{
	if($line !~ /^>/)
	{
		$line=~s/[\r\n\s+]//g;
		$seq.=$line;
	}elsif($line=~/^>(\S+)/)
	{
		print OUT length($seq);
		$seq="";
		print OUT "\n>$1\t";
	}
}

print OUT length($seq)."\n";

close IN;
close OUT;
