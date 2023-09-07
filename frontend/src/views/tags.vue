<template>
    <div>
        <div id='bg'/>
        <navBar/>
        <h2 style="font-size: 2vw; color: white;">請選擇標籤</h2>
        <div id="tagTable_container">
            <tagTable :table_data='tags_data' :key='rerender' @send_tags='send_tags'/>
        </div>
    </div>
</template>

<script>
import navBar from '@/components/navBar'
import tagTable from '@/components/tag/tag_table'
// import {getMe} from '@/apis/SpotifyAPIs/get_genre'
// import {GetRecentlyPlayed} from '@/apis/SpotifyAPIs/get_recently_played'
// import {GetUserPlaylists} from '@/apis/SpotifyAPIs/get_user_playlists'
// import {GetFollowedArtist} from '@/apis/SpotifyAPIs/get_followed_artist'
// import {GetLibraryTracks} from '@/apis/SpotifyAPIs/get_library_tracks'
// import {GetPlaylistTracks} from '@/apis/SpotifyAPIs/get_playlist_tracks'
// import {GetAudiosFeatures} from '@/apis/SpotifyAPIs/get_audios_features'
import {GetRelatedArtist} from '@/apis/SpotifyAPIs/get_related_artists'
// import {GetSeveralArtists} from '@/apis/SpotifyAPIs/get_several_artists'
import {UpdateSeveralTags} from '@/apis/backendAPIs/tags/update_tags'
import {UpdateArtistsInfos} from '@/apis/backendAPIs/artistsInfo/update_artistsInfo'
// import {UpdateTracksInfo} from '@/apis/backendAPIs/tracks/update_tracksInfo'
import {UpdateSongListInfo} from '@/apis/backendAPIs/songListInfo/update_songList_info'
import {GetUserRecentTracks} from '@/apis/backendAPIs/tracks/get_user_recent_tracks.js'
import {UpdateTagStatus} from '@/apis/backendAPIs/tags/update_tag_status'
import { ElLoading } from 'element-plus'
// import axios from 'axios'


