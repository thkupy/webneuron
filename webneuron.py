from flask import Flask, render_template, request,json, jsonify
from neuron import h
import numpy as np

app = Flask(__name__)

def nrngo(tstop,vinit):
    h.finitialize(vinit)
    h.fcurrent()
    while h.t < tstop:
        h.fadvance()

def runsim_iclamp(
        tstop=100.0,
        dt=0.025,
        temp=21.0,
        L=15.0,
        D=15.0,
        C=1.0,
        gl=0.0003,
        iamp1=0.1,
        idur1=50.0,
        istart1=15.0,
        iamp2=0.0,
        idur2=0.0,
        istart2=0.0,
    ):
    Soma = h.Section()
    Soma.L = L
    Soma.diam = D
    Soma.nseg = 7
    Soma.insert("hh")
    Soma.ena = 50
    Soma.gnabar_hh = 0.12
    Soma.gkbar_hh = 0.023
    Soma.gl_hh = gl
    Soma.cm = C
    # GENERAL SETTINGS
    h.dt = dt # simulation (or "sampling") rate
    h.celsius = temp  # simulation global temperature
    Electrode1 = h.IClamp(Soma(0.5))
    Electrode1.delay = istart1
    Electrode1.amp = iamp1
    Electrode1.dur = idur1
    Electrode2 = h.IClamp(Soma(0.5))
    Electrode2.delay = istart2
    Electrode2.amp = iamp2
    Electrode2.dur = idur2
    Vm = h.Vector()
    Vm.record(Soma(0.5)._ref_v)
    nrngo(tstop, -62.0)
    # PACK AND EXPORT DATA
    t = np.linspace(0, tstop-dt, int(np.round(tstop / dt)))
    Vm = np.array(Vm)
    return(t,Vm)

def runsim_vclamp(
        tstop=15.0,
        dt=0.01,
        temp=21.0,
        dur1=5.0,
        dur2=5.0,
        dur3=5.0,
        amp1=-70.0,
        amp2=0.0,
        amp3=-70.0,
        tea=False,
        ttx=False,
    ):
    Soma = h.Section()
    Soma.L = 15
    Soma.nseg = 7
    Soma.diam = 15
    area = np.pi * 15.0 * 15.0#in µm²
    Soma.insert("hh")
    Soma.ena = 50
    if ttx:
        Soma.gnabar_hh = 1e-9
    else:
        Soma.gnabar_hh = 0.12
    if tea:
        Soma.gkbar_hh = 1e-9
    else:
        Soma.gkbar_hh = 0.023
    # GENERAL SETTINGS
    h.dt = dt # simulation (or "sampling") rate
    h.celsius = temp  # simulation global temperature
    SEC = h.SEClamp(Soma(0.5))
    SEC.rs = 0.1
    SEC.dur1 = dur1
    SEC.dur2 = dur2
    SEC.dur3 = dur3
    SEC.amp1 = amp1
    SEC.amp2 = amp2
    SEC.amp3 = amp3
    Vm = h.Vector()
    Vm.record(Soma(0.5)._ref_v)
    INa = h.Vector()
    IK = h.Vector()
    IL = h.Vector()
    INa.record(Soma(0.5)._ref_ina)
    IK.record(Soma(0.5)._ref_ik)
    IL.record(Soma(0.5)._ref_il_hh)
    Ie = h.Vector()
    Ie.record(SEC._ref_i)
    hhm = h.Vector()
    hhm.record(Soma(0.5)._ref_m_hh)
    hhn = h.Vector()
    hhn.record(Soma(0.5)._ref_n_hh)
    hhh = h.Vector()
    hhh.record(Soma(0.5)._ref_h_hh)
    Im = h.Vector()
    Im.record(SEC._ref_i)
    nrngo(tstop,-70.0)
    # PACK AND EXPORT DATA
    t = np.linspace(0, tstop-dt, int(np.round(tstop / dt)))
    Vm = np.array(Vm)
    Im = np.array(INa) + np.array(IK) + np.array(IL)
    #mA/cm2 be multiplied by (area in µm² * 0.01) to get nA
    Im = Im * (area * 0.01)
    Ie = np.array(Ie)
    hhm = np.array(hhm)
    hhn = np.array(hhn)
    hhh = np.array(hhh)
    return(t, Im, Ie, Vm, hhm, hhn, hhh)

