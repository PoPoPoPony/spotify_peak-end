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
// import {get_genre} from '@/apis/test'

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
            code: '',
        }
    },
    created() {
        let urlParams = new URLSearchParams(window.location.search)
        this.code=urlParams.get('code')
        console.log(this.code)
        // this.access_token = hash.split('&')[0]
        // this.access_token = this.access_token.split('=')[1]
        // console.log(this.access_token)
        // this.genre = get_genre(this.access_token)
        // console.log(this.genre)


        // Request Access Token
        if (this.$route.query) {
            this.axios.post('https://accounts.spotify.com/api/token', {
                data:{
                    'code': this.code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': 'http://localhost:8080/tags'

                }, 
                headers: {
                    'Authorization': 'Basic ' + '5e3c611726d54d488fb918a4c8a8739c' + ':' +'d621355d46644b8fb9b1a090fc92cb48'
                },
                json: true
            }).then((response) => {
                console.log(response);
            })
        }



        // var authOptions = {
        // url: 'https://accounts.spotify.com/api/token',
        // form: {
        //     code: code,
        //     redirect_uri: redirect_uri,
        //     grant_type: 'authorization_code'
        // },
        // headers: {
        //     'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
        // },
        // json: true
        // };


        
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



