<?php require_once('Connections/connSDB.php'); ?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Sample</title>
<link href="maincs.css" rel="stylesheet" type="text/css" />
</head>
<body>

</body>
</html>

<?php require_once('../footer.php');?>
<p></p>

<?php
mysql_free_result($rsNews);
mysql_free_result($rsEvents);
mysql_free_result($rsEcat);
mysql_free_result($rsFront);
mysql_free_result($rsAbout);
?>
