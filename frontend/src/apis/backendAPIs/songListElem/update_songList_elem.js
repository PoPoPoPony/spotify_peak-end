import request from '../../../utils/requestBackend'



export function UpdateSongListElem(ElemObj) {
    let data = JSON.stringify({
        songListID: ElemObj.songListID,
        userID: ElemObj.userID,
        trackID: ElemObj.trackID,
        trackShowType: ElemObj.trackShowType,
        splendidScore: ElemObj.splendidScore,
        likeScore: ElemObj.likeScore,
        addSongList: ElemObj.addSongList,
        order: ElemObj.order,
    })


    let config = {
        url: '/songListElem/updateSongListElem',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data:data
    }
    return request(config)
}