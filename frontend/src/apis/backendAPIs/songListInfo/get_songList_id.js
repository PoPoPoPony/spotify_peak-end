import request from '../../../utils/requestBackend'



export function GetSongListID(userID, listType, period) {
    let config = {
        url: '/songListInfo/getSongListID',
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
        params:{
            'userID': userID,
            'listType': listType,
            'period': period
        }
    }
    return request(config)
}