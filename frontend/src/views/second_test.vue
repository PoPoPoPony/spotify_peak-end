<template>
    <div>
        <div id='bg'/>
        <el-row justify="center" style="margin-top: 8vh">
            <el-col :span='18'>
                <h2 style="color: white; font-size: 2vw;">
                    播放列表
                </h2>
                <secondTestSongTable v-if='songTableShow' :table_data='currentSong' :currentSongIdx='currentSongIdx' :song_not_complete='song_not_complete' @loadSource='loadSource' @completeOneSong="completeOneSong" @play_music='play_music' @pause_music='pause_music' :key='rerender' ref='T1'/>
            </el-col>
        </el-row>
        <el-row justify="center" style="margin-top: 50px">
            <el-col :span='18'>
                <player v-show="true" v-if="current_song_source!=''" :key='player_rerender' :source='current_song_source' :isAuto="true" :idx='currentPlayingIdx' @song_listened='song_listened' @song_ended='song_ended' class="animate__animated animate__fadeInUp" ref='player'/>
            </el-col>
        </el-row>
    </div>
</template>

<script>
// import { song_lst } from '@/utils/test_songs'
import secondTestSongTable from '@/components/song_list/second_test_song_table'
import player from '@/components/song_list/player'
// import {UpdateSongListElem} from '@/apis/backendAPIs/songListElem/update_songList_elem'
import {GetSongListElems} from '@/apis/backendAPIs/songListElem/get_songList_elems'
import {GetSongListID} from '@/apis/backendAPIs/songListInfo/get_songList_id'
import {UpdateSongListInfo} from '@/apis/backendAPIs/songListInfo/update_songList_info'
import {GetTracksByID} from '@/apis/SpotifyAPIs/get_tracks_by_ID'
import {GetSongListScoreLen} from '@/apis/backendAPIs/songListScore/get_songList_score'
import {GetTrackInfos} from '@/apis/backendAPIs/tracks/get_track_infos'
import {GetUser} from '@/apis/backendAPIs/user/get_user'

