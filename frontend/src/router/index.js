import { createRouter, createWebHistory } from 'vue-router'
import login from '@/views/login'
import tags from '@/views/tags'

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

]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
})

export default router
