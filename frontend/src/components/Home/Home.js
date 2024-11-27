import React from 'react';
import ChatList from '../ChatList/ChatList';
import ChatRank from '../ChatRank/ChatRank';
import styles from './Home.module.css'
import { useLocation } from 'react-router-dom';

const Home = () => {
    const location = useLocation();
    const { userName } = location.state || {};
    console.log(userName)
    return (
        <div className={styles.home_container}>
            <div className={styles.home_create_room}>
                <input 
                className={styles.home_create_room_button}
                type='button' value='채팅방 생성'></input>
            </div>
            <div className={styles.home_list_container}>
                <ChatRank />
                <ChatList />
            </div>
        </div>
    );
};

export default Home;