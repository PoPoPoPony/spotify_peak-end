<template>
    <div>
        <div id='bg'/>
        <navBar/>
        <el-row>
            <el-col :span="10" :offset='2'>
                <slogan/>
            </el-col>
            <el-col :span="7" :offset='3'>
                <loginPanel/>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import slogan from '@/components/login/slogan'
import loginPanel from '@/components/login/login_panel'
import navBar from '@/components/nav'

export default {
    name: 'login',
    components: {
        slogan,
        loginPanel,
        navBar,
    },
    data(){
        return {
            
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
</style>