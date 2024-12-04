import React,{useEffect, useState,} from 'react';
import styles from './ChatList.module.css'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const ChatList = () => {
    const [data, setData] = useState([])
    const navigate = useNavigate()

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(
                    `http://localhost:8000/api/chat/list/`
                );
                setData(response.data.chat_rooms)
            } catch (error) {
                console.log('error', error);
            }
        };

        fetchData(); // 비동기 함수 호출
    }, []);

    const handleChatRomm = (roomId) =>{
        navigate(`/chat/${roomId}`, {state : {roomId: roomId}})
    }

    return (
        <div className={styles.chat_list_container}>
            <div className={styles.chat_title}>
                <p>채팅방 목록</p>
            </div>
            <div className={styles.chat_room_container}>
                {data.map((room,index)=>(
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