#!/usr/bin/perl

print "Content-type: text/html\n\n";

use Fcntl ':flock';
use CGI;
use XML::LibXML;
use warnings;
use CGI::Carp;
use CGI::Carp qw(fatalsToBrowser);

my $file = "../data/users.xml";
my $parser = XML::LibXML->new();
my $doc = $parser->parse_file($file);
my $root = $doc->getDocumentElement;

my $cgi = new CGI;
my $nickname = $cgi->param('nickname');
my $email = $cgi->param('email');
my $pwd = $cgi->param('pwd');
my $rpwd = $cgi->param('rpwd');
my $js = $cgi->param('js');
my $prec = $cgi->param('prec');

$test = 0;
my $nickname_not_valid = 0;
my $duplicate_user = 0;
my $email_empty = 0;
my $email_incorrect = 0;
my $pwd_empty = 0;
my $pwd_nr = 0;

if ($nickname eq "" || !($nickname =~ /^[a-zA-Z0-9]{2,16}$/)) {
    $nickname_not_valid = 1;
    $test = 1;
}
else {
  $user = $root->findnodes("//user[nickname=\"$nickname\"]");
  if ($user) {
    $duplicate_user = 1;
    $test = 1;
  }
}

if ($email eq "") {
  $email_empty = 1;
  $test = 1;
}
else {
  unless ($email =~ /^[a-zA-Z0-9.-_]+\@[a-zA-Z0-9.-_]+.[a-z]{2,4}$/) {
    $email_incorrect = 1;
    $test = 1;
  }
}

if ($pwd eq "") {
  $pwd_empty = 1;
  $test = 1;
}
elsif ($pwd ne $rpwd) {
  $pwd_nr = 1;
  $test = 1;
}

if ($test==0) {
  ($user,$domain) = split(/\@/,$email);
  $nuovo_el = "  <user admin=\"false\">\n    <nickname>$nickname</nickname>\n    <pwd>$pwd</pwd>\n    <email>$user\@$domain</email>\n  </user>\n\n";
  my $nodo = $parser->parse_balanced_chunk($nuovo_el);
  $root->appendChild($nodo);

  open(OUT, ">$file");
  flock( OUT, LOCK_EX );
  print OUT $doc->toString;
  flock( OUT, LOCK_UN );
  close(OUT);

  if ($js eq 'enabled' and $prec =~ m/tecweb\/~eceron/) {
    if ($prec =~ m/cgi-bin/) {
      ($nope,$redir) = split('cgi-bin/', $prec);
      print "<html><head><meta http-equiv=\"refresh\" content=\"0; url=$redir\"/></head><body></body></html>";
    }
    else {
      print "<html><head><meta http-equiv=\"refresh\" content=\"0; url=index.cgi?page=1\"/></head></html>";
    }
  }
  else {
    print "<html><head><meta http-equiv=\"refresh\" content=\"0; url=index.cgi?page=1\"/></head></html>";
  }

}
else {
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
    <span id="path"><a href="../register.html">Torna indietro</a></span>
  </div>
  <div id="content">
HTML
  print "<strong>Errore</strong><p>Nickname non valido: 2-16 caratteri alfanumerici.</p>\n" if $nickname_not_valid==1;
  print "<strong>Errore</strong><p>Nickname già in uso.</p>\n" if $duplicate_user==1;
  print "<strong>Errore</strong><p>Il campo \"Indirizzo e-mail\" è vuoto.</p>\n" if $email_empty==1;
  print "<strong>Errore</strong><p>Indirizzo e-mail non corretto.</p>\n" if $email_incorrect==1;
  print "<strong>Errore</strong><p>Il campo \"Password\" è vuoto.</p>\n" if $pwd_empty==1;
  print "<strong>Errore</strong><p>La password è troppo corta: minimo 4 caratteri.</p>\n" if length($pwd)<4;
  print "<strong>Errore</strong><p>La password è troppo lunga: massimo 16 caratteri.</p>\n" if length($pwd)>16;
  print "<strong>Errore</strong><p>Le password non corrispondono.</p>\n" if $pwd_nr==1;
  print <<HTML;
    <p><a href="../register.html">Torna indietro</a></p>
  </div>
</body>
</html>
HTML
}

exit;