def runsim_dendrite(
        tstop=500.0,
        dt=0.025,
        temp=21.0,
        somaL = 15.0,
        somaD = 15.0,
        somagleak = 0.0003,
        dendL = 250.0,
        dendD = 2.0,
        dendgleak = 0.00001,
        inputPos = 0.9,
        inputStart = 10.0,
        inputDur = 1.0,
        inputAmp = 0.5,
        syn1Pos = 0.6,
        syn1Start = 50.0,
        syn1g = 0.01,
        syn1Erev = 0.0,
        syn1Tau = 25.0,
        syn2Pos = 0.4,
        syn2Start = 45.0,
        syn2g = 0.005,
        syn2Erev = -80.0,
        syn2Tau = 40.0,
    ):
    #DEFINE MODEL CELL
    Soma = h.Section()
    Soma.L = somaL
    Soma.nseg = 7
    Soma.diam = somaD
    Soma.insert("hh")
    Soma.el_hh = -65.0
    Soma.gl_hh = somagleak
    Soma.ena = 50
    Soma.gnabar_hh = 0.13
    Soma.gkbar_hh = 0.04
    Dend = h.Section()
    Dend.L = dendL
    dendsegs = int(np.round(dendL / 10.0))
    if dendsegs < 3:
        dendsegs = 3
    Dend.nseg = dendsegs 
    Dend.diam = dendD
    Dend.insert("pas")
    Dend.g_pas = dendgleak
    Dend.e_pas = -65.0
    for sec in h.allsec():
        sec.Ra = 150
    Dend.connect(Soma(1))
    #SYNAPSES
    syn1 = h.AlphaSynapse(Dend(syn1Pos))
    syn1.onset = syn1Start
    syn1.tau = syn1Tau
    syn1.gmax = syn1g
    syn1.e = syn1Erev
    syn2 = h.AlphaSynapse(Dend(syn2Pos))
    syn2.onset = syn2Start
    syn2.tau = syn2Tau
    syn2.gmax = syn2g
    syn2.e = syn2Erev
    #GENERAL SETTINGS
    h.dt = dt # simulation (or "sampling") rate
    h.celsius = temp  # simulation global temperature
    #INSTRUMENTATION
    Electrode = h.IClamp(Dend(inputPos))
    Electrode.delay = inputStart
    Electrode.amp = inputAmp
    Electrode.dur = inputDur
    SVm = h.Vector()
    SVm.record(Soma(0.5)._ref_v)
    DVm = h.Vector()
    DVm.record(Dend(inputPos)._ref_v)
    nrngo(tstop,-65.0)
    # PACK AND EXPORT DATA
    t = np.linspace(0,tstop-dt,int(np.round(tstop/dt)))
    SVm = np.array(SVm)
    DVm = np.array(DVm)
    return(t, SVm, DVm)

def runsim_axon(
        tstop=50-0,
        dt=0.01,
        temp=21.0,
        axonD = 2.0,
        inputDur = 1.0,
        inputAmp = 0.5,
    ):
    #DEFINE MODEL CELL
    Axon = h.Section()
    Axon.L = 10000.0
    Axon.nseg = 500
    Axon.diam = axonD
    Axon.insert("hh")

    #GENERAL SETTINGS
    h.dt = dt # simulation (or "sampling") rate
    h.celsius = temp  # simulation global temperature

    #INSTRUMENTATION
    Electrode = h.IClamp(Axon(0.0))
    Electrode.delay = 0.0
    Electrode.amp = inputAmp
    Electrode.dur = inputDur
    Vm100 = h.Vector()
    Vm100.record(Axon(1.0)._ref_v)
    Vm075 = h.Vector()
    Vm075.record(Axon(0.75)._ref_v)
    Vm050 = h.Vector()
    Vm050.record(Axon(0.5)._ref_v)
    Vm010 = h.Vector()
    Vm010.record(Axon(0.1)._ref_v)
    nrngo(tstop,-65.0)
    # PACK AND EXPORT DATA
    t = np.linspace(0,tstop-dt,int(np.round(tstop/dt)))
    Vm100 = np.array(Vm100)
    Vm075 = np.array(Vm075)
    Vm050 = np.array(Vm050)
    Vm010 = np.array(Vm010)
    return(t, Vm100, Vm075, Vm050, Vm010)




@app.route("/")
def selector():
    return render_template("webneuron.html")

@app.route("/webneuron_iclamp")
def runiclamp():
    return render_template("webneuron_iclamp.html")

@app.route("/webneuron_vclamp")
def runvclamp():
    return render_template("webneuron_vclamp.html")

@app.route("/webneuron_dendrite")
def rundendrite():
    return render_template("webneuron_dendrite.html")

@app.route("/webneuron_axon")
def runaxon():
    return render_template("webneuron_axon.html")

@app.route("/simulate_iclamp", methods=["POST"])
def simulate_iclamp():
    tstop = float(request.form["tstop"])
    dt = float(request.form["dt"])
    temp =  float(request.form["temp"])
    L = float(request.form["somaL"])
    D = float(request.form["somaD"])
    C = float(request.form["specc"])
    gl = float(request.form["gleak"])
    start1 = float(request.form["start1"])
    amp1 =  float(request.form["amplitude1"])
    dur1 = float(request.form["duration1"])
    start2 = float(request.form["start2"])
    amp2 =  float(request.form["amplitude2"])
    dur2 = float(request.form["duration2"])
    t, Vm = runsim_iclamp(
        tstop=tstop,
        dt=dt,
        temp=temp,
        L=L,
        D=D,
        C=C,
        gl=gl,
        idur1=dur1,
        iamp1=amp1, 
        istart1=start1,
        idur2=dur2,
        iamp2=amp2, 
        istart2=start2,
    )
    t = np.round(t, 2)
    return jsonify(
                status = "OK",
                randid =  np.random.randn(),
                t =  t.tolist(), 
                Vm = Vm.tolist(),
            )

