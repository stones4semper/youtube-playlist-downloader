<?php
    $apiKey = 'YOUR_YOUTUBE_API_KEY';
    $playlistId = $_GET['playlistId'];
    $requestUrl = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=$playlistId&key=$apiKey";
    $ch = curl_init($requestUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_NOPROGRESS, false);
    curl_setopt($ch, CURLOPT_PROGRESSFUNCTION, function ($downloadSize, $downloaded, $uploadSize, $uploaded) {
        if ($downloadSize > 0) {
            $progress = round(($downloaded / $downloadSize) * 100);
            echo json_encode(['progress' => $progress]);
        }
    });
    $response = curl_exec($ch);
    curl_close($ch);
    echo $response;