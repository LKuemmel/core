import{D as d}from"./HardwareInstallation-b6711c62.js";import{_ as u,u as i,k as p,l,G as t,E as m,y as f}from"./vendor-f90150d8.js";import"./vendor-fortawesome-8488187c.js";import"./index-84ae27ac.js";import"./vendor-bootstrap-99f0c261.js";import"./vendor-jquery-99ccf6d7.js";import"./vendor-axios-871a0510.js";import"./vendor-sortablejs-cfc19546.js";import"./dynamic-import-helper-be004503.js";const b={name:"DeviceSofar",mixins:[d]},v={class:"device-sofar"};function _(o,e,c,g,w,C){const r=i("openwb-base-heading"),s=i("openwb-base-text-input"),a=i("openwb-base-number-input");return p(),l("div",v,[t(r,null,{default:m(()=>e[3]||(e[3]=[f("Einstellungen für Sofar")])),_:1}),t(s,{title:"IP oder Hostname",subtype:"host",required:"","model-value":o.device.configuration.ip_address,"onUpdate:modelValue":e[0]||(e[0]=n=>o.updateConfiguration(n,"configuration.ip_address"))},null,8,["model-value"]),t(a,{title:"Port",required:"",min:1,max:65535,"model-value":o.device.configuration.port,"onUpdate:modelValue":e[1]||(e[1]=n=>o.updateConfiguration(n,"configuration.port"))},null,8,["model-value"]),t(a,{title:"Modbus ID",required:"","model-value":o.device.configuration.modbus_id,min:"1",max:"255","onUpdate:modelValue":e[2]||(e[2]=n=>o.updateConfiguration(n,"configuration.modbus_id"))},null,8,["model-value"])])}const y=u(b,[["render",_],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/sofar/sofar/device.vue"]]);export{y as default};