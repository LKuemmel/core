import{D as r}from"./HardwareInstallation-774805b0.js";import{_ as a,u as t,l as d,m as u,G as n,E as l,y as m}from"./vendor-0c15df0c.js";import"./vendor-fortawesome-231ff303.js";import"./index-6ffbdc7e.js";import"./vendor-bootstrap-83e2d5a1.js";import"./vendor-jquery-84e2bf4a.js";import"./vendor-axios-c9d2afa0.js";import"./vendor-sortablejs-1a751103.js";import"./dynamic-import-helper-be004503.js";const c={name:"DeviceOpenDTU",mixins:[r]},_={class:"device-opendtu"};function f(o,e,v,b,g,x){const i=t("openwb-base-heading"),s=t("openwb-base-text-input");return d(),u("div",_,[n(i,null,{default:l(()=>e[1]||(e[1]=[m("Einstellungen für OpenDTU")])),_:1}),n(s,{title:"IP oder Hostname",subtype:"host",required:"","model-value":o.device.configuration.url,"onUpdate:modelValue":e[0]||(e[0]=p=>o.updateConfiguration(p,"configuration.url"))},null,8,["model-value"])])}const h=a(c,[["render",f],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/opendtu/opendtu/device.vue"]]);export{h as default};