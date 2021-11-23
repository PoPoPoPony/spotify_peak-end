<template>
    <div>
        <iframe :src="source" width="100%" height="80" frameBorder="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
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
