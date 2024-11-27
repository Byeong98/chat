import React,{useEffect, useState} from 'react';
import styles from './ChatList.module.css'
import axios from 'axios';

const ChatList = () => {
    const [data, setData] = useState([])

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(
                    `http://localhost:8000/api/chat/`
                );
                console.log(response.data.chat_rooms);
                setData(response.data.chat_rooms)
            } catch (error) {
                console.log('error', error);
            }
        };

        fetchData(); // 비동기 함수 호출
    }, []);


    return (
        <div className={styles.chat_list_container}>
            <div className={styles.chat_title}>
                <p>채팅방 목록</p>
            </div>
            <div className={styles.chat_room_container}>
                {data.map((room,index)=>(
                    <div key={index} className={styles.chat_room}>
                        <p>{room.name}</p>
                        <p>인원 : {room.users}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ChatList;