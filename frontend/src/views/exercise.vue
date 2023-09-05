<template>
    <div>
        <div id='bg'/>
        <el-row justify="center" style="margin-top: 8vh">
            <el-col :span='18'>
                <h2 style="color: white; font-size: 2vw">
                    播放列表
                </h2>
                <songTable1 :table_data='song_lst' :song_not_complete='song_not_complete' @loadSource='loadSource'  @like_change='like_change' @splendid_change='splendid_change' @completeOneSong="completeOneSongT1" @play_music='play_music' @pause_music='pause_music' ref="T1" :key='rerender'/>
            </el-col>
        </el-row>
        <el-row style="margin-top: 20px">
            <el-col :span='4' :offset='10'>
                <el-button type="primary" style="font-size: 1.3vw" v-if='ct==3' @click="startHandler" :disabled='ct<3' :key='startRerender' class="animate__animated animate__slideInUp">開始正式測驗</el-button>
            </el-col>
        </el-row>
        <el-row justify="center" style="margin-top: 50px">
            <el-col :span='18'>
                <player :key='player_rerender' :source='current_song_source' @song_listened='song_listened' @song_ended='song_ended' :idx='currentPlayingIdx' ref='player' class="animate__animated animate__fadeInUp"/>
            </el-col>
        </el-row>
    </div>
</template>

<script>
// import { song_lst } from '@/utils/test_songs'
import songTable1 from '@/components/song_list/song_table'
import player from '@/components/song_list/player'
import {GetRecentlyPlayed} from '@/apis/SpotifyAPIs/get_recently_played'
import {GetSavedTracks} from '@/apis/SpotifyAPIs/get_saved_tracks'
import {UpdateUserRecentTracks} from '@/apis/backendAPIs/tracks/update_user_recent_track'
import {CheckRecent, CheckSaved} from '@/apis/backendAPIs/tracks/check_user_exist'
import {UpdateUserSavedTracks} from '@/apis/backendAPIs/tracks/update_user_saved_track'
import {InitUser} from '@/apis/backendAPIs/user/init_user'
import {UpdateBasicInfo} from '@/utils/functools'
import {ElLoading} from 'element-plus'


