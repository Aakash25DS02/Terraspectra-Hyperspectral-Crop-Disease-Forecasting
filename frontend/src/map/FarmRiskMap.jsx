import { useMemo, useState } from 'react'
import Map from 'react-map-gl/mapbox'
import DeckGL from '@deck.gl/react'
import { GeoJsonLayer } from '@deck.gl/layers'
import 'mapbox-gl/dist/mapbox-gl.css'

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN

const farmZones = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: {
        zone: 'Zone A',
        risk: 'healthy',
        score: 18,
        disease: 'Low',
        status: 'Healthy'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [76.9, 11.02],
            [76.91, 11.02],
            [76.91, 11.03],
            [76.9, 11.03],
            [76.9, 11.02]
          ]
        ]
      }
    },

    {
      type: 'Feature',
      properties: {
        zone: 'Zone B',
        risk: 'moderate',
        score: 52,
        disease: 'Moderate',
        status: 'Requires Monitoring'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [76.91, 11.02],
            [76.92, 11.02],
            [76.92, 11.03],
            [76.91, 11.03],
            [76.91, 11.02]
          ]
        ]
      }
    },

    {
      type: 'Feature',
      properties: {
        zone: 'Zone C',
        risk: 'high',
        score: 87,
        disease: 'High',
        status: 'Requires Attention'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [76.9, 11.03],
            [76.91, 11.03],
            [76.91, 11.04],
            [76.9, 11.04],
            [76.9, 11.03]
          ]
        ]
      }
    },

    {
      type: 'Feature',
      properties: {
        zone: 'Zone D',
        risk: 'healthy',
        score: 22,
        disease: 'Low',
        status: 'Healthy'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [76.91, 11.03],
            [76.92, 11.03],
            [76.92, 11.04],
            [76.91, 11.04],
            [76.91, 11.03]
          ]
        ]
      }
    }
  ]
}

function getRiskColor (risk) {
  if (risk === 'high') {
    return [220, 70, 70, 150]
  }

  if (risk === 'moderate') {
    return [230, 180, 50, 150]
  }

  return [70, 160, 90, 150]
}

export default function FarmRiskMap ({ onAskAI }) {
  const [selectedZone, setSelectedZone] = useState(null)

  const layers = useMemo(() => {
    return [
      new GeoJsonLayer({
        id: 'farm-risk-zones',

        data: farmZones,

        filled: true,
        stroked: true,

        getFillColor: feature => {
          if (
            selectedZone &&
            feature.properties.zone === selectedZone.properties.zone
          ) {
            return [50, 120, 220, 210]
          }

          return getRiskColor(feature.properties.risk)
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
      })
    ]
  }, [selectedZone])

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
        <h4>Farm Disease Risk</h4>

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
