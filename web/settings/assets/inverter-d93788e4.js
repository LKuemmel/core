import{C as u}from"./HardwareInstallation-774805b0.js";import{_ as a,u as t,l as p,m as l,G as n,E as m,y as c}from"./vendor-0c15df0c.js";import"./vendor-fortawesome-231ff303.js";import"./index-6ffbdc7e.js";import"./vendor-bootstrap-83e2d5a1.js";import"./vendor-jquery-84e2bf4a.js";import"./vendor-axios-c9d2afa0.js";import"./vendor-sortablejs-1a751103.js";import"./dynamic-import-helper-be004503.js";const _={name:"DeviceYoulessInverter",mixins:[u]},d={class:"device-youless-inverter"};function f(o,e,b,v,g,x){const s=t("openwb-base-heading"),i=t("openwb-base-button-group-input");return p(),l("div",d,[n(s,null,{default:m(()=>e[1]||(e[1]=[c(" Einstellungen für Youless LS120 Wechselrichter ")])),_:1}),n(i,{title:"S0-Eingang auslesen",buttons:[{buttonValue:!1,text:"nein"},{buttonValue:!0,text:"ja"}],"model-value":o.component.configuration.source_s0,"onUpdate:modelValue":e[0]||(e[0]=r=>o.updateConfiguration(r,"configuration.source_s0"))},null,8,["model-value"])])}const N=a(_,[["render",f],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/youless/youless/inverter.vue"]]);export{N as default};