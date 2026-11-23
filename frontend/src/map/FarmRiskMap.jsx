import { useEffect, useMemo, useState } from 'react'
import Map from 'react-map-gl/mapbox'
import DeckGL from '@deck.gl/react'
import { GeoJsonLayer, TextLayer } from '@deck.gl/layers'
import 'mapbox-gl/dist/mapbox-gl.css'
import { farmZones } from '../data/farmData'

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN
const zoneGeometry = {
  'Zone A': [
    [
      [76.9, 11.02],
      [76.91, 11.02],
      [76.91, 11.03],
      [76.9, 11.03],
      [76.9, 11.02]
    ]
  ],

  'Zone B': [
    [
      [76.91, 11.02],
      [76.92, 11.02],
      [76.92, 11.03],
      [76.91, 11.03],
      [76.91, 11.02]
    ]
  ],

  'Zone C': [
    [
      [76.9, 11.03],
      [76.91, 11.03],
      [76.91, 11.04],
      [76.9, 11.04],
      [76.9, 11.03]
    ]
  ],

  'Zone D': [
    [
      [76.91, 11.03],
      [76.92, 11.03],
      [76.92, 11.04],
      [76.91, 11.04],
      [76.91, 11.03]
    ]
  ]
}
function getRiskColor (score) {
  if (score >= 80) {
    return [220, 60, 60, 190]
  }

  if (score >= 50) {
    return [240, 180, 50, 180]
  }

  return [60, 170, 90, 160]
}

