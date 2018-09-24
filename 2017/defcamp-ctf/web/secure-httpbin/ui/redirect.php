<!DOCTYPE html>
<html>
<head>
    <title>Redirecting to the sandbox...</title>
    <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <style>
        input[type=submit] { display: block; margin: 10px auto; width: 300px; }
    </style>
</head>
<body>

    <?php $params = ['payload', 'signature'];?>

    <form id="autopost" action="<?php echo SANDBOX_URL; ?>?nolog" method="POST">
        <? $signature = md5(SECRET . http_build_query($params)); ?>
        <input type="hidden" name="payload" value="<?php echo htmlentities($signed['payload']); ?>">
        <input type="hidden" name="signature" value="<?php echo htmlentities($signed['signature']); ?>">
        <input type="hidden" name="action" value="exec">
        <input type="submit" class="btn btn-sm btn-primary" value="click here if you are not redirected automatically...">
    </form>

    <script>
      document.getElementById('autopost').submit();
    </script>

</body>
</html>