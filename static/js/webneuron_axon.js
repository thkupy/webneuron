var myplot;
var chartdata;
Chart.defaults.interaction.mode = 'nearest';

$(function(){
        $('button').click(function(){
                $.ajax({
                        url: '/simulate_axon',
                        data: $('form').serialize(),
                        type: 'POST',
                        success: function(response){
                                //console.log("R---> " + response.randid);
                                ctx = $("#mychart")[0].getContext('2d');
                                chartdata = {
                                  labels: response.t,
                                  datasets: [{
                                    label: 'Vm 100%',
                                    data: response.Vm100,
                                    fill: false,
                                    borderColor: 'rgb(0, 0, 0)',
                                    tension: 0.1,
                                    pointRadius: 0
                                  },
                                  {
                                    label: 'Vm 75%',
                                    data: response.Vm075,
                                    fill: false,
                                    borderColor: 'rgb(50, 50, 50)',
                                    tension: 0.1,
                                    pointRadius: 0
                                  },
                                  {
                                    label: 'Vm 50%',
                                    data: response.Vm050,
                                    fill: false,
                                    borderColor: 'rgb(100, 100, 100)',
                                    tension: 0.1,
                                    pointRadius: 0
                                  },
                                  {
                                    label: 'Vm 10%',
                                    data: response.Vm010,
                                    fill: false,
                                    borderColor: 'rgb(150, 150, 150)',
                                    tension: 0.1,
                                    pointRadius: 0
                                  }]
                                };
                                if (myplot instanceof Chart)
                                {
                                    myplot.destroy()
                                };
                                myplot = new Chart(ctx, {
                                    type: 'line',
                                    data: chartdata,
                                    options: {
                                        title: {
                                            display: true,
                                            text: 'Simulation Result'
                                        },
                                        responsive: true,
                                        maintainAspectRatio: false,
                                        animation: false,
                                        scales: {
                                              x: {
                                                title: {
                                                  display: true,
                                                  text: 'Zeit (ms)'
                                                }
                                              },
                                              y: {
                                                title: {
                                                  display: true,
                                                  text: 'Membranpotential (mV)'
                                                }
                                              }
                                            }
                                    }
                                });
                        },
                        error: function(error){
                                console.log(error);
                        }
                });
        });
});
