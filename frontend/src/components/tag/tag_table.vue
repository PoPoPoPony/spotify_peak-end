<template>
    <div>
        <el-table :data="tags_table_data" :style="table_style" :cell-style="{height: '40px', }" :header-cell-style="{height: '60px', padding: '5px'}">
            <el-table-column prop="class" label="Class" width="180" />
            <el-table-column prop="tags" label="Tags">
                <template #default="scope">
                    <el-checkbox-group v-model="tag_lst" @change="tag_change" :max='5'>
                        <el-checkbox v-for="(tag, index) in tags_table_data[scope.$index]['tags']" :key="index" :label="tag" border />
                    </el-checkbox-group>
                </template>
            </el-table-column>
        </el-table>
        <el-row style="margin-top: 100px">
            <el-col :span='9' :offset='1' style="font-size: 30px; color: white; text-align: left">
                最多選取5個標籤，還剩 {{ 5 - current_tag_num }} 個
            </el-col>
            <el-col :span='4' :offset='10' style="font-size: 30px; color: white;">
                <el-button type="danger" @click="on_clear" >
                    <el-icon><close-bold /></el-icon>
                    <span style="vertical-align: middle;"> 清空 </span>
                </el-button>
                <el-button type="primary" @click="on_send">
                    <el-icon><Select /></el-icon>
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
                'fontSize': '30px',
                'border-radius': '30px',
            },
            current_tag_num: 0,

            // icon
            // i_closeBold: 0,
            // i_select: 0,
            
            // tag_lst: Array(tag_data.length).fill([]),
            tags_table_data: [],
            tag_lst: []

        }
    },
    methods: {
        tag_change(value) {
            this.current_tag_num = value.length
        },
        on_clear() {
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
    font-size: 25px;
}

</style>