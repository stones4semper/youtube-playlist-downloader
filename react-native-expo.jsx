import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet } from 'react-native';
import { Video } from 'expo-av';
import * as FileSystem from 'expo-file-system';

const VideoDownloader = () => {
  const [playlistUrl, setPlaylistUrl] = useState('');
  const [videos, setVideos] = useState([]);
  const [downloading, setDownloading] = useState(false);

  const downloadVideo = async (videoUrl, index) => {
    try {
      const fileUri = `${FileSystem.documentDirectory}${index}.mp4`;
      const downloadResumable = FileSystem.createDownloadResumable(
        videoUrl,
        fileUri,
        {},
        (downloadProgress) => {
          const progress = downloadProgress.totalBytesWritten / downloadProgress.totalBytesExpectedToWrite;
          console.log(`Downloaded ${progress * 100}%`);
        }
      );

      const { uri } = await downloadResumable.downloadAsync();
      console.log('Download complete:', uri);
    } catch (error) {
      console.error('Error downloading video:', error);
    }
  };
  const fetchVideosFromPlaylist = async (playlistUrl) => {
    try {
      const playlistId = playlistUrl.split('list=')[1];
      const apiKey = 'YOUR_YOUTUBE_API_KEY';
      const apiUrl = `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=${playlistId}&key=${apiKey}`;
      const response = await fetch(apiUrl);
      const data = await response.json();
      const videoIds = data.items.map(item => item.snippet.resourceId.videoId);  
      const videoUrls = videoIds.map(videoId => `https://www.youtube.com/watch?v=${videoId}`);
  
      return videoUrls;
    } catch (error) {
      console.error('Error fetching videos from playlist:', error);
      return [];
    }
  };
  const handleDownload = async () => {
    try {
      setDownloading(true);
      const videos = await fetchVideosFromPlaylist(playlistUrl);
      setVideos(videos);
      videos.forEach((videoUrl, index) => {
        downloadVideo(videoUrl, index + 1);
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to download videos');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text>Enter Playlist URL:</Text>
      <TextInput
        style={styles.input}
        onChangeText={setPlaylistUrl}
        value={playlistUrl}
      />
      <Button title="Download" onPress={handleDownload} disabled={downloading} />
      {videos.map((videoUrl, index) => (
        <Video key={index} source={{ uri: videoUrl }} style={styles.video} />
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    width: 300,
  },
  video: {
    width: 300,
    height: 200,
    marginBottom: 10,
  },
});

export default VideoDownloader;
