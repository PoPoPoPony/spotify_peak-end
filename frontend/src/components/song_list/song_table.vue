<template>
    <div class="animate__animated animate__fadeIn">
        <el-table :data="song_lst" :style="table_style" :cell-style="{'height': '40px',}" :header-cell-style="{height: '60px', padding: '5px'}" :key="rerender">
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
                <template #default="scope" >
                    <el-button v-if='playerBtn_show[scope.$index]' :disabled='delete_not_complete' circle @click="play_song(scope)" style="border:0; padding:0;">
                        <el-icon size='50' v-if="play_show[scope.$index]"><VideoPlay /></el-icon>
                        <el-icon size='50' v-if="!play_show[scope.$index]"><VideoPause /></el-icon>
                    </el-button>
                </template>
            </el-table-column>
            <el-table-column prop="like" label="喜好">
                <template #default="scope">
                    <!-- <el-rate v-model="song_lst[scope.$index]['like']" :disabled='delete_not_complete' allow-half @change="like_change" style="line-height: 40px; " /> -->
                    <el-slider v-model="song_lst[scope.$index]['like']" :disabled='delete_not_complete || song_not_complete[scope.$index]' @change='changed=>like_change(scope.$index, changed)' style='padding-left: 10px; padding-right: 10px' v-if="like_show[scope.$index]"></el-slider>
                </template>
            </el-table-column>
            <el-table-column label="驚艷度">
                <template #default="scope">
                    <!-- <el-rate v-model="song_lst[scope.$index]['splendid']" :disabled='delete_not_complete' allow-half @change="splendid_change" style="line-height: 40px; " /> -->
                    <el-slider v-model="song_lst[scope.$index]['splendid']" :disabled='delete_not_complete || song_not_complete[scope.$index]'   @change='changed=>splendid_change(scope.$index, changed)' style='padding-left: 10px; padding-right: 10px' v-if="splendid_show[scope.$index]"></el-slider>
                </template>
            </el-table-column>
            <el-table-column label="加入歌單" width="150" v-if="show_add_song">
                <template #default="scope" >
                    <el-checkbox-group style="padding-top:10px;" v-if="add_show[scope.$index]" v-model="add_song_lst" @change='add_song_change'>
                        <el-checkbox :label="scope.$index" border :disabled='delete_not_complete || song_not_complete[scope.$index]'>{{ }}</el-checkbox>
                    </el-checkbox-group>
                </template>
            </el-table-column>
            <el-table-column label="完成評分" width="150">
                <template #default="scope">
                    <el-button type="primary" v-if="complete_show[scope.$index]" @click="completeOneSong(scope)" style="font-size: 1vw" :disabled='(delete_not_complete || song_not_complete[scope.$index]) || !splendid_changed[scope.$index] || !like_changed[scope.$index] || confirmClicked[scope.$index]'>完成</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>



<script>
import { VideoPlay } from '@element-plus/icons'
import { VideoPause } from '@element-plus/icons'


export default {
    name: 'song_table1',
    props: ['table_data', 'delete_not_complete', 'song_not_complete'],
    components: {
        VideoPlay,
        VideoPause
    },
    created () {
        console.log("songtable1")
        if(this.$store.state.between_subject_type=="1" && !this.$store.isExercise) {
            this.show_add_song = true
        } else {
            this.show_add_song = false
        }
        console.log("show_add_song", this.show_add_song)

        this.play_show = []

        for(var i=0; i<this.song_lst.length; i++) {
            // 預設顯示like、splendid的slider
            this.like_show.push(false)
            this.splendid_show.push(false)
            this.play_show.push(false)
            this.add_show.push(false)
            this.playerBtn_show.push(false)
            this.complete_show.push(false)
            // 初始like、splendid狀態
            this.like_changed.push(true)
            this.splendid_changed.push(true)
        }
        this.rerender+=1
    },
    data() {
        return {
            table_style: {
                'width': '100%',
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
            add_show: [],
            complete_show:[],
            // 判斷兩個slider有沒有被改變過
            like_changed: [],
            splendid_changed: [],
            confirmClicked: new Array(this.table_data.length).fill(false),
            play_show:true,
            current_playing_idx:-1,
            playerBtn_show: [],
        }
    },
    methods: {
        changeStateOnDeleteComplete() {
            for(var i=0; i<this.song_lst.length; i++) {
                console.log(123)
                // 預設顯示like、splendid的slider
                this.like_show[i] = true
                this.splendid_show[i] = true
                this.play_show[i] = true
                this.add_show[i] = true
                this.playerBtn_show[i] = true
                this.complete_show[i] = true
                // 初始like、splendid狀態
                this.like_changed[i] = false
                this.splendid_changed[i] = false
            }
        },


        play_song(scope) {
            if(this.current_playing_idx == scope.$index) {
                if(this.play_show[scope.$index]) {
                    this.$emit("play_music", scope.$index)
                }
                else {
                    this.$emit("pause_music", scope.$index)
                }

                this.play_show[scope.$index] = !this.play_show[scope.$index]
            }
            else if(this.current_playing_idx > -2) {
                this.play_show[this.current_playing_idx] = true
                this.play_show[scope.$index] = false
                this.current_playing_idx = scope.$index

                // true indicates that need to rerender player component
                this.$emit("loadSource", this.song_lst[scope.$index]['song_preview_url'], scope.$index)
            }
            
            // console.log(this.play_show)
            // console.log(this.current_playing_idx)

            // console.log(scope)
            // this.$emit("play_music", this.song_lst[scope.$index]['source'])
            
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
            // this.$emit('add_song_change',Object.values(this.add_song_lst))
        },
        completeOneSong(scope) {
            this.like_show[scope.$index] = false
            this.complete_show[scope.$index] = false
            this.splendid_show[scope.$index] = false
            this.confirmClicked[scope.$index] = true
            this.add_show[scope.$index] = false
            this.playerBtn_show[scope.$index] = false
            this.$emit('completeOneSong')
            this.$emit('add_song_change',Object.values(this.add_song_lst))
        },
        song_ended(idx) {
            this.play_show[idx] = !this.song_not_complete[idx]
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