export default function FarmRiskMap ({
  onAskAI,
  externalRiskFilter = 'all',
  externalSelectedZone = null
}) {
  const [selectedZone, setSelectedZone] = useState(null)
  const [riskFilter, setRiskFilter] = useState('all')
  const [minRiskScore, setMinRiskScore] = useState(0)
  useEffect(() => {
    setRiskFilter(externalRiskFilter)
  }, [externalRiskFilter])

  const farmZoneFeatures = farmZones.map(zone => ({
    type: 'Feature',
    properties: {
      zone: zone.zone,
      risk: zone.risk,
      score: zone.score,
      disease: zone.disease,
      status: zone.status
    },
    geometry: {
      type: 'Polygon',
      coordinates: zoneGeometry[zone.zone]
    }
  }))

  useEffect(() => {
    if (externalSelectedZone) {
      const zone = farmZoneFeatures.find(
        feature => feature.properties.zone === externalSelectedZone
      )

      setSelectedZone(zone || null)
    } else {
      setSelectedZone(null)
    }
  }, [externalSelectedZone])

  const filteredZones = {
    type: 'FeatureCollection',
    features: farmZoneFeatures.filter(feature => {
      const matchesRisk =
        riskFilter === 'all' || feature.properties.risk === riskFilter

      const matchesScore = feature.properties.score >= minRiskScore

      return matchesRisk && matchesScore
    })
  }

  const layers = useMemo(() => {
    return [
      new GeoJsonLayer({
        id: 'farm-risk-zones',
        data: filteredZones,
        filled: true,
        stroked: true,

        getFillColor: feature => {
          if (
            selectedZone &&
            feature.properties.zone === selectedZone.properties.zone
          ) {
            return [50, 120, 220, 210]
          }

          return getRiskColor(feature.properties.score)
        },

        getLineColor: feature => {
          if (
            selectedZone &&
            feature.properties.zone === selectedZone.properties.zone
          ) {
            return [255, 255, 255, 255]
          }

          return [255, 255, 255, 220]
        },

        getLineWidth: feature => {
          if (
            selectedZone &&
            feature.properties.zone === selectedZone.properties.zone
          ) {
            return 5
          }

          return 3
        },

        lineWidthMinPixels: 2,
        pickable: true,

        onClick: ({ object }) => {
          if (object) {
            setSelectedZone(object)
          }
        }
      }),

      new TextLayer({
        id: 'farm-risk-labels',
        data: filteredZones.features,
        pickable: false,

        getPosition: feature => {
          const coordinates = feature.geometry.coordinates[0]

          const longitude =
            coordinates.reduce((sum, coordinate) => sum + coordinate[0], 0) /
            coordinates.length

          const latitude =
            coordinates.reduce((sum, coordinate) => sum + coordinate[1], 0) /
            coordinates.length

          return [longitude, latitude]
        },

        getText: feature =>
          `${feature.properties.zone} ${feature.properties.score}%`,

        getSize: 15,
        getColor: [255, 255, 255, 255],
        getTextAnchor: 'middle',
        getAlignmentBaseline: 'center',
        fontWeight: 'bold',
        backgroundColor: [0, 0, 0, 110],
        backgroundPadding: [3, 2]
      })
    ]
  }, [selectedZone, filteredZones])

  const initialViewState = {
    longitude: 76.91,
    latitude: 11.03,
    zoom: 14,
    pitch: 35,
    bearing: 0
  }

  if (!MAPBOX_TOKEN) {
    return (
      <div className='map-error'>
        <h3>Mapbox Token Required</h3>

        <p>
          Add your Mapbox access token to the frontend environment
          configuration.
        </p>
      </div>
    )
  }

  return (
    <div className='farm-map'>
      <div className='risk-filter'>
        <div className='risk-filter-title'>
          <span>Risk Filter</span>
          <strong>{filteredZones.features.length} zones</strong>
        </div>

        <div className='risk-filter-buttons'>
          <button
            className={riskFilter === 'all' ? 'active' : ''}
            onClick={() => {
              setRiskFilter('all')
              setSelectedZone(null)
            }}
          >
            All
          </button>

          <button
            className={riskFilter === 'healthy' ? 'active healthy' : ''}
            onClick={() => {
              setRiskFilter('healthy')
              setSelectedZone(null)
            }}
          >
            🌱 Healthy
          </button>

          <button
            className={riskFilter === 'moderate' ? 'active moderate' : ''}
            onClick={() => {
              setRiskFilter('moderate')
              setSelectedZone(null)
            }}
          >
            🟡 Moderate
          </button>

          <button
            className={riskFilter === 'high' ? 'active high' : ''}
            onClick={() => {
              setRiskFilter('high')
              setSelectedZone(null)
            }}
          >
            🔴 High
          </button>
        </div>
        <div className='risk-score-filter'>
          <div className='risk-score-header'>
            <span>Minimum Risk Score</span>
            <strong>{minRiskScore}%</strong>
          </div>

          <input
            type='range'
            min='0'
            max='100'
            step='1'
            value={minRiskScore}
            onChange={event => {
              setMinRiskScore(Number(event.target.value))
              setSelectedZone(null)
            }}
          />

          <div className='risk-score-scale'>
            <span>0%</span>
            <span>50%</span>
            <span>100%</span>
          </div>
        </div>
        <button
          className='reset-risk-filter'
          onClick={() => {
            setRiskFilter('all')
            setMinRiskScore(0)
            setSelectedZone(null)
          }}
        >
          ↻ Reset Filters
        </button>
      </div>
      <DeckGL
        initialViewState={initialViewState}
        controller={true}
        layers={layers}
      >
        <Map
          mapboxAccessToken={MAPBOX_TOKEN}
          mapStyle='mapbox://styles/mapbox/satellite-streets-v12'
        />
      </DeckGL>

      {/* Risk Legend */}

      <div className='map-overlay'>
        <h4>Disease Risk Heatmap</h4>

        <div className='legend-item'>
          <span className='legend-color healthy'></span>
          Healthy
        </div>

        <div className='legend-item'>
          <span className='legend-color moderate'></span>
          Moderate Risk
        </div>

        <div className='legend-item'>
          <span className='legend-color high'></span>
          High Risk
        </div>
      </div>

      {/* Selected Zone Panel */}

      {selectedZone && (
        <div className='zone-details'>
          <div className='zone-details-header'>
            <div>
              <span>SELECTED ZONE</span>
              <h3>{selectedZone.properties.zone}</h3>
            </div>

            <button
              className='zone-close'
              onClick={() => setSelectedZone(null)}
            >
              ×
            </button>
          </div>

          <div className='zone-risk'>
            <div>
              <span>Risk Score</span>
              <strong>{selectedZone.properties.score}%</strong>
            </div>

            <div>
              <span>Risk Level</span>
              <strong className={`risk-${selectedZone.properties.risk}`}>
                {selectedZone.properties.risk.toUpperCase()}
              </strong>
            </div>
          </div>

          <div className='zone-info'>
            <div>
              <span>Disease Risk</span>
              <strong>{selectedZone.properties.disease}</strong>
            </div>

            <div>
              <span>Status</span>
              <strong>{selectedZone.properties.status}</strong>
            </div>
          </div>

          <button
            className='zone-ai-button'
            onClick={() => onAskAI(selectedZone.properties)}
          >
            🤖 Ask AI About This Zone
          </button>
        </div>
      )}
    </div>
  )
}
