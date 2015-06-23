#!/usr/bin/env perl

use strict;
use warnings;
use File::Copy::Recursive qw{rcopy};

my $stored_dir = "/media/Локальный диск/GAMES/wh/wh_ehd6_f/m/";
my $main_dir = "";

my @main_dirs = (
'/media/Index/m/'
# '/media/Index/a/',
# '/media/Reserve/a/',
# '/media/INDEX/a/',
# '/media/temp_/Other/',
# '/media/temp/'
);

foreach my $i (@main_dirs) {
	&process_dir($i);
}
print "DONE";

sub process_dir {
	my $dir = $_[0];
	
	opendir(my $dir_handler,$dir);
	while (my $item = readdir($dir_handler)) {
		if ($item !~ /^(\.|\.\.)$/) {
			my $dir_path = join('/',($dir,$item));
			if (-d($dir_path)) {
				&search_res($dir_path,$item);
			}
		}
	}
	
	closedir($dir_handler);
}

sub search_res {
	my $title_dir_path = $_[0];
	my $title_dir = $_[1];
	
	opendir(my $dir_handler,$title_dir_path);
	while (my $item = readdir($dir_handler)) {
		if ($item !~ /^(\.|\.\.)$/) {
			my $dir_path = join('/',($title_dir_path,$item));
			if ((-d($dir_path)) && ($item =~ /^wh$/)) {
				my $new_title_dir_path = join('/',($stored_dir,$title_dir,$item));
				mkdir($new_title_dir_path);
				rcopy($dir_path,$new_title_dir_path);
				print "$title_dir\tDONE\n";
			}
		}
	}
	
	closedir($dir_handler);
}
