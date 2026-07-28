import math
import streamlit as st

st.set_page_config(page_title="Post-pyeloplasty Ultrasound Follow-up Assessment", page_icon="🩺", layout="wide")

st.markdown("""
<style>
:root{--navy:#17365d;--blue:#2f6f9f;--pale:#eef4f8;--green:#287a4a;--amber:#a96800;--red:#b03a2e;--line:#ccd8e2;--ink:#1f2933}
.stApp{background:#f4f6f8;color:var(--ink)}
.block-container{max-width:1120px;padding-top:1.5rem;padding-bottom:2rem}
.hero{background:linear-gradient(120deg,var(--navy),#315f85);color:white;padding:28px 30px;border-radius:18px;box-shadow:0 10px 30px rgba(23,54,93,.18);margin-bottom:20px}
.hero h1{font-size:30px;margin:0 0 7px}.hero p{margin:5px 0;max-width:900px}
.card{background:#fff;border:1px solid #e0e6eb;border-radius:16px;padding:22px;box-shadow:0 5px 18px rgba(20,45,70,.06)}
.card-title{color:var(--navy);font-size:21px;font-weight:700;margin-bottom:10px}
.metric-card{background:var(--pale);padding:12px;border-radius:10px;text-align:center;min-height:94px}
.metric-card b{display:block;font-size:20px;color:var(--navy)}
.result{border-left:7px solid var(--blue);background:#f8fbfd;padding:17px;border-radius:10px;margin-bottom:14px}
.result-green{border-color:var(--green)}.result-green h3{color:var(--green)}
.result-amber{border-color:var(--amber)}.result-amber h3{color:var(--amber)}
.result-red{border-color:var(--red)}.result-red h3{color:var(--red)}
.action{background:#fff7e6;border:1px solid #f1cf8a;padding:14px;border-radius:10px;margin-top:12px}
.report{font-size:13px;background:#f2f5f7;padding:12px;border-radius:10px;margin-top:14px;color:#445361}
.small-note{font-size:13px;color:#536573;margin-top:14px;border-top:1px solid #dce4eb;padding-top:12px}
div[data-testid="stNumberInput"] label, div[data-testid="stCheckbox"] label{font-weight:600}
.stButton>button{border-radius:10px;font-weight:700}
</style>
<div class="hero">
<h1>Post-pyeloplasty Ultrasound Follow-up Assessment</h1>
<p>Compare the current renal pelvic anteroposterior diameter (APD) with the cohort-derived postoperative range for the preoperative APD and time since pyeloplasty.</p>
</div>
""", unsafe_allow_html=True)

BASE=[15.0,25.0,35.0,50.0,70.0]
TIME=[3.0,6.0,12.0,24.0]
MED=[[15.2,12.3,12.3,11.6],[18.5,15.0,15.0,14.2],[21.2,17.2,17.1,16.3],[24.3,19.8,19.7,18.8],[27.8,22.6,22.5,21.4]]
P90=[[28.7,23.3,23.3,22.2],[34.8,28.3,28.3,26.9],[39.6,32.3,32.2,30.6],[45.4,37.0,36.9,35.2],[51.7,42.2,42.1,40.1]]

def interp1(x,xs,ys):
    if x<=xs[0]: return ys[0]
    if x>=xs[-1]: return ys[-1]
    for i in range(1,len(xs)):
        if x<=xs[i]:
            w=(x-xs[i-1])/(xs[i]-xs[i-1])
            return ys[i-1]+w*(ys[i]-ys[i-1])

def interp2(b,t,grid):
    lb,lt=math.log(b),math.log(t)
    xb=[math.log(x) for x in BASE]; xt=[math.log(x) for x in TIME]
    vals=[interp1(lb,xb,[r[j] for r in grid]) for j in range(len(TIME))]
    return interp1(lt,xt,vals)

