import React from 'react';
import styles from './ChatList.module.css'

const ChatList = () => {



    return (
        <div className={styles.chat_list_container}>
            <div className={styles.chat_title}>
                <text>채팅방 목록</text>
            </div>
            <div className={styles.chat_room_container}>
                <div className={styles.chat_room}>
                    <text>채팅방 이름</text>
                    <text>인원</text>
                </div>
            </div>
        </div>
    );
};

export default ChatList;