import React from 'react';
import styles from './ChatList.module.css'

const ChatList = () => {



    return (
        <div className={styles.chat_list_container}>
            <div className={styles.chat_title}>
                <p>채팅방 목록</p>
            </div>
            <div className={styles.chat_room_container}>
                <div className={styles.chat_room}>
                    <p>채팅방 이름</p>
                    <p>인원</p>
                </div>
            </div>
        </div>
    );
};

export default ChatList;