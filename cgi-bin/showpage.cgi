#!/usr/bin/perl

print "Content-type: text/html\n\n";

use XML::LibXSLT;
use XML::LibXML;
use CGI::Session;
use CGI;
use warnings;
use CGI::Carp;
use CGI::Carp qw(fatalsToBrowser);

my $xslt = XML::LibXSLT->new();

$session = CGI::Session->load();
$hash{"logged"}= "'false'";

if ($session->is_empty || $session->is_expired) {
  $style_doc = XML::LibXML->load_xml(location => '../public_html/plant.xsl', no_cdata=>1);
}
else {
  my $file = "../data/users.xml";
  my $parser = XML::LibXML->new();
  my $doc = $parser->parse_file($file);
  my $root = $doc->getDocumentElement;
  $session_name = $session->param("my_name");

  $hash{"logged"}= "'true'";
  $hash{"name"}="'$session_name'";

  $user_node=$root->findnodes("//user[nickname=\"$session_name\"]")->get_node(1);

  if ($user_node->getAttribute("admin") eq "true") {
    $style_doc = XML::LibXML->load_xml(location => '../public_html/admin_plant.xsl', no_cdata=>1);
  } else {
    $style_doc = XML::LibXML->load_xml(location => '../public_html/plant.xsl', no_cdata=>1);
  }
}

my $source = XML::LibXML->load_xml(location => '../data/plants.xml');

my $cgi = CGI->new();
$param = $cgi->param('plant');

my $node = $source->findnodes("//plant[\@id=$param]")->get_node(1);
$hash{"id"} = "'$param'";

my $stylesheet = $xslt->parse_stylesheet($style_doc);

$source->setDocumentElement($node);

my $results = $stylesheet->transform($source,%hash);

print $stylesheet->output_as_bytes($results);

exit;
