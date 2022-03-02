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
            <el-button id="send_btn" type="primary" :disabled='send_disable' @click="send_list_credit">送出</el-button>
        </div>
    </div>
</template>



<script>

export default {
    name: 'list_credit',
    created() {
        let urlParams = new URLSearchParams(window.location.search)
        this.list_type = urlParams.get('list_type')

    },
    data() {
        return {
            credit: 0,
            send_disable: true,
            list_type:0,
        }
    },
    methods: {
        credit_change(val) {
            this.send_disable = false
            console.log(val)
        },
        send_list_credit() {
            if(this.list_type==0) {
                console.log("credit weekly discovery success!")
            } else if(this.list_type==1) {
                console.log("credit seed song list success!")
            }
            if(this.$store.pass_exp_num == 1) {
                // 1 表示只完成第一個實驗，需要導覽至下一個實驗
                // within_subject_type: 
                // 0, 1 -> to seed page
                // 2, 3 -> to weekly discovery page
                
                var new_page = ''
                
                if(["0", 0, "1", 1].includes(this.$store.within_subject_type)) {
                    new_page = 'tags'
                } else if(["2", 2, "3", 3].includes(this.$store.within_subject_type)) {
                    new_page = 'create_list'
                }

                this.$router.push({
                    name: new_page,
                    query: {
                        access_token: this.$store.access_token,
                        between_subject_type: this.$store.between_subject_type,
                        within_subject_type: this.$store.within_subject_type,
                        pass_exp_num: this.$store.pass_exp_num
                    }
                })

            } else if(this.$store.pass_exp_num == 2) {
                console.log("Exp Finish. Thank you!")
            }
        }
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