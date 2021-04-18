<?php
	$servername = "localhost";
	$username = "root";
	$password = "";
	$sSql = "select * from captures;";

	// Create connection
	$conn = mysqli_connect($servername, $username, $password,"vehicles");

	// Check connection
	if (!$conn) {
		die("Connection failed: " . mysqli_connect_error());
		echo "connection failed";
	}

	$result = mysqli_query($conn, $sSql);
	echo "<html>
	<head>
	<link rel='stylesheet' type='text/css' href='view.css' media='all'>
		<script language='JavaScript'>
			function ShowHide(ID) {
				var x = document.getElementById(ID);
				if (x.style.visibility === 'hidden') {
					x.style.visibility = 'visible';
				} else {
					x.style.visibility = 'hidden';
				}
			}
			function ShowForm(UID) {
				var x = document.getElementById('form_container');
				if (x.style.display === 'none') {
					x.style.display = 'block';
					setTimeout(setID(UID), 1000);
				} else {
					x.style.display = 'none';
				}
			}
			function setID(UID){
				document.getElementById('UID').value = UID;
			}
		</script>
	</head>
	<body>
		<h2>LOSERS</h2>
		<div id='form_container' style='display:none;'>
			<h1><a>Update Vehicle Record</a></h1>
			<form class='update'  method='post' action='updateDB.php'>
				<div class='form_description'>
					<h2>Update Vehicle Record</h2>
					<p>Fill out all fields you'd like to update. Then click 'Submit'!</p>
				</div>						
				<ul>
					<li id='li_0' style='display:none;'>
						<input name='UID' id='UID' class='element text medium' maxlength='255' style='display:none;'/> 
					</li>
					<li id='li_1'>
						<label class='description' for='plate'>Plate Value </label>
						<div>
							<input name='plate' class='element text medium' type='text' maxlength='255'/> 
						</div> 
					</li>
					<li id='li_2'>
						<label class='description' for='state'>State </label>
						<div>
							<input name='state' class='element text medium' type='text' maxlength='255'/> 
						</div> 
					</li>
					<li id='li_3'>
						<label class='description' for='veh_make'>Make</label>
						<div>
							<input name='veh_make' class='element text medium' type='text' maxlength='255'/> 
						</div> 
					</li>
					<li id='li_4'>
						<label class='description' for='veh_model'>Model </label>
						<div>
							<input name='veh_model' class='element text medium' type='text' maxlength='255'/> 
						</div> 
					</li>
					<li id='li_5'>
						<label class='description' for='comment'>Comment </label>
						<div>
							<input name='comment' class='element text medium' type='text' maxlength='255'/> 
						</div> 
					</li>
					<li class='buttons'>
						<input id='saveForm' class='button_text' type='submit' name='submit' value='Submit' />
					</li>
				</ul>
			</form>
		</div>
		<table class='format'>
			<thead>
				<tr>
					<th title='Field #1'>ID</th>
					<th title='Field #2'>Plate Value</th>
					<th title='Field #3'>State</th>
					<th title='Field #4'>Make</th>
					<th title='Field #5'>Model</th>
					<th title='Field #6'>Capture</th>
					<th title='Field #7'>Comments</th>
				</tr>
			</thead>
			<tbody>";
	while($row = mysqli_fetch_array($result)){
		$UID = $row["UID"];
		$plate = $row["plate_no"];
		$state = ucwords(strtolower($row["state"]));
		$veh_make = ucwords(strtolower($row["veh_make"]));
		$veh_model = ucwords(strtolower($row["veh_model"]));
		$image = strtolower($row["image"]);
		$comment = $row["comment"];

		echo "<tr>
			<td style='min-width:20px;'>$UID</td>
			<td>$plate</td>
			<td style='min-width:100px;'>$state</td>
			<td>$veh_make</td>
			<td>$veh_model</td>
			<td onload='ShowHide($UID)'>
				<button onclick='ShowHide($UID)' style='margin-top:0;'>toggle image</button>
				<a target='_blank' href='./images/$image'>
					<img id = '$UID' src='./images/$image' style='width:150px;visibility:hidden;'>
				</a>
			</td>
			<td style='font-size: 1.5vw;max-width:150px;'>$comment</td>
			<td class='buttons'><button onclick='ShowForm($UID)'>Edit Vehicle #$UID</button></td>
		</tr>";
	}
	echo "</tbody>
		</table>
		<br><br>
	</body>
	</html>";
?>

<!-- <td>
	<a target='_blank' href='./images/$image.png'>
		<img src='./images/$image.png' style='width:150px'>
	</a>
</td> -->