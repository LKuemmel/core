/*
 * themeConfig.ts
 * colors theme for openwb 2.0
 * Copyright (c) 2022 Claus Hagen
 */

import { computed, reactive } from 'vue'
import { select } from 'd3'
import type { ChargeModeInfo } from './types'
import { shDevices } from '@/components/smartHome/model'
import { ChargeMode } from '@/components/chargePointList/model'
import { sourceSummary } from './model'
export class Config {
	graphToShow = 'powermeter'
	cpToShow = 0
	displayLocked = true
	private _showRelativeArcs = false
	showTodayGraph = true
	private _graphPreference = 'live'
	private _usageStackOrder = 0
	private _displayMode = 'dark'
	private _showGrid = false
	private _smartHomeColors = 'normal'
	private _decimalPlaces = 1
	private _showQuickAccess = true
	private _simpleCpList = false
	private _shortCpList = 'no'
	private _showAnimations = true
	private _preferWideBoxes = false
	private _maxPower = 4000
	private _fluidDisplay = false
	private _showClock = 'no'
	private _showButtonBar = true
	private _showCounters = false
	private _showVehicles = false
	private _showPrices = false
	private _debug: boolean = false
	isEtEnabled: boolean = false
	etPrice: number = 20.5
	showRightButton = true
	showLeftButton = true
	// graphMode = ''
	animationDuration = 300
	animationDelay = 100
	zoomGraph = false
	parentChargePoint1: undefined
	parentChargePoint2: undefined

	constructor() {}
	get showRelativeArcs() {
		return this._showRelativeArcs
	}
	set showRelativeArcs(setting: boolean) {
		this._showRelativeArcs = setting
		savePrefs()
	}
	setShowRelativeArcs(setting: boolean) {
		this._showRelativeArcs = setting
	}
	get graphPreference() {
		return this._graphPreference
	}
	set graphPreference(mode: string) {
		this._graphPreference = mode
		savePrefs()
	}
	setGraphPreference(mode: string) {
		this._graphPreference = mode
	}
	get usageStackOrder() {
		return this._usageStackOrder
	}
	set usageStackOrder(mode: number) {
		this._usageStackOrder = mode
		savePrefs()
	}
	setUsageStackOrder(mode: number) {
		this._usageStackOrder = mode
	}
	get displayMode() {
		return this._displayMode
	}
	set displayMode(mode: string) {
		this._displayMode = mode
		switchTheme(mode)
	}
	setDisplayMode(mode: string) {
		this._displayMode = mode
	}
	get showGrid() {
		return this._showGrid
	}
	set showGrid(setting: boolean) {
		this._showGrid = setting
		savePrefs()
	}
	setShowGrid(setting: boolean) {
		this._showGrid = setting
	}
	get decimalPlaces() {
		return this._decimalPlaces
	}
	set decimalPlaces(setting: number) {
		this._decimalPlaces = setting
		savePrefs()
	}
	setDecimalPlaces(setting: number) {
		this._decimalPlaces = setting
	}
	get smartHomeColors() {
		return this._smartHomeColors
	}
	set smartHomeColors(setting: string) {
		this._smartHomeColors = setting
		switchSmarthomeColors(setting)
		savePrefs()
	}
	setSmartHomeColors(setting: string) {
		this._smartHomeColors = setting
		switchSmarthomeColors(setting)
	}
	get showQuickAccess() {
		return this._showQuickAccess
	}
	set showQuickAccess(show: boolean) {
		this._showQuickAccess = show
		savePrefs()
	}
	setShowQuickAccess(show: boolean) {
		this._showQuickAccess = show
	}
	get simpleCpList() {
		return this._simpleCpList
	}
	set simpleCpList(show: boolean) {
		this._simpleCpList = show
		savePrefs()
	}
	setSimpleCpList(show: boolean) {
		this._simpleCpList = show
	}
	get shortCpList() {
		return this._shortCpList
	}
	set shortCpList(show: string) {
		this._shortCpList = show
		savePrefs()
	}
	setShortCpList(show: string) {
		this._shortCpList = show
	}
	get showAnimations() {
		return this._showAnimations
	}
	set showAnimations(show: boolean) {
		this._showAnimations = show
		savePrefs()
	}
	setShowAnimations(show: boolean) {
		this._showAnimations = show
	}
	get preferWideBoxes() {
		return this._preferWideBoxes
	}
	set preferWideBoxes(yes: boolean) {
		this._preferWideBoxes = yes
		savePrefs()
	}
	setPreferWideBoxes(yes: boolean) {
		this._preferWideBoxes = yes
	}
	get maxPower() {
		return this._maxPower
	}
	set maxPower(max: number) {
		this._maxPower = max
		savePrefs()
	}
	setMaxPower(max: number) {
		this._maxPower = max
	}
	get fluidDisplay() {
		return this._fluidDisplay
	}
	set fluidDisplay(on: boolean) {
		this._fluidDisplay = on
		savePrefs()
	}
	setFluidDisplay(on: boolean) {
		this._fluidDisplay = on
	}
	get showClock() {
		return this._showClock
	}
	set showClock(mode: string) {
		this._showClock = mode
		savePrefs()
	}
	setShowClock(mode: string) {
		this._showClock = mode
	}
	get debug() {
		return this._debug
	}
	set debug(on: boolean) {
		this._debug = on
		savePrefs()
	}
	setDebug(on: boolean) {
		this._debug = on
	}
	get showButtonBar() {
		return this._showButtonBar
	}
	set showButtonBar(show: boolean) {
		this._showButtonBar = show
		savePrefs()
	}
	setShowButtonBar(show: boolean) {
		this._showButtonBar = show
	}
	get showCounters() {
		return this._showCounters
	}
	set showCounters(show: boolean) {
		this._showCounters = show
		savePrefs()
	}
	setShowCounters(show: boolean) {
		this._showCounters = show
	}
	get showVehicles() {
		return this._showVehicles
	}
	set showVehicles(show: boolean) {
		this._showVehicles = show
		savePrefs()
	}
	setShowVehicles(show: boolean) {
		this._showVehicles = show
	}
	get showPrices() {
		return this._showPrices
	}
	set showPrices(show: boolean) {
		this._showPrices = show
		savePrefs()
	}
	setShowPrices(show: boolean) {
		this._showPrices = show
	}
}
export const globalConfig = reactive(new Config())
export const wbSettings: { [key: string]: string | number | undefined } =
	reactive({
		localIp: undefined,
		localBranch: undefined,
		localCommit: undefined,
		localVersion: undefined,
		parentChargePoint1: undefined,
		parentChargePoint2: undefined,
	})

