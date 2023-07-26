<template>
    <div class="animate__animated animate__fadeIn">
        <el-table :data="song_lst" :style="table_style" :cell-style="{'height': '40px',}" :header-cell-style="{height: '60px', padding: '5px'}" :key="rerender">
            <el-table-column prop="listened" label="聽過" width="100">
                <template #default="scope">
                    <el-checkbox-group v-model="listened_lst" style="zoom:2;" v-if="before_listened_show[scope.$index]">
                        <!-- <el-checkbox :label='scope.$index' size='large' @change="delete_change" >{{ }}</el-checkbox> -->
                        <el-checkbox :label='scope.$index' size='large' :disabled='song_not_complete[scope.$index]'>{{ }}</el-checkbox>
                    </el-checkbox-group>
                </template>
            </el-table-column>
            <el-table-column prop="title" label="標題"/>
            <el-table-column prop="artist" label="藝人"/>
            <el-table-column label="播放" width="100">
                <template #default="scope" >
                    <el-button v-if='playerBtn_show[scope.$index]' circle @click="play_song(scope)" style="border:0; padding:0;" :disabled="playerBtn_disable[scope
                .$index]">
                        <el-icon size='50' v-if="play_show[scope.$index]"><VideoPlay /></el-icon>
                        <el-icon size='50' v-if="!play_show[scope.$index]"><VideoPause /></el-icon>
                    </el-button>
                </template>
            </el-table-column>
            <el-table-column prop="like" label="喜好">
                <template #default="scope">
                    <!-- <el-rate v-model="song_lst[scope.$index]['like']" :disabled='delete_not_complete' allow-half @change="like_change" style="line-height: 40px; " /> -->
                    <el-slider v-model="song_lst[scope.$index]['like']" :disabled='song_not_complete[scope.$index]' @change='changed=>like_change(scope.$index, changed)' style='padding-left: 10px; padding-right: 10px' v-if="like_show[scope.$index]" :max="10"></el-slider>
                </template>
            </el-table-column>
            <!--0719變更，原稱為驚豔度，資料庫也用SplendidScore -->
            <el-table-column label="新穎性">
                <template #default="scope">
                    <!-- <el-rate v-model="song_lst[scope.$index]['splendid']" :disabled='delete_not_complete' allow-half @change="splendid_change" style="line-height: 40px; " /> -->
                    <el-slider v-model="song_lst[scope.$index]['splendid']" :disabled='song_not_complete[scope.$index]'   @change='changed=>splendid_change(scope.$index, changed)' style='padding-left: 10px; padding-right: 10px' v-if="splendid_show[scope.$index]" :max="10"></el-slider>
                </template>
            </el-table-column>
            <el-table-column label="收藏" width="150" v-if="show_add_song">
                <template #default="scope" >
                    <el-checkbox-group style="zoom:2;" :max="5" v-if="add_show[scope.$index]" v-model="add_song_lst">
                        <el-checkbox :label="scope.$index" size="large" :disabled='song_not_complete[scope.$index]'>{{ }}</el-checkbox>
                    </el-checkbox-group>
                </template>
            </el-table-column>
            <el-table-column label="完成評分" width="170">
                <template #default="scope">
                    <el-button type="primary" v-if="complete_show[scope.$index]" @click="completeOneSong(scope)" style="font-size: 1vw" :disabled='song_not_complete[scope.$index] || !splendid_changed[scope.$index] || !like_changed[scope.$index] || confirmClicked[scope.$index]'>完成</el-button>
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
    props: ['table_data', 'song_not_complete'],
    components: {
        VideoPlay,
        VideoPause
    },
    created () {
        // console.log("songtable1")
        if(this.$store.state.between_subject_type=="1" && !this.$store.isExercise) {
            this.show_add_song = true
        } else {
            this.show_add_song = false
        }

        // Initialize the status of button, slider and checkbox 
        for(var i=0; i<this.song_not_complete.length; i++) {
            if (!this.song_not_complete[i]) {
                this.complete_show.push(false)
                this.like_show.push(false)
                this.splendid_show.push(false)
                this.add_show.push(false)
                this.before_listened_show.push(false)

                this.playerBtn_disable.push(true)

                this.like_changed.push(true)
                this.splendid_changed.push(true)
                this.play_show.push(false)
                this.playerBtn_show.push(false)

                // load add song list from cookies
                if (this.song_lst[i].add == 1) {
                    this.add_song_lst.push(i)
                }
                
            } else {
                this.complete_show.push(true)
                this.like_show.push(true)
                this.splendid_show.push(true)
                this.before_listened_show.push(true)
                this.play_show.push(true)
                this.add_show.push(true)
                this.playerBtn_show.push(true)

                this.like_changed.push(false)
                this.splendid_changed.push(false)
            }
        }
        // only first one can click initially
        let first_idx = this.song_not_complete.indexOf(true)
        // 還有歌沒有評分完畢
        if (first_idx>=0) {
            this.playerBtn_disable.push(false)
            let temp = Array(this.song_not_complete.length-first_idx-1).fill(true)
            this.playerBtn_disable.push(...temp)
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
            add_song_lst: [],
            splendid_lst: new Array(this.table_data.length).fill(0),
            like_lst: new Array(this.table_data.length).fill(0),
            show_add_song: true,
            rerender:0,
            splendid_show: [],
            like_show: [],
            add_show: [],
            before_listened_show: [],
            complete_show:[],
            // 判斷兩個slider有沒有被改變過
            like_changed: [],
            splendid_changed: [],
            confirmClicked: new Array(this.table_data.length).fill(false),
            play_show:[],
            current_playing_idx:-1,
            playerBtn_show: [],
            playerBtn_disable: [],
            listened_lst: [],
        }
    },
    methods: {
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
            // this.$emit("play_music", scope.$index)
            
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
        completeOneSong(scope) {
            this.like_show[scope.$index] = false
            this.complete_show[scope.$index] = false
            this.splendid_show[scope.$index] = false
            this.confirmClicked[scope.$index] = true
            this.add_show[scope.$index] = false
            this.before_listened_show[scope.$index] = false
            this.playerBtn_show[scope.$index] = false
            if (scope.$index < this.song_lst.length) {
                this.playerBtn_disable[scope.$index+1] = false
            }
            

            this.$emit('add_song_change',Object.values(this.add_song_lst))
            this.$emit('before_listened_change',Object.values(this.listened_lst))
            this.$emit('completeOneSong', scope.$index)
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
    font-size: 1.2vw;
}

.el-checkbox:last-of-type {
    margin-left: 20%
}
</style>