import request from '../../../utils/requestBackend'


// [deprecate]
// export function UpdateArtistsInfo(artistID, artistName, popularity, genres) {
//     var data = JSON.stringify({
//         "artistID": artistID,
//         "artistName": artistName,
//         "popularity": popularity,
//         "genres": genres
//     });

//     let config = {
//         url: '/artistInfo/updateArtistInfo',
//         method: 'POST',
//         headers: {
//             "Content-Type": "application/json"
//         },
//         data: data
//     }
//     return request(config)
// }

// artist_objs -> {"artistID": {"artistName": name, "popularity": p, "genres": g}}
export function UpdateArtistsInfos(artist_objs) {
    var data = JSON.stringify({
        "artistInfos": JSON.stringify(artist_objs)
    });

    let config = {
        url: '/artistInfo/updateArtistInfos',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    

    return request(config)
}