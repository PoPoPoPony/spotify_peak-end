import request from '../../../utils/requestBackend'



export function UpdateTagStatus(userID, tagID) {
    let data = {
        "userID": userID,
        "tagID": tagID
    }
    
    let config = {
        url: '/tags/updateTagStatus',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        params: data
    }
    

    return request(config)
}