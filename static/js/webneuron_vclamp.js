var myplot1;
var myplot2;
var myplot3;
var chartdata1;
var chartdata3;
var chartdata3;
Chart.defaults.interaction.mode = 'nearest';

$(function(){
        $('button').click(function(){
                $.ajax({
                        url: '/simulate_vclamp',
                        data: $('form').serialize(),
                        type: 'POST',
                        success: function(response){
                                console.log("R---> " + response.randid);
                                //CHARTDATA
                                ctx1 = $("#mychart1")[0].getContext('2d');
                                ctx2 = $("#mychart2")[0].getContext('2d');
                                ctx3 = $("#mychart3")[0].getContext('2d');
                                chartdata1 = {
                                  labels: response.t,
                                  datasets: [{
                                    label: 'Im',
                                    data: response.Im,
                                    fill: false,
                                    borderColor: 'rgb(0, 0, 0)',
                                    tension: 0.1,
                                    pointRadius: 0
                                    },
                                    {
                                    label: 'Ie',
                                    data: response.Ie,
                                    fill: false,
                                    borderColor: 'rgb(200, 200, 200)',
                                    tension: 0.1,
                                    pointRadius: 0
                                    }]
                                };
                                chartdata2 = {
                                  labels: response.t,
                                  datasets: [{
                                    label: 'Vm',
                                    data: response.Vm,
                                    fill: false,
                                    borderColor: 'rgb(0, 0, 0)',
                                    tension: 0.1,
                                    pointRadius: 0
                                    }]
                                };
                                chartdata3 = {
                                  labels: response.t,
                                  datasets: [{
                                    label: 'm',
                                    data: response.hhm,
                                    fill: false,
                                    borderColor: 'rgb(0, 0, 255)',
                                    tension: 0.1,
                                    pointRadius: 0},
                                    {
                                    label: 'n',
                                    data: response.hhn,
                                    fill: false,
                                    borderColor: 'rgb(0, 255, 0)',
                                    tension: 0.1,
                                    pointRadius: 0
                                    },
                                    {
                                    label: 'h',
                                    data: response.hhh,
                                    fill: false,
                                    borderColor: 'rgb(255, 0, 0)',
                                    tension: 0.1,
                                    pointRadius: 0
                                    }]
                                };
                                if (myplot1 instanceof Chart)
                                {
                                    myplot1.destroy()
                                };
                                if (myplot2 instanceof Chart)
                                {
                                    myplot2.destroy()
                                };
                                if (myplot3 instanceof Chart)
                                {
                                    myplot3.destroy()
                                };
                                myplot1 = new Chart(ctx1, {
                                    type: 'line',
                                    data: chartdata1,
                                    options: {
                                        title: {
                                            display: true,
                                            text: 'Im'
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
                                                  text: 'Totaler Membranstrom (nA)'
                                                }
                                              }
                                            }
                                    }
                                });
                                myplot2 = new Chart(ctx2, {
                                    type: 'line',
                                    data: chartdata2,
                                    options: {
                                        title: {
                                            display: true,
                                            text: 'Vm'
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
                                myplot3 = new Chart(ctx3, {
                                    type: 'line',
                                    data: chartdata3,
                                    options: {
                                        title: {
                                            display: true,
                                            text: 'HH state variables'
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
                                                  text: 'state'
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