export default {
    name: 'tags',
    components: {
        navBar,
        tagTable,
    },
    data() {
        return {
            recent_tracks_info: 0,

            // 從每個類別找到的genre會存成{genre: frequency}的格式
            // genre_dict: {
            //     "album": {},
            //     "artist": {},
            //     "track": {}
            // },
            genres: [],


            // [artist_name, artist_id] in followed_artist
            // followed_artist: [],
            recently_artist: [],
            recently_played:[],
            // recently_played_artistInfo:[],
            tags_data: [{
                'class': 'Genres',
                'tags': []
            }, {
                'class': 'Artists',
                'tags': []
            }, {
                'class': 'Tracks',
                'tags': []
            }],
            rerender: 0,
            related_songs:[],
            library_playlist_id: [],
            score_obj: {},
        }
    },
    async created() {
        const loadingInstance = ElLoading.service({
            'lock': false,
            'fullscreen': true,
            'text': 'Fetching data',
            'background': 'rgba(0, 0, 0, 0.7)',
        })

        await this.fetchingTags()

        loadingInstance.close()

    },
    methods: {
        getStatistics(numbers, digit=2) {
            const formulaCalc = function formulaCalc(formula, digit) {
                let pow = Math.pow(10, digit);
                return parseInt(formula * pow, 10) / pow;
            };
            let len = numbers.length;
            let sum = (a, b) => formulaCalc(a + b, digit);
            let avg = numbers.reduce(sum) / len;
            let stdDev = Math.sqrt(numbers.map(n=> (n-avg) * (n-avg)).reduce(sum) / len);
            return {
                avg: parseFloat(avg.toFixed(digit)),
                std : parseFloat(stdDev.toFixed(digit))
            }
        },

        async GetTagsData() {
            this.processing_tracks()

            let artists = {}
            for (let i=0; i<this.recent_tracks_info.length; i++) {
                artists[this.recent_tracks_info[i]['artistID']] = {
                    'artistName': this.recent_tracks_info[i]['artistName'],
                    'times': this.recent_tracks_info[i]['times'],
                    'genres': this.recent_tracks_info[i]['genres']
                }
            }

            // [0907 更新] related artist只取前50個artist的realted artist(防止請求過多)
            let related_artists_retv = []
            for(let artistID of Object.keys(artists).slice(0, 50)) {
                let related_artist_retv = await GetRelatedArtist(this.$store.state.access_token, artistID)
                related_artists_retv.push(...related_artist_retv.data['artists'])
            }
            // # artistInfos -> {"artistID": {"artistName": name, "popularity": p, "genres": g}}
            let times = Math.ceil(related_artists_retv.length/50) // 一次post 50個，減輕傳輸壓力
            let promise = []
            for (let t=0; t<times; t++) {
                let sub_related_artists_retv = related_artists_retv.slice(t*50, (t+1)*50)
                let temp_artistInfos = {}
                for (let artistInfo of sub_related_artists_retv) {
                    // await UpdateArtistsInfo(artistInfo['id'], artistInfo['name'], artistInfo['popularity'], artistInfo['genres'].join())
                    temp_artistInfos[artistInfo['id']] = {
                        "artistName": artistInfo['name'],
                        "popularity": artistInfo['popularity'],
                        "genres": artistInfo['genres'].join()
                    }
                }
                promise.push(UpdateArtistsInfos(temp_artistInfos))
            }

            await Promise.all(promise)
            Promise.all([this.processing_artists(artists, related_artists_retv), this.processing_genres(artists, related_artists_retv)]).then(()=>{
                return new Promise((resolve, )=>{resolve()})
            })
        },

        processing_tracks() {
            console.log(456, this.recent_tracks_info)
            let tracks = this.recent_tracks_info.map(x=>[x['trackID'], x['trackName'], x['times']])
            this.recently_played = tracks.sort((a, b)=> {
                return b[2]-a[2]
            }).slice(0, 10)

            this.tags_data[2]['tags'] = this.recently_played.map(x=>x[1])
            return true
        },

        processing_artists(artists, related_artist_retv) {
            // deepcopy
            return new Promise((resolve,) => {
                artists = JSON.parse(JSON.stringify(artists))
                related_artist_retv = JSON.parse(JSON.stringify(related_artist_retv))

                for(let j=0; j<related_artist_retv.length; j++) {
                    let name = related_artist_retv[j]['name']
                    let id = related_artist_retv[j]['id']

                    if(id in artists) {
                        artists[id]['times']+=1
                    } else {
                        artists[id] = {
                            'artistName': name,
                            'times': 1
                        }
                    }
                }

                let artists_lst = []
                Object.keys(artists).forEach(
                    (x) => artists_lst.push([x, artists[x]['artistName'], artists[x]['times']])
                )

                artists_lst = artists_lst.sort((a, b)=> {
                    return b[2]-a[2]
                }).slice(0, 10)

                this.recently_artist = artists_lst
                this.tags_data[1]['tags'] = artists_lst.map(x=>x[1])

                if (this.tags_data[1]['tags'].length==10) {
                    return resolve()
                }
            })
        },

        processing_genres(artists, related_artist_retv) {
            return new Promise((resolve,)=>{
                // deepcopy
                artists = JSON.parse(JSON.stringify(artists))
                related_artist_retv = JSON.parse(JSON.stringify(related_artist_retv))

                let genres = {}
                // processing DB recent tracks' genre
                for (let key of Object.keys(artists)) {
                    let g_lst = artists[key]['genres']
                    let times = artists[key]['times']
                    for (let g of g_lst) {
                        if (g in genres) {
                            genres[g]+=times
                        } else {
                            genres[g]=times
                        }
                    }
                }

                // processing related artists' genre
                for(let j=0; j<related_artist_retv.length; j++) {
                    let g_lst = related_artist_retv[j]['genres']

                    for (let g of g_lst) {
                        if (g in genres) {
                            genres[g]+=1
                        } else {
                            genres[g]=1
                        }
                    }
                }
                let genres_lst = []
                Object.keys(genres).forEach(
                    (x) => genres_lst.push([x, genres[x]])
                )

                genres_lst = genres_lst.sort((a, b)=> {
                    return b[1]-a[1]
                }).slice(0, 10)

                this.genres = genres_lst
                this.tags_data[0]['tags'] = genres_lst.map(x=>x[0])
                if (this.tags_data[0]['tags'].length==10) {
                    return resolve()
                }
            })
            
        },

        GetUserAudioFeatures() {
            var feature_obj = {
                "danceability": [],
                "acousticness": [],
                "instrumentalness": [],
                "energy": [],
                "liveness": [],
                "key": [],
                "tempo": [],
                "valence": [],
            }
            // [lower bound, upper bound]
            var limit_obj = {
                "danceability": [0, 1],
                "acousticness": [0, 1],
                "instrumentalness": [0, 1],
                "energy": [0, 1],
                "liveness": [0, 1],
                "key": [0, 11],
                "tempo": [-1000, 1000],
                "valence": [0, 1],
            }

            // if 近3個月沒有撥放紀錄
            if(this.recent_tracks_info.length==0) {
                for(let i in feature_obj) {
                    this.score_obj['max_'+i] = limit_obj[i][1]
                    this.score_obj['min_'+i] = limit_obj[i][0]
                    
                    if(i=='key') {
                        this.score_obj['target_'+i] = 5
                    } else {
                        this.score_obj['target_'+i] = (limit_obj[i][0] + limit_obj[i][1])/2
                    }
                }
            } else {
                for (let trackInfo of this.recent_tracks_info) {
                    for (let key of Object.keys(feature_obj)) {
                        let times = trackInfo['times']
                        // push audio feature "times" 次
                        Array(times).fill().map(()=>feature_obj[key].push(trackInfo[key]))
                    }
                }
                for(let i in feature_obj) {
                    var statistics = this.getStatistics(feature_obj[i])
                    var target_score = statistics['avg']
                    var std = statistics['std']

                    // var target_score = null
                    // var min_score = target_score
                    // var max_score = target_score

                    // [07/25] 改為正負一倍標準差
                    var min_score = target_score-std
                    var max_score = target_score+std

                    if(min_score < limit_obj[i][0]) {
                        min_score = limit_obj[i][0]
                    }

                    if(max_score > limit_obj[i][1]) {
                        max_score = limit_obj[i][1]
                    }

                    // key 只允許整數
                    if(i=='key') {
                        min_score = parseInt(min_score)
                        target_score = parseInt(target_score)
                        max_score = parseInt(max_score)
                    }

                    this.score_obj['max_'+i] = max_score
                    this.score_obj['min_'+i] = min_score
                    this.score_obj['target_'+i] = target_score
                }
            }
        },

        UpdateDefaultTags() {
            // update genres tags
            let temp_genres = []
            let temp_artist = []
            let temp_tracks = []
            for (let i=0; i<this.genres.length; i++) {
                let elem = {
                    'userID': this.$store.state.userID,
                    'tagID': this.genres[i][0],
                    'tagType': "genre",
                    'tagFreq': this.genres[i][1],
                    'order': i,
                    'tagSelected': false
                }
                temp_genres.push(elem)
            }
            
            // update artist tags
            for (let i=0; i<this.recently_artist.length; i++) {
                let elem = {
                    'userID': this.$store.state.userID,
                    'tagID': this.recently_artist[i][0],
                    'tagType': "artist",
                    'tagFreq': this.recently_artist[i][2],
                    'order': i,
                    'tagSelected': false
                }
                temp_artist.push(elem)
            }

            // update track tags
            for (let i=0; i<this.recently_played.length; i++) {
                let elem = {
                    'userID': this.$store.state.userID,
                    'tagID': this.recently_played[i][0],
                    'tagType': "track",
                    'tagFreq': this.recently_played[i][2],
                    'order': i,
                    'tagSelected': false
                }
                temp_tracks.push(elem)
            }
            UpdateSeveralTags(temp_genres)
            UpdateSeveralTags(temp_artist)
            UpdateSeveralTags(temp_tracks)
        },
        async send_tags(obj) {
            var tag_lst = obj['tags_lst']
            var send_obj = {
                'Tracks': [],
                'Artists': [],
                'Genres': []
            }
            
            // [trackName, trackName, ...], [artistName, artistName, ...]
            let temp_tracks = this.recently_played.map((x)=>x[1])
            let temp_artists = this.recently_artist.map((x)=>x[1])

            for (let tagID of tag_lst) {
                // 標籤是Name，但推薦需要傳ID
                // 找不到時，indexOf回傳-1
                let tracks_i = temp_tracks.indexOf(tagID)
                let artists_i = temp_artists.indexOf(tagID)
                let id=''
                // 紀錄tagName對應的tagID
                
                if (tracks_i>=0) {
                    id=this.recently_played[tracks_i][0]
                    send_obj["Tracks"].push(id)
                } else if (artists_i>=0) {
                    id=this.recently_artist[artists_i][0]
                    send_obj["Artists"].push(id)
                } else {
                    // genre的tagName=tagID
                    id=tagID
                    send_obj["Genres"].push(id)
                }
                await UpdateTagStatus(this.$store.state.userID, id)
            }
            UpdateSongListInfo(this.$store.state.userID, 'Tags', this.$store.state.period).then((res)=>{
                let retv = res.data
                // this.$store.state.T_ID = retv['songListID']
                this.$store.dispatch("initT_ID", retv['songListID'])
                var t = JSON.stringify(send_obj)
                var s = JSON.stringify(this.score_obj)
                this.$router.push({
                    name: 'song_list', 
                    query: {
                        list_type: 1,
                        tags_obj: t,
                        score_obj: s,
                    },
                })
            })
        },
        async fetchingTags() {
            let res = await GetUserRecentTracks(this.$store.state.userID)
            this.recent_tracks_info = await res.data
            await this.GetTagsData()

            this.GetUserAudioFeatures()
            this.UpdateDefaultTags()
        }
        
    },
}
</script>

<style scoped>
#bg {
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, #72BFE6 0%, #46277A 100%);
    background-size: cover;
    position: fixed;
    margin: 0;
    top: 0px;
	left: 0px;
    z-index: -100;
}


#tagTable_container {
    margin-left: 15%;
    width: 70%
}

</style>



