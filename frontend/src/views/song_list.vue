<template>
    <div>
        <div id='bg'/>
        <el-row justify="center" style="margin-top: 8vh">
            <el-col :span='18'>
                <h2 style="color: white; font-size: 2vw;">
                    播放列表
                </h2>
                <songTable1 v-if="table1Show" :table_data='song_lst' :delete_not_complete='delete_not_complete' :song_not_complete='song_not_complete' @loadSource='loadSource' @delete_song='get_delete_song_lst' @like_change='like_change' @splendid_change='splendid_change' @add_song_change='add_song_change' @completeOneSong="completeOneSongT1"  @play_music='play_music' @pause_music='pause_music' :key='rerender' ref='T1'/>
                <songTable2 v-if="table2Show" :table2Idx='table2Idx' :table_data='table2Current' :delete_not_complete='delete_not_complete' :song_not_complete='song_not_completeT2' @loadSource='loadSource' @delete_song='get_delete_song_lst'  @completeOneSong='completeOneSongT2' @play_music='play_music' @pause_music='pause_music' :key='rerender' ref='T2'/>
            </el-col>
        </el-row>
        <el-row style="margin-top: 20px">
            <el-col :xs="{'span':'8' , 'offset': '3'}" :sm="{'span':'6' , 'offset': '3'}" :lg="{'span': '4', 'offset': '3'}">
                <el-button v-if="deleteShow" style="font-size: 1.3vw" type="danger" size="large" :disabled='!delete_not_complete' @click="on_delete">刪除</el-button>
                <el-button v-if="deleteCompleteShow" style="font-size: 1.3vw" type="primary" :disabled='!delete_not_complete' @click="on_complete_delete">刪除完成</el-button>
                <!-- <span v-if="$store.between_subject_type==1 && !islong" style="color: white; font-size: 25px; padding-left:25px; padding-top:10px">
                    請選擇 3 首歌曲加入歌單
                </span>
                <span v-if="$store.between_subject_type==1 && islong" style="color: white; font-size: 25px; padding-left:25px; padding-top:10px">
                    請選擇 5 首歌曲加入歌單
                </span> -->
            </el-col>
            <el-col :xs="{'span':'1'}" :sm="{'span':'2', 'offset': '2'}" :lg="{'span': '2', 'offset': '4'}">
                <!-- :disabled='!(like_sendable && splendid_sendable && add_song_sendable)' -->
                <el-button v-if="table1Show" type="primary" style="font-size: 1.3vw" @click="send_dialog_visible=true" :disabled='!(T1songScoreSendable && add_song_sendable)'>送出</el-button>
            </el-col>

            <!-- <el-col :span='4' :offset='1'>
                <v-html style="color: white; font-size:30px">目前已將 {{ this.addSongLstLen }} 首歌加入歌單</v-html>
            </el-col> -->


        </el-row>
        <el-row justify="center" style="margin-top: 50px">
            <el-col :span='18'>
                <player v-show="true" v-if="current_song_source!=''" :key='player_rerender' :source='current_song_source' :idx='currentPlayingIdx' @song_listened='song_listened' @song_ended='song_ended' class="animate__animated animate__fadeInUp" ref='player'/>
            </el-col>
        </el-row>

        <!-- delete song double confirm dialog start -->
        <el-dialog v-model="delete_dialog_visible" title="確認刪除" width="30vw" center>
            <span style="font-size: 20px;">
                確認完成刪除?
            </span>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="delete_dialog_visible = false">返 回</el-button>
                    <el-button type="primary" @click="confirm_delete_complete">確 認</el-button>
                </span>
            </template>
        </el-dialog>
        <!-- delete song double confirm dialog end -->

        <!-- send backend confirm dialog start -->
        <el-dialog v-model="send_dialog_visible" width="30vw"  title="確認送出" center>
            <span style="font-size: 20px;">
                確認送出?
            </span>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="send_dialog_visible = false">返 回</el-button>
                    <el-button type="primary" @click="confirm_send">確 認</el-button>
                </span>
            </template>
        </el-dialog>
        <!-- send backend confirm dialog end -->
    </div>
</template>

