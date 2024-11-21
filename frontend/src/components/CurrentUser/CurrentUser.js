import React from 'react';
import styles from './CurrentUser.module.css'

const CurrentUser = () => {
    return (
        <div className={styles.current_user_container}>
            <div className={styles.current_user_title}>
                <text>접속자</text>
            </div>
            {/* 리스트 뽑아서 가져오기 */}
            <div className={styles.user_container}>
                <div className={styles.user_name}>
                    <text>유저이름</text>
                </div>
                <div className={styles.user_name}>
                    <text>유저이름</text>
                </div>
                <div className={styles.user_name}>
                    <text>유저이름</text>
                </div>
                <div className={styles.user_name}>
                    <text>유저이름</text>
                </div>
            </div>
        </div>
    );
};

export default CurrentUser;