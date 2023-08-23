<template>
    <div>
        <!-- <iframe :src="source" width="700" height="100%" frameBorder="" allow="clipboard-write; encrypted-media; fullscreen; picture-in-picture" id="mediaplayer"></iframe> -->
        <div class="container">
            <vue-plyr ref="plyr">
                <audio controls crossorigin playsinline>
                    <source
                        :src="source"
                        type="audio/mp3"
                    />
                </audio>
            </vue-plyr>
        </div>
    </div>
</template>

<script>
export default {
    name: 'player',
    props: ['source', 'idx'],

    data() {
        return {
            ifReternedListened: false
        }
    },

    mounted() {
        this.$refs.plyr.player.on('timeupdate', this.updateTimeCallback)
        this.$refs.plyr.player.on('ended', this.endedCallback)
    },
    

    methods: {
        // 原本有show播放元件，所以用這個方法(刪除播放元件後，可改用下面的方法)
        // this.$refs.plyr.player.currentTime> 29
        updateTimeCallback() {
            if(this.$refs.plyr.player.currentTime>29 && !this.ifReternedListened) {
                this.$emit("song_listened", this.idx)


                // 測試用，聽1秒就直接下一首
                // this.$emit("song_ended", this.idx)

                this.ifReternedListened = true
            }
        },
        endedCallback() {
            this.$emit("song_ended", this.idx)
        }
    },
}







</script>

<style scoped>
.container{
    margin: 200px auto;
    max-width: 500px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);

}
</style>
