import { createRouter, createWebHistory } from 'vue-router'
import login from '@/views/login'
import tags from '@/views/tags'
import song_list from '@/views/song_list'
import list_credit from '@/views/list_credit'

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
	{
		path: '/list_credit',
		name: 'list_credit',
		component: list_credit
	}

]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
})

export default router
