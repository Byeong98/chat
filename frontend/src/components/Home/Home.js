import React from 'react';
import ChatList from '../ChatList/ChatList';
import ChatRank from '../ChatRank/ChatRank';
import style from './Home.module.css'

const home = () => {
    return (
        <div className={style.home_container}>
            <div className={style.home_create_room_button}>
                <input type='button' value='채팅방 생성'></input>
            </div>
            <div className={style.home_list_container}>
                <ChatRank />
                <ChatList />
            </div>
        </div>
    );
};

export default home;