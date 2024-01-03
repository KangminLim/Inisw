import React, { memo } from 'react';
import styles from '../video_item/video_item.module.css';

const VideoItem = memo((props) => {
    console.log(props)
    const selectedVideo = props.video;
    const {thumbnails,channelTitle} = props.video.snippet;

    const onSelectVideo = () =>{
        props.onSelect(selectedVideo);
    }

    return( 
        <article className={styles.videoItem} onClick={onSelectVideo}>
            <img className={styles.thumbnail} src={thumbnails.medium.url} alt='thumnail_image'></img>
            <div className={styles.channelTitle}>{channelTitle}</div>
        </article>
    );            
});

export default VideoItem;