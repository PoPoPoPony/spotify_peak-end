<template>
    <div class="animate__animated animate__fadeIn">
        <el-table :data="song_lst" :style="table_style" :cell-style="{'height': '40px','padding-left': '30px'}" :header-cell-style="{height: '60px', padding: '5px 5px 5px 30px'}" :key="rerender">
            <el-table-column prop="title" label="標題"/>
            <el-table-column prop="artist" label="藝人"/>
            <el-table-column label="播放" width="130">
                <el-button circle @click="play_song" style="border:0; padding:0;">
                    <el-icon size='50' v-if="play_show"><VideoPlay /></el-icon>
                    <el-icon size='50' v-if="!play_show"><VideoPause /></el-icon>
                </el-button>
            </el-table-column>
            <el-table-column prop="like" label="喜好">
                <el-slider v-model="song_lst[0]['like']" :disabled='song_not_complete' @change='like_change' style='padding-left: 10px; padding-right: 10px' v-if="like_show"></el-slider>
            </el-table-column>
            <el-table-column label="驚艷度">
                <el-slider v-model="song_lst[0]['splendid']" :disabled='song_not_complete'   @change='splendid_change' style='padding-left: 10px; padding-right: 10px' v-if="splendid_show"></el-slider>
            </el-table-column>
            <el-table-column label="完成評分" width="200">
                <el-button type="primary" v-if="complete_show" @click="completeOneSong" style="font-size: 1vw" :disabled='song_not_complete || !splendid_changed || !like_changed'>完成</el-button>
            </el-table-column>
        </el-table>
    </div>
</template>



<script>
import { VideoPlay } from '@element-plus/icons'
import { VideoPause } from '@element-plus/icons'


export default {
    name: 'secondTestSongTable',
    props: ['table_data', 'currentSongIdx', 'song_not_complete'],
    components: {
        VideoPlay,
        VideoPause
    },
    created () {

    },
    data() {
        return {
            table_style: {
                'width': '100%',
                'border-radius': '20px',
            },
            song_lst: this.table_data,
            splendid_val: 0,
            like_val: 0,
            rerender:0,
            splendid_show: true,
            like_show: true,
            complete_show:true,
            // 判斷兩個slider有沒有被改變過
            like_changed: false,
            splendid_changed: false,
            play_show:true,
            playerBtn_show: true,
            ini_play:true,
        }
    },
    methods: {
        play_song() {
            
            // this.$emit("play_music", this.song_lst[scope.$index]['source'])
            if(this.play_show) {
                if(this.ini_play) {
                    this.$emit("loadSource", this.song_lst[0]['song_preview_url'], this.currentSongIdx)
                    this.ini_play = false
                }
                else {
                    this.$emit("play_music", this.currentSongIdx)
                }
            } 
            else {
                this.$emit("pause_music", this.currentSongIdx)
            }
            
            this.play_show = !this.play_show
        },
        like_change(val) {
            this.like_val = val
            this.like_changed = true
        },
        splendid_change(val) {
            this.splendid_val = val
            this.splendid_changed = true
        },
        completeOneSong() {
            this.$emit('completeOneSong',[this.like_val, this.splendid_val])
        },
        song_ended() {
            this.play_show = !this.song_not_complete
        }
    },
}
</script>

<style scoped>
:deep(.el-table .cell) { 
    line-height: 40px; 
    font-size: 1.25vw;
}

.el-checkbox:last-of-type {
    margin-left: 30%
}
</style> 