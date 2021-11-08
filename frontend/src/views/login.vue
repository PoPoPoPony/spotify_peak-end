<template>
    <div>
        <div id='bg'/>
        <el-row :offset="1">
            <el-col :span="4">
                <img id="spotify_nav" :src="spotify_icon_with_text" alt="">
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="16" :offset='2'>
                <slogan></slogan>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import slogan from '@/components/login/slogan'


export default {
    name: 'login',
    components: {
        slogan,
    },
    data(){
        return {
            spotify_icon_with_text: require('../assets/login/spotify_logo_with_text.png')
        }
    }
}
</script>

<style scoped>
#bg {
    width: 100%;
    height: 100%;
    background: url('~@/assets/login/login_bg_pic.png') center center no-repeat;
    background-size: cover;
    position: fixed;
    margin: 0;
    top: 0px;
	left: 0px;
    z-index: -100;
}

#spotify_nav {
    width: 300px;

}
</style>