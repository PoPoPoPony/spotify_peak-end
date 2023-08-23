import request from '../../../utils/requestBackend'


// [deprecate]
// export function UpdateTracksInfo(trackID, trackName, artistID, popularity, audio_features, preview) {
//     var data = JSON.stringify(Object.assign(
//         {},
//         {
//             "trackID": trackID,
//             "trackName": trackName,
//             "artistID": artistID,
//             "popularity": popularity,
//             "preview": preview
//         }, 
//         audio_features
//     ));


//     let config = {
//         url: '/trackInfo/updateTrackInfo',
//         method: 'POST',
//         headers: {
//             "Content-Type": "application/json"
//         },
//         data: data
//     }
    

//     return request(config)
// }



// tracksInfos -> {"trackID": {"trackName": name, ...}}
export function UpdateTrackInfos(tracksInfos) {
    var data = JSON.stringify({
        'tracksInfos': JSON.stringify(tracksInfos)
    })



    let config = {
        url: '/trackInfo/updateTrackInfos',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    

    return request(config)
}