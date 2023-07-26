import request from '../../../utils/requestBackend'



export function UpdateSongListElem(ElemObj) {
    let data = JSON.stringify({
        songListID: ElemObj.songListID,
        userID: ElemObj.userID,
        trackID: ElemObj.trackID,
        splendidScore: ElemObj.splendidScore,
        likeScore: ElemObj.likeScore,
        addSongList: ElemObj.addSongList,
        order: ElemObj.order,
        beforeListened: ElemObj.beforeListened,
        recommend: ElemObj.recommend
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


export function UpdateSongListElems(elemObjs) {
    var data = JSON.stringify({
        "elems": elemObjs
    });


    let config = {
        url: '/songListElem/updateSongListElems',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data:data
    }
    return request(config)
}