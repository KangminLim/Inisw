import React, { memo } from "react";
import SearchHeader from "../searchHeader/searchHeader";
import VideoMain from "../video_Main/video_main";

const SecondPage = (({onSearch, onInit, videos, selectedVideo, setSelectedVideo}) => { // selectedVideo prop을 받았을 때 이전에 렌더링한 결과 재사용 -> 성능 최적화

  return (
    <>
      <SearchHeader onSearch={onSearch} onInit={onInit}/>
      {/* <VideoMain videos = {videos} selectedVideo = {selectedVideo} onSelect = {setSelectedVideo}/> */}
    </>
  );
});

export default SecondPage;