<html>
<head>
  <title>Secure HTTPbin</title>
  <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>
<body>

  <div class="container">

    <div class="row">
      <div class="col-sm-12 text-center">
        <img style="display: inline-block;" src="<?php echo SANDBOX_URL ?>logo-upload.png" alt="secure httpbin logo">
        <p>
          <strong>Test and debug<sup>*</sup> your webserver with ease!</strong>
        </p>
      </div>
    </div>

    <br><br>

    <?php if(@$error): ?>
      <div class="row">
        <div class="col-sm-12">
          <div class="alert alert-warning">
            <strong>Warning!</strong><br>
            <span><?php echo htmlentities($error); ?></span>
          </div>
        </div>
      </div>
      <br><br>
    <?php endif; ?>

    <div class="row">
      <div class="col-sm-8 col-sm-offset-2">

        <form method="POST">

          <div class="form-group">
            <label for="method">Method</label>
            <select name="method" class="form-control" id="method" autofocus>
              <option value="GET">GET</option>
              <option value="POST">POST</option>
            </select>
          </div>

          <div class="form-group">
            <label for="url">URL</label>
            <input type="url" name="url" class="form-control" id="url" placeholder="URL">
          </div>

          <div class="form-group">
            <label for="data">Data</label>
            <textarea name="data" id="data" class="form-control" rows="10" placeholder="Data (optional)"></textarea>
          </div>

          <button class="btn btn-primary btn-block btn-lg" name="submit" value="yes" type="submit">Submit</button>

        </form>

        <br><br><br><br>

        <small style="display: block; font-size: 10px; line-height: 15px;">
          *
          <span>Please do not submit any passwords/secrets as we do not guarantee their privacy.</span><br>
          <!--
          <span>We had other clients submitting their secrets and they sued us for breaching their security. We were not guilty but since we don't want this to happen again - we are not liable for any submitted secrets.</span><br>
          <span>By using this service you allow to our terms and conditions and agree that your data to be logged.</span><br>
          -->
          <!-- Note: Mark from Legal adviced to remove these ^ and temporarily stop logging until further clarification. -Tom -->
        </small>

      </div>
    </div>
  </div>

</body>
</html>