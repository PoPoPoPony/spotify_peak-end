import request from '../../../utils/requestBackend'



export function UpdateUserSavedTracks(userID, trackIDs) {
    var data = JSON.stringify({
        "userID": userID,
        "trackIDs": trackIDs,
    });


    let config = {
        url: '/userSavedTracks/updateUserSavedTracks',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    

    return request(config)
}