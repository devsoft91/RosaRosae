#!/usr/bin/perl

print "Content-type: text/html\n\n";

#use XML::LibXSLT;
use XML::LibXML;
use CGI::Session;
#use CGI;
use warnings;
use CGI::Carp;
use CGI::Carp qw(fatalsToBrowser);

$session = CGI::Session->load();

print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
<head>
  <title>Rosa Rosae - Contattaci</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <meta name="title" content="Contattaci"/>
  <meta name="description" content="Le informazioni per contattare gli amministratori"/>
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
HTML

if ($session->is_empty || $session->is_expired) {
  print <<HTML;
      <ul id="login">
        <li xml:lang="en"><a href="../login.html">LOGIN</a></li>
        <li><a href="../register.html">REGISTRATI</a></li>
      </ul>
HTML
} else {
  my $file = "../data/users.xml";
  my $parser = XML::LibXML->new();
  my $doc = $parser->parse_file($file);
  my $root = $doc->getDocumentElement;
  $session_name = $session->param("my_name");
  $user_node = $root->findnodes("//user[nickname=\"$session_name\"]")->get_node(1);
  print <<HTML;
      <ul id="login">
        <li>Ciao $session_name</li>
        <li xml:lang="en"><a href="logout.cgi">LOGOUT</a></li>
HTML
  if ($user_node->getAttribute("admin") eq "true") {
    print "<li><a href=\"addContent.cgi\">CREA CONTENUTO</a></li>\n";
  }
  print "      </ul>\n";
}
print <<HTML;
      <ul id="menu">
        <li xml:lang="en"><a href="index.cgi?page=1">HOME</a></li>
        <li>CONTATTACI</li>
      </ul>
    </div>
    <span id="path">Ti trovi in: Contattaci</span>
  </div>
  <div id="content">
    <h1>Contattaci</h1>
    <p>Giacomo Beltrame, Enrico Ceron</p>
    <p>via Luigi Luzzatti, 35121 Padova <abbr title="Italia">IT</abbr></p>
    <p><abbr title="Numero di telefono">tel.</abbr>: 0123 456789</p>
    <p><a href="mailto:info\@rosarosae.it">info\@rosarosae.it</a></p>
  </div>
  <div id="footer">
    <span xml:lang="en">Copyright</span> &#xA9; 2014 - Tutti i diritti riservati.
  </div>
</body>
</html>
HTML

exit;
