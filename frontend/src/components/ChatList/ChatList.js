import React from 'react';
import styles from './ChatList.module.css'
import { useNavigate } from 'react-router-dom';


const ChatList = ({roomList}) => {
    const navigate = useNavigate();

    const handleChatRomm = (roomId) =>{
        navigate(`/chat/${roomId}`, {state : {roomId: roomId}})
    }

    return (
        <div className={styles.chat_list_container}>
            <div className={styles.chat_title}>
                <p>채팅방 목록</p>
            </div>
            <div className={styles.chat_room_container}>
                {roomList.map((room,index)=>(
                    <div key={index} className={styles.chat_room}
                        onClick={()=>handleChatRomm(room.id)}>
                        <p>{room.name}</p>
                        <p>인원 : {room.users}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ChatList;