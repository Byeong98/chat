import React, { useEffect, useState } from 'react';
import styles from './ChatRank.module.css'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ChatRank = ({roomRank}) => {
    const navigate = useNavigate();

    const handleChatRomm = (roomId) =>{
        navigate(`/chat/${roomId}`, {state : {roomId: roomId}})
    }
    
    return (
        <div className={styles.chat_list_container}>
            <div className={styles.chat_title}>
                <p>채팅방 랭킹</p>
            </div>
            {/* 리스트 뽑아서 가져오기 */}
            <div className={styles.chat_room_container}>
                {roomRank.map((room, index) => (
                    <div key={index} 
                        className={styles.chat_room} 
                        onClick={()=>handleChatRomm(room.id)}>
                        <p>{index + 1}</p>
                        <p>{room.name}</p>
                        <p>인원 : {room.users}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ChatRank;