export function initConfig() {
	// readCookie()
	// set the background
	//const doc = select('html')
	//doc.classed('theme-dark', globalConfig.displayMode == 'dark')
	//doc.classed('theme-light', globalConfig.displayMode == 'light')
	//doc.classed('theme-blue', globalConfig.displayMode == 'blue')
	// set the color scheme for devices
	//doc.classed('shcolors-standard', globalConfig.smartHomeColors == 'standard')
	//doc.classed('shcolors-advanced', globalConfig.smartHomeColors == 'advanced')
	//doc.classed('shcolors-normal', globalConfig.smartHomeColors == 'normal')
}
export let animateEnergyGraph = true
export function setAnimateEnergyGraph(val: boolean) {
	animateEnergyGraph = val
}

// Handle wide vs narrow screen layouts
const breakpoint = 992
export const screensize = reactive({
	x: document.documentElement.clientWidth,
	y: document.documentElement.clientHeight,
})
export function updateDimensions() {
	screensize.x = document.documentElement.clientWidth
	screensize.y = document.documentElement.clientHeight
	initConfig()
}
export const widescreen = computed(() => {
	return screensize.x >= breakpoint
})
export const chargemodes: { [key: string]: ChargeModeInfo } = {
	instant_charging: {
		mode: ChargeMode.instant_charging,
		name: 'Sofort',
		color: 'var(--color-charging)',
		icon: 'fa-bolt',
	},
	pv_charging: {
		mode: ChargeMode.pv_charging,
		name: 'PV',
		color: 'var(--color-pv',
		icon: 'fa-solar-panel',
	},
	scheduled_charging: {
		mode: ChargeMode.scheduled_charging,
		name: 'Zielladen',
		color: 'var(--color-battery)',
		icon: 'fa-bullseye',
	},
	eco_charging: {
		mode: ChargeMode.eco_charging,
		name: 'Eco',
		color: 'var(--color-devices)',
		icon: 'fa-coins',
	},
	stop: {
		mode: ChargeMode.stop,
		name: 'Stop',
		color: 'var(--color-fg)',
		icon: 'fa-power-off',
	},
}
// methods
export function savePrefs() {
	writeCookie()
}
export function switchTheme(mode: string) {
	const doc = select('html')

	doc.classed('theme-dark', mode == 'dark')
	doc.classed('theme-light', mode == 'light')
	doc.classed('theme-blue', mode == 'blue')
	savePrefs()
}
export function toggleGrid() {
	globalConfig.showGrid = !globalConfig.showGrid
	savePrefs()
}
export function toggleFixArcs() {
	// globalConfig.etPrice = globalConfig.etPrice + 10
	globalConfig.showRelativeArcs = !globalConfig.showRelativeArcs
	savePrefs()
}
export function resetArcs() {
	globalConfig.maxPower =
		sourceSummary.evuIn.power +
		sourceSummary.pv.power +
		sourceSummary.batOut.power
	savePrefs()
}
export function switchDecimalPlaces() {
	if (globalConfig.decimalPlaces < 4) {
		globalConfig.decimalPlaces = globalConfig.decimalPlaces + 1
	} else {
		globalConfig.decimalPlaces = 0
	}
	savePrefs()
}
export function switchSmarthomeColors(setting: string) {
	const doc = select('html')
	doc.classed('shcolors-normal', setting == 'normal')
	doc.classed('shcolors-standard', setting == 'standard')
	doc.classed('shcolors-advanced', setting == 'advanced')
}

