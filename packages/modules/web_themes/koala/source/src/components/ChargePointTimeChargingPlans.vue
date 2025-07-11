<template>
  <div class="row items-center q-ma-none q-pa-none no-wrap">
    <div class="col row items-center">
      <div class="col text-subtitle2">Zeitladen</div>
      <div class="col">
        <ChargePointTimeCharging :charge-point-id="props.chargePointId" dense />
      </div>
    </div>
  </div>
  <div v-if="timeChargingEnabled" class="row justify-between items-center">
    <div class="text-subtitle2">Termine Zeitladen:</div>
  </div>
  <div
<<<<<<< HEAD
    v-if="plans.length === 0 && timeChargingEnabled"
=======
    v-if="plans.value.length === 0"
>>>>>>> parent of acfc3a169 (Feature integrated charging plans (#2498))
    class="row q-mt-sm q-pa-sm bg-primary text-white no-wrap message-text"
    color="primary"
    style="border-radius: 10px"
  >
    <q-icon name="info" size="sm" class="q-mr-xs" />
    Keine Zeitpläne vorhanden.
  </div>
<<<<<<< HEAD
  <div v-else-if="timeChargingEnabled">
    <div v-for="(plan, index) in plans" :key="index" class="row q-mt-sm">
=======
  <div v-else>
    <div v-for="(plan, index) in plans.value" :key="index" class="row q-mt-sm">
>>>>>>> parent of acfc3a169 (Feature integrated charging plans (#2498))
      <ChargePointTimeChargingPlanButton
        class="full-width"
        :charge-point-id="props.chargePointId"
        :plan="plan"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMqttStore } from 'src/stores/mqtt-store';
import { computed } from 'vue';
import ChargePointTimeCharging from './ChargePointTimeCharging.vue';
import ChargePointTimeChargingPlanButton from './ChargePointTimeChargingPlanButton.vue';

const props = defineProps<{
  chargePointId: number;
}>();

const mqttStore = useMqttStore();

const plans = computed(() =>
  mqttStore.vehicleTimeChargingPlans(props.chargePointId),
);

const timeChargingEnabled = mqttStore.chargePointConnectedVehicleTimeCharging(
  props.chargePointId,
);
</script>

<style scoped>
.full-width {
  width: 100%;
}
</style>
