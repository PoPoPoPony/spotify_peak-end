import request from '../../../utils/requestBackend'



export function GetSongListInfo(userID, listType) {
    let config = {
        url: '/songListInfo/getSongListInfo',
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
        params:{
            'userID': userID,
            'listType': listType
        }
    }
    return request(config)
}