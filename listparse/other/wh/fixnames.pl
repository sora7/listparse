#!/usr/bin/env perl

use strict;
use warnings;
use File::Copy;

my $path = '/home/alex/Загрузки/dir/';

my $count = 0;
&fixdir($path);
print "$count files fixed\n";
print "DONE\n";

sub fixdir {
	my $path = $_[0];
	opendir(my $dir,$path);
	while (my $file = readdir($dir)) {
		if ($file !~ /^(\.|\.\.)$/) {
			my $oldname = join('/',($path,$file));
			if (-d($oldname)) {
				&fixdir($oldname);
			}
			
			my $line = $file;
			my $replace = $line =~ s/[\"\|\!\:\*\?\>\<\\]//g;
			if ($replace) {
				print "OLD - $file\n";
				print "$line\n";
				$count++;
			}
			
			my $newname = join('/',($path,$line));
			rename($oldname,$newname);
		}
	}
	closedir($dir);
	return 0;
}

sub fix_str {
	my $input_str = $_[0];
	
	$input_str =~ s/\ /\\ /g;
	$input_str =~ s/\(/\\(/g;
	$input_str =~ s/\)/\\)/g;
	return $input_str;
}
