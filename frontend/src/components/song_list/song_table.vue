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
                    <!-- <el-rate v-model="song_lst[scope.$index]['like']" :disabled='delete_not_complete' allow-half @change="like_change" style="line-height: 40px; " /> -->
                    <el-slider v-model="song_lst[scope.$index]['like']" :disabled='delete_not_complete' @change='changed=>like_change(scope.$index, changed)' style='padding-left: 10px; padding-right: 10px' v-if="like_show[scope.$index]"></el-slider>
                </template>
            </el-table-column>
            <el-table-column label="驚艷度">
                <template #default="scope">
                    <!-- <el-rate v-model="song_lst[scope.$index]['splendid']" :disabled='delete_not_complete' allow-half @change="splendid_change" style="line-height: 40px; " /> -->
                    <el-slider v-model="song_lst[scope.$index]['splendid']" :disabled='delete_not_complete'   @change='changed=>splendid_change(scope.$index, changed)' style='padding-left: 10px; padding-right: 10px' v-if="splendid_show[scope.$index]"></el-slider>
                </template>
            </el-table-column>
            <el-table-column label="確認評分" width="150">
                <template #default="scope">
                    <el-button type="primary" @click="completeOneSong(scope)" :disabled='delete_not_complete || !splendid_changed[scope.$index] || !like_changed[scope.$index]'>確認</el-button>
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
    name: 'song_table1',
    props: ['table_data', 'delete_not_complete'],
    components: {
        CaretRight
    },
    created () {
        console.log("songtable1")
        if(this.$store.between_subject_type=="1") {
            this.show_add_song = true
        } else {
            this.show_add_song = false
        }
        console.log("show_add_song", this.show_add_song)

        for(var i=0; i<this.song_lst.length; i++) {
            // 預設顯示like、splendid的slider
            this.like_show.push(true)
            this.splendid_show.push(true)
            // 初始like、splendid狀態
            this.like_changed.push(false)
            this.splendid_changed.push(false)
        }
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
            splendid_lst: new Array(this.table_data.length).fill(0),
            like_lst: new Array(this.table_data.length).fill(0),
            show_add_song: true,
            rerender:0,
            splendid_show: [],
            like_show: [],
            // 判斷兩個slider有沒有被改變過
            like_changed: [],
            splendid_changed: [],
            
        }
    },
    methods: {
        play_song(scope) {
            console.log(scope)
            // this.$emit("play_music", this.song_lst[scope.$index]['source'])
            this.$emit("play_music", this.song_lst[scope.$index]['song_preview_url'])
        },
        like_change(idx, val) {
            this.like_lst[idx] = val
            this.like_changed[idx] = true
            this.$emit('like_change', this.like_lst)
        },
        splendid_change(idx, val) {
            this.splendid_lst[idx] = val
            this.splendid_changed[idx] = true
            this.$emit('splendid_change', this.splendid_lst)
        },
        delete_change(){
            var delete_lst = Object.values(this.listened_lst)
            this.$emit('delete_song', delete_lst)
        },
        add_song_change() {
            this.$emit('add_song_change',Object.values(this.add_song_lst))
        },
        completeOneSong(scope) {
            this.like_show[scope.$index] = false
            this.splendid_show[scope.$index] = false
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