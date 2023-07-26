import request from '../../../utils/requestBackend'



export function UpdateUserRecentTrack(userID, trackID, times) {
    var data = JSON.stringify({
        "userID": userID,
        "trackID": trackID,
        "times": times
    });


    let config = {
        url: '/userRecentTracks/updateUserRecentTrack',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    

    return request(config)
}


// trackIDs -> [ID1, ID2, ..., IDn]
// times -> [time1, time2, ..., timeN]
export function UpdateUserRecentTracks(userID, trackIDs, times) {
    var data = JSON.stringify({
        "userID": userID,
        "trackIDs": trackIDs,
        "times": times
    });


    let config = {
        url: '/userRecentTracks/updateUserRecentTracks',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    

    return request(config)
}