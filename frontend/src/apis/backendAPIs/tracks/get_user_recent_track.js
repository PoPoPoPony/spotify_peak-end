import request from '../../../utils/requestBackend'



export function GetUserRecentTrack(userID) {
    let config = {
        url: '/userRecentTracks/getUserRecentTrack?userID='+userID,
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
    }
    

    return request(config)
}