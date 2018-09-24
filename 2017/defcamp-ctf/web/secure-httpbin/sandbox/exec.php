<?php

require 'config.php';

function check_signature($payload, $signature) {
    $signatureok = md5(SECRET . $payload);
    return $signature === $signatureok;
}

function check_params($method, $url, $data) {

    $alllowed_methods = ['GET', 'POST', 'HEAD', 'PUT', 'PATCH', 'OPTIONS', 'DELETE'];

    if (!in_array($method, $alllowed_methods)) {
        throw new Exception('Method not allowed');
    }

    $filter_flags = FILTER_FLAG_SCHEME_REQUIRED | FILTER_FLAG_HOST_REQUIRED | FILTER_FLAG_PATH_REQUIRED;

    if (filter_var($url, FILTER_VALIDATE_URL, $filter_flags) === false) {
        var_dump($url);
        throw new Exception('Invalid URL specified');
    }

    $parsed = parse_url($url);

    if (strtolower($parsed['scheme']) === 'file') {
        throw new Exception('FILE protocol not allowed');
    }

    $ip    = gethostbyname($parsed['host']);
    $flags = FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE;

    if (filter_var($ip, FILTER_VALIDATE_IP, $flags) === false) {
        echo $ip;
        throw new Exception('Invalid URL: IP range not allowed');
    }

    // let the dns record expire if TTL is set to 1
    sleep(1);
}

function execute_request($method, $url, $data) {

    $options = [
        CURLOPT_URL            => $url,
        CURLOPT_HEADER         => true,
        CURLOPT_VERBOSE        => true,
        CURLOPT_CONNECTTIMEOUT => 5,
        CURLOPT_TIMEOUT        => 5,
        CURLOPT_STDERR         => fopen('php://stdout', 'w'),
    ];

    if ($data) {
        $options[CURLOPT_POSTFIELDS] = $data;
    }

    if (strtolower($method) !== 'get') {
        $options[CURLOPT_CUSTOMREQUEST] = $method;
    }

    $curl = curl_init();
    curl_setopt_array($curl, $options);
    curl_exec($curl);

    return (bool)curl_errno($curl);
}

$payload   = $_POST['payload'];
$signature = $_POST['signature'] ?? false;

try {

    $level = error_reporting(E_ALL);
    ini_set('display_errors', 0);
    error_log('Payload: ' . $payload);
    error_log('Signature: ' . $signature);
    ini_set('display_errors', 1);
    error_reporting($level);

    if (!check_signature($payload, $signature)) {
        throw new Exception('Invalid signature');
    }

    parse_str($payload, $extracted);

    $method = $extracted['method'] ?? 'GET';
    $url    = $extracted['url'] ?? '';
    $data   = $extracted['data'] ?? '';

    check_params($method, $url, $data);

} catch (Exception $ex) {
    die('Error: ' . $ex->getMessage());
}

ob_start();
$status = execute_request($method, $url, $data);
$output = ob_get_clean();

if (!isset($_GET['nolog'])) {
    include 'redis-config.php';

    $redis = new Redis();
    $redis->connect($redis_host);
    $redis->set('log_request_' . uniqid(), http_build_query([
        'method' => $method,
        'url'    => $url,
        'data'   => $data,
    ]));
}

?>