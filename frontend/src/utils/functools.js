import {GetAudiosFeatures} from '@/apis/SpotifyAPIs/get_audios_features'
import {GetSeveralArtists} from '@/apis/SpotifyAPIs/get_several_artists'
// import {UpdateArtistsInfo} from '@/apis/backendAPIs/artistsInfo/update_artistsInfo'
import {UpdateArtistsInfos} from '@/apis/backendAPIs/artistsInfo/update_artistsInfo'
// import {UpdateTracksInfo} from '@/apis/backendAPIs/tracks/update_tracksInfo'
import {UpdateTrackInfos} from '@/apis/backendAPIs/tracks/update_trackInfos'


export async function UpdateBasicInfo(access_token, objs) {
    let times = Math.ceil(objs.length/50)
    for (let t=0; t<times; t++) {
        let sub_objs = objs.slice(t*50, (t+1)*50)
        let song_ids = sub_objs.map(x=>x.song_id)
        let song_ids_str = song_ids.join(',')

        let titles = sub_objs.map(x=>x.title)
        let tracks_popularity = sub_objs.map(x=>x.track_popularity)
        let song_preview_urls = sub_objs.map(x=>x.song_preview_url)

        let retv = await GetAudiosFeatures(access_token, song_ids_str)
        retv = retv.data['audio_features']
        let audio_features = []

        for (let r of retv) {
            r['timeSignature'] = r['time_signature']
            // eslint-disable-next-line no-unused-vars
            let {analysis_url, duration_ms, id, track_href, type, uri, time_signature, ...audio_feature} = r
            audio_features.push(audio_feature)
        }

        let artist_ids = sub_objs.map(x=>x.artist_id)
        let artist_ids_str = artist_ids.join(',')
        let artist_names = sub_objs.map(x=>x.artist)
        retv = await GetSeveralArtists(access_token, artist_ids_str)
        retv = retv.data['artists']

        let artists_popularity = []
        let artists_genres = []

        for (let r of retv) {
            artists_popularity.push(r["popularity"])
            artists_genres.push(r["genres"].join())
        }

        // for (let i in artist_ids) {
        //     await UpdateArtistsInfo(artist_ids[i], artist_names[i], artists_popularity[i], artists_genres[i])
        // }

        let artist_objs = {}
        let track_objs = {}

        for (let i in artist_ids) {
            artist_objs[artist_ids[i]] = {
                "artistName": artist_names[i],
                "popularity": artists_popularity[i],
                "genres": artists_genres[i]
            }
        }

        for (let i in song_ids) {
            let infos = {}
            Object.assign(
                infos,
                {
                    "trackName": titles[i],
                    "artistID": artist_ids[i],
                    "popularity": tracks_popularity[i],
                    "preview": song_preview_urls[i]
                }, 
                audio_features[i]
            )
            track_objs[song_ids[i]] = infos
        }

        await UpdateArtistsInfos(artist_objs)

        

        // for (let i in song_ids) {
        //     await UpdateTracksInfo(song_ids[i], titles[i], artist_ids[i], tracks_popularity[i], audio_features[i], song_preview_urls[i])
        // }

        await UpdateTrackInfos(track_objs)
    }
}