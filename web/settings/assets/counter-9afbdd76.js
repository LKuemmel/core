import{_ as c,p as t,k as u,l as p,A as o,L as s,u as a,q as d,x as l}from"./vendor-20bb207d.js";import"./vendor-sortablejs-ad1d2cc8.js";const _={name:"DeviceSunnyBoyCounter",emits:["update:configuration"],props:{configuration:{type:Object,required:!0},deviceId:{default:void 0},componentId:{required:!0}},methods:{updateConfiguration(e,n=void 0){this.$emit("update:configuration",{value:e,object:n})}}},f={class:"device-sunnyboy-counter"},m={class:"small"};function b(e,n,g,y,h,v){const i=t("openwb-base-heading"),r=t("openwb-base-alert");return u(),p("div",f,[o(i,null,{default:s(()=>[a(" Einstellungen für SMA Sunny Boy Zähler "),d("span",m,"(Modul: "+l(e.$options.name)+")",1)]),_:1}),o(r,{subtype:"info"},{default:s(()=>[a(" Diese Komponente benötigt keine Einstellungen. ")]),_:1})])}const $=c(_,[["render",b],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/sma_sunny_boy/counter.vue"]]);export{$ as default};