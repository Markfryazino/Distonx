let tb = document.getElementById('time_balance');
let draw_btn = document.getElementById('draw_btn');
draw_btn.addEventListener('click', startDrawing);

var graph_data;

async function getData(time_start, time_finish, type) {
    const resp = await fetch(`http://0.0.0.0:5000/api/deals?start_time=${time_start}&time_finish=${time_finish}`);
    if (!resp.ok) {
        alert(`Bad request!\n${resp.json()}`);
        return 0
    }
    else {
        const data = resp.json();
        return data
    }
}

function startDrawing() {
    getData().then(data => {
        graph_data = data.data;
        Plotly.newPlot(tb, [{ x: graph_data.candle_time_start, y: graph_data.amount, type: 'scatter' }]);
    }).catch(e => {
        alert("Oops, something went wrong!");
        console.log(e);
    });
}

function updateData() {
    getData().then(data => {
        graph_data.candle_time_start.concat(data.data.candle_time_start);
        graph_data.amount.concat(data.data.amount);
        Plotly.extendTraces(tb,
            [
                {
                    x: data.data.candle_time_start,
                    y: data.data.amount
                }
            ],
            [0],
            data.data.candle_time_start.length()
        );
    })
}

