import{D as a}from"./HardwareInstallation-0477e3e2.js";import{_ as p,u as s,k as u,l as m,G as n,E as d,y as l}from"./vendor-809787c9.js";import"./vendor-fortawesome-e760f6db.js";import"./index-f9dddb60.js";import"./vendor-bootstrap-5ce91dd7.js";import"./vendor-jquery-49acc558.js";import"./vendor-axios-57a82265.js";import"./vendor-sortablejs-d99a4022.js";import"./dynamic-import-helper-be004503.js";const c={name:"DeviceSmartMe",mixins:[a]},f={class:"device-smart-me"};function v(o,e,_,b,g,w){const r=s("openwb-base-heading"),i=s("openwb-base-text-input");return u(),m("div",f,[n(r,null,{default:d(()=>e[2]||(e[2]=[l(" Einstellungen für smart-me ")])),_:1}),n(i,{title:"Benutzername",subtype:"user",required:"","model-value":o.device.configuration.user,"onUpdate:modelValue":e[0]||(e[0]=t=>o.updateConfiguration(t,"configuration.user"))},null,8,["model-value"]),n(i,{title:"Passwort",subtype:"password",required:"","model-value":o.device.configuration.password,"onUpdate:modelValue":e[1]||(e[1]=t=>o.updateConfiguration(t,"configuration.password"))},null,8,["model-value"])])}const q=p(c,[["render",v],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/smart_me/smart_me/device.vue"]]);export{q as default};