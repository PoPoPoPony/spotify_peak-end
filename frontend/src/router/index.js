import { createRouter, createWebHistory } from 'vue-router'
import login from '@/views/login'
import tags from '@/views/tags'
import song_list from '@/views/song_list'

const routes = [
	{
		path: '/',
		name: 'login',
		component: login
	},
	{
		path: '/tags',
		name: 'tags',
		component: tags
	},
	{
		path: '/songList' ,
		name: 'song_list',
		component: song_list
	},

]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
})

export default router
