<template>
    <div>
        <el-row :offset="1">
            <el-col :span="4">
                <img id="spotify_nav" :src="spotify_icon_with_text" alt="">
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
    name: 'nav',
    data () {
        return {
            spotify_icon_with_text: require('@/assets/login/spotify_logo_with_text.png'),
        }
    }
}
</script>

<style scoped>
#spotify_nav {
    width: 300px;
}
</style>