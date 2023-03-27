function chartPlotter(data_cal, sp_labels,data_dig, dig_labels, im_filename, imheight) {
  plotButton = document.getElementById("process_input");
  plotButton.addEventListener("click", function(){
  calChart.destroy();
  digChart.destroy();
  });
  cal_ctx = document.getElementById('calChart').getContext('2d');
  dig_ctx = document.getElementById('digChart').getContext('2d');
  calChart = new Chart(cal_ctx, {
  type: 'line',
    data: {
      labels: sp_labels, 
      datasets: [{
        label: 'Calibrated Spectrum',
        data: data_cal, // Data on Y axis
        borderWidth: 1,
        fill: false,
        borderColor: "#0000ff",
        lineTension: 0.4,
        backgroundColor: "#0000ff",
        pointBackgroundColor: "#0000ff",
        pointBorderColor: "#0000ff",
        pointHoverBackgroundColor: "#0000ff",
        pointHoverBorderColor: "#0000ff",
        pointRadius: 0
    }]
    },
  options: {
    // All of these (default) events trigger a hover and are passed to all plugins,
    // unless limited at plugin options
    events: ['mousemove', 'mouseout', 'click'],
    plugins: {
      tooltip: {
        // Tooltip will only receive click events
        events: ['mousemove']
      }
    }
  }
  });
  const chartAreaImg = {
      id: 'chartAreaImg',

      beforeDraw(chart, args, options) {
      const { ctx, chartArea: { left, top, width, height } } = chart;
      ctx.strokeStyle = options.borderColor;
      ctx.lineWidth = options.borderWidth;
      ctx.setLineDash(options.borderDash || []);
      ctx.lineDashOffset = options.borderDashOffset;
      ctx.strokeRect(left, top, width, height);
      ctx.save();
      image = new Image();
      image.src = im_filename;
      console.log('Hello')
      ctx.drawImage(image, left,top, width, height);
      ctx.restore();
      }
    };
  digChart = new Chart(dig_ctx, {
  type: 'line',
    data: {
      labels: dig_labels, 
      datasets: [{
        label: 'Digitized Spectrum',
        data: data_dig, // Data on Y axis
        borderWidth: 1,
        fill: false,
        borderColor: "#1e1e1e",
        lineTension: 0.4,
        backgroundColor: "#1e1e1e",
        pointBackgroundColor: "#1e1e1e",
        pointBorderColor: "#1e1e1e",
        pointHoverBackgroundColor: "#1e1e1e",
        pointHoverBorderColor: "#1e1e1e",
        pointRadius: 0,                  
        borderWidth: 1,
    }]
    },
    plugins: [ chartAreaImg ],
    options: {
      plugins: {
        chartAreaImg: {
              borderColor: 'red',
              borderWidth: 2,
              borderDash: [ 5, 5 ],
              borderDashOffset: 2,
        }
      },
        scales: {
          y: {
              min: 0,
              max: imheight
          }
}
    },

});
}