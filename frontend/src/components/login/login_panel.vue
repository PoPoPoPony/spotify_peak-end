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
                組別
                <el-row>
                    <el-col>
                        <el-radio-button v-model="exp_type" label="1" size="large" border class="expTypeRadio">1</el-radio-button>
                    </el-col>
                    <el-col>
                        <el-radio-button v-model="exp_type" label="2" size="large" border class="expTypeRadio">2</el-radio-button>
                    </el-col>
                    <el-col>
                        <el-radio-button v-model="exp_type" label="3" size="large" border class="expTypeRadio">3</el-radio-button>
                    </el-col>
                    <el-col>
                        <el-radio-button v-model="exp_type" label="4" size="large" border class="expTypeRadio">4</el-radio-button>
                    </el-col>

                </el-row>
                <el-row style="margin-bottom: 100px; margin-top: 20px;">
                    <el-col :span="4" :offset="8">
                        <el-button type="primary" style="font-size: 25px;" >
                            <el-link :href="backend_url" :underline="false" style="color: white; font-size: 30px" >Redirect</el-link>
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
            backend_url: "http://localhost:8888/login",
            exp_type: 1,
        }
    },
    created() {
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
