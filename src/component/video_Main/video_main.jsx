import React from "react";
import VideoList from "../video_list/video_list";
import styles from "../video_Main/video_main.module.css";
import VideoPlay from "../video_play/video_play";
import { useParams } from "react-router-dom";


const VideoMain = ({ videos, selectedVideo, onSearch, onSelect }) => {
  let { query } = useParams(); //? 쿼리를 받아오고

  const [videos, setVideos] = useState([
    { id: 1, title: 'Platform 9¾  Harry Potter and the Philosophers Stone', path: '/videos/Platform 9¾  Harry Potter and the Philosophers Stone.mp4' },
    { id: 2, title: 'The Sorting Ceremony  Harry Potter and the Philosophers Stone', path: '/videos/The Sorting Ceremony  Harry Potter and the Philosophers Stone.mp4'  },
    { id: 3, title: 'The Ultimatum Queer Love  Official Teaser  Netflix.mp4', path: '/videos/The Ultimatum Queer Love  Official Teaser  Netflix.mp4' },
    { id: 4, title: 'The Ultimatum Queer Love Cast Clears The Air  Netflix', path: '/videos/searching/public/videos/The Ultimatum Queer Love Cast Clears The Air  Netflix.mp4' },
    { id: 5, title: 'Wizard Duel Draco Malfoy vs Harry Potter  Harry Potter and the Chamber of Secrets', path: '/videos/searching/public/videos/Wizard Duel Draco Malfoy vs Harry Potter  Harry Potter and the Chamber of Secrets.mp4' },
    // 추가 동영상 데이터
  ]);
  const [currentVideo, setCurrentVideo] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  
  // todo useeffect 해서 axios.get => 백엔드에 쿼리를 보냄. 그럼 쿼리를 서버에 보내서 받아옴 
  // todo 비디오 []
  let isSelected = selectedVideo ? styles.selected : "";
  return (
    <main className={styles.videoMain}>
      {selectedVideo && (  // selectedVideo가 true 일 때만 괄호 안 실행 
        <section className={styles.videoPlay}>
          <VideoPlay selectedVideo={selectedVideo}></VideoPlay>
        </section>
      )}
      <section className={styles.videoList + " " + isSelected}>
        <VideoList query={query} videos={videos} onSelect={onSelect} />
      </section>
    </main>
  );
};

export default VideoMain;