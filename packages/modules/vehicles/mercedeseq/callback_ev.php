<?php
   //Callback procedure for mercedes SoC API EV 
   if( $_GET["code"] ) {
      #system( "/var/www/html/openWB/packages/modules/vehicles/mercedeseq/auth.py " . $_GET['state'] . " " . $_GET['code']) ;

      # subscribe openWB/vehicle/i/soc_module/config
      # setze code in config
      # publish openWB/set/vehicle/i/soc_module/config
      # publish openWB/vehicle/i/get/force_soc_update, damit zeitnah Token erzeugt werden
   }
   else {
      echo "<html>";
      echo "<p>" . $_GET["error"] . "</p>";
      echo "<p>" . $_GET["error_description"] . "</p>";
      echo "</html>";
   }
?>