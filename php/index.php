<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YouTube Playlist Downloader</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<div class="container mt-5">
  <h2>Enter YouTube Playlist ID:</h2>
  <div class="input-group mb-3">
    <input type="text" id="playlistIdInput" class="form-control" placeholder="Enter Playlist ID">
    <button id="fetchVideosBtn" class="btn btn-primary">Fetch Videos</button>
  </div>

  <div id="videosContainer"></div>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
<script>
$(document).ready(function(){
    $('#fetchVideosBtn').click(function(){
        var playlistId = $('#playlistIdInput').val();
        $.ajax({
            url: 'fetch-videos.php',
            type: 'GET',
            data: { playlistId: playlistId },
            success: function(response){
                var videos = JSON.parse(response).items;
                $('#videosContainer').empty();
                videos.forEach(function(video){
                    var videoId = video.snippet.resourceId.videoId;
                    var videoTitle = video.snippet.title;
                    var videoUrl = 'https://www.youtube.com/watch?v=' + videoId;
                    $('#videosContainer').append('<p><a href="' + videoUrl + '" target="_blank">' + videoTitle + '</a></p>');
                });
            },
            progress: function(event) {
                if (event.lengthComputable) {
                    var progress = Math.round((event.loaded / event.total) * 100);
                    console.log('Download progress:', progress + '%');
                }
            },
            error: function(xhr, status, error){
                console.error('Error fetching videos:', error);
            }
        });
    });
});
</script>

</body>
</html>
