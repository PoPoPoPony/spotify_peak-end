import request from '../../../utils/requestBackend'



export function UpdateSongListInfo(userID, listType) {
    let config = {
        url: '/songListInfo/updateSongListInfo?userID='+userID+'&listType='+listType,
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
    }
    return request(config)
}