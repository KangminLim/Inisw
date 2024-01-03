import React, { memo,useRef } from 'react';
import styles from "./home_page.module.css";
import { Link } from 'react-router-dom';

const HomePage = memo(({ onSearch, onInit}) => {
   
    return (
        <>
            <div className={styles.main} style={{backgroundImage:'url(/img/background.png)'}} >
                <form className={styles.form}>
                   <div>저희 프로그램</div>
                    <Link to='/video'>
                        <button className={styles.button}>
                            <i className="fa-solid fa-magnifying-glass"></i>
                        </button>
                    </Link>
                </form>
            </div>
        </>
    )
})

export default HomePage


{/* <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }} style={{
    backgroundImage: "url(/img/background.png)",
}}>
    <TextField sx={{ width: '50ch', top: 50 }} id="outlined-basic" label="궁금한 상황을 입력해주세요." variant="outlined" />
</Box>


style={ {backgroundImage:'url(/img/background.png)'}}

*/}