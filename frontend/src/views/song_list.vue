<template>
    <div>
        <div id='bg'/>
        <el-row justify="center" style="margin-top: 100px">
            <el-col :span='18'>
                <h2 style="color: white; font-size: 30px;">
                    播放列表
                </h2>
                <songTable1 v-if="table1Show" :table_data='song_lst' :delete_not_complete='delete_not_complete' @play_music='play_music' @delete_song='get_delete_song_lst' @like_change='like_change' @splendid_change='splendid_change' @add_song_change='add_song_change' :key='rerender'/>
                <songTable2 v-if="table2Show" :table2Idx='table2Idx' :table_data='table2Current' :delete_not_complete='delete_not_complete' @play_music='play_music' @delete_song='get_delete_song_lst' @add_song_change='add_song_change' @completeOneSong='completeOneSong'  :key='rerender'/>
            </el-col>
        </el-row>
        <el-row style="margin-top: 20px">
            <el-col :span='6' :offset='2'>
                <el-button v-if="deleteShow" type="danger" :disabled='!delete_not_complete' @click="on_delete">刪除</el-button>
                <el-button v-if="deleteCompleteShow" type="primary" :disabled='!delete_not_complete' @click="on_complete_delete">刪除完成</el-button>
                <span v-if="$store.between_subject_type==1 && !islong" style="color: white; font-size: 25px; padding-left:25px; padding-top:10px">
                    請選擇 3 首歌曲加入歌單
                </span>
                <span v-if="$store.between_subject_type==1 && islong" style="color: white; font-size: 25px; padding-left:25px; padding-top:10px">
                    請選擇 5 首歌曲加入歌單
                </span>
            </el-col>
            <el-col :span='4' :offset='2'>
                <el-button v-if="table1Show" type="primary" :disabled='!(like_sendable && splendid_sendable && add_song_sendable)' @click="send_dialog_visible=true">送出</el-button>
            </el-col>
        </el-row>
        <el-row justify="center" style="margin-top: 50px">
            <el-col :span='18'>
                <player :key='player_rerender' :source='current_song_source' class="animate__animated animate__fadeInUp"/>
            </el-col>
        </el-row>

        <!-- delete song double confirm dialog start -->
        <el-dialog v-model="delete_dialog_visible" title="確認刪除" width="30%" center>
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
        <el-dialog v-model="send_dialog_visible" title="確認送出" width="30%" center>
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
import {GetDiscoverWeekly} from '@/apis/get_discover_weekly'
import {GetSongList} from '@/apis/get_song_list'
import {GetRecommendations} from '@/apis/get_recommendations'


