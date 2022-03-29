<template>
    <div class="animate__animated animate__fadeIn">
        <el-table :data="song_lst" :style="table_style" :cell-style="{height: '40px', }" :header-cell-style="{height: '60px', padding: '5px'}" :key="rerender">
            <el-table-column prop="listened" label="聽過" width="100">
                <template #default="scope">
                    <el-checkbox-group v-model="listened_lst">
                        <el-checkbox :label='scope.$index' :disabled='!delete_not_complete' size='medium' @change="delete_change">{{ }}</el-checkbox>
                    </el-checkbox-group>
                </template>
            </el-table-column>
            <el-table-column prop="title" label="標題"/>
            <el-table-column prop="artist" label="藝人"/>
            <el-table-column label="播放" width="100">
                <template #default="scope">
                    <el-button :disabled='delete_not_complete' circle @click="play_song(scope)">
                        <el-icon><CaretRight /></el-icon>
                    </el-button>
                </template>
            </el-table-column>
            <el-table-column prop="like" label="喜好">
                <template #default="scope">
                    <el-slider v-model="song_lst[scope.$index]['like']" :disabled='delete_not_complete' @change='like_change' style='padding-left: 10px; padding-right: 10px'></el-slider>
                </template>
            </el-table-column>
            <el-table-column label="驚艷度">
                <template #default="scope">
                    <el-slider v-model="song_lst[scope.$index]['splendid']" :disabled='delete_not_complete'   @change='splendid_change' style='padding-left: 10px; padding-right: 10px'></el-slider>
                </template>
            </el-table-column>
            <el-table-column label="確認評分" width="150">
                <template #default="scope">
                    <el-button type="primary" @click="completeOneSong(scope)" :disabled='delete_not_complete || !splendid_changed || !like_changed'>完成</el-button>
                </template>
            </el-table-column>
            <el-table-column label="加入歌單" width="150" v-if="show_add_song">
                <template #default="scope">
                    <el-checkbox-group v-model="add_song_lst" @change='add_song_change' :max='2'>
                        <el-checkbox :label="scope.$index" border :disabled='delete_not_complete'>{{ }}</el-checkbox>
                    </el-checkbox-group>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>



<script>
import { CaretRight } from '@element-plus/icons'

export default {
    name: 'song_table2',
    props: ['table_data', 'delete_not_complete', 'table2Idx'],
    components: {
        CaretRight
    },
    created () {
        console.log("songtable2")
        console.log(this.table2Idx)
        if(this.$store.between_subject_type=="1") {
            this.show_add_song = true
        } else {
            this.show_add_song = false
        }
        console.log("show_add_song", this.show_add_song)
        this.rerender+=1
    },
    data() {
        return {
            table_style: {
                'width': '100%',
                'fontSize': '24px',
                'border-radius': '20px',
            },
            song_lst: this.table_data,
            listened_lst: [],
            add_song_lst: [],
            splendid_val: 0,
            like_val: 0,
            show_add_song: true,
            rerender:0,
            splendid_show: true,
            like_show: true,
            // 判斷兩個slider有沒有被改變過
            like_changed: false,
            splendid_changed: false,
            
        }
    },
    methods: {
        play_song(scope) {
            console.log(scope)
            // this.$emit("play_music", this.song_lst[scope.$index]['source'])
            this.$emit("play_music", this.song_lst[scope.$index]['song_preview_url'])
        },
        like_change(val) {
            this.like_val = val
            this.like_changed = true
        },
        splendid_change(val) {
            this.splendid_val = val
            this.splendid_changed = true
        },
        delete_change(){
            var delete_lst = Object.values(this.listened_lst)
            this.$emit('delete_song', delete_lst)
        },
        add_song_change() {
            this.$emit('add_song_change',Object.values(this.add_song_lst))
        },
        completeOneSong(scope) {
            this.$emit('completeOneSong',[this.like_val, this.splendid_val])
            console.log(scope)
        },
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