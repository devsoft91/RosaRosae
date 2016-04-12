#!/usr/bin/perl

use XML::LibXML;
use CGI;
use CGI::Session;
use warnings;
use CGI::Carp;
use CGI::Carp qw(fatalsToBrowser);

my $file = "../data/users.xml";
my $parser = XML::LibXML->new();
my $doc = $parser->parse_file($file);
my $root = $doc->getDocumentElement;


my $cgi = new CGI;
my $nickname = $cgi->param('nickname');
my $pwd = $cgi->param('pwd');
my $js = $cgi->param('js');
my $prec = $cgi->param('prec');

# controllo che ci sia nickname
$user = $root->findnodes("//user[nickname=\"$nickname\" and pwd=\"$pwd\"]");

if ($user) {
  $cgi = new CGI;
  $session = new CGI::Session("driver:File", $cgi, {Directory=>'/tmp'});
  $session->expire(1800);
  $id = $session->id();
  $session->param("my_name", $nickname);
  $session->param("reload", "true");

  $cookie = $cgi->cookie(CGISESSID => $session->id);
  print $cgi->header( -cookie=>$cookie );
}
else {
  print "Content-type:text/html\n\n";
	print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
<head>
  <title>Rosa Rosae - Errore</title>
  <!-- PAGINA NON INDICIZZATA -->
  <meta name="robots" content="noindex, nofollow"/>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <meta name="title" content="Errore durante l'accesso"/>
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
    <span id="path"><a href="../login.html">Torna indietro</a></span>
  </div>
  <div id="content">
    <strong>Errore</strong>
    <p>Nome utente o password errate.</p>
    <p><a href="../login.html">Torna indietro</a></p>
  </div>
</body>
</html>
HTML
}

if ($user) {
  if ($js eq 'enabled' and $prec =~ m/tecweb\/~eceron/) {
    if ($prec =~ m/cgi-bin/) {
      ($nope,$redir) = split('cgi-bin/', $prec);
      print "<html><head><meta http-equiv=\"refresh\" content=\"0; url=$redir\" /></head><body></body></html>";
    }
    else {
      print "<html><head><meta http-equiv=\"refresh\" content=\"0; url=index.cgi?page=1\"/></head></html>";
    }
  }
  else {
    print "<html><head><meta http-equiv=\"refresh\" content=\"0; url=index.cgi?page=1\"/></head></html>";
  }
}

exit;
