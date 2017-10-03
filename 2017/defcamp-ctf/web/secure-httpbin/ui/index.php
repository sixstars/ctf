<?php

require 'config.php';

function check($method, $url, $data) {

    $filter_flags = FILTER_FLAG_SCHEME_REQUIRED | FILTER_FLAG_HOST_REQUIRED | FILTER_FLAG_PATH_REQUIRED;

    if (filter_var($url, FILTER_VALIDATE_URL, $filter_flags) === false) {
        throw new Exception('Invalid URL specified');
    }

    $parsed = parse_url($url);

    if (!preg_match('/^https?$/i', $parsed['scheme'])) {
        throw new Exception('Only HTTP/HTTPS allowed.');
    }
}

function sign($method, $url, $data) {
    $params = [
        'method' => $method,
        'url'    => $url,
        'data'   => $data,
    ];

    foreach ($params as $name => $param) {
        if (!is_string($param)) {
            throw new Exception("$name is expected to be a string");
        }
    }

    $payload = http_build_query($params);
    $message = SECRET . $payload;

    return [
        'payload'   => $payload,
        'signature' => md5($message),
    ];
}

$submitted = $_POST['submit'] ?? false;
$method    = $_POST['method'] ?? 'GET';
$url       = $_POST['url'] ?? false;
$data      = $_POST['data'] ?? '';
$error     = false;
$signature = false;

try {

    if ($submitted) {
        check($method, $url, $data);
        $signed = sign($method, $url, $data);
        include 'redirect.php';
        exit;
    }

} catch (Exception $ex) {
    $error = $ex->getMessage();
}

include 'view.php';