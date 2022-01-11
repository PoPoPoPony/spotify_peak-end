import axios from 'axios'
axios.defaults.withCredentials = true

const axios_instance = axios.create({
    timeout: 5000
})

export default axios_instance