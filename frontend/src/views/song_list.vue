<template>
    <div>
        <div id='bg'/>
        <el-row justify="center" style="margin-top: 8vh">
            <el-col :span='18'>
                <h2 style="color: white; font-size: 2vw;">
                    播放列表
                </h2>
                <songTable1 v-if="table1Show" :table_data='song_lst'  :song_not_complete='song_not_complete' @loadSource='loadSource' @before_listened_change="before_listened_change" @like_change='like_change' @splendid_change='splendid_change' @add_song_change='add_song_change' @completeOneSong="completeOneSongT1"  @play_music='play_music' @pause_music='pause_music' :key='rerender' ref='T1'/>
                <songTable2 v-if="table2Show" :table_data='table2Current' :added_max="addSongLstLen==max_added_count"  :song_not_complete='song_not_completeT2' @loadSource='loadSource' @completeOneSong='completeOneSongT2' @play_music='play_music' @pause_music='pause_music' :key='rerender' ref='T2'/>
            </el-col>
        </el-row>
        <el-row style="margin-top: 20px">
            <el-col :xs="{'span':'5', 'offset': '10'}" :sm="{'span':'2', 'offset': '11'}" :lg="{'span': '2', 'offset': '11'}">
                <el-button v-if="table1Show" type="primary" style="font-size: 1.3vw" @click="send_dialog_visible=true" :disabled='!(T1songScoreSendable && add_song_sendable)'>送出</el-button>
            </el-col>
        </el-row>
        <el-row justify="end" style="margin-top: 50px">
            <el-col :span='12'>
                <player v-show="true" v-if="current_song_source!=''" :key='player_rerender' :source='current_song_source' :isAuto="false" :idx='currentPlayingIdx' @song_listened='song_listened' @song_ended='song_ended' class="animate__animated animate__fadeInUp" ref='player'/>
            </el-col>
            <el-col :span='4'>
                <el-affix v-if="hint_show" position="bottom" :offset="20">
                    <div id="hint" type="success">已收藏 {{ addSongLstLen }} 首</div>
                </el-affix>
            </el-col>
        </el-row>
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

        <!-- TEST BTN -->
        <!-- <el-button @click="TEST_T1">Fill Data</el-button> -->
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
import {UpdateSongListElems} from '@/apis/backendAPIs/songListElem/update_songList_elem'
import {UpdateUserAudioFeatures} from '@/apis/backendAPIs/userAudioFeatures/update_user_audio_features'
import {UpdateBasicInfo} from '@/utils/functools'
import {ElLoading} from 'element-plus'


