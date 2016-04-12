function toggleVisibility(id) {
  var e = document.getElementById(id);
  if(e.style.visibility == 'visible')
    e.style.visibility = 'hidden';
  else
    e.style.visibility = 'visible';
}

function addtext() {
  var newtext = '<paragraph title=""></paragraph>\n§';
  document.getElementById("addContent").text.value += newtext;
}

function countChar(val) {
  var len = val.value.length;
  if(len > 150)
    val.value = val.value.substring(0,150);
  else
    $('#charNum').text(150-len);
}

function CheckForJavaScript() {   
  document.getElementById("form").js.value = "enabled";
  document.getElementById("form").prec.value = document.referrer;
}