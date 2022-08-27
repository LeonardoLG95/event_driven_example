export function create_delivery(submit) {
    return <div className="card">
        <div className="card-header">
            Create Delivery
        </div>
        <form className="card-body" onSubmit={submit}>
            <div className="mb-3">
                <input type="number" name="budget" className="form-control" placeholder="Budget"></input>
            </div>
            <div className="mb-3">
                <textarea name="notes" className="form-control" placeholder="Notes" />
            </div>
            <button className="btn btn-primary">Submit</button>
        </form>
    </div>
}

export function title(id) {
    return <div className='col-12 mb-4'>
        <h4 className='fw-bold text-white'>Delivery {id}</h4>
    </div>
}

export function progress_bar(status) {
    return <div className='col-12 mb-5'>
        <div className='progress'>
            {status !== 'ready' ?
                <div className={
                    status === 'active' ?
                        'progress-bar bg-success progress-bar-striped progress-bar-animated' :
                        'progress-bar bg-success'}
                    role='progressbar'
                    style={{ width: '50%' }}></div> : ''}
            {status === 'collected' || status === 'completed' ?
                <div className={status === 'completed' ?
                    'progress-bar bg-success' :
                    'progress-bar bg-success progress-bar-striped progress-bar-animated'}
                    role='progressbar'
                    style={{ width: '50%' }}></div> : ''}
        </div>
    </div>
}

export function menu(submit) {
    return <><div className='col-3'>
        <div className="card">
            <div className="card-header">
                Start Delivery
            </div>
            <form className="card-body" onSubmit={e => submit(e, 'START_DELIVERY')}>
                <button className="btn btn-primary">Submit</button>
            </form>
        </div>
    </div><div className='col-3'>
            <div className="card">
                <div className="card-header">
                    Increase budget
                </div>
                <form className="card-body" onSubmit={e => submit(e, 'INCREASE_BUDGET')}>
                    <div className="mb-3">
                        <input type="number" name="budget" className="form-control" placeholder="Budget"></input>
                    </div>
                    <button className="btn btn-primary">Submit</button>
                </form>
            </div>
        </div><div className='col-3'>
            <div className="card">
                <div className="card-header">
                    Pickup products
                </div>
                <form className="card-body" onSubmit={e => submit(e, 'PICKUP_PRODUCTS')}>
                    <div className="mb-3">
                        <input type="number" name="purchase_price" className="form-control" placeholder="Purchase price"></input>
                    </div>
                    <div className="mb-3">
                        <input type="number" name="quantity" className="form-control" placeholder="Quantity"></input>
                    </div>
                    <button className="btn btn-primary">Submit</button>
                </form>
            </div>
        </div><div className='col-3'>
            <div className="card">
                <div className="card-header">
                    Deliver products
                </div>
                <form className="card-body" onSubmit={e => submit(e, 'DELIVER_PRODUCTS')}>
                    <div className="mb-3">
                        <input type="number" name="sell_price" className="form-control" placeholder="Sell price"></input>
                    </div>
                    <div className="mb-3">
                        <input type="number" name="quantity" className="form-control" placeholder="Quantity"></input>
                    </div>
                    <button className="btn btn-primary">Submit</button>
                </form>
            </div>
        </div></>
}

export function show_response(state) {
    return <code className='col-12 mt-4'>
        {
            JSON.stringify(state)
        }
    </code>
}
