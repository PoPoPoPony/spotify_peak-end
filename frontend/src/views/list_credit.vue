<template>
    <div>
        <div id='bg'/>
    </div>
</template>

<script>
export default {
    name: 'list_credit',
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
</style>