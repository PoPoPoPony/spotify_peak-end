import request from '../../../utils/requestBackend'


// [deprecate]
// export function UpdateTags(ElemObj) {
//     let data = JSON.stringify({
//         userID: ElemObj.userID,
//         tagID: ElemObj.tagID,
//         tagType: ElemObj.tagType,
//         tagFreq: ElemObj.tagFreq,
//         order: ElemObj.order,
//         tagSelected: ElemObj.tagSelected,
//     })

//     let config = {
//         url: '/tags/updateTags',
//         method: 'POST',
//         headers: {
//             "Content-Type": "application/json"
//         },
//         data: data
//     }
    

//     return request(config)
// }


export function UpdateSeveralTags(ElemObjs) {
    let data = JSON.stringify({
        'tags': ElemObjs
    })

    let config = {
        url: '/tags/updateSeveralTags',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    

    return request(config)
}