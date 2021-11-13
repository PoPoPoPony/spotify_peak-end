<template>
    <div>
        <div id='bg'/>
        <el-row justify="center" style="margin-top: 100px">
            <el-col :span='18'>
                <h2 style="color: white; font-size: 30px;">
                    播放列表
                </h2>
                <songTable :table_data='song_lst' :delete_not_complete='delete_not_complete' @play_music='play_music' @delete_song='get_delete_song_lst' :key='rerender'/>
            </el-col>
        </el-row>
        <el-row style="margin-top: 20px">
            <el-col :span='3' :offset='3'>
                <el-button type="danger" :disabled='!delete_not_complete' @click="on_delete">刪除</el-button>
                <el-button type="primary" :disabled='!delete_not_complete' @click="on_complete_delete">刪除完成</el-button>
            </el-col>
            <el-col :span='4' :offset='4'>
                <el-button type="primary" :disabled='delete_not_complete'>送出</el-button>
            </el-col>
        </el-row>
        <el-row justify="center" style="margin-top: 50px">
            <el-col :span='18'>
                <player :key='player_rerender' :source='current_song_source' class="animate__animated animate__fadeInUp"/>
            </el-col>
        </el-row>
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


</style>