import React, { useEffect, useState } from 'react'
import { title, progress_bar, menu, show_response } from './Html.js'
import { BACKEND_HOST } from './constants.js'

const Delivery = (props) => {
    const [state, setState] = useState({})
    const [refresh, setRefresh] = useState(false)

    useEffect(() => {
        (async () => {
            const response = await fetch(`http://${BACKEND_HOST}:8000/deliveries/${props.id}/status`)
            const data = await response.json()

            setState(data)
        })()
    }, [refresh])

    const submit = async (e, type) => {
        e.preventDefault()
        const form = new FormData(e.target)
        const data = Object.fromEntries(form.entries())
        const response = await fetch('http://localhost:8000/event', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type,
                data,
                delivery_id: state.id
            })
        })

        if (!response.ok) {
            const { detail } = await response.json()
            alert(detail)
            return
        }

        setRefresh(!refresh)
    }

    return <div className='row w-100'>
        {title(state.id)}
        {progress_bar(state.status)}
        {menu(submit)}
        {show_response(state)}
    </div >

}

export default Delivery