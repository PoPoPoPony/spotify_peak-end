import request from '../../../utils/requestBackend'



export function GetSongListElem(songListID) {
    let config = {
        url: '/songListElem/getSongListElem',
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
        params: {
            'songListID': songListID
        }
    }
    return request(config)
}