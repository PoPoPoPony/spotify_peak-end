<template>
    <div>
        <div id='bg'/>
        <navBar/>
        <h2 style="font-size: 50px; color: white;">請選擇標籤</h2>
        <div id="tagTable_container">
            <tagTable/>
        </div>
    </div>
</template>

<script>
import navBar from '@/components/navBar'
import tagTable from '@/components/tag/tag_table'
import {getMe} from '@/apis/get_genre'
import {GetRecentlyPlayed} from '@/apis/get_recently_played'
import {GetUserPlaylists} from '@/apis/get_user_playlists'
import {GetFollowedArtist} from '@/apis/get_followed_artist'


export default {
    name: 'tags',
    components: {
        navBar,
        tagTable,
    },
    data() {
        return {
            // 從每個類別找到的genre會存成{genre: frequency}的格式
            genre_dict: {
                "album": {},
                "artist": {},
                "track": {}
            },
        }
    },
    created() {
        let urlParams = new URLSearchParams(window.location.search)
        this.$store.access_token = urlParams.get('access_token')
        this.$store.between_subject_type = urlParams.get('between_subject_type')
        this.$store.within_subject_type = urlParams.get('within_subject_type')
        this.$store.pass_exp_num = urlParams.get('pass_exp_num')

        console.log("tags between", this.$store.between_subject_type)
        console.log("tags within", this.$store.within_subject_type)

        // 每到 create list 或 選擇 seed 頁面，就增加做過的實驗數量(每個人應做兩次)
        this.$store.pass_exp_num+=1

        getMe(this.$store.access_token).then((res)=>{
            console.log('call me success')
            console.log(res.data)
        }).catch((err)=>{
            console.log('call me faild')
            console.log(err)
        })

        // GetRecentlyPlayed
        GetRecentlyPlayed(this.$store.access_token).then((res)=>{
            console.log("Call GetRecentlyPlayed API successed!")
            let retv = res.data
            console.log(retv)
        })

        GetUserPlaylists(this.$store.access_token).then((res)=>{
            console.log("Call GetUserPlaylists API successed!")
            let retv = res.data
            console.log(retv)
        })

        GetFollowedArtist(this.$store.access_token).then((res)=>{
            console.log("Call GetFollowedArtist API successed!")
            let retv = res.data
            console.log(retv)
        })

    },
    methods: {
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



