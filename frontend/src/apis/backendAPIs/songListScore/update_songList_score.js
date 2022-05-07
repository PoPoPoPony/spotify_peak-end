import request from '../../../utils/requestBackend'



export function UpdateSongListScore(songListID, score) {
    var data = JSON.stringify({
        "songListID": songListID,
        "score": score,
    });

    let config = {
        url: '/songListScore/updateSongListScore',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    return request(config)
}