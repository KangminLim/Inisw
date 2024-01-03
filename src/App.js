import { StrictMode,useState,useEffect,useCallback} from 'react';
import "./style.css";
import SearchHeader from "./component/searchHeader/searchHeader";
import VideoMain from './component/video_Main/video_main';
import ApiUtil from "./util/apiUtil.js"
import axios from 'axios'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import HomePage from "./component/home/home_page"
import SecondPage from './component/secondPage/secondPage';

function App() {
  const API_KEY = process.env.REACT_APP_YOUTUBE_API_KEY;
  const request = axios.create({
    baseURL: 'https://youtube.googleapis.com/youtube/v3/',
    timeout: 1000,
    params : {'key' : API_KEY}
  });
  const api = new ApiUtil(request);
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);

  useEffect(()=>{
    onInit();
  },[]);

  const onSearch = useCallback( (keyword) => {
    api
    .getSearchResults(keyword)
    .then((items) => {
      setVideos(items);
      setSelectedVideo(null);
    })
    .catch((error) => console.log("error", error));
  },[]);

  const onInit = useCallback(() => {
    api
        .getPopularVideoList() //
        .then((result) => {
          setVideos(result);
          setSelectedVideo(null);
        });
       
  },[])
  window.scrollTo(0,0);
  return (
      <Routes>
        <Route path="/" element={<HomePage />}></Route>
        <Route path="/search" element={<VideoMain />}></Route>
        <Route path="/video" element={<SecondPage onSearch={onSearch} onInit={onInit} videos={videos} selectedVideo={selectedVideo} setSelectedVideo={setSelectedVideo} />}></Route>
      </Routes>
      // <>
      //   <SearchHeader onSearch={onSearch} onInit={onInit}/>
      //   <VideoMain videos = {videos} selectedVideo = {selectedVideo} onSelect = {setSelectedVideo}/>
      // </>
  );
}

export default App;