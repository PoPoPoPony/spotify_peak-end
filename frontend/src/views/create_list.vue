<template>
    <div>
        <div id='bg'/>
        <navBar/>
        <div id="credit_container" class="animate__animated animate__fadeInUp">
            <span id="title">請為整體歌單評分</span>
            <el-image style="width: 200px; height: 200px; margin-top: 50px; display: block; left: 30%" :src="album_src" fit='cover'></el-image>
            <el-button type="primary" style="margin-top: 50px" @click="create">建立</el-button>
        </div>
    </div>
</template>

<script>
import navBar from '@/components/navBar'


export default {
    name: 'create_list',
    components: {
        navBar
    },
    data() {
        return {
            album_src: require('@/assets/create_list/cover.jpeg'),
        }
    },
    methods: {
        create() {
            this.$router.push({
                name: 'song_list',
                params: {

                }
            })
        }
    }
}
</script>

<style scoped>
#bg {
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, #72BFE6 0%, #46277A 100%);
    background-size: cover;
    position: fixed;
    margin: 0;
    top: 0px;
	left: 0px;
    z-index: -100;
}

#credit_container {
    width: 500px;
    height: 200px;
    position: absolute;
    justify-content: center;
    top: 50%;
    left: 50%;
    margin: -300px 0 0 -250px;
    background-color: transparent;
    border-radius: 20px;
    padding-top: 70px
}

#title {
    font-family: 'HYZhengYuan';
    color: white;
    font-size: 40px;
    display: block;
}
</style>