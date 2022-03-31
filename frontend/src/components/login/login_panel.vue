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
                <el-row>
                    <h1>受試組別</h1>
                </el-row>
                <el-row class="row-bg" justify="space-around">
                    <el-col :span="3">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="1" border @change="GroupSelect">1</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :span="3">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="2" border @change="GroupSelect">2</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :span="3">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="3" border @change="GroupSelect">3</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :span="3">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="4" border @change="GroupSelect">4</el-radio-button>
                        </el-radio-group>
                    </el-col>
                </el-row>
                <el-row class="row-bg" justify="space-around" style="padding-top:50px">
                    <el-col :span="3">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="5" border @change="GroupSelect">5</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :span="3">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="6" border @change="GroupSelect">6</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :span="3">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="7" border @change="GroupSelect">7</el-radio-button>
                        </el-radio-group>
                    </el-col>
                    <el-col :span="3">
                        <el-radio-group v-model="exp_type" size="large">
                            <el-radio-button label="8" border @change="GroupSelect">8</el-radio-button>
                        </el-radio-group>
                    </el-col>
                </el-row>
                <el-row style="margin-top: 50px; padding-bottom: 50px">
                    <el-col :span="4" :offset="9">
                        <el-button type="primary" style="font-size: 25px;" :disabled="!GroupSelected" >
                            <el-link :href="backend_url" :underline="false" style="color: white; font-size: 30px" >Start</el-link>
                        </el-button>
                    </el-col>
                </el-row>
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
            // backend_url: "http://localhost:8888/login",
            backend_url: "http://localhost:8080/api/v1/auth/SpotifyAuth",
            exp_type: 0,
            GroupSelected: false,
        }
    },
    created() {

    },
    methods: {
        GroupSelect() {
            this.backend_url = "http://localhost:8080/api/v1/auth/SpotifyAuth"
            // this.backend_url = "http://localhost:8888/login"
            if(this.exp_type == 1) {
                this.$store.between_subject_type=0
                this.$store.within_subject_type=0
            } else if(this.exp_type == 2) {
                this.$store.between_subject_type=0
                this.$store.within_subject_type=1
            } else if(this.exp_type == 3) {
                this.$store.between_subject_type=0
                this.$store.within_subject_type=2
            } else if(this.exp_type == 4) {
                this.$store.between_subject_type=0
                this.$store.within_subject_type=3
            } else if(this.exp_type == 5) {
                this.$store.between_subject_type=1
                this.$store.within_subject_type=0
            } else if(this.exp_type == 6) {
                this.$store.between_subject_type=1
                this.$store.within_subject_type=1
            } else if(this.exp_type ==7) {
                this.$store.between_subject_type=1
                this.$store.within_subject_type=2
            } else if(this.exp_type == 8) {
                this.$store.between_subject_type=1
                this.$store.within_subject_type=3
            }

            // 0, 1 for doing discover weekly first
            // 2, 3 for doing seed first
            if(["0", "1", 0, 1].includes(this.$store.within_subject_type)) {
                this.backend_url+="?redirect_page=0"
            } else {
                this.backend_url+="?redirect_page=1"
            }
            let params="&between_subject_type=" + String(this.$store.between_subject_type)+"&within_subject_type=" + String(this.$store.within_subject_type)
            this.backend_url+=params
            console.log(this.backend_url)

            this.GroupSelected = true
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
    margin: 0 50px 20% 50px;
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

::v-deep .el-radio-button__inner {
    font-size:50px;
}

::v-deep .el-radio-button.is-bordered {
    padding: 30px 20px 30px 20px
}


/* background-color: white;
    border: 1px solid black;
    border-radius:20px; */
</style>
