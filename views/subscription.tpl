<html>
<head>
<style>
#wpe {
	border: 4px solid #652366;
	background: #2f5acc;
	color: rgba(28, 176, 176, 1);
	margin: auto;
	width: 40%;
	padding: 20px;
	font-family: monospace, sans-serif;
}

label, input, select {
	width: 50%;
	padding: 5px;
}
</style>
</head>
  <body>
  <div id='wpe'>
  <h1 align='center'>Weather Powered Email</h1>
  <hr color = '#336633'>
  <form action="/confirm" method="post" align='center'>
  <label for="email_input">Email Address</label><br />
  <input type="email" name="email_input" value="" required /><br /><br />
  <label for="location_input">Location</label><br />
  <select name="location" required>
	% for loc in rows:
		<option>{{ loc }}</option>
	% end
  </select><br /><br />

  <input type="submit" value="Subscribe" />
  </form>
  </div>
  </body>
</html>