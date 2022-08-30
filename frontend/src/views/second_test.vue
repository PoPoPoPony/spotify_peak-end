<template>
    <div>
        <div id='bg'/>
        <el-row justify="center" style="margin-top: 8vh">
            <el-col :span='18'>
                <h2 style="color: white; font-size: 2vw;">
                    播放列表
                </h2>
                <secondTestSongTable v-if='songTableShow' :table_data='currentSong' :currentSongIdx='currentSongIdx' :song_not_complete='song_not_complete[currentSongIdx]' @loadSource='loadSource' @completeOneSong="completeOneSong" @play_music='play_music' @pause_music='pause_music' :key='rerender' ref='T1'/>
            </el-col>
        </el-row>
        <el-row justify="center" style="margin-top: 50px">
            <el-col :span='18'>
                <player v-show="true" v-if="current_song_source!=''" :key='player_rerender' :source='current_song_source' :idx='currentPlayingIdx' @song_listened='song_listened' @song_ended='song_ended' class="animate__animated animate__fadeInUp" ref='player'/>
            </el-col>
        </el-row>
    </div>
</template>

<script>
// import { song_lst } from '@/utils/test_songs'
import secondTestSongTable from '@/components/song_list/second_test_song_table'
import player from '@/components/song_list/player'
import {UpdateSongListElem} from '@/apis/backendAPIs/songListElem/update_songList_elem'
import {GetSongListElem} from '@/apis/backendAPIs/songListElem/get_songList_elem'
import {GetSongListInfo} from '@/apis/backendAPIs/songListInfo/get_songList_info'
import {UpdateSongListInfo} from '@/apis/backendAPIs/songListInfo/update_songList_info'
import {GetTracksByID} from '@/apis/SpotifyAPIs/get_tracks_by_ID'



export default {
    name: 'second_test',
    components: {
        secondTestSongTable,
        player,
    },
    async created(){
        let urlParams = new URLSearchParams(window.location.search)
        this.list_type = urlParams.get('list_type')

        let userObj = {
            "userID": urlParams.get('userID'),
            "access_token": urlParams.get('access_token')
        }

        this.$store.dispatch("initUserData", userObj)

        // 在資料庫中init新歌單
        let firstType = ''
        if(this.list_type==0) {
            firstType = 'Weekly_Discovery'
            UpdateSongListInfo(this.$store.state.userID, firstType+'2').then((res)=> {
                let retv = res.data
                this.$store.dispatch("initWD_ID", retv.songListID)
                console.log(retv.songListID)
            })
        } else {
            firstType = 'Tags'
            UpdateSongListInfo(this.$store.state.userID, firstType+'2').then((res)=> {
                let retv = res.data
                this.$store.dispatch("initT_ID", retv.songListID)
            })
        }
        
        // 獲取第一次實驗歌單
        await GetSongListInfo(this.$store.state.userID, firstType).then((res)=>{
            let retv = res.data
            this.firstTestSongListID = retv['songListID']
        })

        await GetSongListElem(this.firstTestSongListID).then((res)=>{
            let retv = res.data
            if (retv) {
                this.trackIDsStr = retv['trackIDsStr']
            } else {
                console.log("No songs in DB")
            }
            
        })
        await this.getTracksByID()
    },
    data() {
        return {
            // for player
            current_song_source: '',
            
            // for song_table data
            song_lst: [],

            // song_table key
            rerender: 0,

            // need to delete songs first
            song_not_complete: [],

            player_rerender: 0,

            //send backend
            like_sendable: false,
            splendid_sendable: false,
            send_dialog_visible: false,

            // playlist 相關參數
            list_id:'',

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
            trackIDsStr: '',
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
                var elemObj = {
                    'songListID': songListID,
                    'userID': this.$store.state.userID,
                    'trackID': this.song_lst[i]['song_id'],
                    'trackShowType': 'onList',
                    'splendidScore': this.song_lst[i]['splendid'],
                    'likeScore': this.song_lst[i]['like'],
                    'addSongList': false,
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
        completeOneSong(val_lst) {
            this.song_not_complete[this.currentPlayingIdx] = true
            var like = val_lst[0]
            var splendid = val_lst[1]

            this.song_lst[this.currentSongIdx]["splendid"] = splendid
            this.song_lst[this.currentSongIdx]["like"] = like
            if(this.currentSongIdx<this.song_limit-1) {
                this.currentSongIdx+=1
                this.currentSong[0] = this.song_lst[this.currentSongIdx]
                this.rerender+=1
            } else {
                this.confirm_send()
            }

        },
        song_listened(idx) {
            console.log("activate")
            console.log(idx)
            this.song_not_complete[idx] = false
        },
        song_ended(idx) {
            this.song_not_complete[idx] = false
            this.$refs.T1.song_ended(idx)
        },
        async getTracksByID() {
            await GetTracksByID(this.$store.state.access_token, this.trackIDsStr).then((res)=> {
                let retv = res.data['tracks']
                for(let i of retv) {
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
                    this.song_not_complete.push(true)
                }
                this.currentSong.push(this.song_lst[0])
            })
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