import { useLocation } from "react-router-dom";

function DisplayResults() {
    const data = useLocation().state?.data;
    return (
        <div>
            <h2>Results</h2>
            {data ? (
                <ul>
                    {data.data.map((item: any, index: number) => (
                        <li key={index}>
                            <h3>{item.address}</h3>
                            <p>Last Price: {item.last_price}</p>
                            <h4>Historical Prices:</h4>
                            <ul>
                                {item.historical_prices.map((price: any, idx: number) => (
                                    <li key={idx}>{price.date}: ${price.price}</li>
                                ))}
                            </ul>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No results found.</p>
            )}
        </div>
    );
};

export default DisplayResults;