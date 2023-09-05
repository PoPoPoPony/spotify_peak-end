<template>
    <div class="animate__animated animate__fadeInDown">
        <div id="panel">
            <img id="panel_logo" :src="spotify_logo" alt="">
            <div id="panel_elem">
                <!-- <el-form label-position='top' label-width="100px" :model="user">
                    <el-form-item label="Account">
                        <el-input v-model="user.account"></el-input>
                    </el-form-item>
                    <el-form-item label="Password">
                        <el-input v-model="user.pwd" show-password></el-input>
                    </el-form-item>
                </el-form> -->
                <el-row style="font-size: 25px;">
                    <h3 style="font-size: 1.8vw">
                        信箱 : 
                    </h3>
                </el-row>
                <el-row style="padding-bottom: 20px">
                    <el-input placeholder="請輸入常用信箱" v-model="userEmail" clearable  @change="userEmailChanged"></el-input>
                </el-row>
                <el-row>
                    <el-col :xs="{'span':'5', 'offset': '3'}" :sm="{'span':'5', 'offset': '6'}" :lg="{'span': '5', 'offset': '7'}">
                        <el-button type="success" style="font-size: 1vw" size='small' @click="onSecondTest" :disabled='second_test_disable'>
                            <el-icon style="font-size:1vw"><ArrowRightBold /></el-icon>
                            <span style="vertical-align: middle;"> 第二次測驗 </span>
                        </el-button>
                    </el-col>
                </el-row>
                <el-row>
                    <h1 style="font-size: 1.8vw">
                        受試組別
                    </h1>
                </el-row>
                <el-row class="row-bg" justify="space-around">
                    <el-col :xs="{'span':'1'}" :sm="{'span':'2'}" :lg="{'span': '3'}">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="1" border @change="GroupSelect">1</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :xs="{'span':'1'}" :sm="{'span':'2'}" :lg="{'span': '3'}">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="2" border @change="GroupSelect">2</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :xs="{'span':'1'}" :sm="{'span':'2'}" :lg="{'span': '3'}">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="3" border @change="GroupSelect">3</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :xs="{'span':'1'}" :sm="{'span':'2'}" :lg="{'span': '3'}">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="4" border @change="GroupSelect">4</el-radio-button>
                        </el-radio-group>
                    </el-col>
                </el-row>
                <el-row class="row-bg" justify="space-around" style="padding-top:1vw">
                    <el-col :xs="{'span':'1'}"  :sm="{'span':'2'}" :lg="{'span': '3'}">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="5" border @change="GroupSelect">5</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :xs="{'span':'1'}" :sm="{'span':'2'}" :lg="{'span': '3'}">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="6" border @change="GroupSelect">6</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :xs="{'span':'1'}" :sm="{'span':'2'}" :lg="{'span': '3'}">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="7" border @change="GroupSelect">7</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :xs="{'span':'1'}" :sm="{'span':'2'}" :lg="{'span': '3'}">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="8" border @change="GroupSelect">8</el-radio-button>
                        </el-radio-group>
                    </el-col>
                </el-row>
                <el-row style="margin-top: 1.5vw; padding-bottom: 2vw">
                    <el-col :xs="{'span':'1', 'offset': '7'}" :sm="{'span':'3', 'offset': '9'}" :lg="{'span': '4', 'offset': '9'}">
                        <!--  :disabled="!GroupSelected || !userNameInputed"  -->
                        <el-button v-if="GroupSelected && userEmailInputed" type="primary" style="padding: 0; margin: 0">
                            <el-link :href="backend_url" :underline="false" style="color: white; font-size: 1.5vw; padding: 0.7vw 0.9vw 0.7vw 0.9vw;" >Start</el-link>
                        </el-button>
                    </el-col>
                </el-row>

                <!-- Test@gmail.com -->

                <!-- <el-row>
                    <el-col :span="11">
                        <hr style="border: 1px solid black;"/>
                    </el-col>
                    <el-col :span="2">
                        <text style="font-size: 20px">or</text>
                    </el-col>
                    <el-col :span="11">
                        <hr style="border: 1px solid black;"/>
                    </el-col>
                </el-row> -->
                <!-- <div id="avater_container">
                    <el-row justify="space-between">
                        <el-col :span="6" v-for="(item, index) in third_login_src" :key="index" style="border: 1px solid black; border; border-radius: 10px;">
                            <el-avatar shape="square" :size="100" fit="fill" :src="item" style="background-color: white;"></el-avatar>
                        </el-col>
                    </el-row>
                </div> -->
            </div>
        </div>
    </div>
</template>

<script>
// import {SignOut} from '@/apis/sign_out.js'
import { ElNotification } from 'element-plus'
import { ArrowRightBold } from '@element-plus/icons'
import { GetUser } from '@/apis/backendAPIs/user/get_user'
import { uuid } from 'vue-uuid'
// import {UpdateSongListInfo} from '@/apis/backendAPIs/songListInfo/update_songList_info'

