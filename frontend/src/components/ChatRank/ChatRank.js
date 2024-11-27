import React, { useEffect, useState } from 'react';
import styles from './ChatRank.module.css'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ChatRank = () => {
    const [data, setData] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {

        const fetchData = async () => {
            try {
                const response = await axios.get(
                    `http://localhost:8000/api/chat/rank/`
                );
                console.log(response.data.chat_rooms);
                setData(response.data.chat_rooms)
            } catch (error) {
                console.log('error', error);
            }
        };

        fetchData(); // 비동기 함수 호출
    }, []);

    const handleChatRomm = (roomName) =>{
        navigate(`/chat/${roomName}`, {state : {roomName: roomName}})
    }

    return (
        <div className={styles.chat_list_container}>
            <div className={styles.chat_title}>
                <p>채팅방 랭킹</p>
            </div>
            {/* 리스트 뽑아서 가져오기 */}
            <div className={styles.chat_room_container}>
                {data.map((room, index) => (
                    <div key={index} 
                        className={styles.chat_room} 
                        onClick={()=>handleChatRomm(room.name)}>
                        <p>{room.name}</p>
                        <p>인원 : {room.users}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ChatRank;