left,right=st.columns([1,1.08],gap="large")
with left:
    st.markdown('<div class="card"><div class="card-title">Ultrasound and clinical information</div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    baseline=c1.number_input("Preoperative renal pelvic APD (mm)",min_value=1.0,max_value=150.0,value=35.0,step=0.1,help="Cohort-derived range: 15–70 mm.")
    months=c2.number_input("Time since pyeloplasty (months)",min_value=0.1,max_value=120.0,value=12.0,step=0.1,help="Cohort-derived range: 3–24 months.")
    c3,c4=st.columns(2)
    current=c3.number_input("Current renal pelvic APD (mm)",min_value=0.0,max_value=150.0,value=39.0,step=0.1)
    previous=c4.number_input("Previous postoperative APD (mm, optional)",min_value=0.0,max_value=150.0,value=20.0,step=0.1)
    previous_months=st.number_input("Time of previous postoperative ultrasound (months, optional)",min_value=0.1,max_value=120.0,value=6.0,step=0.1)
    symptoms=st.checkbox("Symptoms suggestive of recurrent obstruction")
    uti=st.checkbox("Febrile urinary tract infection")
    thinning=st.checkbox("Progressive renal parenchymal thinning")
    functional=st.checkbox("Deteriorating differential renal function or drainage concern")
    assess=st.button("Assess follow-up ultrasound",type="primary",use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

with right:
    st.markdown('<div class="card"><div class="card-title">Follow-up assessment</div>',unsafe_allow_html=True)
    if baseline<15 or baseline>70 or months<3 or months>24:
        st.markdown('<div class="result"><h3>Outside the cohort-derived range</h3><p>The input lies outside preoperative APD 15–70 mm or 3–24 months after pyeloplasty. Do not extrapolate the reference values.</p></div>',unsafe_allow_html=True)
    else:
        med=interp2(baseline,months,MED); p90=interp2(baseline,months,P90); ratio=current/p90 if p90 else float('nan')
        interval_increase=(current-previous>=5) and ((current-previous)/max(previous,0.1)>=0.20)
        prev_p90=interp2(baseline,previous_months,P90) if 3<=previous_months<=24 else None
        persistent=(prev_p90 is not None and previous>prev_p90 and current>p90)
        clinical=symptoms or uti or thinning or functional
        if clinical or interval_increase or persistent:
            title="Persistent or increasing hydronephrosis, or associated clinical concern"
            cls="result-red"
            desc="Serial ultrasound or clinical findings warrant assessment for recurrent obstruction. Ultrasound alone does not establish recurrent pelvi-ureteric junction obstruction."
            action="Review examination quality and the clinical record; consider diuretic renography and paediatric urology review."
        elif current>p90:
            title="Current APD is above the cohort-derived postoperative range"
            cls="result-amber"
            desc="A single measurement above the cohort-derived upper value may reflect biological or measurement variation."
            action="Confirm bladder filling and measurement technique, and repeat a standardised ultrasound earlier. Escalate if the finding persists or clinical concerns emerge."
        else:
            title="Current APD is within the cohort-derived postoperative range"
            cls="result-green"
            desc="The current APD is within the cohort-derived range for the preoperative APD and time after pyeloplasty, with no selected clinical concern."
            action="Continue ultrasound follow-up according to the local postoperative protocol."
        st.markdown(f'<div class="result {cls}"><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
        m1,m2,m3=st.columns(3)
        m1.markdown(f'<div class="metric-card">Expected median APD<b>{med:.1f}</b>mm</div>',unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card">Expected upper value<b>{p90:.1f}</b>mm</div>',unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card">Current / upper value<b>{ratio:.2f}</b>ratio</div>',unsafe_allow_html=True)
        direction='decreased' if current<previous else ('increased' if current>previous else 'remained stable')
        report=(f"Preoperative renal pelvic APD was {baseline:.1f} mm. At {months:.1f} months after pyeloplasty, renal pelvic APD was {current:.1f} mm; "
                f"the cohort-derived median was {med:.1f} mm and the cohort-derived upper value was {p90:.1f} mm. Compared with the previous postoperative ultrasound, APD {direction}. Assessment: {title}.")
        st.markdown(f'<div class="action"><b>Suggested follow-up:</b> {action}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="report">{report}</div>',unsafe_allow_html=True)
        st.download_button("Download assessment as text",report,file_name="post_pyeloplasty_ultrasound_assessment.txt",use_container_width=True)
    st.markdown('<div class="small-note">The cohort-derived range is intended to support interpretation of structural remodelling. Symptoms, urinary tract infection, renal parenchymal appearance, and renal functional assessment remain integral to follow-up. An APD above the range is not, by itself, a diagnosis of recurrent obstruction or an indication for reoperation.</div></div>',unsafe_allow_html=True)
