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
                        <el-button type="primary" style="font-size: 25px;">Login</el-button>
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
                            <el-avatar shape="square" :size="100" fit="fill" :src="item" @click="test" style="background-color: white;"></el-avatar>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
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
            ]
        }
    },
    methods: {
        test(){
            console.log(123123123)
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

::v-deep .el-input .el-input__inner {
    height: 50px
}

::v-deep .el-form-item .el-form-item__label {
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



// /* spotify_icon 1 */

// position: absolute;
// width: 158px;
// height: 158px;

// background: url(.png);
// filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.5));
