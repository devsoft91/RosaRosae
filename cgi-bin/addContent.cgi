#!/usr/bin/perl

print "Content-type: text/html\n\n";

use XML::LibXML;
use CGI;
use CGI::Session;
use warnings;
use CGI::Carp qw(fatalsToBrowser);

$session = CGI::Session->load();

if ($session->is_empty || $session->is_expired) {
  noadmin();
} else {
  my $file = "../data/users.xml";
  my $parser = XML::LibXML->new();
  my $doc = $parser->parse_file($file);
  my $root = $doc->getDocumentElement;
  $session_name = $session->param("my_name");
  $user_node = $root->findnodes("//user[nickname=\"$session_name\"]")->get_node(1);
  if ($user_node->getAttribute("admin") eq "true") {
    print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
<head>
  <title>Rosa Rosae - Crea contenuto</title>
  <!-- PAGINA NON INDICIZZATA -->
  <meta name="robots" content="noindex, nofollow"/>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <meta name="title" content="Crea contenuto"/>
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
      <ul id="login">
        <li>Ciao $session_name</li>
        <li xml:lang="en"><a href="logout.cgi">LOGOUT</a></li>
        <li>CREA CONTENUTO</li>
      </ul>
      <ul id="menu">
        <li xml:lang="en"><a href="index.cgi?page=1">HOME</a></li>
        <li><a href="about.cgi">CONTATTACI</a></li>
        <li>
      </ul>
    </div>
    <span id="path">Ti trovi in: Crea contenuto (amministrazione)</span>
  </div>
  <div id="content">
    <h1>Creazione contenuto</h1>
    <form id="addContent" action="addPlant.cgi" method="post" enctype="multipart/form-data">
      <fieldset>
        <label for="title">Titolo:</label><br/>
        <input type="text" name="title" id="title"/><br/>
        <label for="image"><span xml:lang="en">Upload</span> immagine (massimo 500<abbr xml:lang="en" title="kilobyte">Kb</abbr>):</label><br/>
        <input type="file" name="image" id="image"/><br/>
        <label for="alt">Alternativa all'immagine:</label><br/>
        <input type="text" name="alternative" id="alt"/><br/>
        <fieldset>
          <input type="checkbox" name="hiquality" id="hiquality" value="hq"/>
          <label for="hiquality">Alta qualità e affidabilità</label><br/>
          <label for="family">Famiglia:</label><br/>
          <input type="text" name="family" id="family"/><br/>
          <label for="height">Altezza (inserire unità di misura):</label><br/>
          <input type="text" name="height" id="height"/><br/>
          <label for="diameter">Diametro (inserire unità di misura):</label><br/>
          <input type="text" name="diameter" id="diameter"/><br/>
          <label for="light">Luce:</label><br/>
            <select name="light" id="light">
              <option value="soleggiato">soleggiato</option>
              <option value="penombra">penombra</option>
              <option value="ombra">ombra</option>
            </select><br/>
          <label for="terrain">Terreno:</label><br/>
            <select name="terrain" id="terrain">
              <option value="asciutto">asciutto</option>
              <option value="umido">umido</option>
              <option value="bagnato">bagnato</option>
            </select>
          <input type="checkbox" name="ph" id="ph" value="ph"/>
          <label for="ph">pH acido</label><br/>
          <label for="temperature"><abbr title="Temperatura minima">Temp. min.</abbr>:</label><br/>
            <select name="temperature" id="temperature">
              <option value="0">0°C</option>
              <option value="-5">-5°C</option>
              <option value="-15">-15°C</option>
            </select><br/>
        </fieldset>
        <label for="description">Descrizione:</label><br/>
        <textarea name="description" id="description" cols="30" rows="3"></textarea><br/>
        <label for="text">Testo:</label><br/>
        <textarea name="text" id="text" cols="35" rows="4"></textarea><br/>
        <input type="button" value="Aggiungi Paragrafo" onClick="addtext();"><br/>
        <input type="submit" value="Pubblica"/><br/>
      </fieldset>
    </form>
  </div>
  <div id="footer">
    <span xml:lang="en">Copyright</span> &#xA9; 2014 - Tutti i diritti riservati.
  </div>
</body>
</html>
HTML
  } else {
    noadmin();
  }
}

sub noadmin {
  print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
<head>
  <title>Rosa Rosae - Errore</title>
  <!-- PAGINA NON INDICIZZATA -->
  <meta name="robots" content="noindex, nofollow"/>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <meta http-equiv=\"refresh\" content=\"4; url=index.cgi?page=1\"/>
  <meta name="title" content="Errore - Area Riservata"/>
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
  </div>
  <div id="content">
    <strong>Errore</strong>
    <p>Non hai i privilegi necessari per poter accedere a questa pagina.</p>
    <p>Reindirizzamento alla Home Page in corso...</p>
  </div>
</body>
</html>
HTML
}

exit;
