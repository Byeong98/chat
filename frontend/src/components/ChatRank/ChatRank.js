import React from 'react';
import styles from './ChatRank.module.css'

const ChatRank = () => {

    return (
        <div className={styles.chat_list_container}>
            <div className={styles.chat_title}>
                <p>채팅방 랭킹</p>
            </div>
            {/* 리스트 뽑아서 가져오기 */}
            <div className={styles.chat_room_container}>
                <div className={styles.chat_room}>
                    <p>채팅방 이름</p>
                    <p>인원</p>
                </div>
            </div>
        </div>
    );
};

export default ChatRank;