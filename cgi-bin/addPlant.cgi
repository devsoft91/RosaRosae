#!/usr/bin/perl

use Fcntl ':flock';
use CGI;
use CGI::Session;
use XML::LibXML;
use warnings;
use CGI::Carp;
use CGI::Carp qw(fatalsToBrowser);
use File::Basename;
use DateTime;

$session = CGI::Session->load();

if ($session->is_empty || $session->is_expired){
  print "Accesso non autorizzato!";
} else {

  $CGI::POST_MAX = 1024*512;
  my $safe_filename_characters = "a-zA-Z0-9_.-";
  my $upload_dir = "/home/0/2012/eceron/tecweb/public_html/img/";

  my $cgi = new CGI;
  my $filename = $cgi->param("image");

  if (!$filename) {
    print $cgi->header();
    print "C'\&egrave; stato un problema nel caricamento dell'immagine!";
    exit;
  }

  my ($name, $path, $extension) = fileparse ($filename, '..*');
  $filename = $name . $extension;
  $filename =~ tr/ /_/;
  $filename =~ s/[^$safe_filename_characters]//g;

  if ($filename =~ /^([$safe_filename_characters]+)$/) {
    $filename = $1;
  } else {
    die "Il nome del file contiene caratteri non validi.";
  }

  my $upload_filehandle = $cgi->upload("image");

  open (UPLOADFILE, ">$upload_dir/$filename") or die "$!";
  binmode UPLOADFILE;

  while (<$upload_filehandle>) {
    print UPLOADFILE;
  }

  close UPLOADFILE;

  my $file = "../data/plants.xml";
  my $parser = XML::LibXML->new();
  my $doc = $parser->parse_file($file);
  my $root = $doc->getDocumentElement;
  my @plants = $root->findnodes("//plant");
  my $num_plants = @plants;
  my $id = $num_plants+1;
  $nuova_pianta = "  <plant id=\"$id\">\n";

  my $dt = DateTime->now;   
  my $date = $dt->ymd;
  $nuova_pianta = $nuova_pianta."    <date>$date</date>\n";

  $session_name = $session->param("my_name");
  $nuova_pianta = $nuova_pianta."    <author>$session_name</author>\n";

  $title=$cgi->param('title');
  $title =~ tr/+/ /;
  $title =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $nuova_pianta=$nuova_pianta."    <title>$title</title>\n";
  
  $alt = $cgi->param('alternative');
  $alt =~ tr/+/ /;
  $alt =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $nuova_pianta = $nuova_pianta."    <img src=\"../img/$filename\" alt=\"$alt\"/>\n";

  $nuova_pianta = $nuova_pianta."    <specs>\n";
  $family = $cgi->param('family');
  $height = $cgi->param('height');
  $diameter = $cgi->param('diameter');
  $light = $cgi->param('light');
  $terrain = $cgi->param('terrain');
  $temperature = $cgi->param('temperature');
  $ph = $cgi->param('ph');
  $hiquality = $cgi->param('hiquality');
  $nuova_pianta = $nuova_pianta."      <family>$family</family>\n      <height>$height</height>\n      <diameter>$diameter</diameter>\n      <light>$light</light>\n      <terrain>$terrain</terrain>\n      <temperature>$temperature</temperature>\n";
  if ($ph ne "") {
    $nuova_pianta = $nuova_pianta."      <ph/>\n";
  }
  if ($hiquality ne "") {
    $nuova_pianta = $nuova_pianta."      <hiquality/>\n";
  }
  $nuova_pianta = $nuova_pianta."    </specs>\n";

  $description = $cgi->param('description');
  $description =~ tr/+/ /;
  $description =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $nuova_pianta = $nuova_pianta."    <description>$description</description>\n";

  $text = $cgi->param ('text');
  $text =~ tr/+/ /;
  $text =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  @array = split(/§/, $text);
  $lung=@array;
  for ($i=0; $i<$lung; $i++) {
    $nuova_pianta = $nuova_pianta."    @array[$i]";
  }

  $nuova_pianta = $nuova_pianta."    <comments>\n    </comments>\n";

  $nuova_pianta = $nuova_pianta."  </plant>\n\n";

  my $nuovo_nodo = $parser->parse_balanced_chunk($nuova_pianta);
  $root->appendChild($nuovo_nodo);

  open(OUT, ">$file");
  flock( OUT, LOCK_EX );
  print OUT $doc->toString;
  flock( OUT, LOCK_UN );
  close(OUT);
  
  print "Content-type: text/html\n\n";
  print "<html><head><meta http-equiv=\"refresh\" content=\"0; url=showpage.cgi?plant=$id\"/></head></html>";
}

exit;
