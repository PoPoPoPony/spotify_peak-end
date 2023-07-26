import request from '../../../utils/requestBackend'


// trackIDs -> trackID1,trackID2,...,trackIDN
export function GetTrackInfos(trackIDs) {
    let config = {
        url: '/trackInfo/getTrackInfos?trackIDs='+trackIDs,
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
    }
    

    return request(config)
}