// Schéma API retourné par GET /events/
interface ApiEvent {
    id_event: number
    title: string
    begin_date: string
    end_date: string
    capacity?: number
    price: number
    reserved: number
    status: string
}

export const useDashboard = () => {
    const { data: eventsData } = useAsyncData<ApiEvent[]>(
        'dashboard-events',
        () => $fetch<ApiEvent[]>('/api/events/'),
        { default: () => [] as ApiEvent[] }
    )

    const { data: organizersData } = useAsyncData(
        'dashboard-organizers',
        () => $fetch<{ id_organizer: number }[]>('/api/organizers/'),
        { default: () => [] as { id_organizer: number }[] }
    )

    const loading = ref(false)
    const error = ref<string | null>(null)

    const totalEvents = computed(() => (eventsData.value || []).length)

    const totalParticipants = computed(() =>
        (eventsData.value || []).reduce((sum, e) => sum + (e.reserved || 0), 0)
    )

    const totalRevenue = computed(() =>
        (eventsData.value || []).reduce((sum, e) => sum + (e.price || 0) * (e.reserved || 0), 0)
    )

    const totalOrganizers = computed(() => (organizersData.value || []).length)

    const fillRate = computed(() => {
        const eventsWithCapacity = (eventsData.value || []).filter(e => e.capacity && e.capacity > 0)
        if (!eventsWithCapacity.length) return 0
        return Math.round(
            eventsWithCapacity.reduce((sum, e) => sum + (e.reserved || 0) / e.capacity!, 0)
            / eventsWithCapacity.length * 100
        )
    })

    const weekData = computed(() => {
        const days = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam']
        const counts: Record<string, number> = { Lun: 0, Mar: 0, Mer: 0, Jeu: 0, Ven: 0, Sam: 0, Dim: 0 }
            ; (eventsData.value || []).forEach(e => {
                const d = new Date(e.begin_date)
                const dayName = days[d.getDay()]
                if (dayName && dayName in counts) {
                    counts[dayName] = (counts[dayName] || 0) + (e.reserved || 0)
                }
            })
        return [
            { name: 'Lun', value: counts['Lun'] ?? 0 },
            { name: 'Mar', value: counts['Mar'] ?? 0 },
            { name: 'Mer', value: counts['Mer'] ?? 0 },
            { name: 'Jeu', value: counts['Jeu'] ?? 0 },
            { name: 'Ven', value: counts['Ven'] ?? 0 },
            { name: 'Sam', value: counts['Sam'] ?? 0 },
            { name: 'Dim', value: counts['Dim'] ?? 0 },
        ]
    })

    const fetchStats = async () => {
        await refreshNuxtData(['dashboard-events', 'dashboard-organizers'])
    }

    return {
        loading,
        error,
        totalEvents,
        totalParticipants,
        totalRevenue,
        fillRate,
        totalOrganizers,
        weekData,
        fetchStats,
    }
}
