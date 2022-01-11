<template>
    <div class="animate__animated animate__fadeInDown">
        <div id="panel">
            <img id="panel_logo" :src="spotify_logo" alt="">
            <div id="panel_elem">
                <el-form label-position='top' label-width="100px" :model="user">
                    <el-form-item label="Account">
                        <el-input v-model="user.account"></el-input>
                    </el-form-item>
                    <el-form-item label="Password">
                        <el-input v-model="user.pwd" show-password></el-input>
                    </el-form-item>
                </el-form>
                <el-row style="margin-bottom: 20px; margin-top: 20px;">
                    <el-col :span="4" :offset="19">
                        <el-button type="primary" style="font-size: 25px;" @click="login" >Login</el-button>
                        <el-button type="primary" style="font-size: 25px;" >
                            <el-link :href="url" :underline="false" style="color: white; font-size: 30px">Login2</el-link>
                        </el-button>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="11">
                        <hr style="border: 1px solid black;"/>
                    </el-col>
                    <el-col :span="2">
                        <text style="font-size: 20px">or</text>
                    </el-col>
                    <el-col :span="11">
                        <hr style="border: 1px solid black;"/>
                    </el-col>
                </el-row>
                <div id="avater_container">
                    <el-row justify="space-between">
                        <el-col :span="6" v-for="(item, index) in third_login_src" :key="index" style="border: 1px solid black; border; border-radius: 10px;">
                            <el-avatar shape="square" :size="100" fit="fill" :src="item" style="background-color: white;"></el-avatar>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {Login} from '@/apis/login.js'


export default {
    name: 'login_panel',
    data() {
        return {
            account: '',
            user: {
                account: '',
                pwd: '',
            },
            spotify_logo: require('@/assets/login/spotify_logo.png'),
            third_login_src: [
                require('@/assets/login/google.png'),
                require('@/assets/login/facebook.png'),
                require('@/assets/login/apple.png')
            ],
            url: 'https://accounts.spotify.com/authorize?client_id=5e3c611726d54d488fb918a4c8a8739c&response_type=code&scope=user-read-playback-position user-read-email playlist-modify-private playlist-read-private user-library-modify playlist-read-collaborative user-follow-read user-read-playback-state user-read-currently-playing user-read-private playlist-modify-public user-library-read user-top-read ugc-image-upload user-follow-modify user-modify-playback-state user-read-recently-played&redirect_uri=http://localhost:8080/tags',
        }
    },
    methods: {
        login(){
            var random_seed = Math.floor(Math.random() * 1)
            console.log(random_seed)
            this.$router.push({
                name: 'tags',
                params: {

                }
            })
        },
        redirect() {
            // var headers = {
            //     "user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            // }
            // var url='https://accounts.spotify.com/authorize?client_id=5e3c611726d54d488fb918a4c8a8739c&response_type=token&redirect_uri=http://127.0.0.1:8000/show_token/&scope=user-read-private'

            // var url='https://accounts.spotify.com/zh-TW/login?continue=https:%2F%2Faccounts.spotify.com%2Fauthorize/'
            // // var url = 'api/login/'

            // this.axios.get(url, headers)
            // .then((response) => console.log(response))
            // .catch((error) => console.log(error))
            // LoginRedirect()
            // .then((response) => console.log(response))
            // .catch((error) => console.log(error))

            // window.location = 'https://accounts.spotify.com/zh-TW/login?continue=https:%2F%2Faccounts.spotify.com%2Fauthorize'

            Login().then((res)=>{
                console.log("call login api success")
                console.log(res['data']['res'])
            }).catch((error)=>{
                console.log("call login api failed", error)
            })

        }
    }
}
</script>

<style scoped>
#panel {
    background-color: white;
    width: 80%;
    border-radius:40px;
    margin-top: 20%;
}

#panel_elem {
    margin: 10% 50px 20% 50px;
}

#panel_logo {
    width: 25%;
    margin-top: -70px;
}

.el-input {
    font-size: 25px;
}

.el-input :deep(.el-input__inner) {
    height: 50px
}

.el-form-item :deep(.el-form-item__label) {
    font-size: 25px
}

#avater_container {
    margin-top: 30px;
    padding-bottom: 10%;
}


/* background-color: white;
    border: 1px solid black;
    border-radius:20px; */
</style>
