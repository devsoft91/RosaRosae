#!/usr/bin/perl

use Fcntl ':flock';
use XML::LibXML;
use CGI::Session;
use CGI;
use DateTime;
use warnings;
use CGI::Carp;
use CGI::Carp qw(fatalsToBrowser);

my $file = "../data/plants.xml";
my $parser = XML::LibXML->new();
my $doc = $parser->parse_file($file);
my $root = $doc->getDocumentElement;

my $cgi = CGI->new();
$text = $cgi->param ('commento');
$value = $cgi->param ('id');

print "Content-type: text/html\n\n";

$text =~ tr/+/ /;
$text =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

$session = CGI::Session->load();

if ($session->is_empty || $session->is_expired) {
	print "<html><head><meta http-equiv=\"refresh\" content=\"2; url=showpage.cgi?plant=$value#comments\"/><title>Errore</title></head><body><h1>Errore</h1>Devi effettuare il login per commentare</body></html>";
} else {
	if (length($text)<151 and length($text)>0) {
		$node = $root->findnodes("//plant[\@id=\"$value\"]/comments")->get_node(1);
		
		$session_name = $session->param("my_name");
		my $dt   = DateTime->now;   
		my $date = $dt->ymd;
		my $time = $dt->hms;

		$nuovo_comm = "      <comment valid=\"true\">\n        <date>$date</date>\n        <time>$time</time>\n        <user>$session_name</user>\n        <text>$text</text>\n      </comment>\n";

		my $nuovo_nodo = $parser->parse_balanced_chunk($nuovo_comm);
		$node->appendChild($nuovo_nodo);

		open(OUT, ">$file");
    flock( OUT, LOCK_EX );
		print OUT $doc->toString;
    flock ( OUT, LOCK_UN );
		close(OUT);

	  print "<html><head><meta http-equiv=\"refresh\" content=\"0; url=showpage.cgi?plant=$value#comments\"/><title>Ok</title></head><body></body></html>";
  } else {
	  print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
<head>
  <title>Rosa Rosae - Errore</title>
  <!-- PAGINA NON INDICIZZATA -->
  <meta name="robots" content="noindex, nofollow"/>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <meta name="title" content="Errore durante la registrazione"/>
  <meta name="author" content="Giacomo Beltrame, Enrico Ceron"/>
  <meta name="language" content="italian it"/>
  <meta name="viewport" content="width=device-width, user-scalable=no"/>
  <meta http-equiv="Content-Script-Type" content="text/javascript"/>
  <link rel="icon" href="../favicon.ico" type="image/ico"/>
  <link href='http://fonts.googleapis.com/css?family=Roboto+Slab:300' rel='stylesheet' type='text/css'/>
  <link href="../stylesheets/mobile.css" rel="stylesheet" type="text/css" media="screen and (max-device-width: 899px)"/>
  <link href="../stylesheets/desktop.css" rel="stylesheet" type="text/css" media="screen and (min-device-width: 900px)"/>
  <link href="../stylesheets/print.css" rel="stylesheet" type="text/css" media="print"/>
  <script type="text/javascript" src="../script/script.js"></script>
</head>
<body>
  <div id="navbar">
    <a class="navigationHelp" href="#content">Vai al contenuto</a>
    <span id="logo" title="Rosa Rosae"></span>
    <span id="menuButton" title="Menu" onclick="toggleVisibility('mobileMenu')"></span>
    <div id="mobileMenu">
      <ul id="menu">
        <li><a href="index.cgi?page=1">HOME</a></li>
        <li><a href="about.cgi">CONTATTACI</a></li>
      </ul>
      <ul id="login">
        <li><a href="../login.html">LOGIN</a></li>
        <li><a href="../register.html">REGISTRATI</a></li>
      </ul>
    </div>
    <span id="path"><a href="showpage.cgi?plant=$value#comments">Torna indietro</a></span>
  </div>
  <div id="content">
HTML
    print "<strong>Errore</strong><p>Il commento è vuoto. Scrivi qualcosa nell'apposito riquadro per commentare</p>\n" if length($text)<1;
    print "<strong>Errore</strong><p>Il commento supera i 150 caratteri.</p>\n" if length($text)>150;
  print <<HTML;
  <p><a href="showpage.cgi?plant=$value">Torna indietro</a></p>
  </div>
</body>
</html>
HTML
	}
}

exit;