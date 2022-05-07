import request from '../../../utils/requestBackend'



export function UpdateAudioFeatures(userID, ElemObj) {
    var data = {}
    for(var n in ElemObj) {
        data[n] = ElemObj[n]
    }

    let config = {
        url: '/audioFeatures/updateAudioFeatures?userID='+userID + '&score_obj='+JSON.stringify(data),
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
    }
    return request(config)
}