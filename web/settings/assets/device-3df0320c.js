import{D as u}from"./HardwareInstallation-774805b0.js";import{_ as m,u as i,l as c,m as b,G as t,E as r,y as a}from"./vendor-0c15df0c.js";import"./vendor-fortawesome-231ff303.js";import"./index-6ffbdc7e.js";import"./vendor-bootstrap-83e2d5a1.js";import"./vendor-jquery-84e2bf4a.js";import"./vendor-axios-c9d2afa0.js";import"./vendor-sortablejs-1a751103.js";import"./dynamic-import-helper-be004503.js";const f={name:"DeviceKostalPlenticore",mixins:[u]},_={class:"device-kostal-plenticore"};function v(o,e,g,w,C,E){const l=i("openwb-base-heading"),p=i("openwb-base-alert"),d=i("openwb-base-text-input"),s=i("openwb-base-number-input");return c(),b("div",_,[t(l,null,{default:r(()=>e[3]||(e[3]=[a(" Einstellungen für Kostal Plenticore ")])),_:1}),t(p,{subtype:"info"},{default:r(()=>e[4]||(e[4]=[a(" Wenn am Kostal Plenticore-Wechselrichter ein EM300 oder Kostal Energy Smart Meter (KSEM) angeschlossen ist, muss eine Zähler-und eine Wechselrichter-Komponente angelegt werden. ")])),_:1}),t(d,{title:"IP oder Hostname",subtype:"host",required:"","model-value":o.device.configuration.ip_address,"onUpdate:modelValue":e[0]||(e[0]=n=>o.updateConfiguration(n,"configuration.ip_address"))},null,8,["model-value"]),t(s,{title:"Port",required:"",min:1,max:65535,"model-value":o.device.configuration.port,"onUpdate:modelValue":e[1]||(e[1]=n=>o.updateConfiguration(n,"configuration.port"))},null,8,["model-value"]),t(s,{title:"Modbus ID",required:"","model-value":o.device.configuration.modbus_id,min:"1",max:"255","onUpdate:modelValue":e[2]||(e[2]=n=>o.updateConfiguration(n,"configuration.modbus_id"))},null,8,["model-value"])])}const $=m(f,[["render",v],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/kostal/kostal_plenticore/device.vue"]]);export{$ as default};