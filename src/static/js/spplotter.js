function spectrumViewer(spectrum){
  var {calibrated_in, wavenumber_lbl,digitized_in,pixel_lbl,im_filename,imheight} = spectrum
  plotButton = document.getElementById("process_input");
  plotButton.addEventListener("click", () => {
  calChart.destroy();
  digChart.destroy();
  });
  cal_data = {
     labels: wavenumber_lbl,
     datasets: [{
      label: 'Calibrated spectrum',
      data: calibrated_in,
      backgroundColor: "blue",       
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
  };
  dig_data = {
     labels: pixel_lbl,
     datasets: [{
      label: 'Digitized spectrum',
      data: digitized_in,
      backgroundColor: "black",       
      borderWidth: 1,
      fill: false,
      borderColor: "#1e1e1e",
      lineTension: 0.4,
      backgroundColor: "#1e1e1e",
      pointBackgroundColor: "#1e1e1e",
      pointBorderColor: "#1e1e1e",
      pointHoverBackgroundColor: "#1e1e1e",
      pointHoverBorderColor: "#1e1e1e",
      pointRadius: 0
    }]
};
  image = new Image();
  image.src = im_filename;
  const chartAreaImg = {
    id: 'chartAreaImg',
    beforeDraw: (chart) => {
      if (image.complete) {
        const ctx = chart.ctx;
        const {top, left, width, height} = chart.chartArea;
        ctx.drawImage(image, left, top, width, height);
      } else {
        image.onload = () => chart.draw();
      }
    }
  };
  
  cal_ctx = $('#calChart')[0].getContext('2d');
  dig_ctx = $('#digChart')[0].getContext('2d');
  calChart = new Chart(cal_ctx, {
    type: 'line',
    data: cal_data,
    options: {    scales: {
        y: {
              min: 0,
              title: {
                display: true,
                text: 'Intensity'
            }
          },
        x: {
              title: {
                display: true,
                text: 'Wavenumber'
            }
          }
        },
      plugins: {


      }
    }
  });
  digChart = new Chart(dig_ctx, {
    type: 'line',
    data: dig_data,
    plugins: [ chartAreaImg ],
    options: {
      plugins: {
        chartAreaImg: {
              borderColor: 'red',
              borderWidth: 2,
              borderDash: [ 5, 5 ],
              borderDashOffset: 2,
        },      
      },
      scales: {
        y: {
              min: 0,
              max: imheight,
              title: {
                display: true,
                text: 'Pixels'
            }
          },

        x: {
              title: {
                display: true,
                text: 'Pixels'
            }
          }
      }  
    }
  });
}