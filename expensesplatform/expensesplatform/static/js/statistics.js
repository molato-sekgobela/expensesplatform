const renderChart = (data, labels) => {
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Expenses per category',
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                datalabels: {
                    color: '#fff', // Text color
                    font: {
                        weight: 'bold'
                    },
                    formatter: (value, ctx) => {
                        return ctx.chart.data.labels[ctx.dataIndex] + '\n' + value; // Display label and value
                    }
                }
            },
            title: {
                display: true,
                text: 'Expenses per category'
            }
        }
    });
};

const getChartData = () => {
    console.log("fetching data");
    fetch("/expense-category-summary")
        .then((res) => res.json())
        .then((results) => {
            const category_data = results.expense_category_data;
            const labels = Object.keys(category_data);
            const data = Object.values(category_data);
            renderChart(data, labels);
            console.log(results);
        })
        .catch((error) => {
            console.error("Error fetching chart data:", error);
        });
};

document.addEventListener('DOMContentLoaded', getChartData);