export default {
    name: 'login_panel',
    components: {
        ArrowRightBold
    },
    data() {
        return {
            spotify_logo: require('@/assets/login/spotify_logo.png'),
            third_login_src: [
                require('@/assets/login/google.png'),
                require('@/assets/login/facebook.png'),
                require('@/assets/login/apple.png')
            ],
            // backend_url: "http://localhost:8888/login",
            backend_url: "http://ponylis.ddns.net:8080/api/v1/auth/SpotifyAuth",
            exp_type: 0,
            GroupSelected: false,
            // for testing
            // userEmail: "",
            userEmail: "",
            userEmailInputed: false,
            // userEmailInputed: true,
            expObject : {
                "within": "0",
                "between":"0",
            },
            second_test_disable: true,
            user_uuid: '',
        }
    },
    created() {

    },
    mounted() {
        this.user_uuid = uuid.v4()
    },
    methods: {
        GroupSelect() {
            if(this.exp_type == 1) {
                this.expObject['between'] = "0"
                this.expObject['within'] = "0"
            } else if(this.exp_type == 2) {
                this.expObject['between'] = "0"
                this.expObject['within'] = "1"
            } else if(this.exp_type == 3) {
                this.expObject['between'] = "0"
                this.expObject['within'] = "2"
            } else if(this.exp_type == 4) {
                this.expObject['between'] = "0"
                this.expObject['within'] = "3"
            } else if(this.exp_type == 5) {
                this.expObject['between'] = "1"
                this.expObject['within'] = "0"
            } else if(this.exp_type == 6) {
                this.expObject['between'] = "1"
                this.expObject['within'] = "1"
            } else if(this.exp_type ==7) {
                this.expObject['between'] = "1"
                this.expObject['within'] = "2"
            } else if(this.exp_type == 8) {
                this.expObject['between'] = "1"
                this.expObject['within'] = "3"
            }

            this.$store.dispatch("initExpType", this.expObject)
            // console.log(this.$store.state.within_subject_type)
            // console.log(this.$store.state.between_subject_type)
            this.setBackendURL()
            this.GroupSelected = true
        },
        async userEmailChanged() {
            let DB_email=''
            await GetUser(this.userEmail).then((res)=>{
                let retv = res.data
                DB_email = retv
            })

            if(this.isEmail(this.userEmail.trim())) {
                this.userEmailInputed = true
                if(DB_email) {
                    this.userEmailInputed = false
                    this.second_test_disable = false
                    ElNotification({
                        title: 'Warning',
                        message: 'This Email is Already in the DataBase!',
                        type: 'warning',
                    })
                } else {
                    this.second_test_disable = true
                }
            } else {
                this.userEmailInputed = false
                this.second_test_disable = true
                ElNotification({
                    title: 'Error',
                    message: 'Wrong Email Format!',
                    type: 'error',
                }) 
            }
            this.setBackendURL()
        }, 
        isEmail(email) {
            var regex = /^([a-zA-Z0-9_.\-+])+@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            if(!regex.test(email)) {
                return false;
            } else {
                return true;
            }
        },

        // 在vuex中存入使用者的信息
        setBackendURL() {
            this.backend_url = "http://ponylis.ddns.net:8080/api/v1/auth/SpotifyAuth"

            // 0, 1 for doing discover weekly first
            // 2, 3 for doing seed first
            if(["0", "1"].includes(this.$store.state.within_subject_type)) {
                this.$store.dispatch("initExerciseRedirectPage", "0")
            } else {
                this.$store.dispatch("initExerciseRedirectPage", "1")
            }

            this.$store.dispatch("initUserID", this.user_uuid)
            this.$store.dispatch("initUserEmail", this.userEmail.trim())
            this.$store.dispatch("initPeriod", "first")

            // console.log(this.backend_url)
        },
        // 做第二次的實驗
        // [TODO] 需修改
        onSecondTest() {
            this.$store.dispatch("initUserEmail", this.userEmail.trim())
            this.$store.dispatch("initPeriod", "second")

            GetUser(this.userEmail.trim()).then((res)=>{
                let retv = res.data
                if(retv) {
                    window.location.assign(
                        "http://ponylis.ddns.net:8080/api/v1/auth/SpotifyAuth2"
                    )
                } else {
                    ElNotification({
                        title: 'Error',
                        message: 'User is not exsist!',
                        type: 'error',
                    })
                }
            }).catch((err)=>{
                console.log('call getUser faild')
                console.log(err)
            })
        },
    }
}
</script>

<style scoped>
#panel {
    background-color: white;
    width: 80%;
    border-radius:40px;
    margin-top: 0%;
    height: 35vw;
}

#panel_elem {
    margin: 0 2vw 0 2vw;
}

#panel_logo {
    width: 25%;
    margin-top: -7vh;
}

.el-input {
    font-size: 1vw;
}

.el-input :deep(.el-input__inner) {
    height: 2.5vw
}

.el-form-item :deep(.el-form-item__label) {
    font-size: 25px
}

/* #avater_container {
    margin-top: 30px;
    padding-bottom: 10%;
} */

::v-deep .el-radio-button__inner {
    font-size:2vw;
    padding: 0.7vw 0.8vw 0.7vw 0.8vw;
}

::v-deep .el-radio-button.is-bordered {
    padding: 2vw 1vw 2vw 1vw
}



/* background-color: white;
    border: 1px solid black;
    border-radius:20px; */
</style>
