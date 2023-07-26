import request from '../../../utils/requestBackend'



export function CheckRecent(userID) {
    let config = {
        url: '/userRecentTracks/checkUserExist?userID='+userID,
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
    }
    
    return request(config)
}

export function CheckSaved(userID) {
    let config = {
        url: '/userSavedTracks/checkUserExist?userID='+userID,
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
    }
    
    return request(config)
}