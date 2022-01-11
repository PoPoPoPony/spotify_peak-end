// export async function getToken(clientId, clientSecret) {
//     const result = await fetch("https://accounts.spotify.com/api/token", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/x-www-form-urlencoded",
//             Authorization: "Basic " + btoa(clientId + ":" + clientSecret),
//         },
//         body: "grant_type=client_credentials",
//     });

//     const data = await result.json();
//     return data.access_token;
// }

import axios from 'axios'
// axios.defaults.withCredentials = true

const axios_instance = axios.create({
    // default fastapi server
    baseURL: 'http://127.0.0.1:8000',
    timeout: 5000,
})

export default axios_instance