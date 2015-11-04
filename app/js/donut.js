var chartData = new Object();
var initialCount = 0;
var chartMin = "";
var MAX_BUCKETS = 5;

function addMapToChart(map, chart) {
    for (var name in map) {
        console.log("Adding to chart: " + name + "(" + map[name][0] + ")");
        if (chartData[name]) {
            // Update the count for the genus with the new map
            chartData[name][0] += map[name][0];

            // Update chart if the genus appears in the chart
            chartIndex = chartData[name][1];
            if (chartIndex > -1) {
                chart.segments[chartIndex].value = chartData[name][0];
                chart.update();
                udpateChartMin(chart);
            } else {
                checkChartUpdates(name, chart);
            }
        } else {
            // Add the new data to the overall chartData
            chartData[name] = map[name];

            // Fill data if chart is empty, otherwise add normally
            if (initialCount < MAX_BUCKETS) {
                fillInitialData(name, chart);
            } else {
                checkChartUpdates(name, chart);
            }
        }
    }
};

function fillInitialData(name, chart) {
    if (initialCount == 0) {
        chartMin = name;
    }

    // Fill chart up until we have 5 buckets
    chartData[name][1] = initialCount;
    initialCount++;

    // Update minimum data point in chart
    if (chartData[chartMin][0] >= chartData[name][0]) {
        chartMin = name;
    };

    chartColor = color();
    chart.addData({
        value: chartData[name][0],
        color: "rgba(" + chartColor + ", 1)",
        highlight: "rgba(" + chartColor + ", .7)",
        label: name
    }, chartData[name][1]);

    if (initialCount == MAX_BUCKETS) {
        // Add one more bucket to denote other
    };
}

function checkChartUpdates(name, chart) {
    if (chartData[chartMin][0] <= chartData[name][0]) {
        tempIndex = chartData[chartMin][1];
        chartData[chartMin][1] = -1;
        chartData[name][1] = tempIndex;
    
        // Remove min name and add new name
        chartColor = color();
        chart.addData({
            value: chartData[name][0],
            color: "rgba(" + chartColor + ", 1)",
            highlight: "rgba(" + chartColor + ", .7)",
            label: name
        }, chartData[name][1]);
        chart.removeData(chartData[name][1]+1);

        // Find new minimum in chart data
        udpateChartMin(chart);
    };
}

function udpateChartMin(chart) {
    var minCount = 100000;
    for (var i = 0; i<chart.segments.length; i++) {
        data = chart.segments[i];
        if (minCount > data.value) {
            chartMin = data.label;
            minCount = data.value;
        };
    }
}

function color() {
    r = Math.floor(Math.random() * 255).toString();
    g = Math.floor(Math.random() * 255).toString();
    b = Math.floor(Math.random() * 255).toString();
    return r+","+g+","+b
}
