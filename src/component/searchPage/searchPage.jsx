import React, { memo, useRef, useState } from 'react';
import SearchHeader from '../searchHeader/searchHeader';
import VideoMain from '../video_Main/video_main';
import styles from "../searchPage/searchPage.module.css"

const searchPage = memo(({onSearch, onInit, videos, selectedVideo, setSelectedVideo}) => {

  return (
      <>
          <SearchHeader onSearch={onSearch} onInit={onInit}/>
          <VideoMain videos = {videos} selectedVideo = {selectedVideo} onSelect = {setSelectedVideo}/>
      </>
  )
  

    // return (
    //     <>
    //       <SearchHeader onSearch={onSearch} onInit={onInit}/>
    //       <VideoMain videos = {videos} selectedVideo = {selectedVideo} onSelect = {setSelectedVideo}/>
    //     </>
    // )
})

export default searchPage