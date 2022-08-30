<template>
    <div>
        <el-table :data="tags_table_data" :style="table_style" :cell-style="{'height': '40px', 'font-size': '1.3vw'}" :header-cell-style="{'height': '60px', 'padding': '5px', 'font-size': '1.3vw'}">
            <el-table-column prop="class" label="Class" width="180" />
            <el-table-column prop="tags" label="Tags">
                <template #default="scope">
                    <el-checkbox-group v-model="tag_lst" @change="tag_change_=>tag_change(scope.$index, tag_change_)" :max='5'>
                        <el-checkbox v-for="(tag, index) in tags_table_data[scope.$index]['tags']" :key="index" :label="tag" border />
                    </el-checkbox-group>
                </template>
            </el-table-column>
        </el-table>
        <el-row style="margin-top: 4vh">
            <el-col :xs="{'span':'12', 'offset': '1'}" :sm="{'span':'12', 'offset': '1'}" :lg="{'span': '10', 'offset': '1'}" style="font-size: 1.3vw; color: white; text-align: left">
                最多選取5個標籤，還剩 {{ 5 - current_tag_num }} 個<br>
                (Genres、Artists、Tracks至少各選一個)
            </el-col>
            <el-col :xs="{'span':'11', 'offset': '0'}" :sm="{'span':'9', 'offset': '2'}" :lg="{'span': '7', 'offset': '5'}" style=" color: white;">
                <el-button type="danger" style="font-size: 1.3vw" @click="on_clear">
                    <el-icon style="font-size:1.3vw"><close-bold /></el-icon>
                    <span style="vertical-align: middle;"> 清空 </span>
                </el-button>
                <el-button type="primary" @click="on_send" style="font-size: 1.3vw" :disabled='!tagsendable'>
                    <el-icon style="font-size:1.3vw"><Select /></el-icon>
                    <span style="vertical-align: middle;"> 確認 </span>
                </el-button>
            </el-col>
        </el-row>
    </div>
</template>
<script>
// import { tag_data } from '@/utils/test_tag_data'
import { CloseBold, Select } from '@element-plus/icons'

export default {
    name: 'tag_table',
    components: {
        CloseBold,
        Select,
    },
    props:['table_data'],
    created() {
        this.tags_table_data = this.table_data
        // this.tag_data = tag_data
        // this.i_closeBold = CloseBold
        // this.i_select = Select
    },
    data() {
        return {
            // tag_data: [],
            table_style: {
                'width': '100%',
                'border-radius': '30px',
            },
            current_tag_num: 0,
            store_tags_idx:{},

            // icon
            // i_closeBold: 0,
            // i_select: 0,
            
            // tag_lst: Array(tag_data.length).fill([]),
            tags_table_data: [],
            tag_lst: [],
            tagsendable: false,

        }
    },
    methods: {
        tag_change(idx, value) {
            let artist_ct=0
            let genres_ct=0
            let tracks_ct=0

            for(let v in value) {
                if(!Object.prototype.hasOwnProperty.call(this.store_tags_idx, value[v])) {
                    this.store_tags_idx[value[v]] = idx
                }
            }

            for(let k in this.store_tags_idx) {
                if(value.includes(k)) {
                    if(this.store_tags_idx[k]==0) {
                        genres_ct+=1
                    } else if(this.store_tags_idx[k]==1) {
                        artist_ct+=1
                    } else {
                        tracks_ct+=1
                    }
                } else {
                    delete this.store_tags_idx[k]
                }
            }



            if(artist_ct>0 && genres_ct>0 && tracks_ct>0) {
                this.tagsendable = true
            } else {
                this.tagsendable = false
            }


            this.current_tag_num = value.length
        },
        on_clear() {
            this.store_tags_idx = {}
            this.tagsendable = false
            this.current_tag_num = 0
            this.tag_lst = []
        },
        on_send() {
            this.$emit('send_tags', {'tags_lst': this.tag_lst})
        },
    }
}
</script>

<style scoped>
:deep(.el-table .cell) { 
    line-height: 40px; 
}

:deep(.el-checkbox__label) {
    font-size: 1.3vw;
}

</style>