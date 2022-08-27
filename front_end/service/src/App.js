import 'bootstrap/dist/css/bootstrap.css'
import { useState } from 'react'
import Delivery from './Delivery'
import { create_delivery } from './Html.js'
import { BACKEND_HOST } from './constants.js'

function App() {
  const [id, setId] = useState("")

  const submit = async (e) => {
    e.preventDefault()

    const form = new FormData(e.target)
    const data = Object.fromEntries(form.entries())
    const response = await fetch(`http://${BACKEND_HOST}:8000/deliveries/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: "CREATE_DELIVERY",
        data
      })
    })

    const { id } = await response.json()
    setId(id)
  }

  return <div className="py-5">
    <div className="d-grid gap-2 d-sm-flex justify-content-sm-center mb-5">
      {id === "" ? create_delivery(submit) : <Delivery id={id} />}
    </div>
  </div>
}

export default App;
