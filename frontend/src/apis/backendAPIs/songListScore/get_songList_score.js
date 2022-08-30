import request from '../../../utils/requestBackend'


export function GetSongListScoreLen(userID) {
    // var data = JSON.stringify({
    //     "userID": userID,
    // });

    let config = {
        url: '/songListScore/getSongListScoreLen?userID='+userID,
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
        // data: data
    }
    return request(config)
}