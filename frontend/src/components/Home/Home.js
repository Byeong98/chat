import React, { useContext, useState, useRef, useEffect, } from 'react';
import { useNavigate } from 'react-router-dom';
import ChatList from '../ChatList/ChatList';
import ChatRank from '../ChatRank/ChatRank';
import styles from './Home.module.css';
import { AuthContext } from '../../AuthContext';
import axios from 'axios';


const Home = () => {
    const navigate = useNavigate();
    const { userName, setUserName } = useContext(AuthContext)
    const [modal, setModal] = useState(false);
    const [roomName, setRoomName] = useState('');
    const chatSocketRef = useRef(null);
    const [roomList, setsRoomList] = useState([]);
    const [roomRank, setsRoomRank] = useState([]);


    useEffect(() => {
        const socket = new WebSocket(
            'ws://127.0.0.1:8000/ws/chat/');
        chatSocketRef.current = socket;

        socket.onopen = () => {
            console.log('연결 완료');
        };

        socket.onclose = () => {
            console.log('연결 끝');
        };

        socket.onerror = () => {
            console.log('연결 에러');
        };

        socket.onmessage = (event) => {
            const newMessage = JSON.parse(event.data);
            
            console.log(newMessage)
            setsRoomList(newMessage.room_list);
            setsRoomRank(newMessage.room_rank);
        };

        return () => {
            socket.close(); // 컴포넌트 언마운트 시 WebSocket 닫기
        };
    }, []);


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

    const handelModal = async () => {
        if (roomName.trim()) {
            try {
                const response = await axios.post(
                    'http://localhost:8000/api/chat/',
                    {"roomName":roomName});
                    navigate(`/chat/${response.data.room_id}`, {state : {roomId: response.data.room_id}})
                    setModal(false);
                    setRoomName('');
            } catch (error) {
                alert(error.response.data.message)
            }
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
                <ChatRank roomRank={roomRank}/>
                <ChatList roomList={roomList}/>
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
                            maxLength='30'
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