export default {
    name: 'song_list',
    components: {
        songTable1,
        songTable2,
        player,
    },
    async created(){
        const loadingInstance = ElLoading.service({
            'lock': false,
            'fullscreen': true,
            'text': 'Fetching data',
            'background': 'rgba(0, 0, 0, 0.7)',
        })

        let urlParams = new URLSearchParams(window.location.search)
        this.list_type = urlParams.get('list_type')
        this.tags_obj = JSON.parse(urlParams.get('tags_obj'))
        this.score_obj = JSON.parse(urlParams.get('score_obj'))

        if(this.$store.state.between_subject_type=="0") {
            // add song column直接設定成可送出，代表不需要add song
            this.add_song_sendable = true
            this.hint_show = false
        } else if(this.$store.state.between_subject_type=="1") {
            this.add_song_sendable = false
            this.hint_show = true
        }

        if(this.list_type==0) {
            if(["0", "3"].includes(this.$store.state.within_subject_type)) {
                this.table1Show = true
                this.table2Show = false
            }
            else {
                this.table1Show = false
                this.table2Show = true
            }
        } else {
            if(["0", "3"].includes(this.$store.state.within_subject_type)) {
                this.table1Show = false
                this.table2Show = true
            }
            else {
                this.table1Show = true
                this.table2Show = false
            }
        }

        let keys = Array(20).fill("song_lst_elem").map((x, i)=>x+i.toString())
        let result = keys.filter((x)=>this.$cookies.get(x) != null)

        // if all song store in the cookies
        if (result.length == this.song_limit) {
            await this.fetching_cookies()
        } else {
            await this.GetSongListFromSpotifyAPI()
        }



        loadingInstance.close()
        // 正式時需用true，測試時用false
        // this.song_not_complete = Array(this.song_limit).fill(false)
        // this.song_not_complete = Array(this.song_limit).fill(true)
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

            // song_table key
            rerender: 0,

            song_not_complete: [],
            song_not_completeT2: true,

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

            temp_song_lst: [],
            T1songScoreSendable: false,
            addSongLstLen:0,
            currentPlayingIdx:-1,
            hint_show: false,
            max_added_count: 20,
            recommend_from_tags_ua_length: 0,
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
        before_listened_change(before_listened_lst) {
            for(var i=0; i<this.song_lst.length; i++) {
                if(before_listened_lst.indexOf(i)>=0) {
                    this.song_lst[i]['before_listened'] = 1
                } else {
                    this.song_lst[i]['before_listened'] = 0
                }
            }
        },
        add_song_change(add_song_lst) {
            this.addSongLstLen = add_song_lst.length

            for(var i=0; i<this.song_lst.length; i++) {
                if(add_song_lst.indexOf(i)>=0) {
                    this.song_lst[i]['add'] = 1
                } else {
                    this.song_lst[i]['add'] = 0
                }
            }
            this.add_song_sendable = true
        },
        async confirm_send() {
            this.send_dialog_visible = false
            let recommend_lst = []


            let songListID = ''
            if(this.list_type==0){
                songListID = this.$store.state.WD_ID
                recommend_lst = Array(this.song_lst.length).fill("WD") // WD沒有細分，所以全部都放WD
            } else {
                songListID = this.$store.state.T_ID
                recommend_lst = Array(this.recommend_from_tags_ua_length).fill("T_A")
                if (this.recommend_from_tags_ua_length<this.song_lst.length) {
                    recommend_lst.push(...Array(this.song_lst.length-this.recommend_from_tags_ua_length).fill("T"))
                }
            }

            // [07/25 新增recommend: WD / T (only from tags) / T_A (from tags and user audio features)]
            let temp_elem = []
            for(var i=0; i<this.song_lst.length; i++) {
                var isAdd = false
                if(this.song_lst[i]['add']==0) {
                    isAdd = false
                } else {
                    isAdd = true
                }

                var isBeforeListened = false
                if(this.song_lst[i]['before_listened']==0) {
                    isBeforeListened = false
                } else {
                    isBeforeListened = true
                }

                var elemObj = {
                    'songListID': songListID,
                    'userID': this.$store.state.userID,
                    'trackID': this.song_lst[i]['song_id'],
                    'splendidScore': this.song_lst[i]['splendid'],
                    'likeScore': this.song_lst[i]['like'],
                    'addSongList': isAdd,
                    'order': i,
                    'beforeListened': isBeforeListened,
                    'recommend': recommend_lst[i]
                }
                // await UpdateSongListElem(elemObj)
                temp_elem.push(elemObj)
            }
            await UpdateSongListElems(temp_elem)
            this.$router.push({
                name: 'list_credit', 
                query: {
                    list_type: this.list_type
                },
            })
        },
        completeOneSongT1(idx) {
            if(this.song_not_complete.indexOf(true)==-1) {
                this.T1songScoreSendable = true
            }
            this.$cookies.set("song_lst_elem"+idx.toString(), this.song_lst[idx])
        },
        completeOneSongT2(val_lst) {
            var like = val_lst[0]
            var splendid = val_lst[1]
            var isAdd = val_lst[2]
            var isBeforeListened = val_lst[3]

            if(isAdd == true) {
                this.addSongLstLen+=1
            }

            this.song_lst[this.table2Idx]["splendid"] = splendid
            this.song_lst[this.table2Idx]["like"] = like
            this.song_lst[this.table2Idx]["add"] = isAdd
            this.song_lst[this.table2Idx]["before_listened"] = isBeforeListened
            this.$cookies.set("song_lst_elem"+this.table2Idx.toString(), this.song_lst[this.table2Idx])

            if(this.table2Idx<this.song_limit-1) {
                this.table2Idx+=1
                this.table2Current[0] = this.song_lst[this.table2Idx]
                this.song_not_completeT2 = true
                this.rerender+=1
            } else {
                this.confirm_send()
            }
        },

        // player 聆聽完畢後觸發
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
        async WrapGetRecommendations(genres, artists, tracks, score_obj) {
            console.log("-----------------------------")
            let ini = true
            while(ini) {
                let retv = await GetRecommendations(this.$store.state.access_token, genres, artists, tracks, score_obj)
                let songs = retv.data["tracks"]
                console.log(retv.data)
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
                } else {
                    // didnt have any song
                    return new Promise((resolve, ) => {
                        resolve()
                    })
                }
            }
        },

        async fetching_cookies() {
            if (this.table1Show) {
                let cookie_song_lst=[]
                for (let i=0; i<this.song_limit; i++) {
                    let song = this.$cookies.get('song_lst_elem'+i.toString())
                    if (song.like>0 && song.splendid>0) {
                        this.song_not_complete.push(false)
                    } else {
                        this.song_not_complete.push(true)
                    }
                    cookie_song_lst.push(song)
                }
                this.song_lst = cookie_song_lst
                this.like_change(cookie_song_lst.map(x=>x.like))
                this.splendid_change(cookie_song_lst.map(x=>x.splendid))
                this.addSongLstLen = this.song_lst.map(x=>x.add).filter(x=>x==1).length
                if(this.song_not_complete.indexOf(true)==-1) {
                    this.T1songScoreSendable = true
                }

                this.rerender+=1

            } else if (this.table2Show) {
                this.song_lst = Array(20).fill("song_lst_elem").map((x, i)=>this.$cookies.get(x+i.toString()))

                let like_not_idx = this.song_lst.map(x=>x.like).indexOf(0)
                let splendid_not_idx = this.song_lst.map(x=>x.splendid).indexOf(0)
                this.addSongLstLen = this.song_lst.map(x=>x.add).filter(x=>x==1).length

                let min_idx = Math.min(like_not_idx, splendid_not_idx)

                if (min_idx == -1) {
                    this.confirm_send()
                } else {
                    this.table2Current.push(this.song_lst[min_idx])
                    this.song_not_completeT2 = true
                    this.table2Idx=min_idx
                }
            }


        },

        async GetSongListFromSpotifyAPI() {
            // list type 決定此頁面會刷weekly discovery的歌單還是seed的歌單
            if(this.list_type == 0) {
                GetDiscoverWeekly(this.$store.state.access_token).then((res)=>{
                    // console.log("Call GetDiscoverWeekly API successed!")
                    let retv = res.data
                    // console.log(retv)
                    this.list_id = retv["playlists"]["items"][0]["id"]
                }).then(() => {
                    var promise = []
                    promise.push(
                        GetSongList(this.$store.state.access_token, this.list_id).then((res2)=>{
                            // console.log("Call GetSongList API successed!")
                            let retv2 = res2.data
                            // console.log("retv2", retv2)
                            this.temp_song_lst = retv2.tracks.items.map((elem)=> {
                                return elem.track
                            })
                        }).catch((err)=>{
                            console.log("Call GetSongList API Failed!")
                            console.log(err)
                        })
                    )

                    Promise.all(promise).then(()=>{
                        // Weekly discovery不足時，用topN補足
                        var topNpromise=GetTopN(this.$store.state.access_token).then((res)=>{
                            // console.log("Call TopN API successed!")
                            let retv = res.data
                            this.temp_song_lst.push(...retv.items)
                        })

                        // 從API收集完所有的歌後
                        topNpromise.then(()=>{
                            this.temp_song_lst = this.temp_song_lst.filter(item=>item.preview_url!==null)
                            for(var i=0; i<this.temp_song_lst.length; i++) {
                                var temp_obj = {
                                    before_listened: 0,
                                    title: this.temp_song_lst[i].name,
                                    artist: this.temp_song_lst[i].artists[0].name,
                                    artist_id: this.temp_song_lst[i].artists[0].id,
                                    song_id: this.temp_song_lst[i].id,
                                    source: "https://open.spotify.com/embed/track/" + this.temp_song_lst[i].id + "?utm_source=generator",
                                    song_preview_url: this.temp_song_lst[i].preview_url,
                                    like: 0,
                                    splendid: 0,
                                    add: 0,
                                    track_popularity: this.temp_song_lst[i].popularity
                                }
                                // 存下所有歌曲，如果有刪除的歌曲可從這裡補剩下的
                                this.all_song_lst.push(temp_obj)
                                if(i<this.song_limit) {
                                    this.song_lst.push(temp_obj)
                                    this.$cookies.set("song_lst_elem"+i.toString(), temp_obj)
                                    this.song_not_complete.push(true) // for song_table.vue
                                }
                            }
                            UpdateBasicInfo(this.$store.state.access_token, this.song_lst)
                            if (this.table2Show) {
                                this.table2Current.push(this.song_lst[0])
                            }
                            this.rerender+=1
                        })
                    })
                })
            } else {
                await UpdateUserAudioFeatures(this.$store.state.userID, this.score_obj)

                // for song list from seeds
                var genres = this.tags_obj['Genres'].join()
                var artists = this.tags_obj['Artists'].join()
                var tracks = this.tags_obj['Tracks'].join()
                var promise = []

                // promise.push(await this.WrapGetRecommendations(genres, artists, tracks))
                promise.push(this.WrapGetRecommendations(genres, artists, tracks, this.score_obj))
                await Promise.all(promise)
                this.temp_song_lst = this.temp_song_lst.filter(item=>item.preview_url!==null)
                this.recommend_from_tags_ua_length = this.temp_song_lst.length
                // Promise.all(promise).then(()=>{
                //     this.temp_song_lst = this.temp_song_lst.filter(item=>item.preview_url!==null)
                //     this.recommend_from_tags_ua_length = this.temp_song_lst.length
                // })
                console.log("this.recommend_from_tags_ua_length", this.recommend_from_tags_ua_length)
                if (this.recommend_from_tags_ua_length<this.song_limit) {
                    // 若加上user audio features的歌曲數量不足時
                    console.log("this.recommend_from_tags_ua_length", this.recommend_from_tags_ua_length)
                    let null_score_obj = {}
                    for (let key in this.score_obj) {
                        null_score_obj[key] = null // 推薦時不使用user audio features而已，資料庫仍然會儲存資訊
                    }
                    promise = []
                    promise.push(this.WrapGetRecommendations(genres, artists, tracks, null_score_obj))
                    await Promise.all(promise)
                }
                this.temp_song_lst = this.temp_song_lst.filter(item=>item.preview_url!==null)
                for(var i=0; i<this.temp_song_lst.length; i++) {
                    console.log("songs", this.temp_song_lst[i].name)
                    var temp_obj = {
                        before_listened: 0,
                        title: this.temp_song_lst[i].name,
                        artist: this.temp_song_lst[i].artists[0].name,
                        song_id: this.temp_song_lst[i].id,
                        artist_id: this.temp_song_lst[i].artists[0].id,
                        source: "https://open.spotify.com/embed/track/" + this.temp_song_lst[i].id + "?utm_source=generator",
                        song_preview_url: this.temp_song_lst[i].preview_url,
                        like: 0,
                        splendid: 0,
                        add: 0,
                        track_popularity: this.temp_song_lst[i].popularity
                    }
                    // 存下所有歌曲，如果有刪除的歌曲可從這裡補剩下的
                    this.all_song_lst.push(temp_obj)

                    if(i<this.song_limit) {
                        this.song_lst.push(temp_obj)
                        this.$cookies.set("song_lst_elem"+i.toString(), temp_obj)
                        this.song_not_complete.push(true)
                    }
                }
                UpdateBasicInfo(this.$store.state.access_token, this.song_lst)
                if (this.table2Show) {
                    this.table2Current.push(this.song_lst[0])
                }
                this.rerender+=1
            }
        },





        TEST_T1() {
            for(let i=0; i<this.song_limit; i++) {
                this.song_lst[i]['splendid'] = Math.floor(Math.random() * 100) + 1
                this.song_lst[i]['like'] = Math.floor(Math.random() * 100) + 1
            }
            
            this.splendid_sendable = true
            this.like_sendable = true

            this.before_listened_change([0, 3, 8, 10, 15, 17, 19])

            if (this.add_song_sendable == false) {
                this.add_song_change([0, 2, 9, 12, 13, 18])
            }
            this.T1songScoreSendable = true
            this.rerender+=1
            // this.confirm_send()
        }
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

#hint {
    color: white;
    font-size: 20px;
}


</style>