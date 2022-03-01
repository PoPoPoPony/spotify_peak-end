<template>
    <div>
        <iframe :src="source" width="700" height="100%" frameBorder="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" id="mediaplayer"></iframe>
    </div>
</template>

<script>
export default {
    name: 'player',
    props: ['source']
}
</script>

<style scoped>

</style>
