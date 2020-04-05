let tb = document.getElementById('time_balance');

var d;

async function test() {
    const resp = await fetch('http://192.168.99.100:42069/api/deals?time=123');
    if (!resp.ok) {
        alert('we fucked up');
        return 0
    }
    else {
        const data = resp.json();
        return data
    }
}

test().then(data => {
    console.log(data);
    Plotly.newPlot(tb, [{ x: data.data.candle_time_start, y: data.data.amount, type: 'scatter' }]);
}).catch(e => console.log(e));
