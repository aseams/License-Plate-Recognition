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
		<style>
		table{
			margin-top:5%;
			margin-left: auto;
			margin-right: auto;
		}
		table, th, td{
			border: 1px solid black;
			border-collapse: collapse;
		}
		table.format tr td {
			font-size: 22px;
			padding: 10px;
			text-align: center;
		}
		body {
			position: center;
		}
		</style>
	</head>
	<body>
		<table class='format'>
			<thead>
				<tr>
					<th title='Field #1'>UID</th>
					<th title='Field #2'>plate_no</th>
					<th title='Field #3'>state</th>
					<th title='Field #4'>veh_make</th>
					<th title='Field #5'>veh_model</th>
					<th title='Field #6'>image</th>
					<th title='Field #7'>comment</th>
				</tr>
			</thead>
			<tbody>";
	while($row = mysqli_fetch_array($result)){
		$UID = $row["UID"];
		$plate = $row["plate_no"];
		$state = ucwords(strtolower($row["state"]));
		$veh_make = ucwords(strtolower($row["veh_make"]));
		$veh_model = ucwords(strtolower($row["veh_model"]));
		$image = strtolower($row["plate_no"]);
		$comment = $row["comment"];

		echo "<tr>
			<td align='right'>$UID</td>
			<td>$plate</td>
			<td>$state</td>
			<td>$veh_make</td>
			<td>$veh_model</td>
			<td>
				<a target='_blank' href='./images/$image.jpg'>
					<img src='./images/$image.png' style='width:150px'>
		   		</a>
			</td>
			<td style='max-width:175px;'>$comment</td>
		</tr>";
	}
	echo "</tbody>
	</table>
	</body>
	</html>";
?>