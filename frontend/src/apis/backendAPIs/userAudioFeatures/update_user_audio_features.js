import request from '../../../utils/requestBackend'



export function UpdateUserAudioFeatures(userID, ElemObj) {
    var data = {}
    for(var n in ElemObj) {
        data[n] = ElemObj[n]
    }

    let config = {
        url: '/userAudioFeatures/updateUserAudioFeatures?userID='+userID + '&score_obj='+JSON.stringify(data),
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
    }
    return request(config)
}