function spectrumViewer(spectrum){
  var {calibrated_in, wavenumber_lbl,digitized_in,pixel_lbl,im_filename,imheight} = spectrum
  plotButton = document.getElementById("process_input");
  plotButton.addEventListener("click", () => {
  calChart.destroy();
  digChart.destroy();
  });
  function fillData(data, labels, color){
      draw_data = {
      labels: labels,
      datasets: [{
        label: 'Digitized spectrum',
        data: data,
        backgroundColor: color,       
        borderWidth: 1,
        fill: false,
        borderColor: color,
        lineTension: 0.4,
        backgroundColor: color,
        pointBackgroundColor: color,
        pointBorderColor: color,
        pointHoverBackgroundColor: color,
        pointHoverBorderColor: color,
        pointRadius: 0
      }]
  };
  return draw_data
  }
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
    data: fillData(calibrated_in, wavenumber_lbl, "#0000ff"),
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
    data: fillData(digitized_in, pixel_lbl,"#1e1e1e"),
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