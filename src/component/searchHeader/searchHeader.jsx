import React, { useRef, memo } from "react";
import styles from "./searchHeader.module.css";

const SearchHeader = memo(({ onSearch, onInit }) => {
  const ref = useRef(); // 특정 dom에 직접 접근

  const onSearchClick = (event) => {
    event.preventDefault();
    const keyword = ref.current.value;
    onSearch(keyword);
  };

  // const onSearchClick = (event) => {
  //   event.preventDefault();
  //   window.location.href = "/search/" + event.target.value
  // };

  //todo : 홈페이지로 가게끔 경로 수정
  const onLogoClick = () => {
    ref.current.value = "";
    console.log(ref.current.value);
    onInit();
  };
  return (
    <header>
      <img
        className={styles.logo}
        src="/img/logo.png"
        alt="project logo"
        onClick={onLogoClick}
      />
      <form className={styles.form} onSubmit={onSearchClick}>
        <input className={styles.searchInput} ref={ref} />
        <button className={styles.button}>
          click
        </button>
      </form>
    </header>
  );
});

export default SearchHeader;