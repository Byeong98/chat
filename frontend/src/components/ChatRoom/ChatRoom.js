import React from 'react';
import styles from './ChatRoom.module.css'
import ChatContainer from '../ChatContainer/ChatContainer';
import CurrentUser from '../CurrentUser/CurrentUser';

const ChatRoom = () => {
    return (
        <div className={styles.chat_room_container}>
        <div className={styles.chat_room_out}>
            <h2 className={styles.chat_title}>채팅방 이름</h2>
            <input className={styles.chat_room_out_button}type='button' value='나가기'></input>
        </div>
        <div className={styles.chat_container}>
            <CurrentUser />
            <ChatContainer />
        </div>
    </div>
    );
};

export default ChatRoom;