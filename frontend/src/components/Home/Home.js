import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ChatList from '../ChatList/ChatList';
import ChatRank from '../ChatRank/ChatRank';
import styles from './Home.module.css';
import { AuthContext } from '../../AuthContext';
import axios from 'axios';


const Home = () => {
    const { userName, setUserName } = useContext(AuthContext)
    const navigate = useNavigate();
    const [modal, setModal] = useState(false);
    const [roomName, setRoomName] = useState('');

    const handelLogout = async () => {
        try {
            const response = await axios.post(
                'http://localhost:8000/api/accounts/logout/');
            setUserName(null);
            localStorage.removeItem('CurrentUser');
        } catch (error) {
            console.log('error', error);
        }
    }

    const handelModal = () => {
        if (roomName.trim()) {
            navigate(`/chat/${roomName}`, {state : {roomName: roomName}})
            setModal(false)
            setRoomName('')
        } else {
            alert('채팅방 이름을 입력하세요')
        } 
    }
    return (
        <div className={styles.home_container}>
            <div className={styles.home_button_room}>
                {!userName ?
                    <input
                        className={styles.home_create_room_button}
                        type='button' value='로그인'
                        onClick={() => navigate('login/')}
                    />
                    :
                    <input
                        className={styles.home_create_room_button}
                        type='button' value='로그아웃'
                        onClick={handelLogout}
                    />
                }

                <input
                    className={styles.home_create_room_button}
                    type='button' value='채팅방 생성'
                    onClick={() => setModal(true)}
                />
            </div>
            <div className={styles.home_list_container}>
                <ChatRank />
                <ChatList />
            </div>
            {modal &&
                <div className={styles.modal_container}>
                    <div className={styles.modal_content}>
                        <p className={styles.modal_title}>그룹 생성</p>
                        <input
                            type="text"
                            id="rooName"
                            name="roomName"
                            placeholder="채팅방 이름 입력"
                            value={roomName}
                            onChange={e => setRoomName(e.target.value)}
                            required
                            
                        />
                        <div>
                            <input
                                className={styles.home_create_room_button}
                                type='button' value='생성'
                                onClick={handelModal}
                            />
                            <input
                                className={styles.home_create_room_button}
                                type='button' value='취소'
                                onClick={() => setModal(false)}
                            />
                        </div>
                    </div>
                </div>
            }
        </div>
    );
};

export default Home;