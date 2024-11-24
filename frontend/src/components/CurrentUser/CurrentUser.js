import React,{ useState, useEffect }  from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './CurrentUser.module.css';
import apiClient from '../../apiClient';

const CurrentUser = () => {
    const navigate = useNavigate();
    const [data, setData] = useState('')

    // useEffect(() => {
    //     const checkLogin = async () => {
    //         try {
    //             const response = await apiClient.get('api/accounts/logged/');
    //             console.log('Login status:', response.data);
    //         } catch (error) {
    //             console.error('Error fetching login status:', error);
    //         }
    //     };
    //     checkLogin();
    // }, []);



    return (
        <div className={styles.current_user_container}>
            <div className={styles.current_user_title}>
                <p>접속자</p>
            </div>
            {/* 리스트 뽑아서 가져오기 */}
            <div className={styles.user_container}>
                <div className={styles.user_name}>
                    <p>유저이름</p>
                </div>
                <div className={styles.user_name}>
                    <p>유저이름</p>
                </div>
                <div className={styles.user_name}>
                    <p>유저이름</p>
                </div>
                <div className={styles.user_name}>
                    <p>유저이름</p>
                </div>
            </div>
        </div>
    );
};

export default CurrentUser;