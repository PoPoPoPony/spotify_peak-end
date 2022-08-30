import request from '../../../utils/requestBackend'



export function UpdateSongListScore(songListID, userID, score) {
    var data = JSON.stringify({
        "songListID": songListID,
        "userID": userID,
        "score": score,
    });

    let config = {
        //?userID='+userID + '&songListID='+songListID+'&score='+score
        url: '/songListScore/updateSongListScore',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    return request(config)
}