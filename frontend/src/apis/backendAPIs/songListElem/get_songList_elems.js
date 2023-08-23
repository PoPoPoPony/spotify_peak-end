import request from '../../../utils/requestBackend'



export function GetSongListElems(songListID, order) {
    let config = {
        url: '/songListElem/getSongListElems',
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
        params: {
            'songListID': songListID,
            'ruleType': 'likeScore',
            'order': order
        }
    }
    return request(config)
}