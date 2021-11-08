<template>
    <div>
        <el-table :data="tag_data" style="width: 100%">
            <el-table-column prop="class" label="Class" width="180" />
            <el-table-column prop="tags" label="Tags">
                <template #default="scope">
                    <el-tag v-for="(tag, index) in tag_data[scope.$index]['tags']" :key="index" effect="plain" type='primary'> {{tag}} </el-tag>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import {tag_data} from '@/utils/test_tag_data'

export default {
    name: 'tag_table',
    created() {
        this.tag_data = tag_data
    },
    data() {
        return {
            tag_data: [],

        }
    },
    methods: {
        test(scope) {
            console.log(scope.row['class'])
        }
    }
}
</script>

<style scoped>

</style>