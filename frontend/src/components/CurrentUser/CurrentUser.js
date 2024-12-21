import React from 'react';
import styles from './CurrentUser.module.css';


const CurrentUser = ({users}) => {

    return (
        <div className={styles.current_user_container}>
            <div className={styles.current_user_title}>
                <p>접속자</p>
            </div>
            {/* 리스트 뽑아서 가져오기 */}
            <div className={styles.user_container}>
                {users.map((username, index) => (
                    <div key={index} className={styles.user_name}>
                        <p>{username}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CurrentUser;