@app.route("/simulate_vclamp", methods=["POST"])
def simulate_vclamp():
    tstop = float(request.form["tstop"])
    dt = float(request.form["dt"])
    temp =  float(request.form["temp"])
    dur1 = float(request.form["vcdur1"])
    dur2 = float(request.form["vcdur2"])
    dur3 = float(request.form["vcdur3"])
    amp1 = float(request.form["vcamp1"])
    amp2 = float(request.form["vcamp2"])
    amp3 = float(request.form["vcamp3"])
    if request.form.get("addttx"):
        ttx = True
    else:
        ttx = False
    if request.form.get("addtea"):
        tea = True
    else:
        tea = False
    t, Im, Ie, Vm, hhm, hhn, hhh = runsim_vclamp(
        tstop=tstop,
        dt=dt,
        temp=temp,
        dur1=dur1,
        dur2=dur2,
        dur3=dur3,
        amp1=amp1,
        amp2=amp2,
        amp3=amp3,
        tea=tea,
        ttx=ttx,
    )
    t = np.round(t,2)
    return jsonify(
                status = "OK",
                randid =  np.random.randn(),
                t =  t.tolist(), 
                Vm = Vm.tolist(),
                Ie = Ie.tolist(),
                Im = Im.tolist(),
                hhm = hhm.tolist(),
                hhn = hhn.tolist(),
                hhh = hhh.tolist(),
            )

@app.route("/simulate_dendrite", methods=["POST"])
def simulate_dendrite():
    tstop = float(request.form["tstop"])
    temp =  float(request.form["temp"])
    dt = float(request.form["dt"])
    somaL = float(request.form["somaL"])
    somaD = float(request.form["somaD"])
    somagleak = float(request.form["somagleak"])
    dendL = float(request.form["dendL"])
    dendD = float(request.form["dendD"])
    dendgleak = float(request.form["dendgleak"])
    inputPos = float(request.form["inputPos"])
    inputStart = float(request.form["inputStart"])
    inputDur = float(request.form["inputDur"])
    inputAmp = float(request.form["inputAmp"])
    syn1Pos =  float(request.form["syn1Pos"])
    syn1Start =  float(request.form["syn1Start"])
    syn1g =  float(request.form["syn1g"])
    syn1Erev =  float(request.form["syn1Erev"])
    syn1Tau =  float(request.form["syn1Tau"])
    syn2Pos =  float(request.form["syn2Pos"])
    syn2Start =  float(request.form["syn2Start"])
    syn2g =  float(request.form["syn2g"])
    syn2Erev =  float(request.form["syn2Erev"])
    syn2Tau =  float(request.form["syn2Tau"])
    t, SVm, DVm = runsim_dendrite(
        tstop=tstop,
        dt=dt,
        temp=temp,
        somaL = somaL,
        somaD = somaD,
        somagleak = somagleak,
        dendL = dendL,
        dendD = dendD,
        dendgleak = dendgleak,
        inputPos = inputPos, 
        inputStart = inputStart,
        inputDur = inputDur,
        inputAmp = inputAmp,
        syn1Pos = syn1Pos,
        syn1Start = syn1Start,
        syn1g = syn1g,
        syn1Erev = syn1Erev,
        syn1Tau = syn1Tau,
        syn2Pos = syn2Pos,
        syn2Start = syn2Start,
        syn2g = syn2g,
        syn2Erev = syn2Erev,
        syn2Tau = syn2Tau,
    )
    t = np.round(t,2)
    return jsonify(
                status = "OK",
                randid =  np.random.randn(),
                t =  t.tolist(), 
                SVm = SVm.tolist(),
                DVm = DVm.tolist(),
            )


@app.route("/simulate_axon", methods=["POST"])
def simulate_axon():
    tstop = float(request.form["tstop"])
    temp =  float(request.form["temp"])
    dt = float(request.form["dt"])
    axonD = float(request.form["axonD"])
    inputDur = float(request.form["inputDur"])
    inputAmp = float(request.form["inputAmp"])
    t, Vm100, Vm075, Vm050, Vm010 = runsim_axon(
        tstop=tstop,
        dt=dt,
        temp=temp,
        axonD = axonD,
        inputDur = inputDur,
        inputAmp = inputAmp,
    )
    t = np.round(t, 2)
    return jsonify(
                status = "OK",
                randid =  np.random.randn(),
                t =  t.tolist(), 
                Vm100 = Vm100.tolist(),
                Vm075 = Vm075.tolist(),
                Vm050 = Vm050.tolist(),
                Vm010 = Vm010.tolist(),
            )


if __name__=="__main__":
    app.run(debug=True)
