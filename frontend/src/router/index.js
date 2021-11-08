import { createRouter, createWebHistory } from 'vue-router'
import login from '@/views/login'

const routes = [
	{
		path: '/',
		name: 'login',
		component: login
	},

]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
})

export default router
