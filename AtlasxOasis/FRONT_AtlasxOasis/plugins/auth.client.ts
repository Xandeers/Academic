export default defineNuxtPlugin((nuxtApp) => {
	console.log("Plugin appelé")
	const auth = useAuthStore()
	auth.restoreSession()
	console.log("user: ", auth.user)
	console.log("token: ", auth.token)
})
