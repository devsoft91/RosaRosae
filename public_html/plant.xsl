<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'
  doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
  doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/>
<xsl:template match="/plant">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
  <title>Rosa Rosae - <xsl:value-of select="title"/></title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <meta name="description" content="Una scheda tecnica e dettagliata sulla pianta"/>
  <meta name="keywords" content="giardinaggio, botanica, piante, fiori"/>
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
  <script type="text/javascript" src="http://code.jquery.com/jquery-1.5.js"></script>
</head>
<body>
  <div id="navbar">
    <a class="navigationHelp" href="#content">Vai al contenuto</a>
    <span id="logo" title="Rosa Rosae"></span>
    <span id="menuButton" title="Menu" onclick="toggleVisibility('mobileMenu')"></span>
    <div id="mobileMenu">
      <xsl:choose>
        <xsl:when test="$logged='true'">
          <ul id="login">
            <li>Ciao <xsl:value-of select="$name"/></li>
            <li xml:lang="en"><a href="logout.cgi">LOGOUT</a></li>
          </ul>
        </xsl:when>
        <xsl:otherwise>
          <ul id="login">
            <li xml:lang="en"><a href="../login.html">LOGIN</a></li>
            <li><a href="../register.html">REGISTRATI</a></li>
          </ul>
        </xsl:otherwise>
      </xsl:choose>
      <ul id="menu">
        <li xml:lang="en"><a href="index.cgi?page=1">HOME</a></li>
        <li><a href="about.cgi">CONTATTACI</a></li>
      </ul>
    </div>
    <span id="path">Ti trovi in: <span xml:lang="en">Home</span> &gt; <xsl:value-of select="title"/></span>
  </div>
  <div id="content">
    <h1><xsl:value-of select="title"/> <xsl:if test="specs/hiquality"><span title="Alta qualità e affidabilità" id="hiquality"/></xsl:if></h1>
    <p><a href="#comments">Vai ai commenti&#x25BC;</a></p>
    <xsl:element name="img"><xsl:attribute name="src"><xsl:value-of select="img/@src"/></xsl:attribute><xsl:attribute name="alt"><xsl:value-of select="img/@alt"/></xsl:attribute></xsl:element>
    <table summary="La tabella elenca le principali caratteristiche della pianta">
      <tr>
        <th>Famiglia</th>
        <td xml:lang="la"><xsl:value-of select="specs/family"/></td>
      </tr>
      <tr>
        <th title="Altezza massima raggiungibile">Altezza</th>
        <td><xsl:value-of select="specs/height"/></td>
      </tr>
      <tr>
        <th title="Larghezza massima di sviluppo">Diametro</th>
        <td><xsl:value-of select="specs/diameter"/></td>
      </tr>
      <tr>
        <th title="Condizione di luce necessaria per la crescita in salute">Luce</th>
        <td><xsl:value-of select="specs/light"/></td>
      </tr>
      <tr>
        <th title="Condizione del terreno necessaria per lo sviluppo ottimale">Terreno</th>
        <td><xsl:value-of select="specs/terrain"/><xsl:if test="specs/ph"> a pH acido</xsl:if></td>
      </tr>
      <tr>
        <th title="Temperatura minima alla quale può resistere">Temp. min.</th>
        <td><xsl:value-of select="specs/temperature"/><abbr title="Gradi Celsius">°C</abbr></td>
      </tr>
    </table>
    <xsl:for-each select="paragraph">
      <strong><xsl:value-of select="@title"/></strong>
      <p><xsl:value-of select="./text()"/></p>
    </xsl:for-each>
    <p class="contentFooter">Pubblicato il <xsl:variable name="dt" select="date"/><xsl:value-of select="concat(substring($dt, 9, 2),'/',substring($dt, 6, 2),'/',substring($dt, 1, 4))"/> da <xsl:value-of select="author"/> - <a href="#content">Torna su&#x25B2;</a></p>
  </div>
  <div id="comments">
    <h1>Commenti</h1>
    <xsl:choose>
      <xsl:when test="$logged='true'">
        <form action="comment.cgi" method="post">
          <fieldset>
            <label for="comment">Commento</label> (<span id="charNum">150</span> caratteri rimanenti):
            <textarea id="comment" name="commento" cols="30" rows="3" onkeyup="countChar(this);"></textarea>
            <input type="hidden" name="id" value="{$id}"/>
            <input type="submit" value="Pubblica commento"/>
          </fieldset>
        </form>
      </xsl:when>
      <xsl:otherwise>
        <p>Esegui il <a xml:lang="en" href="../login.html">login</a> o <a href="../register.html">registrati</a> per commentare.</p>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="comments/comment">
      <div id="comment">
        <xsl:for-each select="comments/comment[@valid='true']">
          <xsl:sort select="date" order="descending"/>
          <xsl:sort select="time" order="descending"/>
          <strong><xsl:value-of select="user"/></strong>
          <p><xsl:value-of select="text"/></p>
          <p class="contentFooter">Pubblicato il <xsl:variable name="dt" select="date"/><xsl:value-of select="concat(substring($dt, 9, 2),'/',substring($dt, 6, 2),'/',substring($dt, 1, 4))"/> alle <xsl:value-of select="time"/> - <a href="#comments">Torna a inizio commenti&#x25B2;</a></p>
        </xsl:for-each>
      </div>
    </xsl:if>
  </div>
  <div id="footer">
    <span xml:lang="en">Copyright</span> &#xA9; 2014 - Tutti i diritti riservati.
  </div>
</body>
</html>
</xsl:template>
</xsl:stylesheet>