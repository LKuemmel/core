import{_ as c,u as n,k as r,l as d,D as o,N as s,y as a,x as u,z as _}from"./vendor-f2b8aa6f.js";import"./vendor-sortablejs-2f1828d0.js";const l={name:"DeviceOpenwbPvKit",emits:["update:configuration"],props:{configuration:{type:Object,required:!0},deviceId:{default:void 0}},methods:{updateConfiguration(e,t=void 0){this.$emit("update:configuration",{value:e,object:t})}}},f={class:"device-openwb-pvkit"},b={class:"small"};function m(e,t,v,g,w,h){const i=n("openwb-base-heading"),p=n("openwb-base-alert");return r(),d("div",f,[o(i,null,{default:s(()=>[a(" Einstellungen für openWB PV-Kit "),u("span",b,"(Modul: "+_(e.$options.name)+")",1)]),_:1}),o(p,{subtype:"info"},{default:s(()=>[a(" Dieses Gerät erfordert keine Einstellungen. ")]),_:1})])}const x=c(l,[["render",m],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/openwb/openwb_pv_kit/device.vue"]]);export{x as default};