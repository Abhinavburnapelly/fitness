// import React, { useState, useEffect } from 'react';
// import '../App.css';

// function LiveFeed() {
//     const [counter, setCounter] = useState(0);

//     useEffect(() => {
//         const fetchCounter = async () => {
//             try {
//                 const response = await fetch('http://localhost:5000/counter');
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 const data = await response.json();
//                 setCounter(data.count_la);
//             } catch (error) {
//                 console.error("There has been a problem with your fetch operation:", error);
//             }
//         };

//         const intervalId = setInterval(fetchCounter, 1000);  // Fetch the counter every second

//         return () => clearInterval(intervalId);  // Clear interval on component unmount
//     }, []);

//     return (
//         <div className="App">
//             <div className="container">
//                 <div className="counter-box left">
//                     <h2>{counter}</h2>
//                     <p>Left Counter</p>
//                 </div>
//                 <div className="video-feed">
//                     <img src="http://localhost:5000/video_feed" alt="Video Feed" />
//                 </div>
//                 <div className="counter-box right">
//                     <h2>{counter}</h2>
//                     <p>Right Counter</p>
//                 </div>
//             </div>
//         </div>
//     );
// }

// export default LiveFeed;
import React, { useState, useEffect } from 'react';
import '../App.css';
import { useParams } from 'react-router-dom';

function LiveFeed() {
    // const { exerciseType } = exerciseType; 
    const [counters, setCounters] = useState({});
    let {exerciseType}=useParams()
    // console.log(exerciseType)
    useEffect(() => {
        const fetchCounters = async () => {
            try {
                const response = await fetch(`http://localhost:5000/${exerciseType}_counter`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                // console.log(data);
                setCounters(data);
            } catch (error) {
                console.error("There has been a problem with your fetch operation:", error);
            }
        };

        const intervalId = setInterval(fetchCounters, 1000);  // Fetch the counters every second

        return () => clearInterval(intervalId);  // Clear interval on component unmount
    }, []);
     const fetch_data=async ()=>{
        try {
            const response = await fetch(`http://localhost:5000/send_data`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data);
            
        } catch (error) {
            console.error("There has been a problem with your fetch operation:", error);
        }
    }
    // Splitting counters into two groups
    const counterKeys = Object.keys(counters);
    const midIndex = Math.ceil(counterKeys.length / 2);
    const leftCounters = counterKeys.slice(0, midIndex);
    const rightCounters = counterKeys.slice(midIndex);

    return (
        <div className="App">
            <div className="container" style={{ display: 'flex', justifyContent: 'space-between' }}>
                {/* Left Counters */}
                <div className="counter-group">
                    {leftCounters.map(counterKey => (
                        <div className="counter-box" key={counterKey}>
                            <h2>{counters[counterKey]}</h2>
                            <p>{counterKey}</p>
                        </div> 
                    ))}
                </div>
                
                {/* Video Feed */}
                <div className="video-feed">
                    <img src="http://localhost:5000/video_feed" alt="Video Feed" />
                </div>

                {/* Right Counters */}
                <div className="counter-group">
                    {rightCounters.map(counterKey => (
                        <div className="counter-box" key={counterKey}>
                            <h2>{counters[counterKey]}</h2>
                            <p>{counterKey}</p>
                        </div>
                    ))}
                </div>
            </div>
            <button onClick={fetch_data}>Send Data</button>
        </div>
    );
}

export default LiveFeed;