export default {
    name: 'song_list',
    components: {
        songTable1,
        songTable2,
        player,
    },
    created(){
        let urlParams = new URLSearchParams(window.location.search)
        this.list_type = urlParams.get('list_type')
        this.tags_obj = JSON.parse(urlParams.get('tags_obj'))
        this.score_obj = JSON.parse(urlParams.get('score_obj'))
        // console.log(this.tags_obj['Genres'])
        // console.log(this.tags_obj['Artists'])
        // console.log(this.tags_obj['Tracks'])

        if(this.$store.between_subject_type==0) {
            // add song column直接設定成可送出，代表不需要add song
            this.add_song_sendable = true
        } else if(this.$store.between_subject_type==1) {
            this.add_song_sendable = false
        }


        if(this.$store.between_subject_type==1) {
            if(this.list_type==0) {
                if(["0", "3", 0, 3].includes(this.$store.within_subject_type)) {
                    this.islong = false
                } else {
                    this.islong = true
                }
            } else {
                if(["1", "2", 1, 2].includes(this.$store.within_subject_type)) {
                    this.islong = false
                } else {
                    this.islong = true
                }
            }
        }


        // list type 決定此頁面會刷weekly discovery的歌單還是seed的歌單
        if(this.list_type == 0) {
            GetDiscoverWeekly(this.$store.access_token).then((res)=>{
                console.log("Call GetDiscoverWeekly API successed!")
                let retv = res.data
                console.log(retv)
                this.list_id = retv["playlists"]["items"][0]["id"]
            }).then(() => {
                GetSongList(this.$store.access_token, this.list_id).then((res2)=>{
                    console.log("Call GetSongList API successed!")
                    let retv2 = res2.data
                    console.log(retv2.tracks)
                    var temp_song_lst = retv2.tracks.items

                    // 在0, 3的實驗組別中，weekly discovery是短歌單
                    // 在1, 2的實驗組別中，weekly discovery是長歌單
                    // 目前設定長歌單的歌曲數量為12，短歌單的歌曲數量為8
                    // 測試用長的先用5，短的先用3

                    if(["0", "3", 0, 3].includes(this.$store.within_subject_type)) {
                        this.song_limit = 8
                    } else {
                        this.song_limit = 12
                    }
                    this.last_song_pointer = this.song_limit-1

                    for(var i=0; i<temp_song_lst.length; i++) {
                        var temp_obj = {
                            listened: 0,
                            title: temp_song_lst[i].track.name,
                            artist: temp_song_lst[i].track.artists[0].name,
                            song_id: temp_song_lst[i].track.id,
                            source: "https://open.spotify.com/embed/track/" + temp_song_lst[i].track.id + "?utm_source=generator",
                            song_preview_url: temp_song_lst[i].track.preview_url,
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
                }).catch((err)=>{
                    console.log("Call GetSongList API Failed!")
                    console.log(err)
                })
            })

        } else {
            
            // for song list from seeds
            var genres = this.tags_obj['Genres'].join()
            var artists = this.tags_obj['Artists'].join()
            var tracks = this.tags_obj['Tracks'].join()
            
            GetRecommendations(this.$store.access_token, genres, artists, tracks, this.score_obj).then((res)=>{
                console.log("Call GetRecommendations API successed!")
                let retv = res.data
                var temp_song_lst = retv["tracks"]
                console.log(temp_song_lst)

                // 在0, 3的實驗組別中，weekly discovery是短歌單
                // 在1, 2的實驗組別中，weekly discovery是長歌單
                // 目前設定長歌單的歌曲數量為12，短歌單的歌曲數量為8
                // 測試用長的先用5，短的先用3

                if(["1", "2", 1, 2].includes(this.$store.within_subject_type)) {
                    this.song_limit = 8
                } else {
                    this.song_limit = 12
                }
                this.last_song_pointer = this.song_limit-1

                for(var i=0; i<temp_song_lst.length; i++) {
                    var temp_obj = {
                        listened: 0,
                        title: temp_song_lst[i].name,
                        artist: temp_song_lst[i].artists[0].name,
                        song_id: temp_song_lst[i].id,
                        source: "https://open.spotify.com/embed/track/" + temp_song_lst[i].id + "?utm_source=generator",
                        song_preview_url: temp_song_lst[i].preview_url,
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
            song_limit: 0,
            last_song_pointer: 0,
            tags_obj: {},
            score_obj: {},
            table1Show: true,
            table2Show: false,
            table2Current:[],
            table2Idx: 0,

            //判斷是長/短歌單
            islong: false,
        }
    },
    methods: {
        play_music(source) {
            this.player_rerender+=1
            this.current_song_source = source
        },
        on_delete() {
            while(this.delete_lst.length) {
                this.song_lst.splice(this.delete_lst.pop(), 1);
            }

            var push_num = this.song_limit-this.song_lst.length

            for(var i=0; i<push_num;i++) {
                console.log("execute!")
                this.last_song_pointer+=1
                this.song_lst.push(this.all_song_lst[this.last_song_pointer])
            }

            console.log(this.song_lst)

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
            if(this.$store.between_subject_type==0) {
                this.table1Show = false
                this.table2Show = true
                this.table2Current.push(this.song_lst[0])

            } else if(this.$store.between_subject_type==1) {
                this.table1Show = true
                this.table2Show = false
            }
            this.delete_dialog_visible = false
            this.delete_not_complete = false
            this.rerender+=1
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
            // 目前最少選1首
            if(add_song_lst.length===0) {
                this.add_song_sendable = false
            }
            else {
                for(var i=0; i<add_song_lst.length; i++) {
                    this.song_lst[add_song_lst[i]]['add'] = 1
                }
                this.add_song_sendable = true
            }
        },
        confirm_send() {
            this.send_dialog_visible = false
            // send code to write
            

            this.$router.push({
                name: 'list_credit', 
                query: {
                    list_type: this.list_type
                },
            })
        },
        completeOneSong(val_lst) {
            var like = val_lst[0]
            var splendid = val_lst[1]

            this.song_lst[this.table2Idx]["splendid"] = splendid
            this.song_lst[this.table2Idx]["like"] = like
            if(this.table2Idx<this.song_limit-1) {
                this.table2Idx+=1
                this.table2Current[0] = this.song_lst[this.table2Idx]
                this.rerender+=1
            } else {
                this.confirm_send()
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