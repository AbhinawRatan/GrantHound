import React, { useState } from "react";
import axios from "axios";

const GrantRecommendation = () => {
    const [description, setDescription] = useState("");
    const [grants, setGrants] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await axios.post("http://localhost:8000/recommend_grants", {
            description,
        }, {
            headers: {
                "api-key": "samrfdidh"
            }
        });

        setGrants(response.data);
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label>
                    Project Description:
                    <input
                        type="text"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                </label>
                <button type="submit">Get Recommendations</button>
            </form>

            <div>
                {grants.map((grant, index) => (
                    <div key={index}>
                        <h3>{grant.grant_name}</h3>
                        <p>{grant.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default GrantRecommendation;
