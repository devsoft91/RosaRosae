#!/usr/bin/perl

print "Content-type: text/html\n\n";

use CGI::Session;
use CGI;
use warnings;
use CGI::Carp;
use CGI::Carp qw(fatalsToBrowser);

$session = CGI::Session->load();

$session->close();
$session->delete();
$session->flush();

print "<html><head><meta http-equiv=\"refresh\" content=\"0; url=index.cgi?page=1\"/></head></html>";

exit;
