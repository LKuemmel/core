import{E as o}from"./GeneralChargeConfig-866a1615.js";import{_ as a,u as n,l as s,m as c,G as l,E as p,B as f}from"./vendor-25d394b4.js";import"./index-93388667.js";import"./vendor-fortawesome-66071a0e.js";import"./vendor-bootstrap-374cd88e.js";import"./vendor-jquery-3364d39b.js";import"./vendor-axios-ac33d60c.js";import"./vendor-sortablejs-0eb84ec8.js";import"./dynamic-import-helper-be004503.js";const d={name:"ElectricityTariffAwattar",mixins:[o]},u={class:"electricity-tariff-awattar"};function m(t,e,_,w,b,v){const i=n("openwb-base-select-input");return s(),c("div",u,[l(i,{title:"Land","not-selected":"Bitte auswählen",options:[{value:"de",text:"Deutschland"},{value:"at",text:"Österreich"}],"model-value":t.electricityTariff.configuration.country,"onUpdate:modelValue":e[0]||(e[0]=r=>t.updateConfiguration(r,"configuration.country"))},{help:p(()=>e[1]||(e[1]=[f(" Es werden die abgefragten Börsenpreise verwendet, die aWATTar bereitstellt. aWATTar-Gebühren oder Steuern werden nicht berücksichtigt. ",-1)])),_:1},8,["model-value"])])}const k=a(d,[["render",m],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/electricity_tariffs/awattar/electricity_tariff.vue"]]);export{k as default};
