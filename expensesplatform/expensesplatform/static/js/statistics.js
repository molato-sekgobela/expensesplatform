const renderChart = (data, labels) => {
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          label: 'Last 6 Months Expenses per category',
          data: data,
          borderWidth: 1
        }]
      },
      options: {
          title: {
              display: true,
              text: 'Expenses per category',
          },
        
      },
    });
}

const getChartData = () => {
    console.log("fetching data");
    fetch("/expense-category-summary")
    .then((res) => res.json())
    .then((results) => {

         const category_data = results.expense_category_data;
         const [labels, data] = [
            Object.keys(category_data), 
            Object.values(category_data)
        ];
         renderChart(data, labels);
        console.log(results);
    });
}

document.onload = getChartData();
