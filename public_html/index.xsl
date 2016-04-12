<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'
  doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
  doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/>
<xsl:template match="/">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
  <title>Rosa Rosae - Home</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <meta name="title" content="Rosa Rosae"/>
  <meta name="description" content="Qui puoi trovare informazioni riguardanti il giardinaggio e la botanica"/>
  <meta name="keywords" content="giardinaggio, botanica, piante, fiori"/>
  <meta name="author" content="Giacomo Beltrame, Enrico Ceron"/>
  <meta name="language" content="italian it"/>
  <meta name="viewport" content="width=device-width, user-scalable=no"/>
  <meta http-equiv="Content-Script-Type" content="text/javascript"/>
  <link rel="icon" href="../favicon.ico" type="image/ico"/>
  <link href='http://fonts.googleapis.com/css?family=Roboto+Slab:300' rel='stylesheet' type='text/css'/>
  <link href="../stylesheets/mobile.css" rel="stylesheet" type="text/css" media="screen and (max-device-width: 899px)"/>
  <link href="../stylesheets/home.css" rel="stylesheet" type="text/css" media="screen and (min-device-width: 900px)"/>
  <link href="../stylesheets/print.css" rel="stylesheet" type="text/css" media="print"/>
  <script type="text/javascript" src="../script/script.js"></script>
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
        <li xml:lang="en">HOME</li>
        <li><a href="about.cgi">CONTATTACI</a></li>
      </ul>
    </div>
    <span id="path">Ti trovi in: <span xml:lang="en">Home</span></span>
  </div>
  <div id="content">
    <xsl:for-each select="//plant">
      <xsl:variable name="id" select="@id"/>
      <div class="tile">
        <h1><a href="showpage.cgi?plant={$id}"><xsl:value-of select="title"/></a></h1>
        <xsl:element name="img"><xsl:attribute name="src"><xsl:value-of select="img/@src"/></xsl:attribute><xsl:attribute name="alt"><xsl:value-of select="img/@alt"/></xsl:attribute></xsl:element>
        <p><xsl:value-of select="description"/></p>
        <p class="contentFooter">Pubblicato il <xsl:variable name="dt" select="date"/><xsl:value-of select="concat(substring($dt, 9, 2),'/',substring($dt, 6, 2),'/',substring($dt, 1, 4))"/> da <xsl:value-of select="author"/></p>
      </div>
    </xsl:for-each>
  </div>
  <div id="pagesNav">
    <p>Pagina <xsl:value-of select="$page"/></p>
    <xsl:choose>
      <xsl:when test="$page='1'">
        Inizio
      </xsl:when>
      <xsl:otherwise>
        <a href="index.cgi?page=1">Inizio</a>
      </xsl:otherwise>
    </xsl:choose> | 
    <xsl:choose>
      <xsl:when test="$prec='0'">
        Precedente
      </xsl:when>
      <xsl:otherwise>
        <a href="index.cgi?page={$prec}">Precedente</a>
      </xsl:otherwise>
    </xsl:choose> | 
    <xsl:choose>
      <xsl:when test="//plant[last()]/@id &gt; '1'">
        <a href="index.cgi?page={$succ}">Successiva</a> | <a href="index.cgi?page={$ultima}">Fine</a>
      </xsl:when>
      <xsl:otherwise>
        Successiva | Fine
      </xsl:otherwise>
    </xsl:choose>
  </div>
  <div id="footer">
    <span xml:lang="en">Copyright</span> &#xA9; 2014 - Tutti i diritti riservati.
  </div>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
