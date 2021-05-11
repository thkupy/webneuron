var myplot;
var chartdata;
Chart.defaults.interaction.mode = 'nearest';

$(function(){
        $('button').click(function(){
                $.ajax({
                        url: '/simulate_dendrite',
                        data: $('form').serialize(),
                        type: 'POST',
                        success: function(response){
                                //console.log("R---> " + response.randid);
                                ctx = $("#mychart")[0].getContext('2d');
                                chartdata = {
                                  labels: response.t,
                                  datasets: [{
                                    label: 'Soma Vm',
                                    data: response.SVm,
                                    fill: false,
                                    borderColor: 'rgb(0, 0, 0)',
                                    tension: 0.1,
                                    pointRadius: 0
                                    },
                                    {
                                    label: 'Dendrit Vm',
                                    data: response.DVm,
                                    fill: false,
                                    borderColor: 'rgb(200, 200, 200)',
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
