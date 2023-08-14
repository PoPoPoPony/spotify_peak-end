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
import {GetUserRecentTrack} from '@/apis/backendAPIs/tracks/get_user_recent_track.js'
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

        
        // let urlParams = new URLSearchParams(window.location.search)
        // this.$store.access_token = urlParams.get('access_token')
        // this.$store.between_subject_type = urlParams.get('between_subject_type')
        // this.$store.within_subject_type = urlParams.get('within_subject_type')
        // if(!this.$store.userID) {
        //     this.$store.userID = urlParams.get('uuid')
        // }

        // console.log("userID", this.$store.userID )


        // getMe(this.$store.state.access_token).then((res)=>{
        //     console.log('call me success')
        //     console.log(res.data)
        // }).catch((err)=>{
        //     console.log('call me faild')
        //     console.log(err)
        // })

        // 獲取最近撥放的歌曲
        // [Deprecate]
        // GetRecentlyPlayed(this.$store.state.access_token).then((res)=>{
        //     console.log("Call GetRecentlyPlayed API successed!")
        //     let retv = res.data
        //     var temp_map = {}
        //     var temp_artist_map = {}
        //     for(var i=0; i<retv["items"].length; i++) {
        //         var track_name = retv["items"][i]["track"]["name"]
        //         var track_id = retv["items"][i]["track"]["id"]
        //         var artist_name = retv["items"][i]["track"]["artists"][0]["name"]
        //         var artist_id = retv["items"][i]["track"]["artists"][0]["id"]
        //         this.related_songs.push(track_id)

        //         if(!(track_name in temp_map)) {
        //             this.recently_played.push([track_name, track_id])
        //             this.recently_played_artistInfo.push([artist_id, artist_name])
        //             // 隨便丟一個值(確認這個track_name有被記錄過而已)
        //             temp_map[track_name] = 0
        //         }

        //         if(!(artist_id in temp_artist_map)) {
        //             this.recently_artist.push([artist_name, artist_id, 1])
        //             // 隨便丟一個值(確認這個artist_name有被記錄過而已)
        //             temp_artist_map[artist_id] = 0
        //         } else {
        //             for(var j=0; j<this.recently_artist.length; j++) {
        //                 if(this.recently_artist[j][1]==artist_id) {
        //                     this.recently_artist[j][2]+=1
        //                 }
        //             }
        //         }
        //     }

        // }).then(()=>{
        //     this.recently_artist.sort((a, b)=> {
        //         return b[2]-a[2]
        //     })

        //     var recently_artist_id = this.recently_artist.map((elem)=> {
        //         return elem[1]
        //     })

        //     var temp_map = {}
        //     for(var i=0; i<recently_artist_id.length; i++) {
        //         temp_map[recently_artist_id[i]]=0
        //     }
        //     var promise = []

        //     for(i=0; i<recently_artist_id.length; i++) {
        //         promise.push(
        //             GetRelatedArtist(this.$store.state.access_token, recently_artist_id[i]).then((res)=>{
        //                 console.log("Call RelatedArtist API successed!")
        //                 let retv = res.data
        //                 var artists = retv["artists"]
        //                 for(var j=0; j<artists.length; j++) {
        //                     var id = artists[j]["id"]
        //                     var name = artists[j]["name"]
        //                     if(!(id in temp_map)) {
        //                         this.recently_artist.push([name, id, 1])
        //                         temp_map[id]=0
        //                     } else {
        //                         for(var k=0; k<this.recently_artist.length; k++) {
        //                             if(this.recently_artist[k][1]==id) {
        //                                 this.recently_artist[k][2]+=1
        //                             }
        //                         }
        //                     }
        //                 }
        //             })
        //         )
        //     }
        //     Promise.all(promise).then(()=>{
        //         // set tags table items
        //         // recently_artist = [[artist_name, artist_id, freq], [artist_name, artist_id, freq], ...]
        //         this.recently_artist.sort((a, b)=> {
        //             return b[2]-a[2]
        //         })

        //         var recently_artist_name = this.recently_artist.map((elem)=> {
        //             return elem[0]
        //         })

        //         this.tags_data[1]['tags'] = recently_artist_name.slice(0, 10)

        //         // recently_played = [[track_name, track_id], [track_name, track_id], ...]
        //         var track_name = this.recently_played.map((elem)=> {
        //             return elem[0]
        //         })

        //         this.tags_data[2]['tags'] = track_name.slice(0, 10)

        //     }).then(()=>{
        //         var recentlyArtistsStr = ""
        //         for(var i=0; i<this.recently_artist.length; i++) {
        //             if(i<50) {
        //                 recentlyArtistsStr+=this.recently_artist[i][1]

        //                 if(i<this.recently_artist.length-1 && i<49) {
        //                     recentlyArtistsStr+=','
        //                 }
        //             }
        //         }
        //         if (recentlyArtistsStr) {
        //             GetSeveralArtists(this.$store.state.access_token, recentlyArtistsStr).then((res)=>{
        //                 let retv = res.data
        //                 var artists = retv['artists']
        //                 for(var i=0; i<artists.length; i++) {
        //                     var genres = artists[i]['genres']
        //                     for(var genre of genres) {
        //                         if(!(genre in this.genre_dict['artist'])) {
        //                             this.genre_dict['artist'][genre]=1
        //                         } else {
        //                             this.genre_dict['artist'][genre]+=1
        //                         }
        //                     }
        //                 }
        //                 var genere_freq_lst = []

        //                 //dict to 2d array
        //                 for(var [key, val] of Object.entries(this.genre_dict['artist'])) {
        //                     genere_freq_lst.push([key, val])
        //                 }

        //                 // sort by genere's frequency
        //                 genere_freq_lst.sort((a, b)=> {
        //                     return b[1]-a[1]
        //                 })

        //                 genere_freq_lst = genere_freq_lst.map((elem=>{
        //                     return elem[0]
        //                 }))
        //                 this.tags_data[0]['tags'] = genere_freq_lst.slice(0, 10)

        //             })
        //         }
                
        //     })

        // })

        // // 取得相關(Related songs)歌曲，以計算歌曲平均物理參數
        // axios.all([this.WrapGetLibraryTracks(), this.WrapGetPlaylistTracks()]).then(axios.spread(()=> {
        //     var top100songs = this.related_songs.slice(0, 100)
        //     // 還有以下參數尚未使用
        //     // time_signature、speechiness、popularity
            // var feature_obj = {
            //     "danceability": [],
            //     "acousticness": [],
            //     "instrumentalness": [],
            //     "energy": [],
            //     "liveness": [],
            //     "key": [],

            //     // 加入loudness 容易推薦不到
            //     // "loudness": [],

            //     // mode的值域怪怪的
            //     // "mode": [],

            //     "tempo": [],
            //     "valence": [],
            // }

            // var limit_obj = {
            //     "danceability": [0, 1],
            //     "acousticness": [0, 1],
            //     "instrumentalness": [0, 1],
            //     "energy": [0, 1],
            //     "liveness": [0, 1],
            //     "key": [0, 11],

            //     // loudness 沒有限制值域
            //     // "loudness": [],

            //     // "mode": [0, 1],
                
            //     // tempo 沒有限制值域

            //     "tempo": [-1000, 1000],
            //     "valence": [0, 1],
            // }

            // if(top100songs.length==0) {
            //     for(i in feature_obj) {
            //         this.score_obj['max_'+i] = limit_obj[i][1]
            //         this.score_obj['min_'+i] = limit_obj[i][0]
                    
            //         if(i=='key') {
            //             this.score_obj['target_'+i] = 5
            //         } else {
            //             this.score_obj['target_'+i] = (limit_obj[i][0] + limit_obj[i][1])/2
            //         }
            //     }
        //         console.log(this.score_obj)
        //     } else {
        //         var audiosString = ''
        //         for(var i=0; i<top100songs.length;i++) {
        //             audiosString+=top100songs[i]
        //             if(i<top100songs.length-1) {
        //                 audiosString+=','
        //             }
        //         }

        //         GetAudiosFeatures(this.$store.state.access_token, audiosString).then((res)=>{
        //             console.log("Call GetAudiosFeatures API successed!")
        //             let retv = res.data
        //             var feature_lst = retv['audio_features']

        //             for(i=0; i<feature_lst.length;i++) {
        //                 for(var j in feature_obj) {
        //                     feature_obj[j].push(feature_lst[i][j])
        //                 }
        //             }
                    // for(i in feature_obj) {
                    //     var statistics = this.getStatistics(feature_obj[i])
                    //     var target_score = statistics['avg']
                    //     var std = statistics['std']
                    //     var min_score = target_score-2*std
                    //     var max_score = target_score+2*std

                    //     if(min_score < limit_obj[i][0]) {
                    //         min_score = limit_obj[i][0]
                    //     }

                    //     if(max_score > limit_obj[i][1]) {
                    //         max_score = limit_obj[i][1]
                    //     }

                    //     // key 只允許整數
                    //     if(i=='key') {
                    //         min_score = parseInt(min_score)
                    //         target_score = parseInt(target_score)
                    //         max_score = parseInt(max_score)
                    //     }

                    //     this.score_obj['max_'+i] = max_score
                    //     this.score_obj['min_'+i] = min_score
                    //     this.score_obj['target_'+i] = target_score
        //             }
        //         })
        //     }

            
        // }))

    },
    methods: {
        // 全部的genere、artist都從最近播放歌曲中獲得，這邊暫時棄用
        // WrapGetFollowedArtist() {
        //     // 獲取使用者追隨的藝人
        //     return GetFollowedArtist(this.$store.state.access_token).then((res)=>{
        //         console.log("Call GetFollowedArtist API successed!")
        //         let retv = res.data
        //         var artist_lst = retv['artists']['items']

        //         if(artist_lst.length>0) {
        //             for(var i=0; i<artist_lst.length; i++) {
        //                 var artist_name = artist_lst[i]["name"]
        //                 var artist_id = artist_lst[i]["id"]
        //                 this.followed_artist.push([artist_name, artist_id])

        //                 var artist_genres = artist_lst[i]["genres"]
        //                 // 若此artist有genre list的話，則循環加入genre_dict["artist"]來計次
        //                 if(artist_genres.length>0) {
        //                     for(var j=0; j<artist_genres.length; j++) {
        //                         // 若此genre已存在於genre_dict["artist"]，則計次+1
        //                         // 否則新建一組key-value表示genre-frequency
        //                         if(artist_genres[j] in this.genre_dict["artist"]) {
        //                             this.genre_dict["artist"][artist_genres[j]]+=1
        //                         } else {
        //                             this.genre_dict["artist"][artist_genres[j]]=1
        //                         }
        //                     }
        //                 }
        //             }
        //         }
        //     })
        // },
        // WrapGetLibraryTracks() {
        //     // 獲取最近撥放的歌曲
        //     return GetLibraryTracks(this.$store.state.access_token).then((res)=>{
        //         console.log("Call GetLibraryTracks API successed!")
        //         let retv = res.data
        //         var items = retv['items']
        //         var tracks_id = []
        //         tracks_id = items.map((elem)=> {
        //             return elem['track']['id']
        //         })
        //         this.related_songs.push(...tracks_id)
        //     })
        // },
        // WrapGetPlaylistTracks() {
        //     // 獲取使用者建立的播放清單
        //     GetUserPlaylists(this.$store.state.access_token).then((res)=>{
        //         console.log("Call GetUserPlaylists API successed!")
        //         let retv = res.data
        //         var items = retv['items']
        //         items = items.map((elem)=>{
        //             return elem['id']
        //         })
        //         this.library_playlist_id.push(...items)
        //     }).then(()=>{
        //         if(this.library_playlist_id.length>0) {
        //             GetPlaylistTracks(this.$store.state.access_token, this.library_playlist_id[0]).then((res)=>{
        //                 console.log("Call GetPlaylistTracks API successed!")
        //                 let retv = res.data
        //                 var items = retv['tracks']['items']
        //                 items = items.map((elem)=> {
        //                     return elem['track']['id']
        //                 })
        //                 this.related_songs.push(...items)
        //             })
        //         }
        //     })
        // },


        // genres
        // recently_artist
        // recently_played

        // async send_tags(obj) {
        //     var send_obj = {
        //         'Genres':[],
        //         'Artists': [],
        //         'Tracks': []
        //     }

        //     var tags_lst = obj['tags_lst']
            
        //     for(var i=0; i<tags_lst.length; i++) {
        //         for(var j=0; j<this.tags_data.length;j++) {
        //             if(this.tags_data[j]['tags'].includes(tags_lst[i])) {
        //                 if(j==0) {
        //                     send_obj[this.tags_data[j]['class']].push(tags_lst[i])
        //                 } else if(j==1) {
        //                     for(var k=0; k<this.recently_artist.length; k++) {
        //                         if(this.recently_artist[k][0]==tags_lst[i]) {
        //                             send_obj[this.tags_data[j]['class']].push(this.recently_artist[k][1])
        //                         }
        //                     }
                            
        //                 } else if(j==2) {
        //                     for(k=0; k<this.recently_played.length; k++) {
        //                         if(this.recently_played[k][0]==tags_lst[i]) {
        //                             send_obj[this.tags_data[j]['class']].push(this.recently_played[k][1])
        //                         }
        //                     }
                            
        //                 }
        //             } 
        //         }
        //     }

        //     var send_backend_lst = []
        //     var send_backend_obj = {}
        //     var allPromise_lst = []

        //     for(i=0; i<this.tags_data.length; i++) {
        //         let c = this.tags_data[i]['class']
        //         for(j=0; j<this.tags_data[i]['tags'].length; j++) {
        //             let tagName = this.tags_data[i]['tags'][j]
        //             let is_selected = false
        //             if(obj['tags_lst'].includes(tagName)) {
        //                 is_selected = true
        //             }
        //             if(c=='Genres') {
        //                 send_backend_obj = {
        //                     'userID': this.$store.state.userID,
        //                     'tagID': tagName,
        //                     'tagType': c,
        //                     'tagFreq': this.genres[j][1],
        //                     'order': -1,
        //                     'tagSelected': is_selected
        //                 }
        //                 send_backend_lst.push(send_backend_obj)
                        
        //             } else if(c=='Artists') {
        //                 let freq = 0
        //                 let id = 0
        //                 for(k=0; k<this.recently_artist.length; k++) {
        //                     if(this.recently_artist[k][0] == tagName) {
        //                         id = this.recently_artist[k][1]
        //                         freq = this.recently_artist[k][2]
        //                         break
        //                     }
        //                 }

        //                 let promiseArtist = await UpdateArtistsInfo(id, tagName).then((res)=>{
        //                     let retv = res.data
        //                     console.log(retv)
        //                     send_backend_obj = {
        //                         'userID': this.$store.state.userID,
        //                         'tagID': id,
        //                         'tagType': c,
        //                         'tagFreq': freq,
        //                         'order': -1,
        //                         'tagSelected': is_selected
        //                     }
        //                 })
        //                 send_backend_lst.push(send_backend_obj)
        //                 allPromise_lst.push(promiseArtist)

        //             } else if(c=='Tracks') {
        //                 await UpdateArtistsInfo(this.recently_played_artistInfo[j][0], this.recently_played_artistInfo[j][1])

        //                 let promiseTrack = await UpdateTracksInfo(this.recently_played[j][1], this.recently_played[j][0], this.recently_played_artistInfo[j][0])

        //                 send_backend_obj = {
        //                     'userID': this.$store.state.userID,
        //                     'tagID': this.recently_played[j][1],
        //                     'tagType': c,
        //                     'tagFreq': -1,
        //                     'order': j,
        //                     'tagSelected': is_selected
        //                 }

        //                 send_backend_lst.push(send_backend_obj)
        //                 allPromise_lst.push(promiseTrack)
        //             }
        //         }
        //     }



        //     var updateTagsPromise = []
        //     Promise.all(allPromise_lst).then(()=>{
        //         for(i=0; i<send_backend_lst.length; i++) {
        //             updateTagsPromise.push(
        //                 UpdateTags(send_backend_lst[i])
        //             )
        //         }
        //     })


        //     Promise.all(updateTagsPromise).then(()=>{
                // UpdateSongListInfo(this.$store.state.userID, 'Tags').then((res)=>{
                //     let retv = res.data
                //     // this.$store.state.T_ID = retv['songListID']
                //     this.$store.dispatch("initT_ID", retv['songListID'])
                //     var t = JSON.stringify(send_obj)
                //     var s = JSON.stringify(this.score_obj)
                //     this.$router.push({
                //         name: 'song_list', 
                //         query: {
                //             list_type: 1,
                //             tags_obj: t,
                //             score_obj: s,
                //         },
                //     })
                // })
        //     })

        // },

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

            let related_artists_retv = []
            for(let artistID of Object.keys(artists)) {
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
            let res = await GetUserRecentTrack(this.$store.state.userID)
            // console.log(res)
            this.recent_tracks_info = await res.data
            // console.log(123, this.recent_tracks_info)
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



