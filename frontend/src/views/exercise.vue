<template>
    <div>
        <div id='bg'/>
        <el-row justify="center" style="margin-top: 100px">
            <el-col :span='18'>
                <h2 style="color: white; font-size: 30px;">
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


export default {
    name: 'exercise',
    components: {
        songTable1,
        player,
    },
    created(){
        this.$store.isExercise = true
        let urlParams = new URLSearchParams(window.location.search)

        let userObj = {
            "userID": urlParams.get('uuid'),
            "access_token": urlParams.get('access_token')
        }

        this.$store.dispatch("initUserData", userObj)

        let expType = {
            "within": urlParams.get('within_subject_type'),
            "between": urlParams.get('between_subject_type')
        }

        this.$store.dispatch("initExpType", expType)

        this.redirectPage = urlParams.get('redirect_page')
        this.add_song_sendable = true

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

    mounted() {
        this.$refs.T1.changeStateOnDeleteComplete()
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
            redirectPage: '',
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
            if(this.redirectPage=='0') {
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