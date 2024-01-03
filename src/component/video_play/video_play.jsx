import React, { memo } from "react";
import styles from "./video_play.module.css";

const VideoPlay = memo(({ selectedVideo }) => { // selectedVideo prop을 받았을 때 이전에 렌더링한 결과 재사용 -> 성능 최적화
  const id = selectedVideo.id;
  const { title, channelTitle, description } =
    selectedVideo.snippet;
  return (
    <>
      <iframe
        className={styles.video}
        title="video player"
        id="player"
        type="text/html"
        src={`https://www.youtube.com/embed/${id}?autoplay=1&origin=http://example.com`}
      />
    </>
  );
});

export default VideoPlay;