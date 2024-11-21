import React from 'react';
import styles from './ChatRank.module.css'

const ChatRank = () => {

    return (
        <div className={styles.chat_list_container}>
            <div className={styles.chat_title}>
                <text>채팅방 랭킹</text>
            </div>
            {/* 리스트 뽑아서 가져오기 */}
            <div className={styles.chat_room_container}>
                <div className={styles.chat_room}>
                    <text>채팅방 이름</text>
                    <text>인원</text>
                </div>
            </div>
        </div>
    );
};

export default ChatRank;