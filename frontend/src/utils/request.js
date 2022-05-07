import axios from 'axios'


// axios.defaults.withCredentials = true
// axios.defaults.headers.get['Content-Type'] = 'application/x-www-form-urlencoded'



const axios_instance = axios.create({
    baseURL: "https://api.spotify.com/v1",
    timeout: 5000,
})

export default axios_instance