<script>
// import { song_lst } from '@/utils/test_songs'
import songTable1 from '@/components/song_list/song_table'
import songTable2 from '@/components/song_list/song_table2'
import player from '@/components/song_list/player'
import {GetDiscoverWeekly} from '@/apis/SpotifyAPIs/get_discover_weekly'
import {GetSongList} from '@/apis/SpotifyAPIs/get_song_list'
import {GetRecommendations} from '@/apis/SpotifyAPIs/get_recommendations'
import {GetTopN} from '@/apis/SpotifyAPIs/get_topN'
import {UpdateArtists} from '@/apis/backendAPIs/artists/update_artists'
import {UpdateTracksInfo} from '@/apis/backendAPIs/tracks/update_tracksInfo'
import {UpdateSongListElem} from '@/apis/backendAPIs/songListElem/update_songList_elem'
import {UpdateAudioFeatures} from '@/apis/backendAPIs/audioFeatures/update_audio_features'
import { ElLoading } from 'element-plus'


export default {
    name: 'song_list',
    components: {
        songTable1,
        songTable2,
        player,
    },
    async created(){
        let urlParams = new URLSearchParams(window.location.search)
        this.list_type = urlParams.get('list_type')
        this.tags_obj = JSON.parse(urlParams.get('tags_obj'))
        this.score_obj = JSON.parse(urlParams.get('score_obj'))
        // console.log(this.tags_obj['Genres'])
        // console.log(this.tags_obj['Artists'])
        // console.log(this.tags_obj['Tracks'])

        if(this.$store.state.between_subject_type=="0") {
            // add song column直接設定成可送出，代表不需要add song
            this.add_song_sendable = true
        } else if(this.$store.state.between_subject_type=="1") {
            this.add_song_sendable = false
        }


        if(this.$store.state.between_subject_type=="1") {
            if(this.list_type==0) {
                if(["0", "3"].includes(this.$store.state.within_subject_type)) {
                    this.islong = false
                } else {
                    this.islong = true
                }
            } else {
                if(["1", "2"].includes(this.$store.state.within_subject_type)) {
                    this.islong = false
                } else {
                    this.islong = true
                }
            }
        }


        // list type 決定此頁面會刷weekly discovery的歌單還是seed的歌單
        if(this.list_type == 0) {
            GetDiscoverWeekly(this.$store.state.access_token).then((res)=>{
                console.log("Call GetDiscoverWeekly API successed!")
                let retv = res.data
                console.log(retv)
                this.list_id = retv["playlists"]["items"][0]["id"]
            }).then(() => {
                var promise = []
                promise.push(
                    GetSongList(this.$store.state.access_token, this.list_id).then((res2)=>{
                        console.log("Call GetSongList API successed!")
                        let retv2 = res2.data
                        console.log("retv2", retv2)
                        this.temp_song_lst = retv2.tracks.items.map((elem)=> {
                            return elem.track
                        })
                        
                        
                    }).catch((err)=>{
                        console.log("Call GetSongList API Failed!")
                        console.log(err)
                    })
                )

                Promise.all(promise).then(()=>{
                    var topNpromise=GetTopN(this.$store.state.access_token).then((res)=>{
                        console.log("Call TopN API successed!")
                        let retv = res.data
                        this.temp_song_lst.push(...retv.items)
                    })
                    topNpromise.then(()=>{
                        this.temp_song_lst = this.temp_song_lst.filter(item=>item.preview_url!==null)

                        for(var i=0; i<this.temp_song_lst.length; i++) {
                            var temp_obj = {
                                listened: 0,
                                title: this.temp_song_lst[i].name,
                                artist: this.temp_song_lst[i].artists[0].name,
                                artist_id: this.temp_song_lst[i].artists[0].id,
                                song_id: this.temp_song_lst[i].id,
                                source: "https://open.spotify.com/embed/track/" + this.temp_song_lst[i].id + "?utm_source=generator",
                                song_preview_url: this.temp_song_lst[i].preview_url,
                                like: 0,
                                splendid: 0,
                                add: 0,
                            }
                            // 存下所有歌曲，如果有刪除的歌曲可從這裡補剩下的
                            this.all_song_lst.push(temp_obj)

                            if(i<this.song_limit) {
                                this.song_lst.push(temp_obj)
                            }
                        }
                        console.log(this.song_lst)
                        this.rerender+=1
                    })
                })
                
                
                // Promise.all(promise).then(()=>{
                //     var artistPromise = []
                //     for(var i=0; i<this.temp_song_lst.length; i++) {
                //         let artistObj = this.temp_song_lst[i].track.artists[0]
                //         artistPromise.push(UpdateArtists(artistObj.id, artistObj.name))
                //     }
                //     console.log(artistPromise)
                //     Promise.all(artistPromise).then(()=>{
                //         for(var i=0; i<this.temp_song_lst.length; i++) {
                //             UpdateTracksInfo(this.temp_song_lst[i].track.id, this.temp_song_lst[i].track.name, this.temp_song_lst[i].track.artists[0].id)
                //         }
                //     })
                // })
            })

        } else {
            UpdateAudioFeatures(this.$store.state.userID, this.score_obj)

            // for song list from seeds
            var genres = this.tags_obj['Genres'].join()
            var artists = this.tags_obj['Artists'].join()
            var tracks = this.tags_obj['Tracks'].join()
            var promise = []

            // promise.push(GetRecommendations(this.$store.state.access_token, genres, artists, tracks, this.score_obj, 0).then((res)=>{
            //     console.log("Call GetRecommendations API successed!")
            //     let retv = res.data
            //     console.log("offset 0", retv)
            //     if(retv["tracks"].length>0) {
            //         this.temp_song_lst.push(...retv["tracks"])
            //         ini0 = false
            //     }
            // }))
            
            // promise.push(GetRecommendations(this.$store.state.access_token, genres, artists, tracks, this.score_obj, 50).then((res)=>{
            //     console.log("Call GetRecommendations API successed!")
            //     let retv = res.data
            //     console.log("offset50", retv)
            //     if(retv["tracks"].length>0) {
            //         this.temp_song_lst.push(...retv["tracks"])
            //         ini50 = false
            //     }
                
            // }))

            

            promise.push(await this.WrapGetRecommendations(genres, artists, tracks))
            // promise.push(await this.WrapGetRecommendations(genres, artists, tracks, 50))
            // promise.push(await this.WrapGetRecommendations(genres, artists, tracks, 100))

            Promise.all(promise).then(()=>{
                this.temp_song_lst = this.temp_song_lst.filter(item=>item.preview_url!==null)
                for(var i=0; i<this.temp_song_lst.length; i++) {
                    console.log("songs", this.temp_song_lst[i].name)
                    var temp_obj = {
                        listened: 0,
                        title: this.temp_song_lst[i].name,
                        artist: this.temp_song_lst[i].artists[0].name,
                        song_id: this.temp_song_lst[i].id,
                        artist_id: this.temp_song_lst[i].artists[0].id,
                        source: "https://open.spotify.com/embed/track/" + this.temp_song_lst[i].id + "?utm_source=generator",
                        song_preview_url: this.temp_song_lst[i].preview_url,
                        like: 0,
                        splendid: 0,
                        add: 0,
                    }
                    // 存下所有歌曲，如果有刪除的歌曲可從這裡補剩下的
                    this.all_song_lst.push(temp_obj)

                    if(i<this.song_limit) {
                        this.song_lst.push(temp_obj)
                    }
                }
            })



        




            // for(var s in this.song_lst) {
            //     console.log(s.song_preview_url)
            // }
            // promise.then(()=>{
            //     var artistPromise = []
            //     for(var i=0; i<this.temp_song_lst.length; i++) {
            //         let artistObj = this.temp_song_lst[i].artists[0]
            //         artistPromise.push(UpdateArtists(artistObj.id, artistObj.name))
            //     }
            //     console.log(artistPromise)
            //     Promise.all(artistPromise).then(()=>{
            //         for(var i=0; i<this.temp_song_lst.length; i++) {
            //             UpdateTracksInfo(this.temp_song_lst[i].id, this.temp_song_lst[i].name, this.temp_song_lst[i].artists[0].id)
            //         }
            //     })
            // })
        }

    },
    data() {
        return {
            // 0 for discover weekly
            // 1 for seed
            list_type:0,

            // for player
            current_song_source: '',
            
            // for song_table data
            song_lst: [],
            all_song_lst: [],

            // store song_table return delete song
            delete_lst: [],

            // song_table key
            rerender: 0,

            // need to delete songs first
            delete_not_complete: true,
            song_not_complete: [],
            song_not_completeT2: true,
            deleteShow: true,
            deleteCompleteShow: true,

            delete_dialog_visible: false,

            player_rerender: 0,

            //send backend
            like_sendable: false,
            splendid_sendable: false,
            add_song_sendable: false,
            send_dialog_visible: false,

            // playlist 相關參數
            list_id:'',

            // 測試暫時用3首，之後改成20
            song_limit: 20,
            last_song_pointer: 19,
            tags_obj: {},
            score_obj: {},
            table1Show: true,
            table2Show: false,
            table2Current:[],
            table2Idx: 0,

            //判斷是長/短歌單
            islong: false,

            temp_song_lst: [],
            T1Complete: [],
            T1songScoreSendable: false,
            addSongLstLen:0,
            currentPlayingIdx:-1,
        }
    },
    methods: {
        loadSource(source, idx) {
            this.currentPlayingIdx = idx
            this.current_song_source = source
            this.player_rerender+=1
        },
        play_music(idx) {
            this.currentPlayingIdx = idx
            this.$refs.player.$refs.plyr.player.play()
        },
        pause_music(idx) {
            this.currentPlayingIdx = idx
            this.$refs.player.$refs.plyr.player.pause()
        },
        async on_delete() {
            console.log("len1", this.song_lst.length)
            const loadingInstance = ElLoading.service({
                'lock': false,
                'fullscreen': true,
                'text': 'Fetching data',
                'background': 'rgba(0, 0, 0, 0.7)',
            })

            console.log(loadingInstance)

            var deleteObj = []
            let songListID = ''
            if(this.list_type==0){
                songListID = this.$store.state.WD_ID
            } else {
                songListID = this.$store.state.T_ID
            }

            for(let songIdx of this.delete_lst) {
                console.log(songIdx)
                // console.log(this.all_song_lst[songIdx])

                var elemObj = {
                    'songListID': songListID,
                    'userID': this.$store.state.userID,
                    'trackID': this.song_lst[songIdx]['song_id'],
                    'trackShowType': 'deleted',
                    'splendidScore': -1,
                    'likeScore': -1,
                    'addSongList': false,
                    'order': -1,
                }

                deleteObj.push({
                    'elemObj': elemObj,
                    'artist_id': this.song_lst[songIdx]['artist_id'],
                    'artist': this.song_lst[songIdx]['artist'],
                    'title': this.song_lst[songIdx]['title'],
                })
            }

            let add = []
            

            this.song_lst = await this.song_lst.filter((ele, pos)=>{
                let result = !this.delete_lst.includes(pos)
                if(!result) {
                    this.last_song_pointer+=1
                    add.push(this.all_song_lst[this.last_song_pointer])
                }
                
                return result
            })



            this.delete_lst = []
            this.song_lst.push(...add)

            // this.song_lst.splice(songIdx, 1)
            // this.last_song_pointer+=1
            // console.log("this.last_song_pointer", this.last_song_pointer)
            // this.song_lst.push(this.all_song_lst[this.last_song_pointer])
            
            let all_promise = []
            for(let Obj of deleteObj) {
                var promise = []
                promise.push(await UpdateArtists(Obj['artist_id'], Obj['artist']))
                promise.push(await UpdateTracksInfo(Obj['elemObj']['trackID'], Obj['title'], Obj['artist_id']))

                Promise.all(promise).then(()=> {
                    all_promise.push(UpdateSongListElem(Obj['elemObj']).then((res)=> {
                        let retv = res.data
                        console.log(retv)
                    }))
                })
            }
            
            Promise.all(all_promise).then(()=>{
                loadingInstance.close()
            })

            this.rerender+=1
            
            
        },
        get_delete_song_lst(lst) {
            this.delete_lst = lst
        },
        on_complete_delete() {
            this.delete_dialog_visible = true
        },
        confirm_delete_complete() {
            this.deleteShow = false
            this.deleteCompleteShow = false
            if(this.list_type==0) {
                if(["0", "3"].includes(this.$store.state.within_subject_type)) {
                    this.table1Show = true
                    this.$refs.T1.changeStateOnDeleteComplete()

                    this.table2Show = false
                }
                else {
                    this.table1Show = false
                    this.table2Show = true
                    this.table2Current.push(this.song_lst[0])
                }
            } else {
                if(["0", "3"].includes(this.$store.state.within_subject_type)) {
                    this.table1Show = false
                    this.table2Show = true
                    this.table2Current.push(this.song_lst[0])
                }
                else {
                    this.table1Show = true
                    this.$refs.T1.changeStateOnDeleteComplete()
                    this.table2Show = false
                }
            }
            

            var artistPromise = []
            for(var i=0; i<this.song_lst.length; i++) {
                artistPromise.push(UpdateArtists(this.song_lst[i].artist_id, this.song_lst[i].artist))
            }

            Promise.all(artistPromise).then(()=>{
                for(var i=0; i<this.song_lst.length; i++) {
                    UpdateTracksInfo(this.song_lst[i].song_id, this.song_lst[i].title, this.song_lst[i].artist_id)
                }
            })

            this.song_not_complete = Array(this.song_limit).fill(true)
            this.delete_dialog_visible = false
            this.delete_not_complete = false
            console.log("this.song_lst", this.song_lst)
            // this.rerender+=1
        },
        like_change(like_lst) {
            if(like_lst.includes(0)) {
                this.like_sendable = false
            }
            else {
                for(var i=0; i<like_lst.length; i++) {
                    this.song_lst[i]['like'] = like_lst[i]
                }
                this.like_sendable = true
            }
        },
        splendid_change(splendid_lst) {
            if(splendid_lst.includes(0)) {
                this.splendid_sendable = false
            }
            else {
                for(var i=0; i<splendid_lst.length; i++) {
                    this.song_lst[i]['splendid'] = splendid_lst[i]
                }
                this.splendid_sendable = true
            }
        },

        add_song_change(add_song_lst) {
            this.addSongLstLen = add_song_lst.length
            console.log(add_song_lst)
            // 目前最少選3首
            // if(add_song_lst.length < -1) {
            //     this.add_song_sendable = false
            // }
            // else {
                for(var i=0; i<this.song_lst.length; i++) {
                    if(add_song_lst.indexOf(i)>=0) {
                        this.song_lst[i]['add'] = 1
                    } else {
                        this.song_lst[i]['add'] = 0
                    }
                }
                this.add_song_sendable = true
            // }
        },

        async confirm_send() {
            this.send_dialog_visible = false
            console.log(this.song_lst)

            let songListID = ''
            if(this.list_type==0){
                songListID = this.$store.state.WD_ID
            } else {
                songListID = this.$store.state.T_ID
            }


            for(var i=0; i<this.song_lst.length; i++) {
                var isAdd = false
                if(this.song_lst[i]['add']==0) {
                    isAdd = false
                } else {
                    isAdd = true
                }

                var elemObj = {
                    'songListID': songListID,
                    'userID': this.$store.state.userID,
                    'trackID': this.song_lst[i]['song_id'],
                    'trackShowType': 'onList',
                    'splendidScore': this.song_lst[i]['splendid'],
                    'likeScore': this.song_lst[i]['like'],
                    'addSongList': isAdd,
                    'order': i,
                }
                await UpdateSongListElem(elemObj).then((res)=>{
                    console.log(res)
                })
            }

            

            this.$router.push({
                name: 'list_credit', 
                query: {
                    list_type: this.list_type
                },
            })
        },
        completeOneSongT1() {
            this.T1Complete.push(1)
            if(this.T1Complete.length == this.song_limit) {
                this.T1songScoreSendable = true
            }
        },
        completeOneSongT2(val_lst) {
            this.song_not_completeT2 = true
            var like = val_lst[0]
            var splendid = val_lst[1]
            var isAdd = val_lst[2]

            if(isAdd == true) {
                this.addSongLstLen+=1
            }

            this.song_lst[this.table2Idx]["splendid"] = splendid
            this.song_lst[this.table2Idx]["like"] = like
            this.song_lst[this.table2Idx]["add"] = isAdd
            if(this.table2Idx<this.song_limit-1) {
                this.table2Idx+=1
                this.table2Current[0] = this.song_lst[this.table2Idx]
                this.rerender+=1
            } else {
                this.confirm_send()
            }
        },
        song_listened(idx) {
            if(this.table1Show) {
                this.song_not_complete[idx] = false
            } else {
                this.song_not_completeT2 = false
            }
        },
        song_ended(idx) {
            if(this.table1Show) {
                this.song_not_complete[idx] = false
                this.$refs.T1.song_ended(idx)
            } else {
                this.$refs.T2.song_ended()
            }
        },
        async WrapGetRecommendations(genres, artists, tracks) {
            console.log("-----------------------------")
            let ini = true
            while(ini) {
                let retv = await GetRecommendations(this.$store.state.access_token, genres, artists, tracks, this.score_obj)
                let songs = retv.data["tracks"]
                let names = []
                let ids = []
                for(let g of this.temp_song_lst) {
                    names.push(g.name)
                    ids.push(g.id)
                }
                if(songs.length>0) {
                    songs = songs.filter((ele=>{
                        let res = !(names.includes(ele.name) || ids.includes(ele.id))
                        names.push(ele.name)
                        ids.push(ele.id)
                        return res
                    }))

                    this.temp_song_lst.push(...songs)
                    ini = false
                    return new Promise((resolve, reject) => {
                        if(!ini) {
                            resolve()
                        } else {
                            reject()
                        }
                    })
                }
            }
        },
        
        
    }
}
</script>

<style scoped>
#bg {
    width: 100%;
    height: 100%;
    background: black;
    background-size: cover;
    position: fixed;
    margin: 0;
    top: 0px;
	left: 0px;
    z-index: -100;
}



</style>