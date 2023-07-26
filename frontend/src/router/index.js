import { createRouter, createWebHistory } from 'vue-router'
import login from '@/views/login'
import tags from '@/views/tags'
import song_list from '@/views/song_list'
import list_credit from '@/views/list_credit'
import create_list from '@/views/create_list'
import exercise from '@/views/exercise'
import second_test from '@/views/second_test'
import thanks from '@/views/thanks'


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
	},
	{
		path: '/create_list',
		name: 'create_list',
		component: create_list
	},
	{
		path: '/exercise',
		name: 'exercise',
		component: exercise
	},
	{
		path: '/second_test',
		name: 'second_test',
		component: second_test
	},
	{
		path: '/thanks',
		name: 'thanks',
		component: thanks
	},
]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
})

export default router
