import request from '../../../utils/requestBackend'



export function GetSongListElem(songListID, order) {
    let config = {
        url: '/songListElem/getSongListElem',
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
        params: {
            'songListID': songListID,
            'order': order
        }
    }
    return request(config)
}