<template>
    <div>
        <div id='bg'/>
        <navBar/>
        <h2 style="font-size: 50px; color: white;">請選擇標籤</h2>
        <div id="tagTable_container">
            <tagTable/>
        </div>
    </div>
</template>

<script>
import navBar from '@/components/navBar'
import tagTable from '@/components/tag/tag_table'

export default {
    name: 'tags',
    components: {
        navBar,
        tagTable,
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


#tagTable_container {
    margin-left: 15%;
    width: 70%
}
</style>



