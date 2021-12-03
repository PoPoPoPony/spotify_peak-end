<template>
    <div>
        <div id='bg'/>
        <div id="credit_container" class="animate__animated animate__fadeInUp">
            <span id="title">請為整體歌單評分</span>
            <el-row justify="center">
                <el-col :span="16">
                    <el-slider v-model="credit" @change='credit_change' style='padding-top: 20px'></el-slider>
                </el-col>
            </el-row>
            <el-button id="send_btn" type="primary" :disabled='send_disable'>Success</el-button>
        </div>
    </div>
</template>

<script>




export default {
    name: 'list_credit',
    data() {
        return {
            credit: 0,
            send_disable: true
        }
    },
    methods: {
        credit_change(val) {
            this.send_disable = false
            console.log(val)
        },
    }
}
</script>

<style scoped>
#bg {
    width: 100%;
    height: 100%;
    background: black;
    background-size: cover;
    position: fixed;
    margin: 0;
    top: 0px;
	left: 0px;
    z-index: -100;
}

#credit_container {
    width: 800px;
    height: 200px;
    position: absolute;
    top: 50%;
    left: 50%;
    margin: -200px 0 0 -400px;
    background-color: white;
    border-radius: 20px;
    padding-top: 70px
}

#title {
    color: black;
    font-size: 40px;

}

:deep(.el-rate__icon) {
    font-size: 50px;
}

#send_btn {
    margin-top: 30px;
}

</style>