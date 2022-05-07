import request from '../../../utils/requestBackend'



export function UpdateTags(ElemObj) {
    let data = JSON.stringify({
        userID: ElemObj.userID,
        tagID: ElemObj.tagID,
        tagType: ElemObj.tagType,
        tagFreq: ElemObj.tagFreq,
        order: ElemObj.order,
        tagSelected: ElemObj.tagSelected,
    })

    let config = {
        url: '/tags/updateTags',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    

    return request(config)
}