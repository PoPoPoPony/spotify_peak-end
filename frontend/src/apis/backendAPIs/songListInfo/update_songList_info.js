import request from '../../../utils/requestBackend'



export function UpdateSongListInfo(userID, listType, period) {
    let config = {
        url: '/songListInfo/updateSongListInfo?userID='+userID+'&listType='+listType+'&period='+period,
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
    }
    return request(config)
}