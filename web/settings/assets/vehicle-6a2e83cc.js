import{_ as h,a4 as c,a5 as _,a6 as f,u as r,l as b,m as k,G as i,E as a,y as s,x as v}from"./vendor-0c15df0c.js";import{a as w}from"./vendor-axios-c9d2afa0.js";import{C as y}from"./index-6ffbdc7e.js";import{V as C}from"./VehicleConfig-87862d5f.js";import"./vendor-sortablejs-1a751103.js";import"./vendor-fortawesome-231ff303.js";import"./vendor-bootstrap-83e2d5a1.js";import"./vendor-jquery-84e2bf4a.js";import"./dynamic-import-helper-be004503.js";const T={name:"VehicleSocTesla",mixins:[y,C],data(){return{tesla_api_oauth2:"https://auth.tesla.com/oauth2/v3",tesla_api_redirect:"https://auth.tesla.com/void/callback",tesla_api_owners:"https://owner-api.teslamotors.com/oauth/token",user_agent:"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",code_challenge:null,code_verifier:null,page_not_found_url:null}},methods:{tesla_login_window(){this.tesla_gen_challenge();var e=window.open(this.tesla_gen_url(),"TeslaLogin","width=800,height=600,status=yes,scrollbars=yes,resizable=yes");e.focus()},tesla_gen_challenge(){this.code_verifier=c.encode(_.randomBytes(86)).replace(/[^a-zA-Z0-9]/gi,"").substring(0,86);const e=_.createHash("sha256").update(this.code_verifier).digest();this.code_challenge=c.encode(e),console.debug(this.code_verifier,this.code_verifier.length,this.code_challenge,this.code_challenge.length)},tesla_gen_url(){const e=new URL(this.tesla_api_oauth2+"/authorize/");return e.searchParams.append("client_id","ownerapi"),e.searchParams.append("code_challenge",this.code_challenge),e.searchParams.append("code_challenge_method","S256"),e.searchParams.append("redirect_uri",this.tesla_api_redirect),e.searchParams.append("response_type","code"),e.searchParams.append("scope","openid email offline_access"),e.searchParams.append("state","myteslaapp"),e},async tesla_login(){const e=f.parse(this.page_not_found_url,!0).query;if(console.debug("queryObject",e),!e.code){console.error("Something is wrong... Code does not exist in URL"),this.$root.postClientMessage("Die eingegebene URL ist ungültig.","danger");return}const n={url:this.tesla_api_owners,user_agent:this.user_agent,data:{grant_type:"authorization_code",client_id:"ownerapi",code:e.code,code_verifier:this.code_verifier,redirect_uri:this.tesla_api_redirect}};try{const o=await w.post(location.protocol+"//"+location.host+"/openWB/web/settings/modules/vehicles/tesla/tesla.php",JSON.parse(JSON.stringify(n)),{headers:{"Content-Type":"application/json",Accept:"application/json"}});console.debug("response",o),this.updateConfiguration({access_token:o.data.access_token,refresh_token:o.data.refresh_token,created_at:o.data.created_at,expires_in:o.data.expires_in},"configuration.token"),this.$root.postClientMessage("Token erfolgreich abgerufen.","success")}catch(o){console.error(o),this.$root.postClientMessage("Beim Abruf der Token ist ein Fehler aufgetreten!<pre>"+o+"</pre>","danger")}}}},U={class:"vehicle-soc-tesla"};function B(e,n,o,z,l,p){const u=r("openwb-base-number-input"),m=r("openwb-base-heading"),g=r("openwb-base-button-input"),d=r("openwb-base-text-input");return b(),k("div",U,[i(u,{title:"Fahrzeug-ID",required:"",min:0,"model-value":e.vehicle.configuration.tesla_ev_num,"onUpdate:modelValue":n[0]||(n[0]=t=>e.updateConfiguration(t,"configuration.tesla_ev_num"))},{help:a(()=>n[6]||(n[6]=[s(' Die ID des Fahrzeugs bei Tesla. Normalerweise "0" bei nur einem Fahrzeug im Konto. ')])),_:1},8,["model-value"]),i(m,null,{default:a(()=>n[7]||(n[7]=[s("Token abrufen oder eingeben")])),_:1}),i(g,{title:"1. Anmelden","button-text":"Bei Tesla Anmelden",subtype:"success",onButtonClicked:p.tesla_login_window},{help:a(()=>n[8]||(n[8]=[s(" Es wird ein neues Browserfenster geöffnet, in dem Sie sich bei Tesla mit Ihren Zugangsdaten anmelden können. ")])),_:1},8,["onButtonClicked"]),i(d,{modelValue:l.page_not_found_url,"onUpdate:modelValue":n[1]||(n[1]=t=>l.page_not_found_url=t),title:"2. URL kopieren und einfügen",subtype:"url","empty-value":null},{help:a(()=>n[9]||(n[9]=[s(' Hier die komplette URL (Text in der Adresszeile) aus dem geöffneten Browserfenster einfügen, wenn dort "Page Not Found" angezeigt wird. ')])),_:1},8,["modelValue"]),i(g,{title:"3. Token abrufen","button-text":"Jetzt abrufen",subtype:"success",disabled:l.page_not_found_url===null,onButtonClicked:p.tesla_login},{help:a(()=>n[10]||(n[10]=[s(" Der in der eingegebenen URL enthaltene Code wird genutzt, um ein Anmeldetoken bei Tesla abzurufen. Ist dies erfolgreich, so werden die Daten des Token in den weiteren Feldern automatisch eingegeben. ")])),_:1},8,["disabled","onButtonClicked"]),n[13]||(n[13]=v("hr",null,null,-1)),i(d,{title:"Access Token",pattern:"^(ey).*",required:"","model-value":e.vehicle.configuration.token?e.vehicle.configuration.token.access_token:"","onUpdate:modelValue":n[2]||(n[2]=t=>e.updateConfiguration(t,"configuration.token.access_token"))},null,8,["model-value"]),i(d,{title:"Refresh Token",pattern:"^(ey).*",required:"","model-value":e.vehicle.configuration.token?e.vehicle.configuration.token.refresh_token:"","onUpdate:modelValue":n[3]||(n[3]=t=>e.updateConfiguration(t,"configuration.token.refresh_token"))},null,8,["model-value"]),i(u,{title:"Erstellt um",required:"","model-value":e.vehicle.configuration.token?e.vehicle.configuration.token.created_at:0,"onUpdate:modelValue":n[4]||(n[4]=t=>e.updateConfiguration(t,"configuration.token.created_at"))},{help:a(()=>n[11]||(n[11]=[s(" Unix Timestamp des Zeitpunktes, an dem das Token erzeugt wurde. ")])),_:1},8,["model-value"]),i(u,{title:"Ungültig in",unit:"s",required:"","model-value":e.vehicle.configuration.token?e.vehicle.configuration.token.expires_in:0,"onUpdate:modelValue":n[5]||(n[5]=t=>e.updateConfiguration(t,"configuration.token.expires_in"))},{help:a(()=>n[12]||(n[12]=[s(" Zeitspanne in Sekunden, nach der das Token ungültig wird. ")])),_:1},8,["model-value"])])}const x=h(T,[["render",B],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/vehicles/tesla/vehicle.vue"]]);export{x as default};