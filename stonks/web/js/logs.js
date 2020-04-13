let tb = document.getElementById('time_balance');
let draw_btn = document.getElementById('draw_btn');
draw_btn.addEventListener('click', startDrawing);

var graph_data;
var update_interval;

async function getData(time_start, time_finish, type) {
    const resp = await fetch(`http://0.0.0.0:5000/api/deals?time_start=${time_start}&time_finish=${time_finish}`);
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
    let now = (new Date()).getTime();
    getData(now - 60, now)
        .then(data => {
            graph_data = data.data;
            Plotly.react(tb, [{ x: graph_data.candle_time_start, y: graph_data.amount, type: 'scatter' }]);
            update_interval = setInterval(updateData, 1000);
        }).catch(e => {
            alert("Oops, something went wrong!");
            console.log(e);
        });
}

function updateData() {
    let now = (new Date()).getTime();
    getData(graph_data.candle_time_start[graph_data.candle_time_start.length - 1], now)
        .then(data => {
            graph_data.candle_time_start.concat(data.data.candle_time_start);
            graph_data.amount.concat(data.data.amount);
            console.log(data.data.candle_time_start);
            Plotly.react(tb,
                [{
                    x: graph_data.candle_time_start,
                    y: graph_data.amount,
                    type: 'scatter'
                }]
            );
        });
}
