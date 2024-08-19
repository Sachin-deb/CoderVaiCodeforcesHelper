import Link from 'next/link';

const Home = () => {
    return (
        <div>
            <h1>Welcome to the Leaderboard App</h1>
            <p>Click the link below to view the leaderboard:</p>
            <Link href="/leaderboard">
                <a>Go to Leaderboard</a>
            </Link>
        </div>
    );
};

export default Home;
