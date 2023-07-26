<template>
    <div class="animate__animated animate__fadeIn">
        <el-table :data="song_lst" :style="table_style" :cell-style="{height: '40px', 'font-size': '1.25vw'}" :header-cell-style="{height: '60px', padding: '5px'}" max-height='50vh' :key="rerender">
            <el-table-column width="100"/>

            <!-- <el-table-column prop="listened" label="聽過" width="100">
                <template #default="scope">
                    <el-checkbox-group v-model="listened_lst" style="zoom:2;" @change="before_listened_change">
                        <el-checkbox :label='scope.$index' size='medium' :disabled="song_not_complete">{{ }}</el-checkbox>
                    </el-checkbox-group>
                </template>
            </el-table-column> -->
            <el-table-column prop="title" label="標題"/>
            <el-table-column prop="artist" label="藝人"/>
            <el-table-column label="播放" width="300">
                <template #default="scope" >
                    <el-button circle @click="play_song(scope.$index)" style="border:0; padding:0;">
                        <el-icon size='50' v-if="play_show"><VideoPlay /></el-icon>
                        <el-icon size='50' v-if="!play_show"><VideoPause /></el-icon>
                    </el-button>
                </template>
            </el-table-column>
            <!-- <el-table-column prop="like" label="喜好">
                <template #default="scope">
                    <el-slider v-model="song_lst[scope.$index]['like']" :disabled='song_not_complete' @change='like_change' style='padding-left: 10px; padding-right: 10px'></el-slider>
                </template>
            </el-table-column>
            <el-table-column label="驚艷度">
                <template #default="scope">
                    <el-slider v-model="song_lst[scope.$index]['splendid']" :disabled='song_not_complete' @change='splendid_change' style='padding-left: 10px; padding-right: 10px'></el-slider>
                </template>
            </el-table-column>
            <el-table-column label="收藏" width="150" v-if="show_add_song">
                <template #default="scope">
                    <el-checkbox-group v-model="add_song_lst" style="zoom:2;" @change='add_song_change'>
                        <el-checkbox :label="scope.$index" :disabled='song_not_complete || added_max'>{{ }}</el-checkbox>
                    </el-checkbox-group>
                </template>
            </el-table-column> -->
            <!-- <el-table-column label="" width="150">
                <template #default="scope">
                    <el-button type="primary" style="font-size: 1vw" @click="completeOneSong(scope)" :disabled='song_not_complete'>完成</el-button>
                </template>
            </el-table-column>
            <el-table-column width="100"/> -->
        </el-table>
    </div>
</template>



<script>
import { VideoPlay } from '@element-plus/icons'
import { VideoPause } from '@element-plus/icons'

export default {
    name: 'second_test_song_table',
    props: ['table_data', 'table2Idx', 'song_not_complete'],
    components: {
        VideoPlay,
        VideoPause,
    },
    created () {

    },
    data() {
        return {
            table_style: {
                'width': '100%',
                'fontSize': '24px',
                'border-radius': '20px',
            },
            song_lst: this.table_data,
            rerender:0,
            play_show: true,
            ini_play:true,
        }
    },
    mounted () {
        // 自動撥放可以在這邊call play_song
    },
    methods: {
        play_song(idx) {
            // this.$emit("play_music", this.song_lst[scope.$index]['source'])
            // console.log(this.song_lst[idx]['song_preview_url'])
            if(this.play_show) {
                if(this.ini_play) {
                    this.$emit("loadSource", this.song_lst[idx]['song_preview_url'], 0)
                    this.ini_play = false
                }
                else {
                    this.$emit("play_music", 0)
                }
            } 
            else {
                this.$emit("pause_music", 0)
            }
            
            this.play_show = !this.play_show
        },
        completeOneSong() {
            this.$emit('completeOneSong')
        },
        song_ended() {
            this.play_show = !this.song_not_complete
            this.$emit('completeOneSong')
        }
    },
}
</script>

<style scoped>
:deep(.el-table .cell) { 
    line-height: 40px; 
}

.el-checkbox:last-of-type {
    margin-left: 30%
}
</style>