export const infotext: { [key: string]: string } = {
	chargemode: 'Der Lademodus für das Fahrzeug an diesem Ladepunkt',
	vehicle: 'Das Fahrzeug, das an diesem Ladepounkt geladen wird',
	locked: 'Für das Laden sperren',
	priority:
		'Fahrzeuge mit Priorität werden bevorzugt mit mehr Leistung geladen, falls verfügbar',
	timeplan: 'Das Laden nach Zeitplan für dieses Fahrzeug aktivieren',
	minsoc:
		'Immer mindestens bis zum eingestellten Ladestand laden. Wenn notwendig mit Netzstrom.',
	minpv:
		'Durchgehend mit mindestens dem eingestellten Strom laden. Wenn notwendig mit Netzstrom.',
	pricebased:
		'Laden bei dynamischem Stromtarif, wenn eingestellter Maximalpreis unterboten wird.',
}

interface Preferences {
	hideSH?: number[]
	showLG?: boolean
	displayM?: string
	stackO?: number
	showGr?: boolean
	decimalP?: number
	smartHomeC?: string
	relPM?: boolean
	maxPow?: number
	showQA?: boolean
	simpleCP?: boolean
	shortCP?: string
	animation?: boolean
	wideB?: boolean
	fluidD?: boolean
	clock?: string
	showButtonBar?: boolean
	showCounters?: boolean
	showVehicles?: boolean
	showPrices?: boolean
	debug?: boolean
}

function writeCookie() {
	const prefs: Preferences = {}
	prefs.hideSH = [...shDevices.values()]
		.filter((device) => !device.showInGraph)
		.map((device) => device.id)
	prefs.showLG = globalConfig.graphPreference == 'live'
	prefs.displayM = globalConfig.displayMode
	prefs.stackO = globalConfig.usageStackOrder
	prefs.showGr = globalConfig.showGrid
	prefs.decimalP = globalConfig.decimalPlaces
	prefs.smartHomeC = globalConfig.smartHomeColors
	prefs.relPM = globalConfig.showRelativeArcs
	prefs.maxPow = globalConfig.maxPower
	prefs.showQA = globalConfig.showQuickAccess
	prefs.simpleCP = globalConfig.simpleCpList
	prefs.shortCP = globalConfig.shortCpList
	prefs.animation = globalConfig.showAnimations
	prefs.wideB = globalConfig.preferWideBoxes
	prefs.fluidD = globalConfig.fluidDisplay
	prefs.clock = globalConfig.showClock
	prefs.showButtonBar = globalConfig.showButtonBar
	prefs.showCounters = globalConfig.showCounters
	prefs.showVehicles = globalConfig.showVehicles
	prefs.showPrices = globalConfig.showPrices
	prefs.debug = globalConfig.debug

	document.cookie =
		'openWBColorTheme=' +
		JSON.stringify(prefs) +
		';max-age=16000000;samesite=strict'
}
