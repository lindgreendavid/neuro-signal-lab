const participants = [
  ["sub-001",6.7296],["sub-002",5.5590],["sub-003",6.7622],["sub-004",5.1942],
  ["sub-005",5.9845],["sub-006",5.3790],["sub-007",3.7437],["sub-008",5.8649],
  ["sub-009",5.5704],["sub-010",8.7178],["sub-011",5.0803],["sub-012",3.2153],["sub-013",5.7066]
];

const thresholds = {
  100:{mean:5.827,lo:4.893,hi:6.761,label:"prespecified sensitivity"},
  150:{mean:5.654,lo:4.833,hi:6.476,label:"confirmatory endpoint"},
  200:{mean:5.738,lo:4.825,hi:6.652,label:"prespecified sensitivity"}
};

const chart = document.querySelector("#participant-chart");
const summary = document.querySelector("#chart-summary");
let sorted = false;

function renderParticipants(){
  const values = [...participants];
  if(sorted) values.sort((a,b)=>b[1]-a[1]);
  chart.replaceChildren(...values.map(([id,value])=>{
    const row=document.createElement("div");
    row.className="participant"; row.tabIndex=0; row.setAttribute("role","listitem");
    row.setAttribute("aria-label",`${id}: positive ${value.toFixed(2)} microvolts`);
    row.innerHTML=`<span>${id.replace("sub-","")}</span><div class="track"><div class="bar" style="--value:${value}"></div></div><strong>+${value.toFixed(2)}</strong>`;
    row.addEventListener("mouseenter",()=>summary.textContent=`${id}: +${value.toFixed(2)} µV`);
    row.addEventListener("focus",()=>summary.textContent=`${id}: +${value.toFixed(2)} µV`);
    return row;
  }));
}

document.querySelector("#sort-button").addEventListener("click",event=>{
  sorted=!sorted; event.currentTarget.textContent=sorted?"Restore participant order":"Sort by effect"; renderParticipants();
});

function showThreshold(value){
  const result=thresholds[value];
  document.querySelectorAll("[data-threshold]").forEach(button=>button.classList.toggle("active",button.dataset.threshold===value));
  const interval=document.querySelector("#interval");
  interval.style.setProperty("--lo",`${result.lo/8*100}%`); interval.style.setProperty("--hi",`${result.hi/8*100}%`); interval.style.setProperty("--mean",`${result.mean/8*100}%`);
  document.querySelector("#threshold-result").innerHTML=`<strong>+${result.mean.toFixed(2)} µV</strong> mean; 95% CI +${result.lo.toFixed(2)} to +${result.hi.toFixed(2)} µV · ${result.label}.`;
}

document.querySelector("#threshold-control").addEventListener("click",event=>{if(event.target.dataset.threshold)showThreshold(event.target.dataset.threshold)});
renderParticipants(); showThreshold("150");
