<?php
	$servername = "localhost";
	$username = "root";
	$password = "";
	// Create connection
	$conn = mysqli_connect($servername, $username, $password,"vehicles");

	// Check connection
	if (!$conn) {
		die("Connection failed: ".mysqli_connect_error());
		echo "connection failed";
	}

	if (isset($_POST['submit'])){
		$UID = $_POST['UID'];
		$plate = $_POST['plate'];
		$state = $_POST['state'];
		$veh_make = $_POST['veh_make'];
		$veh_model = $_POST['veh_model'];
		$comment = $_POST['comment'];
		$filename = strtolower($plate).'.png';
		$selectQuery = "SELECT * FROM captures WHERE UID='$UID'";
		$updateQuery = "UPDATE captures SET plate_no='$plate', state='$state', veh_make='$veh_make',veh_model='$veh_model',comment='$comment' WHERE UID='$UID'";
		mysqli_query($conn, $updateQuery);
		if(mysqli_affected_rows($conn) > 0){
			echo '<h3>Record Updated</h3>';
		}
		else{
			echo '<h3>Record NOT Updated!</h3>';
			echo '<h3>'.mysqli_error($conn).'</h3>';
			exit;
		}
	}
    
	$result = mysqli_query($conn, $selectQuery);

	echo"<html>
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
		</script>
			</head>
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
						<button onclick='ShowHide($UID)' style='margin-top:0;display:block;margin-left:auto;margin-right:auto;'>toggle image</button>
						<a target='_blank' href='./images/$image.png'>
							<img id = '$UID' src='./images/$image.png' style='width:150px;visibility:hidden;'>
						</a>
					</td>
					<td style='font-size: 1.5vw;max-width:150px;'>$comment</td>
					</tr>";
			}
			echo "</tbody>
				</table>
				</html>";
?>