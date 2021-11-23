<template>
    <div>
        <div id='bg'/>
        <el-row justify="center" style="margin-top: 100px">
            <el-col :span='18'>
                <h2 style="color: white; font-size: 30px;">
                    播放列表
                </h2>
                <songTable :table_data='song_lst' :delete_not_complete='delete_not_complete' @play_music='play_music' @delete_song='get_delete_song_lst' @like_change='like_change' @splendid_change='splendid_change' @add_song_change='add_song_change' :key='rerender'/>
            </el-col>
        </el-row>
        <el-row style="margin-top: 20px">
            <el-col :span='3' :offset='3'>
                <el-button type="danger" :disabled='!delete_not_complete' @click="on_delete">刪除</el-button>
                <el-button type="primary" :disabled='!delete_not_complete' @click="on_complete_delete">刪除完成</el-button>
            </el-col>
            <el-col :span='4' :offset='4'>
                <el-button type="primary" :disabled='!(like_sendable && splendid_sendable && add_song_sendable)' @click="send_dialog_visible=true">送出</el-button>
            </el-col>
        </el-row>
        <el-row justify="center" style="margin-top: 50px">
            <el-col :span='18'>
                <player :key='player_rerender' :source='current_song_source' class="animate__animated animate__fadeInUp"/>
            </el-col>
        </el-row>

        <!-- delete song double confirm dialog start -->
        <el-dialog v-model="delete_dialog_visible" title="Warning" width="30%" center>
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
        <el-dialog v-model="send_dialog_visible" title="Warning" width="30%" center>
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
import { song_lst } from '@/utils/test_songs'
import songTable from '@/components/song_list/song_table'
import player from '@/components/song_list/player'

export default {
    name: 'song_list',
    components: {
        songTable,
        player,
    },
    created(){
        this.song_lst = song_lst
    },
    data() {
        return {
            // for player
            current_song_source: '',
            
            // for song_table data
            song_lst: [],

            // store song_table return delete song
            delete_lst: [],

            // song_table key
            rerender: 0,

            // need to delete songs first
            delete_not_complete: true,

            delete_dialog_visible: false,

            player_rerender: 0,

            //send backend
            like_sendable: false,
            splendid_sendable: false,
            add_song_sendable: false,
            send_dialog_visible: false,
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
            this.rerender+=1
            
        },
        get_delete_song_lst(lst) {
            this.delete_lst = lst
        },
        on_complete_delete() {
            this.delete_dialog_visible = true
        },
        confirm_delete_complete() {
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
                params: {},
            })

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