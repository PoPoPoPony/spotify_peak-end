import request from '../../../utils/requestBackend'



export function GetUserRecentTracks(userID) {
    let config = {
        url: '/userRecentTracks/getUserRecentTracks?userID='+userID,
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
    }
    

    return request(config)
}