import{_ as d,u as t,k as p,l as c,D as n,N as l,y as _,x as f,z as g}from"./vendor-f2b8aa6f.js";import"./vendor-sortablejs-2f1828d0.js";const m={name:"DevicePowerdogCounter",emits:["update:configuration"],props:{configuration:{type:Object,required:!0},deviceId:{default:void 0},componentId:{required:!0}},methods:{updateConfiguration(o,e=void 0){this.$emit("update:configuration",{value:o,object:e})}}},b={class:"device-powerdog-counter"},v={class:"small"};function w(o,e,u,h,x,a){const i=t("openwb-base-heading"),s=t("openwb-base-button-group-input");return p(),c("div",b,[n(i,null,{default:l(()=>[_(" Einstellungen für Powerdog Zähler "),f("span",v,"(Modul: "+g(o.$options.name)+")",1)]),_:1}),n(s,{title:"Einbau-Position",buttons:[{buttonValue:!1,text:"Hausverbrauch"},{buttonValue:!0,text:"EVU-Punkt"}],"model-value":u.configuration.position_evu,"onUpdate:modelValue":e[0]||(e[0]=r=>a.updateConfiguration(r,"configuration.position_evu"))},null,8,["model-value"])])}const k=d(m,[["render",w],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/powerdog/powerdog/counter.vue"]]);export{k as default};