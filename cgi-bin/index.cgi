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
$hash{"logged"} = "'false'";

if ($session->is_empty || $session->is_expired) {
	$style_doc = XML::LibXML->load_xml(location => '../public_html/index.xsl', no_cdata=>1);
}
else {
	my $file = "../data/users.xml";
	my $parser = XML::LibXML->new();
	my $doc = $parser->parse_file($file);
	my $root = $doc->getDocumentElement;
	$session_name = $session->param("my_name");
  $hash{"logged"} = "'true'";
  $hash{"name"} = "'$session_name'";
	$user_node = $root->findnodes("//user[nickname=\"$session_name\"]")->get_node(1);
	if ($user_node->getAttribute("admin") eq "true") {
		$style_doc = XML::LibXML->load_xml(location => '../public_html/admin_index.xsl', no_cdata=>1);
	} else {
		$style_doc = XML::LibXML->load_xml(location => '../public_html/index.xsl', no_cdata=>1);
	}
}

my $source = XML::LibXML->load_xml(location => '../data/plants.xml');

my $source1 = XML::LibXML->load_xml(location => '../data/empty_plants.xml');

my $cgi = CGI->new();
$page = $cgi->param ('page');
$lgap = $page-1;
$hgap = $page+1;
$hash{page} = $page;
$hash{prec} = $lgap;
$hash{succ} = $hgap;
#%hash = (prec => $lgap, succ => $hgap);
$page--;

$element_per_page=3;
@nodi = $source->findnodes("//plant");
$lung = @nodi;
$fetch = $lung-($element_per_page*$page);
$pagine = $lung/$element_per_page;

if ($lung%$element_per_page>0) {
	$resto = $lung%$element_per_page;
	$resto_dec = $resto/$element_per_page;
	$pagine -= $resto_dec;
	$pagine += 1;
}
$hash{ultima} = $pagine;

$radice = $source->getDocumentElement;
$radice1 = $source1->getDocumentElement;

#$fetch=3;
for ($i=0;$i<$element_per_page;$i++) {
	if ($fetch>0) {
		my $node = $source->findnodes("//plant")->get_node($fetch);
		$radice1->appendChild($node);
		$fetch--;
	}
}

$source1->setDocumentElement($radice1);

my $stylesheet = $xslt->parse_stylesheet($style_doc);

my $results = $stylesheet->transform($source1,%hash);

print $stylesheet->output_as_bytes($results);

exit;
