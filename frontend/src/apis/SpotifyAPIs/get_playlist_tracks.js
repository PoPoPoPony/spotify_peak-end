import request from '../../utils/request'

export function GetPlaylistTracks(accessToken, playlist_id) {
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/playlists/'+playlist_id,
        method: 'GET',
        params: {
            fields: "tracks.items.track.id"
        }
    }

    return request(config)
}