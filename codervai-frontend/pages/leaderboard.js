import { useEffect, useState } from 'react';

const Leaderboard = () => {
    const [leaderboard, setLeaderboard] = useState([]);

    useEffect(() => {
        const fetchLeaderboard = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/leaderboard/566', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                console.log('Response data:', data);  // Log the entire response data

                // Assuming the data is an array of objects directly
                const json_response = data.map(row => ({
                    handle: row.handle,
                    points: row.points,
                }));

                console.log(json_response);
                setLeaderboard(json_response);
            } catch (error) {
                console.error('Error fetching leaderboard:', error);
            }
        };

        fetchLeaderboard();
    }, []);

    return (
        <div>
            <h1>Leaderboard</h1>
            <ul>
                {leaderboard.map((item, index) => (
                    <li key={index}>
                        {item.handle} - {item.points} points
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Leaderboard;
