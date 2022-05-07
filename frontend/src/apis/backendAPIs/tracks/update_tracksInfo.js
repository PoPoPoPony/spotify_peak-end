import request from '../../../utils/requestBackend'



export function UpdateTracksInfo(trackID, trackName, artistID) {
    var data = JSON.stringify({
        "trackID": trackID,
        "trackName": trackName,
        "artistID": artistID
    });

    let config = {
        url: '/trackInfo/updateTrackInfo',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    

    return request(config)
}