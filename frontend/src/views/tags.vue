<template>
    <div>
        <div id='bg'/>
        <navBar/>
        <h2 style="font-size: 50px; color: white;">請選擇標籤</h2>
        <div id="tagTable_container">
            <tagTable/>
        </div>
        <el-button type="primary" @click="api_test">Primary</el-button>
    </div>
</template>

<script>
import navBar from '@/components/navBar'
import tagTable from '@/components/tag/tag_table'
import {getMe} from '@/apis/get_genre'

export default {
    name: 'tags',
    components: {
        navBar,
        tagTable,
    },
    data() {
        return {
            access_token: '',
            genre: '',
        }
    },
    created() {
        let urlParams = new URLSearchParams(window.location.search)
        this.access_token=urlParams.get('access_token')

        console.log(this.access_token)

        getMe(this.access_token).then((res)=>{
            console.log('call me success')
            console.log(res.data)
        }).catch((err)=>{
            console.log('call me faild')
            console.log(err)
        })




        


        
    },
    methods: {
        api_test() {

        }
    },
}
</script>

<style scoped>
#bg {
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, #72BFE6 0%, #46277A 100%);
    background-size: cover;
    position: fixed;
    margin: 0;
    top: 0px;
	left: 0px;
    z-index: -100;
}


#tagTable_container {
    margin-left: 15%;
    width: 70%
}
</style>