export default {
    name: 'second_test',
    components: {
        secondTestSongTable,
        player,
    },
    async created(){
        let urlParams = new URLSearchParams(window.location.search)
        this.$store.dispatch("initUserAccessToken", urlParams.get('access_token'))

        await GetUser(this.$store.state.userEmail).then((res)=>{
            let retv = res.data
            this.$store.dispatch("initUserID", retv.userID)
            this.secondaryType = retv.secondaryType
        })

        await GetSongListScoreLen(this.$store.state.userID).then((res)=>{
            let retv = res.data
            // pass_exp_num=2 -> 正在進行第二次的第一個歌單
            // pass_exp_num=3 -> 正在進行第二次的第二個歌單
            this.pass_exp_num = retv

            // secondary type
            // 0: week(高->低) -> tag(低->高)
            // 1: week(低->高) -> tag(高->低)
            // 2: tag(高->低) -> week(低->高)
            // 3: tag(低->高) -> week(高->低)

            if (retv==2) {
                if ([0, 1].indexOf(this.secondaryType)>=0) {
                    this.list_type = 0
                } else {
                    this.list_type = 1
                }
            } else {
                if ([0, 1].indexOf(this.secondaryType)>=0) {
                    this.list_type = 1
                } else {
                    this.list_type = 0
                }
            }

            // 在資料庫中init新歌單
            if(this.list_type==0) {
                this.first_type = "Weekly_Discovery"
                UpdateSongListInfo(this.$store.state.userID, this.first_type, this.$store.state.period).then((res)=> {
                    let retv = res.data
                    this.$store.dispatch("initWD_ID", retv.songListID)
                })
            } else {
                this.first_type = "Tags"
                UpdateSongListInfo(this.$store.state.userID, this.first_type, this.$store.state.period).then((res)=> {
                    let retv = res.data
                    this.$store.dispatch("initT_ID", retv.songListID)
                    
                })
            }
        })

        // this.list_type = urlParams.get('list_type')
        // this.secondaryType = urlParams.get('secondaryType')

        // let userObj = {
        //     "userID": urlParams.get('userID'),
            // "access_token": urlParams.get('access_token')
        // }

        // this.$store.dispatch("initUserData_original", userObj)

        // 獲取第一次實驗歌單
        await GetSongListID(this.$store.state.userID, this.first_type, "first").then((res)=>{
            let retv = res.data
            this.firstTestSongListID = retv['songListID']
        })


        // console.log(this.firstTestSongListID, this.pass_exp_num)
        // console.log("st", this.secondaryType, "pen", this.pass_exp_num)
        

        // 獲取排序後的歌單Str
        if (this.pass_exp_num==2) {
            if ([1, 3].indexOf(this.secondaryType)>=0) {
                this.GetSongData(this.firstTestSongListID, 0)
            } else {
                this.GetSongData(this.firstTestSongListID, 1)
            }
        } else {
            if ([1, 3].indexOf(this.secondaryType)>=0) {
                this.GetSongData(this.firstTestSongListID, 1)
            } else {
                this.GetSongData(this.firstTestSongListID, 0)
            }
        }

    },
    data() {
        return {
            pass_exp_num: 0,
            first_type:'',
            secondaryType: 0,
            // for player
            current_song_source: '',
            
            // for song_table data
            song_lst: [],

            // song_table key
            rerender: 0,

            // need to delete songs first
            song_not_complete: true,

            player_rerender: 0,

            //send backend
            like_sendable: false,
            splendid_sendable: false,
            send_dialog_visible: false,

            // playlist 相關參數
            list_id:'',
            list_type: -1,

            // 測試暫時用3首，之後改成20
            tags_obj: {},
            score_obj: {},

            temp_song_lst: [],
            songComplete: [],
            songScoreSendable: false,
            currentPlayingIdx:-1,
            songTableShow: false,
            song_limit:20,
            currentSong: [],
            currentSongIdx: 0,
            firstTestSongListID: '',
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

        async confirm_send() {
            this.send_dialog_visible = false

            this.$router.push({
                name: 'list_credit', 
                query: {
                    list_type: this.list_type,
                },
            })
        },

        completeOneSong() {
            this.song_not_complete = false

            if(this.currentSongIdx<this.song_limit-1) {
                this.currentSongIdx+=1
                this.currentSong[0] = this.song_lst[this.currentSongIdx]
                this.song_not_complete = true
                this.rerender+=1
            } else {
                this.confirm_send()
            }

        },
        song_listened() {
            // console.log("activate")
            // console.log(idx)
            this.song_not_complete = false
        },
        song_ended() {
            this.song_not_complete = false
            this.$refs.T1.song_ended()
        },

        async GetSongData(song_list_id, order) {
            let trackIDsStr = ''
            await GetSongListElems(song_list_id, order).then((res)=>{
                let retv = res.data
                if (retv) {
                    trackIDsStr = retv.map((x)=>x.trackID).join(',')
                } else {
                    console.log("No songs in DB")
                }
            })

            // [0720] 先查SpotifyAPI，有缺preview_url的話再走DB的TracksInfo.preview
            await GetTracksByID(this.$store.state.access_token, trackIDsStr).then((res)=> {
                let retv = res.data['tracks']
                // console.log(retv)
                for(let i of retv) {
                    // 若SpotifyAPI少了preview_url
                    var temp_obj = {
                        title: i.name,
                        artist: i.artists[0].name,
                        // artist_id: i.artists[0].id,
                        song_id: i.id,
                        // source: "https://open.spotify.com/embed/track/" + i.id + "?utm_source=generator",
                        song_preview_url: i.preview_url,
                        like: 0,
                        splendid: 0,
                    }
                    this.song_lst.push(temp_obj)
                }
            })
            
            // 取DB中預先儲存的preview
            for (let temp_obj of this.song_lst) {
                if (!temp_obj['song_preview_url']) {
                    await GetTrackInfos(temp_obj.song_id).then((res)=> {
                        let retv = res.data
                        temp_obj['song_preview_url'] = retv[0].preview
                    })
                }
            }
            
            this.currentSong.push(this.song_lst[0])
            this.songTableShow = true
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