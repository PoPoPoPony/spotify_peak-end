<template>
    <div>
        <div id='bg'/>
        <div id="credit_container" class="animate__animated animate__fadeInDown">
            <span id="title">請為整體歌單評分</span>
            <el-row justify="center">
                <el-col :span="16">
                    <el-slider v-model="credit" @change='credit_change' style='padding-top: 20px'></el-slider>
                </el-col>
            </el-row>
            <el-button id="send_btn" type="primary" :disabled='send_disable' @click="send_list_credit">送出</el-button>
            <!-- <div v-if="unauth_show" class="animate__animated animate__fadeInDown">
                <h1>
                    Thank You!
                    <br>
                    You can unauthorize this app if you want : 
                    <br>
                    <v-html>https://www.spotify.com/tw/account/apps/</v-html>
                </h1>
            </div> -->
        </div>
    </div>
</template>



<script>
import {UpdateSongListScore} from '@/apis/backendAPIs/songListScore/update_songList_score'
import {GetSongListScoreLen} from '@/apis/backendAPIs/songListScore/get_songList_score'

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
            unauth_show: false,
            exp_num : 0,
            promise: '',
        }
    },
    methods: {
        credit_change(val) {
            this.send_disable = false
            console.log(val)
        },
        async send_list_credit() {
            if(this.list_type==0) {
                await UpdateSongListScore(this.$store.state.WD_ID, this.$store.state.userID, this.credit)
                GetSongListScoreLen(this.$store.state.userID).then((res)=>{
                    let retv = res.data
                    this.redirect(retv)
                })


                // redirect()
            } else if(this.list_type==1) {
                await UpdateSongListScore(this.$store.state.T_ID, this.$store.state.userID, this.credit)
                GetSongListScoreLen(this.$store.state.userID).then((res)=>{
                    let retv = res.data
                    this.redirect(retv)
                })
            }

        },

        redirect(pass_exp_num) {
            // [TODO] get exp num from DB
            if(pass_exp_num == 1) {
                // 1 表示只完成第一個實驗，需要導覽至下一個實驗
                // within_subject_type: 
                // 0, 1 -> to seed page
                // 2, 3 -> to weekly discovery page
                
                var new_page = ''
                
                if(["0", "1"].includes(this.$store.state.within_subject_type)) {
                    new_page = 'tags'
                } else if(["2", "3"].includes(this.$store.state.within_subject_type)) {
                    new_page = 'create_list'
                }

                this.$router.push({
                    name: new_page,
                    query: {
                        access_token: this.$store.state.access_token,
                        between_subject_type: this.$store.state.between_subject_type,
                        within_subject_type: this.$store.state.within_subject_type,
                    }
                })

            } else if(pass_exp_num == 2) {
                window.location = "https://forms.gle/LGjTEhG7Qeq6Lg5K6"
            } else if (pass_exp_num == 3) { // 相當於第二次做了一次
                this.$router.push({
                    name: 'second_test',
                    query: {
                        userID: this.$store.state.userID,
                        access_token: this.$store.state.access_token,
                        list_type: 1
                    }
                })
            } else if (pass_exp_num == 4) {
                window.location = "www.youtube.com"
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