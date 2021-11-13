<template>
    <div>
        <el-table :data="song_lst" :style="table_style" :cell-style="{height: '40px', }" :header-cell-style="{height: '60px', padding: '5px'}">
            <el-table-column prop="listened" label="聽過" width="100">
                <template #default="scope">
                    <el-checkbox-group v-model="listened_lst">
                        <el-checkbox :label='scope.$index' :disabled='!delete_not_complete' size='medium' @change="delete_change">{{ }}</el-checkbox>
                    </el-checkbox-group>
                </template>
            </el-table-column>
            <el-table-column prop="title" label="標題"/>
            <el-table-column prop="artist" label="藝人"/>
            <el-table-column prop="spend" label="時長" />
            <el-table-column label="播放" width="100">
                <template #default="scope">
                    <el-button :icon='i_video_play' :disabled='delete_not_complete' circle @click="play_song(scope)" />
                </template>
            </el-table-column>
            <el-table-column prop="like" label="符合喜好">
                <template #default="scope">
                    <el-rate v-model="song_lst[scope.$index]['like']" :disabled='delete_not_complete' allow-half @change="like_change" style="line-height: 40px; " />
                </template>
            </el-table-column>
            <el-table-column prop="splendid" label="驚艷度">
                <template #default="scope">
                    <el-rate v-model="song_lst[scope.$index]['splendid']" :disabled='delete_not_complete' allow-half @change="splendid_change" style="line-height: 40px; " />
                </template>
            </el-table-column>
            <el-table-column prop="add_song_lst" label="加入歌單" width="150" />
        </el-table>
    </div>
</template>



<script>
import { CaretRight } from '@element-plus/icons'

export default {
    name: 'song_table',
    props: ['table_data', 'delete_not_complete'],
    created () {
        this.i_video_play = CaretRight
    },
    data() {
        return {
            table_style: {
                'width': '100%',
                'fontSize': '24px',
                'border-radius': '20px',
            },
            song_lst: this.table_data,
            i_video_play: 0,
            listened_lst: [],
        }
    },
    methods: {
        play_song(scope) {
            console.log(scope)
            this.$emit("play_music", this.song_lst[scope.$index]['source'])
        },
        like_change(val) {
            console.log(val)
        },
        splendid_change(val) {
            console.log(val)
        },
        delete_change(){
            var delete_lst = Object.values(this.listened_lst)
            this.$emit('delete_song', delete_lst)
        }
    },
}
</script>

<style scoped>
::v-deep .el-table .cell { 
    line-height: 40px; 
}

.el-checkbox:last-of-type {
    margin-left: 30%
}
</style>