export default {
    name: 'exercise',
    components: {
        songTable1,
        player,
    },
    created(){
        this.$store.isExercise = true
        let urlParams = new URLSearchParams(window.location.search)
        this.$store.dispatch("initUserAccessToken", urlParams.get("access_token"))

        this.song_lst = [
            {
                listened: 0,
                title: "愛情你比我想的閣較偉大 -《當男人戀愛時》電影主題曲",
                artist: "茄子蛋",
                song_id: "4fJlSLYLiu5trFCMZdSQDC",
                source: "https://open.spotify.com/embed/track/4fJlSLYLiu5trFCMZdSQDC?utm_source=generator",
                song_preview_url: "https://p.scdn.co/mp3-preview/9c7d634b71050d160bda74a26ec08662c9bd3c71?cid=774b29d4f13844c495f206cafdad9c86",
                like: 0,
                splendid: 0,
                add: 0,
            },
            {
                listened: 0,
                title: "Dreaming of you",
                artist: "MY FIRST STORY",
                song_id: "6cutt8thPFUICMfxaYerWd",
                source: "https://open.spotify.com/embed/track/6cutt8thPFUICMfxaYerWd?utm_source=generator",
                song_preview_url: "https://p.scdn.co/mp3-preview/497a105aca4e71f96e1fc8defad3acb75a85356d?cid=774b29d4f13844c495f206cafdad9c86",
                like: 0,
                splendid: 0,
                add: 0,
            },
            {
                listened: 0,
                title: "告白氣球",
                artist: "周杰倫",
                song_id: "4ICIjhyIi03aU3e4gIcSlP",
                source: "https://open.spotify.com/embed/track/4ICIjhyIi03aU3e4gIcSlP?utm_source=generator",
                song_preview_url: "https://p.scdn.co/mp3-preview/68d90856df789dd9b821ef71a457003561f96921?cid=774b29d4f13844c495f206cafdad9c86",
                like: 0,
                splendid: 0,
                add: 0,
            },
        ]
        
    },

    async mounted() {   
        const loadingInstance = ElLoading.service({
            'lock': false,
            'fullscreen': true,
            'text': 'Fetching data',
            'background': 'rgba(0, 0, 0, 0.7)',
        })
        setTimeout(() => {
            loadingInstance.close()
        }, 1000)
        
        await InitUser(
            this.$store.state.userID,
            this.$store.state.userEmail,
            this.$store.state.between_subject_type,
            this.$store.state.within_subject_type
        )      
        
        // 3000
        // 收集近3個月聆聽的歌曲
        CheckRecent(this.$store.state.userID).then((res)=>{
            let retv = res.data
            if(!retv) {
                this.updateRecentTracks()
            }
        })

        // 收集近3個月收藏的歌曲
        CheckSaved(this.$store.state.userID).then((res)=>{
            let retv = res.data
            if(!retv) {
                this.updateSavedTracks()
            }
        })
    },

    data() {
        return {
            // for player
            current_song_source: '',
            
            // for song_table data
            song_lst: [],

            // song_table key
            rerender: 0,
            player_rerender: 0,

            // playlist 相關參數
            list_id:'',
            song_limit: 0,
            last_song_pointer: 0,
            tags_obj: {},
            score_obj: {},
            table1Show: true,
            table2Show: false,
            table2Current:[],
            table2Idx: 0,

            ct: 0,
            startRerender: 0,
            song_not_complete: Array(3).fill(true),
            currentPlayingIdx: -1,

        }
    },
    methods: {
        loadSource(source, idx) {
            this.currentPlayingIdx = idx
            this.current_song_source = source
            this.player_rerender+=1
        },
        play_music(idx) {
            console.log(idx)
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
        completeOneSongT1() {
            this.ct+=1
            if(this.ct==3) {
                this.startRerender+=1
            }
        },

        startHandler() {
            this.$store.isExercise = false
            if(this.$store.state.exercise_redirect_page=='0') {
                this.$router.push({
                    name: 'create_list',
                })
            } else {
                this.$router.push({
                    name: 'tags',
                })
            }
        },
        song_listened(idx) {
            this.song_not_complete[idx] = false
        },

        song_ended(idx) {
            this.$refs.T1.song_ended(idx)
        },

        getThresholdTime() {
            let today = new Date();
            let newDay = new Date(
                today.getFullYear(),
                today.getMonth()-3,
                today.getDate(),
                today.getHours(),
                today.getMinutes(),
                today.getSeconds(),
                today.getMilliseconds()
            )

            return newDay
        },
        async updateRecentTracks() {
            var unix_time = this.getThresholdTime().getTime()
            var recent_play_tracks = []
            var accumulate_tracks = {}
            var objs = {}

            // eslint-disable-next-line no-constant-condition
            while (true) {
                let retv = await GetRecentlyPlayed(this.$store.state.access_token, unix_time)
                retv = retv.data
                recent_play_tracks.push(...retv['items'])

                if (retv['next'] === null) {
                    break
                } else {
                    unix_time = parseInt(retv['cursors']['after'])
                }
            }

            if (recent_play_tracks.length > 0) {
                for(let i=0; i<recent_play_tracks.length; i++) {
                    let song_id = recent_play_tracks[i]['track']['id']
                    if (song_id in accumulate_tracks) {
                        accumulate_tracks[song_id]+=1
                    } else {
                        accumulate_tracks[song_id]=1
                        objs[song_id] = {
                            "artist_id": recent_play_tracks[i]['track']['artists'][0]['id'],
                            "artist": recent_play_tracks[i]['track']['artists'][0]['name'],
                            "song_id": song_id,
                            "title": recent_play_tracks[i]['track']['name'],
                            "track_popularity": recent_play_tracks[i]['track']['popularity'],
                            "song_preview_url": recent_play_tracks[i]['track']['preview_url']
                        }
                    }
                }

                await UpdateBasicInfo(this.$store.state.access_token, Object.values(objs))

                // for(var key in accumulate_tracks) {
                //     UpdateUserRecentTrack(this.$store.state.userID, key, accumulate_tracks[key])
                // }
                await UpdateUserRecentTracks(this.$store.state.userID, Object.keys(accumulate_tracks), Object.values(accumulate_tracks))
                console.log(accumulate_tracks)
            }
            
        },
        async updateSavedTracks() {
            var all_saved_tracks = []
            let offset = 0
            let time_threshold = this.getThresholdTime().toISOString()

            // eslint-disable-next-line no-constant-condition
            while (true) {
                let retv = await GetSavedTracks(this.$store.state.access_token, offset)
                retv = retv.data
                all_saved_tracks.push(...retv['items'])

                if (retv['next'] === null) {
                    break
                } else {
                    offset = parseInt(retv['next'].slice(
                        retv['next'].indexOf("offset=")+7,
                        retv['next'].indexOf("&limit")
                    ))
                }
            }

            if (all_saved_tracks.length > 0) {
                let objs = []
                for(let i=0; i<all_saved_tracks.length; i++) {
                    let add_at = all_saved_tracks[i]['added_at']
                    if (add_at>=time_threshold) {
                        let song_id = all_saved_tracks[i]['track']['id']
                        let obj = {
                            "artist_id": all_saved_tracks[i]['track']['artists'][0]['id'],
                            "artist": all_saved_tracks[i]['track']['artists'][0]['name'],
                            "song_id": song_id,
                            "title": all_saved_tracks[i]['track']['name'],
                            "track_popularity": all_saved_tracks[i]['track']['popularity'],
                            "song_preview_url": all_saved_tracks[i]['track']['preview_url']
                        }
                        objs.push(obj)
                    }
                }
                if (objs.length>0) {
                    await UpdateBasicInfo(this.$store.state.access_token, objs)
                    let saved_song_ids = objs.map(x=>x['song_id'])
                    let saved_song_ids_str = saved_song_ids.join(',')
                    await UpdateUserSavedTracks(this.$store.state.userID, saved_song_ids_str)
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