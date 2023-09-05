<template>
    <div>
        <div id='bg'/>
        <el-row>
            <el-col :span="12" :offset='6'>
                <h1 class="animate__animated animate__fadeInLeft">
                    Thanks!
                </h1>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="4" :offset='3'>
                <img id='capoo' :src="require('@/assets/thanks/capoo.gif')"/>
            </el-col>
        </el-row>
        
    </div>
</template>

<script>
import {Update} from '@/apis/backendAPIs/statistics/update_statistics'

export default {
    name: 'thanks',
    components: {

    },
    mounted() {
        Update()
    },
    data(){
        return {
            
        }
    },
    created(){

    }
}
</script>

<style scoped>
#bg {
    width: 100%;
    height: 100%;
    background: url('~@/assets/thanks/capoo_bg.jpg') center center no-repeat;
    background-size: cover;
    position: fixed;
    margin: 0;
    top: 0px;
	left: 0px;
    z-index: -100;
}


h1 {
    font-size: 12vw;
    color: white;
    text-align: center;
    font-family: 'Reluctant-Aviator';
}
</style>