<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

$file = basename($_REQUEST['action'] ?? '') . '.php';
if ($file != 'index.php') {
    include $file;
}
