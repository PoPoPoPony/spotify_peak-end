import request from '../../../utils/requestBackend'



export function UpdateSongListScore(songListID, userID, satisfyScore, diversityScore, noveltyScore) {
    var data = JSON.stringify({
        "songListID": songListID,
        "userID": userID,
        "satisfyScore": satisfyScore,
        "diversityScore": diversityScore,
        "noveltyScore": noveltyScore
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