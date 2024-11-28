import React, { useEffect, useRef, useState, useContext } from 'react';
import styles from './ChatRoom.module.css'
// import ChatContainer from '../ChatContainer/ChatContainer';
import CurrentUser from '../CurrentUser/CurrentUser';
import { useNavigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../../AuthContext';
import axios from 'axios';


const ChatRoom = () => {
    const chatSocketRef = useRef(null);
    const [messages, setMessages] = useState([]);
    const navigate = useNavigate();
    const [currentUsers, setCurrentUsers] = useState([]);
    const { userName } = useContext(AuthContext);
    const location = useLocation();
    const roomId = location.state.roomId;

    const fetchCurrentUsers = async () => {
        try {
            const response = await axios.get(
                `http://localhost:8000/api/chat/${roomId}/users/`
            );
            setCurrentUsers(response.data.users); // 접속자 목록 업데이트
        } catch (error) {
            console.error('접속자 정보를 가져오는 중 오류 발생:', error);
        }
    };

    useEffect(() => {
        const socket = new WebSocket(
            'ws://127.0.0.1:8000/ws/chat/' + `${roomId}` + '/' + `?user=${userName}`);
        chatSocketRef.current = socket;

        socket.onopen = () => {
            console.log('WebSocket 연결 성공');
        };

        socket.onclose = () => {
            console.log('연결 종료');
        };

        socket.onerror = () => {
            console.log('연결 에러');
        };

        socket.onmessage = (event) => {
            const newMessage = JSON.parse(event.data);
            setMessages((prev) => [...prev, newMessage]);

            if (newMessage.sender_user === 0) {
                fetchCurrentUsers(); // 접속자 목록 다시 가져오기
            }
        };

        return () => {
            socket.close(); // 컴포넌트 언마운트 시 WebSocket 닫기
        };
    }, [roomId, userName]);

    const sendMessage = () => {
        const textInput = document.getElementById('chat-message-input');
        const imageInput = document.getElementById('chat-image-input');
        const message = textInput.value.trim();
        const image = imageInput.files?.[0] || null; // 이미지 파일이 있을 경우

        if (!message && !image) {
            console.log('메시지 또는 이미지를 입력하세요.');
            return;
        }

        const sender_user = userName;

        // 메시지 전송
        chatSocketRef.current.send(
            JSON.stringify({ message, image: image?.name, sender_user })
        );

        // 입력 필드 초기화
        textInput.value = '';
        imageInput.value = '';
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };


    const handleHome = () => {
        navigate('/')
    };


    return (
        <div className={styles.chat_room_container}>
            <div className={styles.chat_room_out}>
                <h2 className={styles.chat_title}>채팅방 이름</h2>
                <input
                    className={styles.chat_room_out_button}
                    type="button"
                    value="나가기"
                    onClick={handleHome}
                />
            </div>
            <div className={styles.chat_container}>
                <CurrentUser users={currentUsers} />
                <div className={styles.chatting_container}>
                    <div className={styles.chat_content_container}>
                        {/* 메시지 표시 */}
                        {messages.map((message, index) => (
                            <div key={index}>
                                {message.sender_user === 0 ? (
                                    <p style={{ textAlign: 'center' }}>
                                        {message.message}
                                    </p>
                                ) : message.sender_user === userName ? (
                                    <p style={{ textAlign: 'right' }}>
                                        {message.sender_user} : {message.message}
                                    </p>
                                ) : (
                                    <p style={{ textAlign: 'left' }}>
                                        {message.sender_user} : {message.message}
                                    </p>
                                )}
                            </div>
                        ))}
                    </div>
                    <div className={styles.chat_input_container}>
                        <label
                            htmlFor="chat-image-input"
                            className={styles.chat_image_label}
                        >
                            사진 선택
                        </label>
                        <input
                            className={styles.chat_image_input}
                            id="chat-image-input"
                            accept="image/*"
                            type="file"
                            onKeyDown={handleKeyPress}
                        />
                        <input
                            className={styles.chat_message_input}
                            id="chat-message-input"
                            type="text"
                            maxLength="50"
                            placeholder="메시지를 입력하세요"
                            aria-label="메시지 입력"
                            onKeyDown={handleKeyPress}
                        />
                        <input
                            className={styles.chat_message_submit}
                            id="chat-message-submit"
                            type="button"
                            value="Send"
                            onClick={sendMessage}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatRoom;
