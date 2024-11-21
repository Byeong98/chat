import React from 'react';
import ChatList from '../ChatList/ChatList';
import ChatRank from '../ChatRank/ChatRank';
import styles from './Home.module.css'

const home = () => {
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

export default home;