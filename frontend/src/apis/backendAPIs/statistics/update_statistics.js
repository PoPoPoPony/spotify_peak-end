import request from '../../../utils/requestBackend'



export function Update() {
    let config = {
        url: '/temp/update_statistic_files',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
    }
    

    return request(config)
}