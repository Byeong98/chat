import React, { useState, useEffect } from 'react';
import styles from './CurrentUser.module.css';
import apiClient from '../../apiClient';
import axios from 'axios';

const CurrentUser = () => {
    const [data, setData] = useState([])
    const roomName = 'admin'

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(
                    `http://localhost:8000/api/chat/${roomName}/users/`
                );
                console.log(response.data);
                setData(response.data.users)
            } catch (error) {
                console.log('error', error);
            }
        };

        fetchData(); // 비동기 함수 호출
    }, [roomName]);

    return (
        <div className={styles.current_user_container}>
            <div className={styles.current_user_title}>
                <p>접속자</p>
            </div>
            {/* 리스트 뽑아서 가져오기 */}
            <div className={styles.user_container}>
                {data.map((username, index) => (
                    <div key={index} className={styles.user_name}>
                        <p>{username}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CurrentUser;